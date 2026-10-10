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
    const url = new URL(req.url);
    let code = url.searchParams.get("code");
    let state = url.searchParams.get("state");

    // Fallback jika dipanggil via POST body JSON
    if (!code || !state) {
      try {
        const body = await req.json();
        code = body.code || code;
        state = body.state || state;
      } catch (_) {
        // Biarkan jika request tidak memiliki body JSON
      }
    }

    const appBaseUrl = Deno.env.get("APP_BASE_URL") || "https://meta.ixiera.id";

    if (!code || !state) {
      return new Response(JSON.stringify({ error: "Missing code or state in request" }), {
        status: 400,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
    const serviceRoleKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
    const supabase = createClient(supabaseUrl, serviceRoleKey);

    // 1. Validasi OAuth State
    const { data: stateData, error: stateError } = await supabase
      .schema("threads")
      .from("oauth_states")
      .select("*")
      .eq("state", state)
      .eq("used", false)
      .single();

    if (stateError || !stateData || new Date(stateData.expires_at) < new Date()) {
      return new Response(JSON.stringify({ error: "Invalid or expired state" }), {
        status: 400,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    // Tandai state sudah dipakai
    await supabase
      .schema("threads")
      .from("oauth_states")
      .update({ used: true })
      .eq("state", state);

    const appId = Deno.env.get("THREADS_APP_ID")!;
    const appSecret = Deno.env.get("THREADS_APP_SECRET")!;
    const redirectUri = Deno.env.get("THREADS_REDIRECT_URI")!;

    // 2. Tukar Authorization Code dengan Short-Lived Access Token
    const tokenRes = await fetch("https://graph.threads.net/oauth/access_token", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({
        client_id: appId,
        client_secret: appSecret,
        grant_type: "authorization_code",
        redirect_uri: redirectUri,
        code: code,
      }),
    });

    const tokenData = await tokenRes.json();
    if (tokenData.error) throw new Error(tokenData.error.message || JSON.stringify(tokenData.error));

    const shortToken = tokenData.access_token;

    // 3. Tukar Short-Lived Token ke Long-Lived Token (60 Hari)
    const longTokenRes = await fetch(
      `https://graph.threads.net/access_token?grant_type=th_exchange_token&client_secret=${appSecret}&access_token=${shortToken}`
    );
    const longTokenData = await longTokenRes.json();
    if (longTokenData.error) throw new Error(longTokenData.error.message || JSON.stringify(longTokenData.error));

    const longToken = longTokenData.access_token;
    const expiresIn = longTokenData.expires_in || 5184000;
    const expiresAt = new Date(Date.now() + expiresIn * 1000).toISOString();

    // 4. Ambil Profil Threads User
    const profileRes = await fetch(`https://graph.threads.net/v1.0/me?fields=id,username&access_token=${longToken}`);
    const profileData = await profileRes.json();
    if (profileData.error) throw new Error(profileData.error.message || JSON.stringify(profileData.error));

    // 5. Simpan Akun ke Database threads.threads_accounts
    const { error: accountError } = await supabase
      .schema("threads")
      .from("threads_accounts")
      .upsert(
        {
          user_id: stateData.user_id,
          threads_user_id: profileData.id,
          username: profileData.username,
          connection_status: "connected",
          connected_at: new Date().toISOString(),
          token_expires_at: expiresAt,
          last_error: null,
        },
        { onConflict: "threads_user_id" }
      );

    if (accountError) throw accountError;

    // 6. Redirect kembali ke Web App Settings
    return Response.redirect(`${appBaseUrl}/settings?connected=true`, 302);

  } catch (err: any) {
    console.error("OAuth Callback Error:", err);
    return new Response(JSON.stringify({ error: err.message }), {
      status: 500,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }
});
