import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

const CANDIDATE_MODELS = [
  "gemini-3.8-flash",
  "gemini-3.5-flash-lite",
  "gemini-2.5-flash"
];

async function getEmbedding(text: string, apiKey: string): Promise<number[] | null> {
  try {
    const res = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/text-embedding-004:embedContent?key=${apiKey}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "models/text-embedding-004",
          content: { parts: [{ text }] }
        }),
      }
    );
    const data = await res.json();
    return data.embedding?.values || null;
  } catch {
    return null;
  }
}

async function generateReplyWithFallback(apiKey: string, systemPrompt: string) {
  let lastError = "";
  for (const model of CANDIDATE_MODELS) {
    try {
      const res = await fetch(
        `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            contents: [{ parts: [{ text: systemPrompt }] }],
            generationConfig: { responseMimeType: "application/json" }
          }),
        }
      );
      const data = await res.json();
      if (res.ok && !data.error) {
        return { success: true, modelUsed: model, data };
      }
      lastError = data.error?.message || `Status HTTP ${res.status}`;
    } catch (err: any) {
      lastError = err.message;
    }
  }
  return { success: false, error: lastError };
}

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
    const serviceRoleKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
    const geminiApiKey = Deno.env.get("GEMINI_API_KEY")!;
    const supabase = createClient(supabaseUrl, serviceRoleKey);

    let incomingComment = "";
    let mediaId = "";

    try {
      const body = await req.json();
      incomingComment = body.comment || "";
      mediaId = body.media_id || "simulated_media";
    } catch {
      // Default jika dipanggil tanpa body
    }

    if (!incomingComment) {
      incomingComment = "Project machine learning XGBoost churn ini akurasinya berapa persen bro?";
    }

    const { data: account } = await supabase
      .schema("threads")
      .from("threads_accounts")
      .select("id")
      .limit(1)
      .maybeSingle();

    if (!account) {
      return new Response(
        JSON.stringify({ error: "Belum ada akun Threads tersambung." }),
        { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const { data: settings } = await supabase
      .schema("threads")
      .from("auto_reply_settings")
      .select("*")
      .eq("account_id", account.id)
      .maybeSingle();

    const mode = settings?.mode || "review";
    const tonePrompt = settings?.tone_prompt || "Gunakan bahasa kasual, ramah, to the point, dan profesional.";

    let ragContexts: string[] = [];
    const commentVector = await getEmbedding(incomingComment, geminiApiKey);
    if (commentVector) {
      const { data: matchedDocs } = await supabase.rpc("match_brand_knowledge", {
        query_embedding: JSON.stringify(commentVector),
        match_threshold: 0.25,
        match_count: 5,
        p_account_id: account.id
      }, { schema: "threads" });

      if (matchedDocs && matchedDocs.length > 0) {
        ragContexts = matchedDocs.map((d: any) => `[FAKTA KNOWLEDGE BASE: ${d.title}] ${d.content}`);
      }
    }

    const systemPrompt = `Kamu adalah AI Auto-Reply Assistant untuk Threads (Meta).
Tugasmu membalas komentar audiens secara natural berdasarkan fakta bisnis & persona yang diberikan.

FAKTA/DOKUMEN RAG TERKAIT (Vector Search Result):
${ragContexts.length > 0 ? ragContexts.join("\n") : "Tidak ada fakta khusus yang ditemukan."}

TONE & INSTRUKSI PENULISAN:
${tonePrompt}

KOMENTAR AUDIENS TERMASUK:
"${incomingComment}"

ATURAN BALASAN:
1. Balas dengan ringkas (1-3 kalimat).
2. Jangan gunakan emoji berlebihan.
3. Langsung jawab fakta dari RAG jika ditanyakan detail teknis/bisnis.
4. HANYA kembalikan JSON valid:
{
  "reply": "isi teks balasan..."
}`;

    const result = await generateReplyWithFallback(geminiApiKey, systemPrompt);
    if (!result.success || !result.data) {
      return new Response(
        JSON.stringify({ error: result.error }),
        { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    let rawText = result.data.candidates?.[0]?.content?.parts?.[0]?.text || "{}";
    rawText = rawText.replace(/```json/g, "").replace(/```/g, "").trim();

    let generatedText = "";
    try {
      const parsed = JSON.parse(rawText);
      generatedText = parsed.reply || rawText;
    } catch {
      generatedText = rawText;
    }

    const initialStatus = mode === "auto" ? "sent" : "pending";
    const { data: insertedLog, error: logErr } = await supabase
      .schema("threads")
      .from("auto_reply_logs")
      .insert({
        account_id: account.id,
        reply_id: crypto.randomUUID(),
        status: initialStatus,
        generated_text: generatedText,
        final_text: generatedText,
        llm_meta: {
          model: result.modelUsed,
          incoming_comment: incomingComment,
          media_id: mediaId,
          rag_matched_count: ragContexts.length
        }
      })
      .select('*')
      .single();

    if (logErr) throw logErr;

    return new Response(
      JSON.stringify({ success: true, log: insertedLog }),
      { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );

  } catch (err: any) {
    return new Response(
      JSON.stringify({ error: err.message }),
      { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
