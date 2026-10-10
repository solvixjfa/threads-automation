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
    const authHeader = req.headers.get("Authorization");
    const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
    const serviceRoleKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
    const geminiApiKey = Deno.env.get("GEMINI_API_KEY");

    if (!geminiApiKey) {
      return new Response(
        JSON.stringify({ error: "GEMINI_API_KEY belum terpasang di Secrets." }),
        { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const { topic, tone } = await req.json();

    if (!topic || typeof topic !== "string") {
      return new Response(
        JSON.stringify({ error: "Topik/ide postingan tidak boleh kosong." }),
        { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const supabase = createClient(supabaseUrl, serviceRoleKey);
    let userTonePrompt = "";
    let userKnowledgeBase = "";

    // Tarik persona & context spesifik milik tenant yang sedang login
    if (authHeader) {
      const userClient = createClient(supabaseUrl, Deno.env.get("SUPABASE_ANON_KEY")!, {
        global: { headers: { Authorization: authHeader } }
      });
      const { data: { user } } = await userClient.auth.getUser();

      if (user) {
        const { data: account } = await supabase
          .schema("threads")
          .from("threads_accounts")
          .select("id")
          .eq("user_id", user.id)
          .limit(1)
          .maybeSingle();

        if (account) {
          const { data: settings } = await supabase
            .schema("threads")
            .from("auto_reply_settings")
            .select("tone_prompt, knowledge_base")
            .eq("account_id", account.id)
            .maybeSingle();

          if (settings) {
            userTonePrompt = settings.tone_prompt || "";
            userKnowledgeBase = settings.knowledge_base || "";
          }
        }
      }
    }

    const systemPrompt = `Kamu adalah AI Assistant pembuat konten Threads (Meta).
Tugasmu adalah merancang 3 variasi draf postingan Threads berdasarkan topik yang diberikan.

FAKTA / KNOWLEDGE BASE USER (Gunakan jika relevan):
${userKnowledgeBase ? userKnowledgeBase : 'Tidak ada fakta tambahan.'}

INSTRUKSI PERSONA, TONE & ATURAN PENULISAN USER:
${userTonePrompt ? userTonePrompt : 'Gunakan bahasa kasual, natural, tanpa emoji berlebihan, dan tidak kaku.'}

TOPIK UTAMA POSTINGAN:
"${topic}"

GAYA PILIHAN: "${tone || 'Edukasi & Insight'}"

ATURAN OUTPUT:
1. Hasilkan 3 opsi draf postingan.
2. Draf 1: Ringkas & Direct (100-200 karakter)
3. Draf 2: Insight / Storytelling (300-450 karakter)
4. Draf 3: Utasan / Thread Panjang (> 500 karakter)
5. HANYA kembalikan JSON array valid tanpa teks/penjelasan tambahan:
[
  { "id": 1, "title": "Ringkas & Direct", "content": "isi draf 1..." },
  { "id": 2, "title": "Insight & Storytelling", "content": "isi draf 2..." },
  { "id": 3, "title": "Format Utasan / Thread", "content": "isi draf 3..." }
]`;

    const res = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${geminiApiKey}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          contents: [{ parts: [{ text: systemPrompt }] }],
          generationConfig: { responseMimeType: "application/json" }
        }),
      }
    );

    const data = await res.json();

    if (!res.ok || data.error) {
      const errMsg = data.error?.message || "Terjadi kesalahan saat menghubungi Gemini API.";
      return new Response(
        JSON.stringify({ error: errMsg }),
        { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    let rawText = data.candidates?.[0]?.content?.parts?.[0]?.text || "[]";
    rawText = rawText.replace(/```json/g, "").replace(/```/g, "").trim();

    let options = [];
    try {
      options = JSON.parse(rawText);
    } catch {
      options = [{ id: 1, title: "Draf Post", content: rawText }];
    }

    return new Response(
      JSON.stringify({ success: true, options }),
      { headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (err: any) {
    return new Response(
      JSON.stringify({ error: err.message }),
      { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
