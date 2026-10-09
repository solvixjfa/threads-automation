import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { corsHeaders } from "../_shared/cors.ts";
import { checkAndIncrementQuota } from "../_shared/quota.ts";

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
    const serviceRoleKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
    const supabase = createClient(supabaseUrl, serviceRoleKey);

    const now = new Date().toISOString();

    // 1. Ambil post yang siap dipublish
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
      
      // Abaikan jika akun dalam kondisi kill_switch aktif atau suspended
      if (!account || account.kill_switch || account.connection_status === "suspended") {
        continue;
      }

      // Cek Quota (Maks 250 post / 24 jam)
      const { allowed } = await checkAndIncrementQuota(supabase, account.id, "publish", 250);
      if (!allowed) {
        // Kuota habis: tunda postingan ke jam berikutnya
        await supabase
          .schema("threads")
          .from("scheduled_posts")
          .update({ last_error: "Rate limit reached. Postponed." })
          .eq("id", post.id);
        
        results.push({ post_id: post.id, status: "quota_exceeded" });
        continue;
      }

      // Kunci status jadi 'publishing' untuk cegah duplikasi
      await supabase
        .schema("threads")
        .from("scheduled_posts")
        .update({ status: "publishing", attempts: post.attempts + 1 })
        .eq("id", post.id);

      try {
        const accessToken = account.last_error || ''; // Token 60 hari
        const userId = account.threads_user_id;

        // Step A: Buat Container Post di Threads
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
          if (createData.error) throw new Error(createData.error.message);
          
          creationId = createData.id;
          
          // Simpan creation_id untuk idempotency
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
        if (pubData.error) throw new Error(pubData.error.message);

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
        const isFailedPermanently = post.attempts >= 5;
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
