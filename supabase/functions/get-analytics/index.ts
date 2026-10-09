import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { corsHeaders } from "../_shared/cors.ts";

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    const authHeader = req.headers.get("Authorization");
    if (!authHeader) {
      return new Response(JSON.stringify({ error: "Missing Authorization header" }), {
        status: 401,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
    const supabaseAnonKey = Deno.env.get("SUPABASE_ANON_KEY")!;
    const serviceRoleKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;

    // Client via Auth User
    const userClient = createClient(supabaseUrl, supabaseAnonKey, {
      global: { headers: { Authorization: authHeader } },
    });

    const { data: { user } } = await userClient.auth.getUser();
    if (!user) {
      return new Response(JSON.stringify({ error: "Unauthorized" }), {
        status: 401,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const supabase = createClient(supabaseUrl, serviceRoleKey);

    // Ambil akun Threads milik user
    const { data: account, error: accErr } = await supabase
      .schema("threads")
      .from("threads_accounts")
      .select("id")
      .eq("user_id", user.id)
      .single();

    if (accErr || !account) {
      return new Response(JSON.stringify({ error: "Threads account not found" }), {
        status: 444,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    // 1. Overview & Post Performance Summary
    const { data: posts, error: postsErr } = await supabase
      .schema("threads")
      .from("posts")
      .select(`
        id, threads_media_id, text, permalink, posted_at,
        post_metrics (views, likes, replies, reposts, quotes, snapshot_label)
      `)
      .eq("account_id", account.id)
      .order("posted_at", { ascending: false });

    if (postsErr) throw postsErr;

    let totalViews = 0;
    let totalLikes = 0;
    let totalReplies = 0;
    let totalReposts = 0;

    const formattedPosts = (posts || []).map((p: any) => {
      // Ambil snapshot 'latest' atau paling relevan
      const latestMetrics = p.post_metrics?.find((m: any) => m.snapshot_label === 'latest') || p.post_metrics?.[0] || {
        views: 0, likes: 0, replies: 0, reposts: 0, quotes: 0
      };

      totalViews += latestMetrics.views || 0;
      totalLikes += latestMetrics.likes || 0;
      totalReplies += latestMetrics.replies || 0;
      totalReposts += latestMetrics.reposts || 0;

      const engagement = (latestMetrics.views > 0)
        ? ((latestMetrics.likes + latestMetrics.replies + latestMetrics.reposts) / latestMetrics.views) * 100
        : 0;

      return {
        id: p.id,
        threads_media_id: p.threads_media_id,
        text: p.text,
        permalink: p.permalink,
        posted_at: p.posted_at,
        metrics: latestMetrics,
        engagement_rate: parseFloat(engagement.toFixed(2))
      };
    });

    // Sort Top Posts berdasarkan engagement rate
    const topPosts = [...formattedPosts].sort((a, b) => b.engagement_rate - a.engagement_rate).slice(0, 5);

    // 2. Daily Trends
    const { data: dailyInsights } = await supabase
      .schema("threads")
      .from("account_insights_daily")
      .select("*")
      .eq("account_id", account.id)
      .order("date", { ascending: true })
      .limit(30);

    const overview = {
      total_posts: posts?.length || 0,
      total_views: totalViews,
      total_likes: totalLikes,
      total_replies: totalReplies,
      total_reposts: totalReposts,
      avg_engagement_rate: formattedPosts.length > 0 
        ? parseFloat((formattedPosts.reduce((acc, p) => acc + p.engagement_rate, 0) / formattedPosts.length).toFixed(2))
        : 0
    };

    return new Response(
      JSON.stringify({
        success: true,
        overview,
        top_posts: topPosts,
        recent_posts: formattedPosts.slice(0, 20),
        daily_trends: dailyInsights || []
      }),
      { headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (err: any) {
    return new Response(JSON.stringify({ error: err.message }), {
      status: 500,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }
});
