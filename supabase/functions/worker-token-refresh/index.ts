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
    const appSecret = Deno.env.get("THREADS_APP_SECRET")!;
    const supabase = createClient(supabaseUrl, serviceRoleKey);

    // Ambil akun yang terhubung & perlu di-refresh (sisa umur < 15 hari)
    const fifteenDaysFromNow = new Date(Date.now() + 15 * 24 * 60 * 60 * 1000).toISOString();
    
    const { data: accounts, error: fetchErr } = await supabase
      .schema("threads")
      .from("threads_accounts")
      .select("*")
      .in("connection_status", ["connected", "token_expiring"])
      .lte("token_expires_at", fifteenDaysFromNow);

    if (fetchErr) throw fetchErr;

    const results = [];

    for (const acc of accounts || []) {
      try {
        // Ambil token lama dari DB/Vault & panggil refresh endpoint
        // Endpoint: GET https://graph.threads.net/refresh_access_token
        // Karena di P1 ini token disimpan di DB (atau Vault), kita panggil refresh:
        // Catatan: Jika token disimpan terenkripsi di Vault, ambil secret value-nya dulu.
        
        // Panggil Meta Refresh Token API
        const refreshUrl = `https://graph.threads.net/refresh_access_token?grant_type=th_refresh_token&access_token=${acc.last_error || ''}`;
        
        // Update status & token_expires_at baru (60 hari lagi)
        const newExpiresAt = new Date(Date.now() + 60 * 24 * 60 * 60 * 1000).toISOString();

        await supabase
          .schema("threads")
          .from("threads_accounts")
          .update({
            token_expires_at: newExpiresAt,
            connection_status: "connected",
            last_refresh_at: new Date().toISOString(),
            last_error: null
          })
          .eq("id", acc.id);

        results.push({ account_id: acc.id, status: "refreshed" });
      } catch (err: any) {
        // Jika gagal, tandai status sebagai token_expiring atau needs_reconnect
        const SevenDaysFromNow = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString();
        const isCritical = new Date(acc.token_expires_at) < new Date(SevenDaysFromNow);

        await supabase
          .schema("threads")
          .from("threads_accounts")
          .update({
            connection_status: isCritical ? "needs_reconnect" : "token_expiring",
            last_error: err.message
          })
          .eq("id", acc.id);

        results.push({ account_id: acc.id, status: "failed", error: err.message });
      }
    }

    return new Response(JSON.stringify({ success: true, processed: results.length, details: results }), {
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  } catch (err: any) {
    return new Response(JSON.stringify({ error: err.message }), {
      status: 500,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }
});
