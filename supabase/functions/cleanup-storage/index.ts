import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "npm:@supabase/supabase-js@2";

serve(async () => {
  const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
  const serviceRoleKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
  const supabase = createClient(supabaseUrl, serviceRoleKey);
  const now = Date.now();
  const ONE_DAY = 24 * 60 * 60 * 1000;

  let deletedCount = 0;

  try {
    // 1. Ambil semua file di bucket threads-media
    const { data: files, error: listErr } = await supabase.storage.from("threads-media").list();
    if (listErr) throw listErr;

    // 2. Ambil semua URL media yang lagi dipake di scheduled_posts
    const { data: posts, error: postErr } = await supabase.schema("threads").from("scheduled_posts").select("media, status, created_at");
    if (postErr) throw postErr;

    // Kumpulin semua URL yang valid (yang masih scheduled/publishing)
    const activeUrls = new Set();
    const publishedUrls = new Map(); // url -> created_at

    for (const p of posts || []) {
      if (p.media && p.media.url) {
        if (p.status === "scheduled" || p.status === "publishing" || p.status === "error") {
          activeUrls.add(p.media.url);
        } else if (p.status === "published") {
          publishedUrls.set(p.media.url, new Date(p.created_at).getTime());
        }
      }
    }

    const filesToDelete: string[] = [];

    // 3. Cek tiap file
    for (const f of files || []) {
      // Bikin URL publik file ini (sesuai format Supabase)
      const fileUrl = `${supabaseUrl}/storage/v1/object/public/threads-media/${f.name}`;
      
      // Skenario A: File Sampah (gak masuk ke DB sama sekali, umur > 1 Jam)
      const fileAge = now - new Date(f.created_at).getTime();
      if (!activeUrls.has(fileUrl) && !publishedUrls.has(fileUrl)) {
        if (fileAge > 60 * 60 * 1000) { // 1 jam
           filesToDelete.push(f.name);
        }
      }
      
      // Skenario B: File dari post yang SUDAH PUBLISH (umur > 24 Jam)
      if (publishedUrls.has(fileUrl)) {
        const postCreatedAt = publishedUrls.get(fileUrl)!;
        if (now - postCreatedAt > ONE_DAY) {
          filesToDelete.push(f.name);
        }
      }
    }

    // 4. Hapus dari Storage
    if (filesToDelete.length > 0) {
      const { error: delErr } = await supabase.storage.from("threads-media").remove(filesToDelete);
      if (delErr) throw delErr;
      deletedCount = filesToDelete.length;
    }

    return new Response(JSON.stringify({ success: true, deleted: deletedCount }), { headers: { "Content-Type": "application/json" } });

  } catch (err: any) {
    return new Response(JSON.stringify({ error: err.message }), { status: 500, headers: { "Content-Type": "application/json" } });
  }
});
