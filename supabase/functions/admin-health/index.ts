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

    const adminClient = createClient(supabaseUrl, serviceRoleKey);

    const { data: profile } = await adminClient
      .schema("threads")
      .from("profiles")
      .select("role")
      .eq("id", user.id)
      .single();

    if (!profile || profile.role !== "admin") {
      return new Response(JSON.stringify({ error: "Forbidden: Admin role required" }), {
        status: 403,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    // Single queries for counts to ensure speed and performance
    const { count: failedPostsCount } = await adminClient
      .schema("threads")
      .from("scheduled_posts")
      .select("*", { count: "exact", head: true })
      .eq("status", "failed");

    const { count: expiringTokensCount } = await adminClient
      .schema("threads")
      .from("threads_accounts")
      .select("*", { count: "exact", head: true })
      .in("connection_status", ["token_expiring", "needs_reconnect"]);

    const { count: totalConnectedCount } = await adminClient
      .schema("threads")
      .from("threads_accounts")
      .select("*", { count: "exact", head: true })
      .eq("connection_status", "connected");

    return new Response(
      JSON.stringify({
        success: true,
        health: {
          failed_posts: failedPostsCount || 0,
          expiring_or_broken_tokens: expiringTokensCount || 0,
          connected_accounts: totalConnectedCount || 0,
          timestamp: new Date().toISOString()
        }
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
