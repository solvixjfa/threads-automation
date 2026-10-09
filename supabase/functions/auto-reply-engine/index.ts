import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { corsHeaders } from "../_shared/cors.ts";
import { generateAutoReply } from "../_shared/llm.ts";

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
    const serviceRoleKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
    const supabase = createClient(supabaseUrl, serviceRoleKey);

    // 1. Ambil balasan yang sudah terklasifikasi tapi belum diproses auto-reply
    const { data: pendingReplies, error: replyErr } = await supabase
      .schema("threads")
      .from("replies")
      .select("*, threads_accounts(*)")
      .neq("classification", "unclassified")
      .is("processed_at", null)
      .limit(10);

    if (replyErr) throw replyErr;

    const results = [];

    for (const reply of pendingReplies || []) {
      const account = reply.threads_accounts;
      if (!account || account.kill_switch || reply.is_own) {
        continue;
      }

      // Ambil pengaturan auto reply akun
      const { data: settings } = await supabase
        .schema("threads")
        .from("auto_reply_settings")
        .select("*")
        .eq("account_id", account.id)
        .maybeSingle();

      if (!settings || !settings.enabled) {
        await supabase
          .schema("threads")
          .from("replies")
          .update({ processed_at: new Date().toISOString() })
          .eq("id", reply.id);
        continue;
      }

      // Filter Toxic & Spam
      if (reply.classification === "toxic" || reply.classification === "spam") {
        if (settings.hide_toxic) {
          // Aksi Auto-Hide via Threads API
          // POST /{reply_id}/manage_reply (hide=true)
        }
        await supabase
          .schema("threads")
          .from("auto_reply_logs")
          .upsert({
            account_id: account.id,
            reply_id: reply.id,
            status: "skipped",
            skip_reason: `Classification was ${reply.classification}`
          });

        await supabase
          .schema("threads")
          .from("replies")
          .update({ processed_at: new Date().toISOString() })
          .eq("id", reply.id);

        continue;
      }

      // Filter Aturan 'only_questions'
      if (settings.rules?.only_questions && reply.classification !== "question") {
        await supabase
          .schema("threads")
          .from("auto_reply_logs")
          .upsert({
            account_id: account.id,
            reply_id: reply.id,
            status: "skipped",
            skip_reason: "Only questions filter enabled"
          });

        await supabase
          .schema("threads")
          .from("replies")
          .update({ processed_at: new Date().toISOString() })
          .eq("id", reply.id);

        continue;
      }

      // Generate Balasan via LLM Helper
      let generatedText = "";
      try {
        generatedText = await generateAutoReply(
          settings.tone_prompt,
          settings.knowledge_base,
          reply.text,
          reply.author_username
        );
      } catch (err: any) {
        await supabase
          .schema("threads")
          .from("auto_reply_logs")
          .upsert({
            account_id: account.id,
            reply_id: reply.id,
            status: "failed",
            skip_reason: `LLM Error: ${err.message}`
          });
        continue;
      }

      // Mode Review (Pending) vs Mode Auto (Kirim Langsung)
      if (settings.mode === "review") {
        await supabase
          .schema("threads")
          .from("auto_reply_logs")
          .upsert({
            account_id: account.id,
            reply_id: reply.id,
            status: "pending_review",
            generated_text: generatedText,
            final_text: generatedText
          });
      } else if (settings.mode === "auto") {
        // Kirim balasan langsung via API Threads
        const accessToken = account.last_error || "";
        const pubRes = await fetch(`https://graph.threads.net/v1.0/${account.threads_user_id}/threads`, {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: new URLSearchParams({
            media_type: "TEXT",
            text: generatedText,
            reply_to_id: reply.threads_reply_id,
            access_token: accessToken,
          }),
        });
        const pubData = await pubRes.json();

        if (pubData.error) {
          await supabase
            .schema("threads")
            .from("auto_reply_logs")
            .upsert({
              account_id: account.id,
              reply_id: reply.id,
              status: "failed",
              generated_text: generatedText,
              skip_reason: pubData.error.message
            });
        } else {
          // Publish container balasan
          await fetch(`https://graph.threads.net/v1.0/${account.threads_user_id}/threads_publish`, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: new URLSearchParams({
              creation_id: pubData.id,
              access_token: accessToken,
            }),
          });

          await supabase
            .schema("threads")
            .from("auto_reply_logs")
            .upsert({
              account_id: account.id,
              reply_id: reply.id,
              status: "sent",
              generated_text: generatedText,
              final_text: generatedText,
              sent_media_id: pubData.id
            });
        }
      }

      await supabase
        .schema("threads")
        .from("replies")
        .update({ processed_at: new Date().toISOString() })
        .eq("id", reply.id);

      results.push({ reply_id: reply.id, status: settings.mode });
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
