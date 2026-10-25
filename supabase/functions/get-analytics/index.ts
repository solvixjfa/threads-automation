import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "npm:@supabase/supabase-js@2";
import { corsHeaders } from "../_shared/cors.ts";

serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });

  try {
    const authHeader = req.headers.get("Authorization");
    if (!authHeader) return new Response(JSON.stringify({ error: "Missing Authorization header" }), { status: 401, headers: { ...corsHeaders, "Content-Type": "application/json" } });

    const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
    const supabaseAnonKey = Deno.env.get("SUPABASE_ANON_KEY")!;
    const serviceRoleKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;

    const userClient = createClient(supabaseUrl, supabaseAnonKey, { global: { headers: { Authorization: authHeader } } });
    const { data: { user } } = await userClient.auth.getUser();
    if (!user) return new Response(JSON.stringify({ error: "Unauthorized" }), { status: 401, headers: { ...corsHeaders, "Content-Type": "application/json" } });

    const supabase = createClient(supabaseUrl, serviceRoleKey);
    const { data: account, error: accErr } = await supabase.schema("threads").from("threads_accounts").select("id").eq("user_id", user.id).maybeSingle();

    if (accErr || !account) return new Response(JSON.stringify({ error: "Threads account not found" }), { status: 444, headers: { ...corsHeaders, "Content-Type": "application/json" } });

    const { data: publishedScheduled } = await supabase.schema("threads").from("scheduled_posts").select("id, text, published_media_id, scheduled_for, created_at").eq("account_id", account.id).eq("status", "published");
    const { data: postsWithMetrics } = await supabase.schema("threads").from("posts").select(`id, threads_media_id, created_at, post_metrics (views, likes, replies, reposts, quotes, snapshot_label)`).eq("account_id", account.id);

    const scheduledMap = new Map();
    (publishedScheduled || []).forEach((sp: any) => {
      if (sp.published_media_id) scheduledMap.set(String(sp.published_media_id), sp);
    });

    let totalViews = 0, totalLikes = 0, totalReplies = 0, totalReposts = 0;

    const formattedPosts = (postsWithMetrics || []).map((p: any) => {
      const sp = scheduledMap.get(String(p.threads_media_id));
      const latestMetrics = p.post_metrics?.find((m: any) => m.snapshot_label === 'latest') || p.post_metrics?.[0] || { views: 0, likes: 0, replies: 0, reposts: 0, quotes: 0 };

      totalViews += latestMetrics.views || 0;
      totalLikes += latestMetrics.likes || 0;
      totalReplies += latestMetrics.replies || 0;
      totalReposts += latestMetrics.reposts || 0;

      const engagement = (latestMetrics.views > 0) ? ((latestMetrics.likes + latestMetrics.replies + latestMetrics.reposts) / latestMetrics.views) * 100 : 0;

      return {
        id: p.id,
        threads_media_id: p.threads_media_id,
        text: sp?.text || `Post Without Text (ID: ${p.threads_media_id?.slice(0, 8) || 'Unknown'})`,
        permalink: p.threads_media_id ? `https://www.threads.net/post/${p.threads_media_id}` : null, // FIX LINK
        posted_at: sp?.scheduled_for || p.created_at || new Date().toISOString(),
        metrics: latestMetrics,
        engagement_rate: parseFloat(engagement.toFixed(2))
      };
    });

    const { data: dailyInsights } = await supabase.schema("threads").from("account_insights_daily").select("*").eq("account_id", account.id).order("date", { ascending: true }).limit(30);
    if (totalViews === 0 && totalLikes === 0 && dailyInsights && dailyInsights.length > 0) {
      dailyInsights.forEach((d: any) => { totalViews += d.views || 0; totalLikes += d.likes || 0; totalReplies += d.replies || 0; totalReposts += d.reposts || 0; });
    }

    const sortedByDate = [...formattedPosts].sort((a, b) => new Date(b.posted_at).getTime() - new Date(a.posted_at).getTime());
    const overview = {
      total_posts: publishedScheduled?.length || formattedPosts.length || 0,
      total_views: totalViews, total_likes: totalLikes, total_replies: totalReplies, total_reposts: totalReposts,
      avg_engagement_rate: formattedPosts.length > 0 ? parseFloat((formattedPosts.reduce((acc, p) => acc + p.engagement_rate, 0) / formattedPosts.length).toFixed(2)) : 0
    };

    return new Response(JSON.stringify({ success: true, overview, all_posts: sortedByDate.slice(0, 50), daily_trends: dailyInsights || [] }), { headers: { ...corsHeaders, "Content-Type": "application/json" } });
  } catch (err: any) {
    return new Response(JSON.stringify({ error: err.message }), { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } });
  }
});
