import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

serve(async (req) => {
  const appBaseUrl = Deno.env.get("APP_BASE_URL") || "https://meta.ixiera.id";

  try {
    const url = new URL(req.url);
    const code = url.searchParams.get("code");
    const state = url.searchParams.get("state");
    const errorReason = url.searchParams.get("error_reason") || url.searchParams.get("error");

    if (errorReason) {
      return Response.redirect(`${appBaseUrl}/settings?error=${encodeURIComponent(errorReason)}`, 302);
    }

    if (!code || !state) {
      return Response.redirect(`${appBaseUrl}/settings?error=Missing_code_or_state`, 302);
    }

    const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
    const serviceRoleKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
    const supabase = createClient(supabaseUrl, serviceRoleKey);

    // 1. Check & Consume OAuth State
    const { data: stateData, error: stateError } = await supabase
      .schema("threads")
      .from("oauth_states")
      .select("*")
      .eq("state", state)
      .eq("used", false)
      .single();

    if (stateError || !stateData) {
      return Response.redirect(`${appBaseUrl}/settings?error=Invalid_or_expired_state`, 302);
    }

    await supabase
      .schema("threads")
      .from("oauth_states")
      .update({ used: true })
      .eq("state", state);

    const appId = Deno.env.get("THREADS_APP_ID")!;
    const appSecret = Deno.env.get("THREADS_APP_SECRET")!;
    const redirectUri = Deno.env.get("THREADS_REDIRECT_URI")!;

    // 2. Exchange Short-Lived Access Token
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
    if (tokenData.error) {
      const errMsg = tokenData.error.message || tokenData.error_message || JSON.stringify(tokenData.error);
      return Response.redirect(`${appBaseUrl}/settings?error=${encodeURIComponent(errMsg)}`, 302);
    }

    const shortToken = tokenData.access_token;

    // 3. Exchange Long-Lived Token (60 Days)
    const longTokenRes = await fetch(
      `https://graph.threads.net/access_token?grant_type=th_exchange_token&client_secret=${appSecret}&access_token=${shortToken}`
    );
    const longTokenData = await longTokenRes.json();
    if (longTokenData.error) {
      const errMsg = longTokenData.error.message || JSON.stringify(longTokenData.error);
      return Response.redirect(`${appBaseUrl}/settings?error=${encodeURIComponent(errMsg)}`, 302);
    }

    const longToken = longTokenData.access_token;
    const expiresIn = longTokenData.expires_in || 5184000;
    const expiresAt = new Date(Date.now() + expiresIn * 1000).toISOString();

    // 4. Fetch Threads User Profile
    const profileRes = await fetch(`https://graph.threads.net/v1.0/me?fields=id,username&access_token=${longToken}`);
    const profileData = await profileRes.json();
    if (profileData.error) {
      const errMsg = profileData.error.message || JSON.stringify(profileData.error);
      return Response.redirect(`${appBaseUrl}/settings?error=${encodeURIComponent(errMsg)}`, 302);
    }

    // 5. Save/Upsert Account to DB threads.threads_accounts
    const { error: accountError } = await supabase
      .schema("threads")
      .from("threads_accounts")
      .upsert(
        {
          threads_user_id: profileData.id,
          username: profileData.username,
          connection_status: "connected",
          connected_at: new Date().toISOString(),
          token_expires_at: expiresAt,
          last_error: null,
        },
        { onConflict: "threads_user_id" }
      );

    if (accountError) {
      return Response.redirect(`${appBaseUrl}/settings?error=${encodeURIComponent(accountError.message)}`, 302);
    }

    // 6. SUCCESS! Redirect back to Frontend Settings with Success Flag
    return Response.redirect(`${appBaseUrl}/settings?connected=true&username=${profileData.username}`, 302);

  } catch (err: any) {
    console.error("Callback Error:", err);
    return Response.redirect(`${appBaseUrl}/settings?error=${encodeURIComponent(err.message)}`, 302);
  }
});
