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

    let action = "poll";
    let commentText = "";
    let approveLogId = "";
    let finalTextToPublish = "";

    try {
      const body = await req.json();
      action = body.action || "poll";
      commentText = body.comment || "";
      approveLogId = body.log_id || "";
      finalTextToPublish = body.final_text || "";
    } catch {
      // Default action is poll
    }

    // Ambil akun Threads terhubung
    const { data: account } = await supabase
      .schema("threads")
      .from("threads_accounts")
      .select("*")
      .eq("connection_status", "connected")
      .limit(1)
      .maybeSingle();

    if (!account) {
      return new Response(
        JSON.stringify({ error: "Belum ada akun Threads tersambung." }),
        { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const accessToken = account.settings?.access_token || "";
    const threadsUserId = account.threads_user_id || "";

    // ACTION 1: PUBLISH APPROVED REPLY TO THREADS API
    if (action === "publish_reply") {
      if (!approveLogId || !finalTextToPublish) {
        return new Response(
          JSON.stringify({ error: "Parameter log_id dan final_text wajib diisi." }),
          { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
        );
      }

      const { data: targetLog } = await supabase
        .schema("threads")
        .from("auto_reply_logs")
        .select("*")
        .eq("id", approveLogId)
        .single();

      if (!targetLog) throw new Error("Log balasan tidak ditemukan.");

      const targetReplyId = targetLog.llm_meta?.threads_reply_id || targetLog.reply_id;

      // 1. Create Reply Container
      const createRes = await fetch(`https://graph.threads.net/v1.0/${threadsUserId}/threads`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({
          media_type: "TEXT",
          text: finalTextToPublish,
          reply_to_id: targetReplyId,
          access_token: accessToken,
        }),
      });
      const createData = await createRes.json();
      if (createData.error) throw new Error(createData.error.message);

      // 2. Publish Container
      const pubRes = await fetch(`https://graph.threads.net/v1.0/${threadsUserId}/threads_publish`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({
          creation_id: createData.id,
          access_token: accessToken,
        }),
      });
      const pubData = await pubRes.json();
      if (pubData.error) throw new Error(pubData.error.message);

      // Update Log Status
      await supabase
        .schema("threads")
        .from("auto_reply_logs")
        .update({
          status: "sent",
          final_text: finalTextToPublish,
          sent_media_id: pubData.id
        })
        .eq("id", approveLogId);

      return new Response(
        JSON.stringify({ success: true, published_media_id: pubData.id }),
        { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    // ACTION 2: SIMULATE OR POLL COMMENTS FROM THREADS GRAPH API
    const { data: settings } = await supabase
      .schema("threads")
      .from("auto_reply_settings")
      .select("*")
      .eq("account_id", account.id)
      .maybeSingle();

    const mode = settings?.mode || "review";
    const tonePrompt = settings?.tone_prompt || "Gunakan bahasa kasual, ramah, to the point, dan profesional.";

    let itemsToProcess: Array<{ reply_id: string; comment: string; media_id: string }> = [];

    if (commentText) {
      // Manual/Simulated
      itemsToProcess.push({
        reply_id: crypto.randomUUID(),
        comment: commentText,
        media_id: "simulated_media"
      });
    } else {
      // Real Polling dari Meta Threads API
      const { data: publishedPosts } = await supabase
        .schema("threads")
        .from("scheduled_posts")
        .select("published_media_id")
        .eq("status", "published")
        .not("published_media_id", "is", null)
        .order("created_at", { ascending: false })
        .limit(5);

      for (const p of publishedPosts || []) {
        if (!p.published_media_id || !accessToken) continue;
        try {
          const res = await fetch(`https://graph.threads.net/v1.0/${p.published_media_id}/replies?access_token=${accessToken}`);
          const resData = await res.json();

          if (resData.data && Array.isArray(resData.data)) {
            for (const rep of resData.data) {
              itemsToProcess.push({
                reply_id: rep.id,
                comment: rep.text || "",
                media_id: p.published_media_id
              });
            }
          }
        } catch {
          // Ignore polling errors for individual posts
        }
      }
    }

    const processedLogs = [];

    for (const item of itemsToProcess) {
      // Cek apakah reply_id sudah pernah dicatat di auto_reply_logs
      const { data: existing } = await supabase
        .schema("threads")
        .from("auto_reply_logs")
        .select("id")
        .eq("reply_id", item.reply_id)
        .maybeSingle();

      if (existing) continue; // Skip jika sudah pernah diolah

      // RAG Vector Similarity Search
      let ragContexts: string[] = [];
      const commentVector = await getEmbedding(item.comment, geminiApiKey);
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

KOMENTAR AUDIENS:
"${item.comment}"

ATURAN BALASAN:
1. Balas dengan ringkas (1-3 kalimat).
2. Jangan gunakan emoji berlebihan.
3. Langsung jawab fakta dari RAG jika ditanyakan detail teknis/bisnis.
4. HANYA kembalikan JSON valid:
{
  "reply": "isi teks balasan..."
}`;

      const result = await generateReplyWithFallback(geminiApiKey, systemPrompt);
      if (!result.success || !result.data) continue;

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
      const { data: insertedLog } = await supabase
        .schema("threads")
        .from("auto_reply_logs")
        .insert({
          account_id: account.id,
          reply_id: item.reply_id,
          status: initialStatus,
          generated_text: generatedText,
          final_text: generatedText,
          llm_meta: {
            model: result.modelUsed,
            incoming_comment: item.comment,
            threads_reply_id: item.reply_id,
            media_id: item.media_id,
            rag_matched_count: ragContexts.length
          }
        })
        .select('*')
        .single();

      if (insertedLog) processedLogs.push(insertedLog);
    }

    return new Response(
      JSON.stringify({ success: true, processedCount: processedLogs.length, logs: processedLogs }),
      { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );

  } catch (err: any) {
    return new Response(
      JSON.stringify({ error: err.message }),
      { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
