import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

async function fetchWithTimeout(resource: string, options: any = {}, timeoutMs = 6000) {
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

serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });

  try {
    const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
    const serviceRoleKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
    const supabase = createClient(supabaseUrl, serviceRoleKey);

    const body = await req.json().catch(() => ({}));
    const action = body.action || "sync";
    const userId = body.user_id || "";
    const commentText = body.comment || "";
    const approveLogId = body.log_id || "";
    const finalTextToPublish = body.final_text || "";

    if (!userId) {
      return new Response(JSON.stringify({ error: "user_id wajib dikirim." }), { status: 400, headers: corsHeaders });
    }

    const { data: account } = await supabase.schema("threads").from("threads_accounts")
      .select("*").eq("user_id", userId).eq("connection_status", "connected").maybeSingle();

    if (!account) {
      return new Response(JSON.stringify({ error: "Belum ada akun Threads tersambung." }), { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } });
    }

    const accessToken = account.settings?.access_token || "";
    const threadsUserId = account.threads_user_id || "";

    // ACTION 1: SYNC MURNI (Tarik data dari Meta dan simpan ke Database, Tanpa AI)
    if (action === "sync") {
      let itemsToInsert = [];

      if (commentText) {
        itemsToInsert.push({ account_id: account.id, reply_id: crypto.randomUUID(), status: "unprocessed", generated_text: "", final_text: "", llm_meta: { incoming_comment: commentText, media_id: "simulated_media" } });
      } else {
        const { data: publishedPosts } = await supabase.schema("threads").from("scheduled_posts")
          .select("published_media_id").eq("account_id", account.id).eq("status", "published")
          .not("published_media_id", "is", null).order("created_at", { ascending: false }).limit(2);

        if (publishedPosts && publishedPosts.length > 0 && accessToken) {
          for (const p of publishedPosts) {
            try {
              const res = await fetchWithTimeout(`https://graph.threads.net/v1.0/${p.published_media_id}/replies?access_token=${accessToken}`, {}, 4000);
              const resData = await res.json();
              if (resData?.data && Array.isArray(resData.data)) {
                for (const rep of resData.data) {
                  itemsToInsert.push({ account_id: account.id, reply_id: rep.id, status: "unprocessed", generated_text: "", final_text: "", llm_meta: { incoming_comment: rep.text || "", threads_reply_id: rep.id, media_id: p.published_media_id } });
                }
              }
            } catch {} // Abaikan timeout per post
          }
        }
      }

      let newInsertedCount = 0;
      for (const item of itemsToInsert) {
        const { data: existing } = await supabase.schema("threads").from("auto_reply_logs").select("id").eq("reply_id", item.reply_id).maybeSingle();
        if (!existing) {
          await supabase.schema("threads").from("auto_reply_logs").insert(item);
          newInsertedCount++;
        }
      }

      return new Response(JSON.stringify({ success: true, message: "Sync selesai.", newItems: newInsertedCount }), { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } });
    }

    // ACTION 2: PUBLISH BALASAN MANUAL (Biar tombol 'Kirim ke Threads' di UI tetap jalan kalau diisi manual)
    if (action === "publish_reply") {
      if (!approveLogId || !finalTextToPublish) throw new Error("Parameter tidak lengkap.");
      const { data: targetLog } = await supabase.schema("threads").from("auto_reply_logs").select("*").eq("id", approveLogId).maybeSingle();
      if (!targetLog) throw new Error("Log balasan tidak ditemukan.");
      
      const targetReplyId = targetLog.llm_meta?.threads_reply_id || targetLog.reply_id;
      const createRes = await fetchWithTimeout(`https://graph.threads.net/v1.0/${threadsUserId}/threads`, { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body: new URLSearchParams({ media_type: "TEXT", text: finalTextToPublish, reply_to_id: targetReplyId, access_token: accessToken }) }, 8000);
      const createData = await createRes.json();
      if (createData.error) throw new Error(createData.error.message);

      const pubRes = await fetchWithTimeout(`https://graph.threads.net/v1.0/${threadsUserId}/threads_publish`, { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body: new URLSearchParams({ creation_id: createData.id, access_token: accessToken }) }, 8000);
      const pubData = await pubRes.json();
      if (pubData.error) throw new Error(pubData.error.message);

      await supabase.schema("threads").from("auto_reply_logs").update({ status: "sent", final_text: finalTextToPublish, sent_media_id: pubData.id }).eq("id", approveLogId);
      return new Response(JSON.stringify({ success: true }), { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } });
    }

    return new Response(JSON.stringify({ error: "Action tidak valid." }), { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } });
  } catch (err: any) {
    return new Response(JSON.stringify({ error: err.message }), { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } });
  }
});
