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

    // 1. Ambil post yang siap dipublish (status: scheduled dan scheduled_for <= now)
    const { data: duePosts, error: fetchErr } = await supabase
      .schema("threads")
      .from("scheduled_posts")
      .select("*, threads_accounts(*)")
      .eq("status", "scheduled")
      .lte("scheduled_for", now)
      .limit(10);

    if (fetchErr) throw fetchErr;

    const results = [];

    for (const post of duePosts || []) {
      const account = post.threads_accounts;

      if (!account || account.kill_switch || account.connection_status === "suspended") {
        continue;
      }

      // Ambil token dari settings JSONB
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

      // Kunci status ke 'publishing'
      await supabase
        .schema("threads")
        .from("scheduled_posts")
        .update({ status: "publishing", attempts: (post.attempts || 0) + 1 })
        .eq("id", post.id);

      try {
        // Step A: Buat Container Post di Threads API
        let creationId = post.creation_id;
        if (!creationId) {
          const createRes = await fetch(`https://graph.threads.net/v1.0/${userId}/threads`, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: new URLSearchParams({
              media_type: "TEXT",
              text: post.text || "",
              access_token: accessToken,
            }),
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

        // Step B: Publish Container
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

        // Update status ke 'published'
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
