import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

// Deklarasi Global EdgeRuntime agar Deno tidak mematikan isolate di background
declare const EdgeRuntime: {
  waitUntil(promise: Promise<any>): void;
};

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

const CANDIDATE_MODELS = [
  "gemini-3.8-flash",
  "gemini-3.5-flash-lite",
  "gemini-2.5-flash"
];

async function fetchWithTimeout(resource: string, options: any = {}, timeoutMs = 8000) {
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const response = await fetch(resource, { ...options, signal: controller.signal });
    clearTimeout(id);
    return response;
  } catch (err) {
    clearTimeout(id);
    throw err;
  }
}

async function getEmbedding(text: string, apiKey: string): Promise<number[] | null> {
  try {
    const res = await fetchWithTimeout(
      `https://generativelanguage.googleapis.com/v1beta/models/text-embedding-004:embedContent?key=${apiKey}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "models/text-embedding-004",
          content: { parts: [{ text }] }
        }),
      },
      6000
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
      const res = await fetchWithTimeout(
        `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            contents: [{ parts: [{ text: systemPrompt }] }],
            generationConfig: { responseMimeType: "application/json" }
          }),
        },
        8000
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

    let action = "sync";
    let commentText = "";
    let approveLogId = "";
    let finalTextToPublish = "";

    try {
      const body = await req.json();
      action = body?.action || "sync";
      commentText = body?.comment || "";
      approveLogId = body?.log_id || "";
      finalTextToPublish = body?.final_text || "";
    } catch {
      // Default action: sync
    }

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

    // 1. PUBLISH APPROVED REPLY
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
        .maybeSingle();

      if (!targetLog) throw new Error("Log balasan tidak ditemukan.");

      const targetReplyId = targetLog.llm_meta?.threads_reply_id || targetLog.reply_id;

      const createRes = await fetchWithTimeout(`https://graph.threads.net/v1.0/${threadsUserId}/threads`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({
          media_type: "TEXT",
          text: finalTextToPublish,
          reply_to_id: targetReplyId,
          access_token: accessToken,
        }),
      }, 10000);
      const createData = await createRes.json();
      if (createData.error) throw new Error(createData.error.message);

      const pubRes = await fetchWithTimeout(`https://graph.threads.net/v1.0/${threadsUserId}/threads_publish`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({
          creation_id: createData.id,
          access_token: accessToken,
        }),
      }, 10000);
      const pubData = await pubRes.json();
      if (pubData.error) throw new Error(pubData.error.message);

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

    // 2. FAST SYNC (< 1 DETIK)
    if (action === "sync" || action === "sync_and_process") {
      let itemsToInsert = [];

      if (commentText) {
        itemsToInsert.push({
          account_id: account.id,
          reply_id: crypto.randomUUID(),
          status: "unprocessed",
          generated_text: "",
          final_text: "",
          llm_meta: {
            incoming_comment: commentText,
            media_id: "simulated_media"
          }
        });
      } else {
        const { data: publishedPosts } = await supabase
          .schema("threads")
          .from("scheduled_posts")
          .select("published_media_id")
          .eq("status", "published")
          .not("published_media_id", "is", null)
          .order("created_at", { ascending: false })
          .limit(5);

        if (publishedPosts && publishedPosts.length > 0 && accessToken) {
          for (const p of publishedPosts) {
            try {
              const res = await fetchWithTimeout(`https://graph.threads.net/v1.0/${p.published_media_id}/replies?access_token=${accessToken}`, {}, 5000);
              const resData = await res.json();
              if (resData?.data && Array.isArray(resData.data)) {
                for (const rep of resData.data) {
                  itemsToInsert.push({
                    account_id: account.id,
                    reply_id: rep.id,
                    status: "unprocessed",
                    generated_text: "",
                    final_text: "",
                    llm_meta: {
                      incoming_comment: rep.text || "",
                      threads_reply_id: rep.id,
                      media_id: p.published_media_id
                    }
                  });
                }
              }
            } catch {
              // Ignore individual fetch error
            }
          }
        }
      }

      let newInsertedCount = 0;
      for (const item of itemsToInsert) {
        const { data: existing } = await supabase
          .schema("threads")
          .from("auto_reply_logs")
          .select("id")
          .eq("reply_id", item.reply_id)
          .maybeSingle();

        if (!existing) {
          await supabase.schema("threads").from("auto_reply_logs").insert(item);
          newInsertedCount++;
        }
      }

      // Tahan Isolate Deno via waitUntil agar background process AI tidak mati paksa
      if (typeof EdgeRuntime !== "undefined" && EdgeRuntime.waitUntil) {
        EdgeRuntime.waitUntil(
          fetch(`${supabaseUrl}/functions/v1/worker-replies`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${serviceRoleKey}`
            },
            body: JSON.stringify({ action: "process_queue" })
          }).catch((err) => console.error("Background Queue Error:", err))
        );
      }

      return new Response(
        JSON.stringify({ success: true, message: "Sync selesai.", newItems: newInsertedCount }),
        { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    // 3. ASYNC AI QUEUE PROCESSOR
    if (action === "process_queue") {
      const { data: settings } = await supabase
        .schema("threads")
        .from("auto_reply_settings")
        .select("*")
        .eq("account_id", account.id)
        .maybeSingle();

      const mode = settings?.mode || "review";
      const tonePrompt = settings?.tone_prompt || "Gunakan bahasa kasual, ramah, to the point, dan profesional.";

      const { data: queueItems } = await supabase
        .schema("threads")
        .from("auto_reply_logs")
        .select("*")
        .eq("status", "unprocessed")
        .limit(3);

      if (!queueItems || queueItems.length === 0) {
        return new Response(
          JSON.stringify({ success: true, message: "Antrean kosong." }),
          { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
        );
      }

      for (const item of queueItems) {
        try {
          const incomingComment = item.llm_meta?.incoming_comment || "";
          if (!incomingComment) {
            await supabase.schema("threads").from("auto_reply_logs").delete().eq("id", item.id);
            continue;
          }

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

KOMENTAR AUDIENS:
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
            await supabase.schema("threads").from("auto_reply_logs").update({ status: "failed" }).eq("id", item.id);
            continue;
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

          const targetStatus = mode === "auto" ? "sent" : "pending";

          await supabase
            .schema("threads")
            .from("auto_reply_logs")
            .update({
              status: targetStatus,
              generated_text: generatedText,
              final_text: generatedText,
              llm_meta: {
                ...item.llm_meta,
                model: result.modelUsed,
                rag_matched_count: ragContexts.length
              }
            })
            .eq("id", item.id);

        } catch {
          await supabase.schema("threads").from("auto_reply_logs").update({ status: "failed" }).eq("id", item.id);
        }
      }

      return new Response(
        JSON.stringify({ success: true, message: "Queue AI selesai diproses." }),
        { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    return new Response(
      JSON.stringify({ error: "Action tidak dikenal." }),
      { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );

  } catch (globalErr: any) {
    return new Response(
      JSON.stringify({ error: globalErr.message }),
      { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
