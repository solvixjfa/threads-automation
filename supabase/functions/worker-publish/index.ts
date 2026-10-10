import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
    const serviceRoleKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
    const supabase = createClient(supabaseUrl, serviceRoleKey);

    const now = new Date().toISOString();

    const { data: duePosts, error: fetchErr } = await supabase
      .schema("threads")
      .from("scheduled_posts")
      .select("*, threads_accounts(*)")
      .eq("status", "scheduled")
      .lte("scheduled_for", now)
      .order("sequence_number", { ascending: true })
      .limit(10);

    if (fetchErr) throw fetchErr;

    const results = [];

    for (const post of duePosts || []) {
      const account = post.threads_accounts;

      if (!account || account.kill_switch || account.connection_status === "suspended") {
        continue;
      }

      const accessToken = account.settings?.access_token || '';
      const userId = account.threads_user_id;

      if (!accessToken || !userId) {
        await supabase
          .schema("threads")
          .from("scheduled_posts")
          .update({ last_error: "Missing access token or threads_user_id" })
          .eq("id", post.id);

        results.push({ post_id: post.id, status: "error", error: "Missing token" });
        continue;
      }

      // Jika post ini adalah bagian dari thread (memiliki parent_id), pastikan parent sudah dipublish
      let replyToMediaId: string | null = null;
      if (post.parent_id) {
        const { data: parentPost } = await supabase
          .schema("threads")
          .from("scheduled_posts")
          .select("status, published_media_id")
          .eq("id", post.parent_id)
          .single();

        if (!parentPost || parentPost.status !== "published" || !parentPost.published_media_id) {
          // Parent belum selesai terbit, tunda eksekusi part ini
          continue;
        }
        replyToMediaId = parentPost.published_media_id;
      }

      await supabase
        .schema("threads")
        .from("scheduled_posts")
        .update({ status: "publishing", attempts: (post.attempts || 0) + 1 })
        .eq("id", post.id);

      try {
        let creationId = post.creation_id;
        if (!creationId) {
          const bodyParams: Record<string, string> = {
            media_type: "TEXT",
            text: post.text || "",
            access_token: accessToken,
          };

          if (replyToMediaId) {
            bodyParams.reply_to_id = replyToMediaId;
          }

          const createRes = await fetch(`https://graph.threads.net/v1.0/${userId}/threads`, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: new URLSearchParams(bodyParams),
          });
          const createData = await createRes.json();
          if (createData.error) throw new Error(createData.error.message || JSON.stringify(createData.error));

          creationId = createData.id;

          await supabase
            .schema("threads")
            .from("scheduled_posts")
            .update({ creation_id: creationId })
            .eq("id", post.id);
        }

        const pubRes = await fetch(`https://graph.threads.net/v1.0/${userId}/threads_publish`, {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: new URLSearchParams({
            creation_id: creationId,
            access_token: accessToken,
          }),
        });
        const pubData = await pubRes.json();
        if (pubData.error) throw new Error(pubData.error.message || JSON.stringify(pubData.error));

        await supabase
          .schema("threads")
          .from("scheduled_posts")
          .update({
            status: "published",
            published_media_id: pubData.id,
            last_error: null,
          })
          .eq("id", post.id);

        results.push({ post_id: post.id, status: "published", media_id: pubData.id });
      } catch (err: any) {
        const isFailedPermanently = (post.attempts || 1) >= 5;
        await supabase
          .schema("threads")
          .from("scheduled_posts")
          .update({
            status: isFailedPermanently ? "failed" : "scheduled",
            last_error: err.message,
          })
          .eq("id", post.id);

        results.push({ post_id: post.id, status: "error", error: err.message });
      }
    }

    return new Response(JSON.stringify({ success: true, processed: results }), {
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  } catch (err: any) {
    return new Response(JSON.stringify({ error: err.message }), {
      status: 500,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }
});
