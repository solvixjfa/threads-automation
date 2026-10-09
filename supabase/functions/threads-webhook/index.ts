import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { corsHeaders } from "../_shared/cors.ts";

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  const url = new URL(req.url);

  // 1. Handshake Challenge dari Meta (GET)
  if (req.method === "GET") {
    const mode = url.searchParams.get("hub.mode");
    const token = url.searchParams.get("hub.verify_token");
    const challenge = url.searchParams.get("hub.challenge");

    const expectedToken = Deno.env.get("THREADS_WEBHOOK_VERIFY_TOKEN");

    if (mode === "subscribe" && token === expectedToken) {
      return new Response(challenge, { status: 200 });
    }
    return new Response("Forbidden", { status: 403 });
  }

  // 2. Incoming Webhook Event (POST)
  if (req.method === "POST") {
    try {
      const payload = await req.json();
      const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
      const serviceRoleKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
      const supabase = createClient(supabaseUrl, serviceRoleKey);

      // Ingest entries
      const entries = payload.entry || [];
      for (const entry of entries) {
        const changes = entry.changes || [];
        for (const change of changes) {
          if (change.field === "replies" || change.field === "mentions") {
            const val = change.value;
            const threadsUserId = entry.id;

            // Cari account_id dari threads_user_id
            const { data: acc } = await supabase
              .schema("threads")
              .from("threads_accounts")
              .select("id")
              .eq("threads_user_id", threadsUserId)
              .maybeSingle();

            if (acc) {
              await supabase
                .schema("threads")
                .from("replies")
                .upsert({
                  account_id: acc.id,
                  threads_reply_id: val.reply_id || val.id,
                  parent_reply_id: val.parent_id || null,
                  author_username: val.from?.username || "unknown",
                  text: val.text || "",
                  replied_at: new Date(val.timestamp * 1000).toISOString(),
                  raw: val
                }, { onConflict: "threads_reply_id" });
            }
          }
        }
      }

      return new Response(JSON.stringify({ success: true }), {
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    } catch (err: any) {
      return new Response(JSON.stringify({ error: err.message }), {
        status: 500,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }
  }

  return new Response("Method not allowed", { status: 405 });
});
