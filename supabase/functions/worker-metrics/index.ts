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

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });

  try {
    const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
    const serviceRoleKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
    const supabase = createClient(supabaseUrl, serviceRoleKey);

    console.log("[worker-metrics] Starting metrics sync worker...");

    const { data: accounts, error: accErr } = await supabase
      .schema("threads")
      .from("threads_accounts")
      .select("*")
      .eq("connection_status", "connected");

    if (accErr) {
      console.error("[worker-metrics] Error fetching accounts:", accErr.message);
    }

    console.log(`[worker-metrics] Found ${accounts?.length || 0} connected accounts.`);

    if (!accounts || accounts.length === 0) {
      return new Response(JSON.stringify({ message: "Tidak ada akun connected." }), { status: 200, headers: corsHeaders });
    }

    let syncedPostsCount = 0;

    for (const acc of accounts) {
      const accessToken = acc.settings?.access_token;
      if (!accessToken) {
        console.log(`[worker-metrics] Account ${acc.id} (${acc.username}) has no access_token in settings.`);
        continue;
      }

      const { data: publishedPosts, error: postErr } = await supabase
        .schema("threads")
        .from("scheduled_posts")
        .select("published_media_id, text, scheduled_for, created_at")
        .eq("account_id", acc.id)
        .eq("status", "published")
        .not("published_media_id", "is", null);

      if (postErr) {
        console.error(`[worker-metrics] Error fetching scheduled_posts:`, postErr.message);
      }

      console.log(`[worker-metrics] Found ${publishedPosts?.length || 0} published posts.`);

      if (!publishedPosts || publishedPosts.length === 0) continue;

      for (const sp of publishedPosts) {
        const mediaId = sp.published_media_id;
        console.log(`[worker-metrics] Processing media_id: ${mediaId}`);

        let { data: postRecord, error: selectPostErr } = await supabase
          .schema("threads")
          .from("posts")
          .select("id")
          .eq("threads_media_id", mediaId)
          .maybeSingle();

        if (selectPostErr) {
          console.error(`[worker-metrics] Error selecting post record:`, selectPostErr.message);
        }

        if (!postRecord) {
          const postedAtVal = sp.scheduled_for || sp.created_at || new Date().toISOString();
          const { data: insertedPost, error: insertPostErr } = await supabase
            .schema("threads")
            .from("posts")
            .insert({
              account_id: acc.id,
              threads_media_id: mediaId,
              posted_at: postedAtVal
            })
            .select("id")
            .single();

          if (insertPostErr) {
            console.error(`[worker-metrics] Failed inserting to posts table:`, insertPostErr.message);
            continue;
          }
          postRecord = insertedPost;
        }

        if (!postRecord) continue;

        try {
          const insightUrl = `https://graph.threads.net/v1.0/${mediaId}/insights?metric=views,likes,replies,reposts,quotes&access_token=${accessToken}`;
          const res = await fetchWithTimeout(insightUrl, {}, 5000);
          const resData = await res.json();

          if (resData.error) {
            console.error(`[worker-metrics] Meta Graph API Error for ${mediaId}:`, JSON.stringify(resData.error));
            continue;
          }

          if (resData?.data && Array.isArray(resData.data)) {
            const metricsObj: any = { views: 0, likes: 0, replies: 0, reposts: 0, quotes: 0 };
            for (const item of resData.data) {
              if (item.name && item.values?.[0]?.value !== undefined) {
                metricsObj[item.name] = item.values[0].value;
              }
            }

            console.log(`[worker-metrics] Metrics fetched for ${mediaId}:`, JSON.stringify(metricsObj));

            const { error: insertMetricErr } = await supabase
              .schema("threads")
              .from("post_metrics")
              .insert({
                post_id: postRecord.id,
                snapshot_label: "latest",
                views: metricsObj.views || 0,
                likes: metricsObj.likes || 0,
                replies: metricsObj.replies || 0,
                reposts: metricsObj.reposts || 0,
                quotes: metricsObj.quotes || 0
              });

            if (insertMetricErr) {
              console.error(`[worker-metrics] Error inserting post_metrics:`, insertMetricErr.message);
            } else {
              syncedPostsCount++;
            }
          }
        } catch (apiErr: any) {
          console.error(`[worker-metrics] Exception during Meta API call:`, apiErr.message);
        }
      }
    }

    console.log(`[worker-metrics] Finished. Synced ${syncedPostsCount} posts.`);

    return new Response(
      JSON.stringify({ success: true, message: `Berhasil sinkronisasi ${syncedPostsCount} metrik postingan.` }),
      { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (err: any) {
    console.error("[worker-metrics] Fatal Worker Error:", err.message);
    return new Response(JSON.stringify({ error: err.message }), { status: 500, headers: corsHeaders });
  }
});
