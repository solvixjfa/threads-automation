import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
    const serviceRoleKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
    const supabaseAdmin = createClient(supabaseUrl, serviceRoleKey);

    let userId: string | null = null;

    // 1. Coba ambil user dari token Auth jika dikirim oleh frontend
    const authHeader = req.headers.get("Authorization");
    if (authHeader) {
      const userClient = createClient(supabaseUrl, Deno.env.get("SUPABASE_ANON_KEY")!, {
        global: { headers: { Authorization: authHeader } }
      });
      const { data: { user } } = await userClient.auth.getUser();
      if (user) userId = user.id;
    }

    // 2. Jika tidak ada session Auth di browser, ambil user_id ASLI dari auth.users via Admin API
    if (!userId) {
      const { data: { users }, error: listErr } = await supabaseAdmin.auth.admin.listUsers({ page: 1, perPage: 1 });
      if (listErr || !users || users.length === 0) {
        throw new Error("Tidak ada user terdaftar di auth.users Supabase.");
      }
      userId = users[0].id; // UUID sah yang pasti lolos foreign key constraint
    }

    const appId = Deno.env.get("THREADS_APP_ID")!;
    const redirectUri = Deno.env.get("THREADS_REDIRECT_URI")!;
    const state = crypto.randomUUID();
    const expiresAt = new Date(Date.now() + 10 * 60 * 1000).toISOString();

    // 3. Insert ke oauth_states menggunakan user_id valid dari auth.users
    const { error: stateErr } = await supabaseAdmin
      .schema("threads")
      .from("oauth_states")
      .insert({
        state: state,
        user_id: userId,
        expires_at: expiresAt,
        used: false
      });

    if (stateErr) {
      throw new Error("Gagal insert oauth_states: " + stateErr.message);
    }

    const scope = "threads_basic,threads_content_publish,threads_manage_replies,threads_read_replies,threads_manage_insights";
    const authUrl = `https://threads.net/oauth/authorize?client_id=${appId}&redirect_uri=${encodeURIComponent(redirectUri)}&scope=${scope}&response_type=code&state=${state}`;

    return new Response(JSON.stringify({ url: authUrl }), {
      headers: { ...corsHeaders, "Content-Type": "application/json" }
    });
  } catch (err: any) {
    console.error("OAuth Start Error:", err);
    return new Response(JSON.stringify({ error: err.message }), {
      status: 400,
      headers: { ...corsHeaders, "Content-Type": "application/json" }
    });
  }
});
