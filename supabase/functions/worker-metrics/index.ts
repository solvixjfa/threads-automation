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

    // 1. Cari semua akun Threads yang connected
    const { data: accounts } = await supabase
      .schema("threads")
      .from("threads_accounts")
      .select("*")
      .eq("connection_status", "connected");

    if (!accounts || accounts.length === 0) {
      return new Response(JSON.stringify({ message: "Tidak ada akun connected." }), { status: 200, headers: corsHeaders });
    }

    let syncedPostsCount = 0;

    for (const acc of accounts) {
      const accessToken = acc.settings?.access_token;
      if (!accessToken) continue;

      // 2. Ambil postingan terbit dari scheduled_posts yang punya published_media_id
      const { data: publishedPosts } = await supabase
        .schema("threads")
        .from("scheduled_posts")
        .select("published_media_id")
        .eq("account_id", acc.id)
        .eq("status", "published")
        .not("published_media_id", "is", null);

      if (!publishedPosts || publishedPosts.length === 0) continue;

      for (const sp of publishedPosts) {
        const mediaId = sp.published_media_id;

        // A. Pastikan terdaftar di tabel threads.posts (hanya kolom account_id & threads_media_id)
        let { data: postRecord } = await supabase
          .schema("threads")
          .from("posts")
          .select("id")
          .eq("threads_media_id", mediaId)
          .maybeSingle();

        if (!postRecord) {
          const { data: insertedPost } = await supabase
            .schema("threads")
            .from("posts")
            .insert({ account_id: acc.id, threads_media_id: mediaId })
            .select("id")
            .single();
          postRecord = insertedPost;
        }

        if (!postRecord) continue;

        // B. Tarik statistik /insights dari Meta Threads API
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

            // C. Simpan snapshot metrik ke post_metrics
            await supabase
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

            syncedPostsCount++;
          }
        } catch {
          // Abaikan jika post tertentu error saat ditarik metriknya
        }
      }
    }

    return new Response(
      JSON.stringify({ success: true, message: `Berhasil sinkronisasi ${syncedPostsCount} metrik postingan.` }),
      { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (err: any) {
    return new Response(JSON.stringify({ error: err.message }), { status: 500, headers: corsHeaders });
  }
});
