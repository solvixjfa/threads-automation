import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { corsHeaders } from "../_shared/cors.ts";

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    const { account_id, cursor } = await req.json();
    if (!account_id) {
      return new Response(JSON.stringify({ error: "Missing account_id" }), {
        status: 400,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
    const serviceRoleKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
    const supabase = createClient(supabaseUrl, serviceRoleKey);

    // Ambil akun & token
    const { data: account, error: accErr } = await supabase
      .schema("threads")
      .from("threads_accounts")
      .select("*")
      .eq("id", account_id)
      .single();

    if (accErr || !account) throw new Error("Account not found");

    // Ambil token (di P1 tersimpan/terhubung)
    const accessToken = account.last_error || ''; // ganti dengan token asli dari Vault/DB

    // Panggil Threads API GET /me/threads
    let apiUrl = `https://graph.threads.net/v1.0/me/threads?fields=id,text,media_type,permalink,timestamp&limit=25`;
    if (cursor) {
      apiUrl += `&after=${cursor}`;
    }

    const res = await fetch(apiUrl, {
      headers: { Authorization: `Bearer ${accessToken}` },
    });
    const threadsData = await res.json();

    if (threadsData.error) throw new Error(threadsData.error.message);

    const posts = threadsData.data || [];
    const nextCursor = threadsData.paging?.cursors?.after || null;

    let importedCount = 0;

    for (const item of posts) {
      // Upsert ke tabel threads.posts
      const { data: insertedPost, error: postErr } = await supabase
        .schema("threads")
        .from("posts")
        .upsert(
          {
            account_id: account.id,
            threads_media_id: item.id,
            text: item.text || "",
            media_type: item.media_type,
            permalink: item.permalink,
            posted_at: item.timestamp,
            source: "imported",
            raw: item,
          },
          { onConflict: "threads_media_id" }
        )
        .select("id")
        .single();

      if (!postErr && insertedPost) {
        importedCount++;
        // Tarik metrics per post via API /{media_id}/insights jika diizinkan
        // Simpan baseline ke post_metrics
      }
    }

    return new Response(
      JSON.stringify({
        success: true,
        imported: importedCount,
        next_cursor: nextCursor,
        has_more: !!nextCursor,
      }),
      { headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (err: any) {
    return new Response(JSON.stringify({ error: err.message }), {
      status: 500,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }
});
