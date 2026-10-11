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

async function generateContentWithFallback(apiKey: string, systemPrompt: string) {
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
    const authHeader = req.headers.get("Authorization");
    const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
    const serviceRoleKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
    const anonKey = Deno.env.get("SUPABASE_ANON_KEY") || serviceRoleKey;
    const geminiApiKey = Deno.env.get("GEMINI_API_KEY")!;

    const { topic, tone } = await req.json();
    if (!topic) {
      return new Response(
        JSON.stringify({ error: "Topik tidak boleh kosong." }),
        { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const supabase = createClient(supabaseUrl, serviceRoleKey);
    let userTonePrompt = "";
    let ragContexts: string[] = [];

    if (authHeader) {
      const userClient = createClient(supabaseUrl, anonKey, {
        global: { headers: { Authorization: authHeader } }
      });
      const { data: { user } } = await userClient.auth.getUser();

      if (user) {
        const { data: account } = await supabase
          .schema("threads")
          .from("threads_accounts")
          .select("id")
          .eq("user_id", user.id)
          .limit(1)
          .maybeSingle();

        if (account) {
          const { data: settings } = await supabase
            .schema("threads")
            .from("auto_reply_settings")
            .select("tone_prompt")
            .eq("account_id", account.id)
            .maybeSingle();

          if (settings) userTonePrompt = settings.tone_prompt || "";

          // SEMANTIC VECTOR SEARCH (Threshold diturunkan ke 0.15)
          const topicVector = await getEmbedding(topic, geminiApiKey);
          if (topicVector) {
            const { data: matchedDocs } = await supabase.rpc("match_brand_knowledge", {
              query_embedding: JSON.stringify(topicVector),
              match_threshold: 0.15,
              match_count: 5,
              p_account_id: account.id
            }, { schema: "threads" });

            if (matchedDocs && matchedDocs.length > 0) {
              ragContexts = matchedDocs.map((d: any) => `[FAKTA RELEVAN: ${d.title}] ${d.content}`);
            }
          }
        }
      }
    }

    const systemPrompt = `Kamu adalah AI Assistant pembuat konten Threads (Meta).
Tugasmu merancang 3 variasi draf postingan Threads berdasarkan topik yang diberikan dan FAKTA RELEVAN dari Knowledge Base.

FAKTA/KONTEKS RAG TERKAIT (Wajib digunakan jika ada):
${ragContexts.length > 0 ? ragContexts.join("\n") : "Tidak ada dokumen khusus yang cocok."}

INSTRUKSI PERSONA & TONE:
${userTonePrompt || "Gunakan bahasa kasual, natural, tanpa emoji berlebihan, dan tidak kaku."}

TOPIK UTAMA: "${topic}"
GAYA PILIHAN: "${tone || 'Edukasi & Insight'}"

ATURAN OUTPUT:
1. Hasilkan 3 opsi draf postingan.
2. Draf 1: Ringkas & Direct (100-200 karakter)
3. Draf 2: Insight / Storytelling (300-450 karakter)
4. Draf 3: Utasan / Thread Panjang (> 500 karakter)
5. HANYA kembalikan JSON array valid:
[
  { "id": 1, "title": "Ringkas & Direct", "content": "isi draf 1..." },
  { "id": 2, "title": "Insight & Storytelling", "content": "isi draf 2..." },
  { "id": 3, "title": "Format Utasan / Thread", "content": "isi draf 3..." }
]`;

    const result = await generateContentWithFallback(geminiApiKey, systemPrompt);
    if (!result.success || !result.data) {
      return new Response(
        JSON.stringify({ error: result.error }),
        { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    let rawText = result.data.candidates?.[0]?.content?.parts?.[0]?.text || "[]";
    rawText = rawText.replace(/```json/g, "").replace(/```/g, "").trim();

    let options = [];
    try {
      options = JSON.parse(rawText);
    } catch {
      options = [{ id: 1, title: "Draf Post", content: rawText }];
    }

    return new Response(
      JSON.stringify({ success: true, options }),
      { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (err: any) {
    return new Response(
      JSON.stringify({ error: err.message }),
      { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
