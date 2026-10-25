import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "npm:@supabase/supabase-js@2";
import { corsHeaders } from "../_shared/cors.ts";

function minutesAgo(iso: string | null): number | null {
  if (!iso) return null;
  const diff = Date.now() - new Date(iso).getTime();
  return Math.round(diff / 60000);
}

function computeStatus(agoMin: number | null, healthyMax: number, warningMax: number): string {
  if (agoMin === null) return "unknown";
  if (agoMin <= healthyMax) return "healthy";
  if (agoMin <= warningMax) return "warning";
  return "error";
}

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

    const { data: postIds } = await supabase
      .schema("threads")
      .from("posts")
      .select("id")
      .eq("account_id", account.id);

    const ids = (postIds || []).map((p: any) => p.id);

    let latestMetricIso: string | null = null;
    if (ids.length > 0) {
      const { data } = await supabase
        .schema("threads")
        .from("post_metrics")
        .select("captured_at")
        .in("post_id", ids)
        .order("captured_at", { ascending: false })
        .limit(1)
        .maybeSingle();
      latestMetricIso = data?.captured_at || null;
    }

    const { data: latestReply } = await supabase
      .schema("threads")
      .from("replies")
      .select("processed_at")
      .eq("account_id", account.id)
      .order("processed_at", { ascending: false })
      .limit(1)
      .maybeSingle();

    const metricAgo = minutesAgo(latestMetricIso);
    const replyAgo = minutesAgo(latestReply?.processed_at || null);

    const workers = [
      {
        name: "metrics-sync",
        description: "Sync metrics post dari Meta",
        last_run_at: latestMetricIso,
        last_run_ago_minutes: metricAgo,
        status: computeStatus(metricAgo, 90, 180),
      },
      {
        name: "replies-sync",
        description: "Fetch reply komentar baru",
        last_run_at: latestReply?.processed_at || null,
        last_run_ago_minutes: replyAgo,
        status: computeStatus(replyAgo, 20, 60),
      },
    ];

    let overall = "healthy";
    for (const w of workers) {
      if (w.status === "error") { overall = "error"; break; }
      if (w.status === "warning" && overall !== "error") overall = "warning";
    }

    return new Response(
      JSON.stringify({
        success: true,
        workers,
        overall_status: overall,
        generated_at: new Date().toISOString(),
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
