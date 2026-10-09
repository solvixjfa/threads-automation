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

    // Client via Auth Header untuk cek role Admin
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
    
    // Cek apakah user ini role admin
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

    const { target_user_id, action, username } = await req.json();

    if (action === "mark_invited") {
      await adminClient
        .schema("threads")
        .from("threads_accounts")
        .update({
          connection_status: "invited",
          invited_at: new Date().toISOString()
        })
        .eq("user_id", target_user_id);
    } else if (action === "suspend") {
      await adminClient
        .schema("threads")
        .from("threads_accounts")
        .update({ connection_status: "suspended" })
        .eq("user_id", target_user_id);
    } else if (action === "unsuspend") {
      await adminClient
        .schema("threads")
        .from("threads_accounts")
        .update({ connection_status: "connected" })
        .eq("user_id", target_user_id);
    }

    return new Response(JSON.stringify({ success: true, action }), {
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  } catch (err: any) {
    return new Response(JSON.stringify({ error: err.message }), {
      status: 500,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }
});
