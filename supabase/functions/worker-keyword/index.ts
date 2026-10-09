import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { corsHeaders } from "../_shared/cors.ts";
import { checkAndIncrementQuota } from "../_shared/quota.ts";

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
    const serviceRoleKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
    const supabase = createClient(supabaseUrl, serviceRoleKey);

    // Ambil keyword watches yang aktif
    const { data: watches, error: watchErr } = await supabase
      .schema("threads")
      .from("keyword_watches")
      .select("*, threads_accounts(*)")
      .eq("is_active", true);

    if (watchErr) throw watchErr;

    const results = [];

    for (const watch of watches || []) {
      const account = watch.threads_accounts;
      if (!account || account.kill_switch || account.connection_status !== "connected") {
        continue;
      }

      // Cek Quota (Limit Keyword Search: Max 500 queries per 7 hari)
      const { allowed } = await checkAndIncrementQuota(supabase, account.id, "keyword", 500);
      if (!allowed) {
        results.push({ watch_id: watch.id, status: "quota_exceeded" });
        continue;
      }

      try {
        const accessToken = account.last_error || "";
        const searchUrl = `https://graph.threads.net/v1.0/keyword_search?q=${encodeURIComponent(
          watch.query
        )}&search_type=${watch.search_type}&access_token=${accessToken}`;

        const res = await fetch(searchUrl);
        const searchData = await res.json();

        if (searchData.error) throw new Error(searchData.error.message);

        const items = searchData.data || [];
        let savedCount = 0;

        for (const item of items) {
          const { error: insertErr } = await supabase
            .schema("threads")
            .from("keyword_results")
            .upsert(
              {
                watch_id: watch.id,
                threads_media_id: item.id,
                username: item.username || "unknown",
                text: item.text || "",
                posted_at: item.timestamp ? new Date(item.timestamp).toISOString() : new Date().toISOString(),
              },
              { onConflict: "watch_id,threads_media_id" }
            );

          if (!insertErr) savedCount++;
        }

        // Update last_run_at
        await supabase
          .schema("threads")
          .from("keyword_watches")
          .update({ last_run_at: new Date().toISOString() })
          .eq("id", watch.id);

        results.push({ watch_id: watch.id, query: watch.query, fetched: items.length, saved: savedCount });
      } catch (err: any) {
        results.push({ watch_id: watch.id, status: "error", error: err.message });
      }
    }

    return new Response(JSON.stringify({ success: true, processed: results }), {
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  } catch (err: any) {
    return new Response(JSON.stringify({ error: err.message }), {
      status: 500,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }
});
