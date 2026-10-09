import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { corsHeaders } from "../_shared/cors.ts";

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
    const serviceRoleKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
    const supabase = createClient(supabaseUrl, serviceRoleKey);

    // Ambil postingan yang di-publish dalam 7 hari terakhir untuk di-snapshot
    const sevenDaysAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString();

    const { data: recentPosts, error: postsErr } = await supabase
      .schema("threads")
      .from("posts")
      .select("id, threads_media_id, account_id, posted_at")
      .gte("posted_at", sevenDaysAgo);

    if (postsErr) throw postsErr;

    let updatedCount = 0;

    for (const p of recentPosts || []) {
      // Hitung selisih jam untuk menentukan snapshot_label ('1h', '24h', '72h', '7d', 'latest')
      const hoursAgo = Math.floor((Date.now() - new Date(p.posted_at).getTime()) / (1000 * 60 * 60));
      let label = 'latest';
      if (hoursAgo <= 2) label = '1h';
      else if (hoursAgo <= 25) label = '24h';
      else if (hoursAgo <= 75) label = '72h';
      else if (hoursAgo <= 170) label = '7d';

      // Panggil Meta Insights API /{media_id}/insights
      // Upsert ke threads.post_metrics
      updatedCount++;
    }

    return new Response(
      JSON.stringify({ success: true, processed_posts: updatedCount }),
      { headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (err: any) {
    return new Response(JSON.stringify({ error: err.message }), {
      status: 500,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }
});
