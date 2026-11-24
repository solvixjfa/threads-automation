import { createClient } from "npm:@supabase/supabase-js@2";

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

    let targetAccountId = "";
    if (req.method !== "GET") {
      try {
        const body = await req.json();
        targetAccountId = body?.account_id || "";
      } catch {
        // Ignore empty body
      }
    }

    let accQuery = supabase
      .schema("threads")
      .from("threads_accounts")
      .select("*")
      .eq("connection_status", "connected");

    if (targetAccountId) {
      accQuery = accQuery.eq("id", targetAccountId);
    }

    const { data: accounts, error: accErr } = await accQuery;
    if (accErr) console.error("[worker-metrics] Error fetching accounts:", accErr.message);
    if (!accounts || accounts.length === 0) {
      return new Response(JSON.stringify({ success: true, message: "Tidak ada akun connected." }), {
        status: 200,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    let syncedPostsCount = 0;
    let skippedPostsCount = 0;
    let newlyDiscoveredCount = 0;
    const todayStr = new Date().toISOString().split("T")[0];
    const thirtyDaysAgo = new Date();
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);

    for (const acc of accounts) {
      const accessToken = acc.settings?.access_token;
      if (!accessToken) continue;

      // 1. Sinkronkan foto profil & username terbaru dari Threads API
      try {
        const meRes = await fetchWithTimeout(
          `https://graph.threads.net/v1.0/me?fields=id,username,threads_profile_picture_url&access_token=${accessToken}`,
          {},
          5000
        );
        const meData = await meRes.json();
        if (meData && !meData.error) {
          const updatePayload: Record<string, any> = {
            last_synced_at: new Date().toISOString(),
          };
          if (meData.username) updatePayload.username = meData.username;
          if (meData.threads_profile_picture_url) {
            updatePayload.profile_picture_url = meData.threads_profile_picture_url;
          }
          await supabase
            .schema("threads")
            .from("threads_accounts")
            .update(updatePayload)
            .eq("id", acc.id);
        }
      } catch (meErr: any) {
        console.warn(`[worker-metrics] Profile sync skipped for ${acc.username}:`, meErr.message);
      }

      // 2. Tarik dan lengkapi daftar postingan terbaru di tabel threads.posts
      try {
        const mediaListUrl = `https://graph.threads.net/v1.0/me/threads?fields=id,text,permalink,timestamp,media_type&limit=25&access_token=${accessToken}`;
        const mediaRes = await fetchWithTimeout(mediaListUrl, {}, 6000);
        const mediaJson = await mediaRes.json();

        if (Array.isArray(mediaJson?.data)) {
          for (const item of mediaJson.data) {
            const mediaId = String(item.id || "");
            if (!mediaId) continue;

            const postedTs = item.timestamp || new Date().toISOString();
            const { data: existingPost } = await supabase
              .schema("threads")
              .from("posts")
              .select("id, text, permalink")
              .eq("account_id", acc.id)
              .eq("threads_media_id", mediaId)
              .maybeSingle();

            if (!existingPost) {
              await supabase.schema("threads").from("posts").insert({
                account_id: acc.id,
                threads_media_id: mediaId,
                text: item.text || null,
                media_type: item.media_type || null,
                permalink: item.permalink || null,
                posted_at: postedTs,
                source: "imported",
              });
              newlyDiscoveredCount++;
            } else {
              await supabase
                .schema("threads")
                .from("posts")
                .update({
                  text: item.text || existingPost.text || null,
                  media_type: item.media_type || null,
                  permalink: item.permalink || existingPost.permalink || null,
                  posted_at: postedTs,
                })
                .eq("id", existingPost.id);
            }
          }
        }
      } catch (listErr: any) {
        console.warn(`[worker-metrics] Media list fetch skipped for ${acc.username}:`, listErr.message);
      }

      // 3. Tarik Insights (Views, Likes, Replies, Reposts, Quotes) untuk post 30 hari terakhir
      const { data: allPosts } = await supabase
        .schema("threads")
        .from("posts")
        .select("id, threads_media_id, posted_at, created_at")
        .eq("account_id", acc.id)
        .gte("posted_at", thirtyDaysAgo.toISOString())
        .not("threads_media_id", "is", null);

      if (!allPosts || allPosts.length === 0) continue;

      let accDailyViews = 0;
      let accDailyLikes = 0;
      let accDailyReplies = 0;
      let accDailyReposts = 0;
      let accDailyQuotes = 0;

      for (const post of allPosts) {
        const mediaId = post.threads_media_id;
        if (!mediaId) continue;

        try {
          const insightUrl = `https://graph.threads.net/v1.0/${mediaId}/insights?metric=views,likes,replies,reposts,quotes&access_token=${accessToken}`;
          const res = await fetchWithTimeout(insightUrl, {}, 5000);
          const resData = await res.json();

          if (resData?.data && Array.isArray(resData.data)) {
            const metricsObj: any = { views: 0, likes: 0, replies: 0, reposts: 0, quotes: 0 };
            for (const item of resData.data) {
              if (item.name && item.values?.[0]?.value !== undefined) {
                metricsObj[item.name] = item.values[0].value;
              }
            }

            accDailyViews += metricsObj.views || 0;
            accDailyLikes += metricsObj.likes || 0;
            accDailyReplies += metricsObj.replies || 0;
            accDailyReposts += metricsObj.reposts || 0;
            accDailyQuotes += metricsObj.quotes || 0;

            await supabase
              .schema("threads")
              .from("post_metrics")
              .delete()
              .eq("post_id", post.id)
              .eq("snapshot_label", "latest");

            await supabase.schema("threads").from("post_metrics").insert({
              post_id: post.id,
              snapshot_label: "latest",
              views: metricsObj.views || 0,
              likes: metricsObj.likes || 0,
              replies: metricsObj.replies || 0,
              reposts: metricsObj.reposts || 0,
              quotes: metricsObj.quotes || 0,
              captured_at: new Date().toISOString(),
            });

            syncedPostsCount++;
          } else {
            skippedPostsCount++;
          }
        } catch (apiErr: any) {
          console.error(`[worker-metrics] Error API for ${mediaId}:`, apiErr.message);
          skippedPostsCount++;
        }
      }

      await supabase.schema("threads").from("account_insights_daily").upsert(
        {
          account_id: acc.id,
          date: todayStr,
          views: accDailyViews,
          likes: accDailyLikes,
          replies: accDailyReplies,
          reposts: accDailyReposts,
          quotes: accDailyQuotes,
        },
        { onConflict: "account_id,date" }
      );
    }

    return new Response(
      JSON.stringify({
        success: true,
        message: `Synced ${syncedPostsCount} metrics, discovered ${newlyDiscoveredCount} posts.`,
        synced: syncedPostsCount,
        discovered: newlyDiscoveredCount,
        skipped: skippedPostsCount,
      }),
      { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (err: any) {
    return new Response(JSON.stringify({ error: err.message }), {
      status: 500,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }
});
