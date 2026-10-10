import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

serve(async (req) => {
  const appBaseUrl = Deno.env.get("APP_BASE_URL") || "https://meta.ixiera.id";

  try {
    const url = new URL(req.url);
    const code = url.searchParams.get("code");
    const state = url.searchParams.get("state");
    const errorReason = url.searchParams.get("error_reason") || url.searchParams.get("error");

    if (errorReason) return Response.redirect(`${appBaseUrl}/settings?error=${encodeURIComponent(errorReason)}`, 302);
    if (!code || !state) return Response.redirect(`${appBaseUrl}/settings?error=Missing_code_or_state`, 302);

    const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
    const serviceRoleKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
    const supabase = createClient(supabaseUrl, serviceRoleKey);

    // 1. Verifikasi OAuth State
    const { data: stateData, error: stateError } = await supabase
      .schema("threads")
      .from("oauth_states")
      .select("user_id")
      .eq("state", state)
      .eq("used", false)
      .single();

    if (stateError || !stateData) {
      return Response.redirect(`${appBaseUrl}/settings?error=Invalid_or_expired_state`, 302);
    }

    await supabase.schema("threads").from("oauth_states").update({ used: true }).eq("state", state);

    // 2. Exchange Short Token
    const appId = Deno.env.get("THREADS_APP_ID")!;
    const appSecret = Deno.env.get("THREADS_APP_SECRET")!;
    const redirectUri = Deno.env.get("THREADS_REDIRECT_URI")!;

    const tokenRes = await fetch("https://graph.threads.net/oauth/access_token", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({ client_id: appId, client_secret: appSecret, grant_type: "authorization_code", redirect_uri: redirectUri, code }),
    });
    const tokenData = await tokenRes.json();
    if (tokenData.error) throw new Error(tokenData.error.message || JSON.stringify(tokenData.error));

    // 3. Exchange Long Token (60 Hari)
    const longTokenRes = await fetch(`https://graph.threads.net/access_token?grant_type=th_exchange_token&client_secret=${appSecret}&access_token=${tokenData.access_token}`);
    const longTokenData = await longTokenRes.json();
    if (longTokenData.error) throw new Error(longTokenData.error.message || JSON.stringify(longTokenData.error));

    const longToken = longTokenData.access_token;

    // 4. Ambil Profil User
    const profileRes = await fetch(`https://graph.threads.net/v1.0/me?fields=id,username&access_token=${longToken}`);
    const profileData = await profileRes.json();
    if (profileData.error) throw new Error(profileData.error.message || JSON.stringify(profileData.error));

    const expiresAt = new Date(Date.now() + (longTokenData.expires_in || 5184000) * 1000).toISOString();

    // 5. Cek ketersediaan akun berdasarkan user_id
    const { data: existingAccount } = await supabase
      .schema("threads")
      .from("threads_accounts")
      .select("id, settings")
      .eq("user_id", stateData.user_id)
      .maybeSingle();

    const currentSettings = existingAccount?.settings && typeof existingAccount.settings === 'object' ? existingAccount.settings : {};
    const updatedSettings = { ...currentSettings, access_token: longToken };

    const accountPayload = {
      threads_user_id: profileData.id,
      username: profileData.username,
      connection_status: "connected",
      connected_at: new Date().toISOString(),
      token_expires_at: expiresAt,
      kill_switch: false,
      settings: updatedSettings, // Long token disimpan di sini!
      last_error: null
    };

    if (existingAccount) {
      const { error: updateError } = await supabase
        .schema("threads")
        .from("threads_accounts")
        .update(accountPayload)
        .eq("id", existingAccount.id);

      if (updateError) throw new Error("DB Update Error: " + updateError.message);
    } else {
      const { error: insertError } = await supabase
        .schema("threads")
        .from("threads_accounts")
        .insert({
          user_id: stateData.user_id,
          ...accountPayload
        });

      if (insertError) throw new Error("DB Insert Error: " + insertError.message);
    }

    return Response.redirect(`${appBaseUrl}/settings?connected=true&username=${profileData.username}`, 302);
  } catch (err: any) {
    console.error("Callback Error:", err);
    return Response.redirect(`${appBaseUrl}/settings?error=${encodeURIComponent(err.message)}`, 302);
  }
});
