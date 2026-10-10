import { serve } from "https://deno.land/std@0.168.0/http/server.ts";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    const { topic, tone } = await req.json();

    if (!topic) {
      return new Response(JSON.stringify({ error: "Topik tidak boleh kosong." }), {
        status: 400,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const geminiApiKey = Deno.env.get("GEMINI_API_KEY");
    if (!geminiApiKey) {
      throw new Error("GEMINI_API_KEY belum dikonfigurasi di Supabase Secrets.");
    }

    const prompt = `Kamu adalah seorang ahli strategi konten media sosial profesional untuk platform Threads (Meta).
Tugasmu adalah membuat 3 opsi draf postingan Threads yang sangat engaging, natural, tanpa bahasa kaku atau jargon korporat.

Topik: "${topic}"
Gaya Bahasa / Tone: "${tone || 'Edukasi & Insight'}"

ATURAN FORMAL DRAFT:
1. Jangan gunakan emoji berlebihan (maksimal 1-2 jika sangat relevan).
2. Tulis dengan gaya bahasa kasual, to the point, dan memancing diskusi.
3. Buat variasi panjang:
   - Draf 1: Ringkas & Direct (100-200 karakter)
   - Draf 2: Storytelling / Insight Panjang (300-450 karakter)
   - Draf 3: Format Utasan / Thread Panjang (> 600 karakter, terpisah dalam paragraf rapi)

Kembalikan respon MURNI JSON array tanpa markdown formatting:
[
  { "id": 1, "title": "Ringkas & To The Point", "content": "isi draf 1..." },
  { "id": 2, "title": "Insight & Storytelling", "content": "isi draf 2..." },
  { "id": 3, "title": "Format Thread / Utasan Panjang", "content": "isi draf 3..." }
]`;

    const res = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${geminiApiKey}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          contents: [{ parts: [{ text: prompt }] }],
          generationConfig: { responseMimeType: "application/json" }
        }),
      }
    );

    const data = await res.json();
    if (data.error) throw new Error(data.error.message);

    const rawText = data.candidates?.[0]?.content?.parts?.[0]?.text || "[]";
    const options = JSON.parse(rawText);

    return new Response(JSON.stringify({ success: true, options }), {
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  } catch (err: any) {
    return new Response(JSON.stringify({ error: err.message }), {
      status: 500,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }
});
