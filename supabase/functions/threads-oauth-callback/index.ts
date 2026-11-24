import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "npm:@supabase/supabase-js@2";

function getMaxAccounts(plan: string, role: string): number {
  if (role === "admin") return 50;
  if (plan === "paid_credit") return 10;
  if (plan === "paid_byok") return 3;
  return 1;
}

serve(async (req) => {
  const appBaseUrl = Deno.env.get("APP_BASE_URL") || "https://app.ixiera.online";

  try {
    const url = new URL(req.url);
    const code = url.searchParams.get("code");
    const state = url.searchParams.get("state");
    const errorReason = url.searchParams.get("error_reason") || url.searchParams.get("error");

    if (errorReason) {
      return Response.redirect(`${appBaseUrl}/profile/account?error=${encodeURIComponent(errorReason)}`, 302);
    }
    if (!code || !state) {
      return Response.redirect(`${appBaseUrl}/profile/account?error=Missing_code_or_state`, 302);
    }

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
      return Response.redirect(`${appBaseUrl}/profile/account?error=Invalid_or_expired_state`, 302);
    }

    await supabase.schema("threads").from("oauth_states").update({ used: true }).eq("state", state);

    // 2. Exchange Short Token
    const appId = Deno.env.get("THREADS_APP_ID")!;
    const appSecret = Deno.env.get("THREADS_APP_SECRET")!;
    const redirectUri = Deno.env.get("THREADS_REDIRECT_URI")!;

    const tokenRes = await fetch("https://graph.threads.net/oauth/access_token", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({
        client_id: appId,
        client_secret: appSecret,
        grant_type: "authorization_code",
        redirect_uri: redirectUri,
        code,
      }),
    });
    const tokenData = await tokenRes.json();
    if (tokenData.error) throw new Error(tokenData.error.message || JSON.stringify(tokenData.error));

    // 3. Exchange Long Token (60 Hari)
    const longTokenRes = await fetch(
      `https://graph.threads.net/access_token?grant_type=th_exchange_token&client_secret=${appSecret}&access_token=${tokenData.access_token}`
    );
    const longTokenData = await longTokenRes.json();
    if (longTokenData.error) throw new Error(longTokenData.error.message || JSON.stringify(longTokenData.error));

    const longToken = longTokenData.access_token;

    // 4. Ambil Profil User
    const profileRes = await fetch(`https://graph.threads.net/v1.0/me?fields=id,username&access_token=${longToken}`);
    const profileData = await profileRes.json();
    if (profileData.error) throw new Error(profileData.error.message || JSON.stringify(profileData.error));

    const expiresAt = new Date(Date.now() + (longTokenData.expires_in || 5184000) * 1000).toISOString();

    // 5. Cek apakah akun Threads ini sudah pernah terhubung sebelumnya
    const { data: existingByThreads } = await supabase
      .schema("threads")
      .from("threads_accounts")
      .select("id, user_id, settings")
      .eq("threads_user_id", profileData.id)
      .maybeSingle();

    if (existingByThreads && existingByThreads.user_id !== stateData.user_id) {
      return Response.redirect(
        `${appBaseUrl}/profile/account?error=${encodeURIComponent("Akun Threads ini sudah terhubung ke pengguna Ixiera lain.")}`,
        302
      );
    }

    if (existingByThreads && existingByThreads.user_id === stateData.user_id) {
      // Reconnect akun yang sudah ada milik user ini
      const currentSettings =
        existingByThreads.settings && typeof existingByThreads.settings === "object"
          ? existingByThreads.settings
          : {};
      const updatedSettings = { ...currentSettings, access_token: longToken };

      const { error: updateError } = await supabase
        .schema("threads")
        .from("threads_accounts")
        .update({
          username: profileData.username,
          connection_status: "connected",
          connected_at: new Date().toISOString(),
          token_expires_at: expiresAt,
          kill_switch: false,
          settings: updatedSettings,
          last_error: null,
        })
        .eq("id", existingByThreads.id);

      if (updateError) throw new Error("DB Update Error: " + updateError.message);

      return Response.redirect(
        `${appBaseUrl}/profile/account?connected=true&username=${encodeURIComponent(profileData.username)}`,
        302
      );
    }

    // 6. Koneksi akun baru: validasi batas maksimal akun sesuai paket user
    const { data: userAccounts } = await supabase
      .schema("threads")
      .from("threads_accounts")
      .select("id, plan, role")
      .eq("user_id", stateData.user_id);

    const { data: userProfile } = await supabase
      .schema("threads")
      .from("profiles")
      .select("plan, role")
      .eq("id", stateData.user_id)
      .maybeSingle();

    const accountsList = userAccounts || [];
    const currentCount = accountsList.length;

    const effectiveRole =
      accountsList.some((a: any) => a.role === "admin") || userProfile?.role === "admin"
        ? "admin"
        : "user";

    let effectivePlan = userProfile?.plan || "free";
    for (const acc of accountsList) {
      if (acc.plan === "paid_credit") {
        effectivePlan = "paid_credit";
        break;
      }
      if (acc.plan === "paid_byok" && effectivePlan !== "paid_credit") {
        effectivePlan = "paid_byok";
      } else if (acc.plan === "trial" && effectivePlan === "free") {
        effectivePlan = "trial";
      }
    }

    const maxAccounts = getMaxAccounts(effectivePlan, effectiveRole);

    if (currentCount >= maxAccounts) {
      const msg = `Batas maksimal paket kamu (${maxAccounts} akun Threads) sudah tercapai. Upgrade paket untuk menambah akun.`;
      return Response.redirect(`${appBaseUrl}/profile/account?error=${encodeURIComponent(msg)}`, 302);
    }

    // Trigger database trg_inherit_user_plan_on_insert otomatis menyalin plan, kredit, dan BYOK keys
    const { error: insertError } = await supabase
      .schema("threads")
      .from("threads_accounts")
      .insert({
        user_id: stateData.user_id,
        threads_user_id: profileData.id,
        username: profileData.username,
        connection_status: "connected",
        connected_at: new Date().toISOString(),
        token_expires_at: expiresAt,
        kill_switch: false,
        settings: { access_token: longToken },
        last_error: null,
      });

    if (insertError) throw new Error("DB Insert Error: " + insertError.message);

    return Response.redirect(
      `${appBaseUrl}/profile/account?connected=true&username=${encodeURIComponent(profileData.username)}`,
      302
    );
  } catch (err: any) {
    console.error("Callback Error:", err);
    return Response.redirect(`${appBaseUrl}/profile/account?error=${encodeURIComponent(err.message)}`, 302);
  }
});
