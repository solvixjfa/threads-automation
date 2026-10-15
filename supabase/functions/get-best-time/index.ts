import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { corsHeaders } from "../_shared/cors.ts";

const WEEKDAY_NAMES = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

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

    const { data: account } = await supabase
      .schema("threads")
      .from("threads_accounts")
      .select("id")
      .eq("user_id", user.id)
      .maybeSingle();

    if (!account) {
      return new Response(JSON.stringify({ error: "Threads account not found" }), {
        status: 404,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const { data: publishedScheduled } = await supabase
      .schema("threads")
      .from("scheduled_posts")
      .select("id, published_media_id, scheduled_for")
      .eq("account_id", account.id)
      .eq("status", "published");

    const { data: posts } = await supabase
      .schema("threads")
      .from("posts")
      .select(`
        id,
        threads_media_id,
        posted_at,
        created_at,
        post_metrics (views, likes, replies, reposts, snapshot_label)
      `)
      .eq("account_id", account.id);

    const scheduledMap = new Map();
    (publishedScheduled || []).forEach((sp: any) => {
      if (sp.published_media_id) {
        scheduledMap.set(sp.published_media_id, sp);
      }
    });

    const dataPoints: { day: number; hour: number; er: number }[] = [];

    (posts || []).forEach((p: any) => {
      const metricsArr = p.post_metrics || [];
      const latest = metricsArr.find((m: any) => m.snapshot_label === "latest") || metricsArr[0];
      if (!latest || !latest.views || latest.views <= 0) return;

      const engagement = ((latest.likes || 0) + (latest.replies || 0) + (latest.reposts || 0)) / latest.views * 100;

      const sp: any = scheduledMap.get(p.threads_media_id);
      const timestampToUse = (sp && sp.scheduled_for) ? sp.scheduled_for : (p.posted_at || p.created_at);
      if (!timestampToUse) return;

      const d = new Date(timestampToUse);
      const dayIndex = d.getDay();
      const hour = d.getHours();

      dataPoints.push({ day: dayIndex, hour, er: engagement });
    });

    const sumMatrix: number[][] = Array(7).fill(0).map(() => Array(24).fill(0));
    const countMatrix: number[][] = Array(7).fill(0).map(() => Array(24).fill(0));

    dataPoints.forEach(dp => {
      sumMatrix[dp.day][dp.hour] += dp.er;
      countMatrix[dp.day][dp.hour] += 1;
    });

    const matrix: number[][] = Array(7).fill(0).map(() => Array(24).fill(0));
    for (let d = 0; d < 7; d++) {
      for (let h = 0; h < 24; h++) {
        if (countMatrix[d][h] > 0) {
          matrix[d][h] = parseFloat((sumMatrix[d][h] / countMatrix[d][h]).toFixed(2));
        }
      }
    }

    const slots: { day: number; hour: number; avg_er: number; sample_size: number }[] = [];
    for (let d = 0; d < 7; d++) {
      for (let h = 0; h < 24; h++) {
        if (countMatrix[d][h] >= 1) {
          slots.push({
            day: d,
            hour: h,
            avg_er: matrix[d][h],
            sample_size: countMatrix[d][h],
          });
        }
      }
    }
    slots.sort((a, b) => b.avg_er - a.avg_er);

    const top_slots = slots.slice(0, 5).map(s => ({
      weekday: WEEKDAY_NAMES[s.day],
      weekday_index: s.day,
      hour: `${s.hour.toString().padStart(2, "0")}:00`,
      er_pct: s.avg_er,
      sample_size: s.sample_size,
    }));

    const totalPosts = dataPoints.length;
    let confidence = "low";
    if (totalPosts >= 50) confidence = "high";
    else if (totalPosts >= 20) confidence = "medium";

    return new Response(
      JSON.stringify({ success: true, matrix, top_slots, total_posts: totalPosts, confidence }),
      { headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (err: any) {
    return new Response(JSON.stringify({ error: err.message }), {
      status: 500,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }
});
