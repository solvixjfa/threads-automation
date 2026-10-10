import { serve } from "https://deno.land/std@0.168.0/http/server.ts";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

const CANDIDATE_MODELS = [
  "gemini-3.8-flash",
  "gemini-3.5-flash-lite",
  "gemini-2.5-flash"
];

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    const { text } = await req.json();
    const geminiApiKey = Deno.env.get("GEMINI_API_KEY");

    if (!geminiApiKey) {
      return new Response(
        JSON.stringify({ error: "GEMINI_API_KEY belum terpasang." }),
        { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const prompt = `Analisa draf postingan Threads berikut dan berikan skor potensi engagement (0-100) serta feedback singkat.
Teks: "${text || ''}"

HANYA kembalikan JSON valid format berikut:
{
  "score": 85,
  "feedback": "Teks sudah ringkas dan to the point, bahasanya natural."
}`;

    let lastError = "";
    for (const model of CANDIDATE_MODELS) {
      try {
        const res = await fetch(
          `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${geminiApiKey}`,
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
        if (res.ok && !data.error) {
          let rawText = data.candidates?.[0]?.content?.parts?.[0]?.text || "{}";
          rawText = rawText.replace(/```json/g, "").replace(/```/g, "").trim();
          const parsed = JSON.parse(rawText);

          return new Response(
            JSON.stringify({ success: true, modelUsed: model, score: parsed.score || 80, feedback: parsed.feedback || "Cukup baik." }),
            { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
          );
        }
        lastError = data.error?.message || res.statusText;
      } catch (e: any) {
        lastError = e.message;
      }
    }

    return new Response(
      JSON.stringify({ error: "Gagal memproses skor AI: " + lastError }),
      { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (err: any) {
    return new Response(
      JSON.stringify({ error: err.message }),
      { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
