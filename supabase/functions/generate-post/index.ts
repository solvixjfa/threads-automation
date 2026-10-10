import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

// List model dengan prioritas fallback
const CANDIDATE_MODELS = [
  "gemini-3.8-flash",
  "gemini-3.5-flash-lite",
  "gemini-2.5-flash"
];

async function generateContentWithFallback(apiKey: string, systemPrompt: string) {
  let lastError = "";

  for (const model of CANDIDATE_MODELS) {
    console.log(`[GENERATE-POST] Trying model: ${model}`);
    try {
      const res = await fetch(
        `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`,
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

      if (res.ok && !data.error) {
        console.log(`[GENERATE-POST] Success using model: ${model}`);
        return { success: true, modelUsed: model, data };
      }

      lastError = data.error?.message || `Status HTTP ${res.status}`;
      console.warn(`[GENERATE-POST] Model ${model} returned error: ${lastError}`);
    } catch (err: any) {
      lastError = err.message;
      console.warn(`[GENERATE-POST] Exception calling model ${model}: ${lastError}`);
    }
  }

  return { success: false, error: `Semua model Gemini gagal. Error terakhir: ${lastError}` };
}

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    const authHeader = req.headers.get("Authorization");
    const supabaseUrl = Deno.env.get("SUPABASE_URL");
    const serviceRoleKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
    const geminiApiKey = Deno.env.get("GEMINI_API_KEY");

    if (!supabaseUrl || !serviceRoleKey) {
      return new Response(
        JSON.stringify({ error: "Environment SUPABASE_URL / SERVICE_ROLE_KEY belum terpasang." }),
        { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    if (!geminiApiKey) {
      return new Response(
        JSON.stringify({ error: "GEMINI_API_KEY belum terpasang di Supabase Secrets." }),
        { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    let body;
    try {
      body = await req.json();
    } catch {
      return new Response(
        JSON.stringify({ error: "Format JSON request tidak valid." }),
        { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const { topic, tone } = body || {};

    if (!topic || typeof topic !== "string") {
      return new Response(
        JSON.stringify({ error: "Topik/ide postingan tidak boleh kosong." }),
        { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const supabase = createClient(supabaseUrl, serviceRoleKey);
    let userTonePrompt = "";
    let userKnowledgeBase = "";
    let ragDocs: string[] = [];

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

          const { data: docs } = await supabase
            .schema("threads")
            .from("brand_knowledge")
            .select("category, title, content")
            .eq("account_id", account.id)
            .limit(10);

          if (docs && docs.length > 0) {
            ragDocs = docs.map(d => `[${d.category.toUpperCase()}] ${d.title}: ${d.content}`);
          }
        }
      }
    }

    const systemPrompt = `Kamu adalah AI Assistant pembuat konten Threads (Meta).
Tugasmu adalah merancang 3 variasi draf postingan Threads berdasarkan topik yang diberikan.

KONTEKS RAG / BRAND KNOWLEDGE:
${ragDocs.length > 0 ? ragDocs.join("\n") : (userKnowledgeBase || 'Tidak ada dokumen konteks khusus.')}

INSTRUKSI PERSONA & TONE:
${userTonePrompt || 'Gunakan bahasa kasual, natural, tanpa emoji berlebihan, dan tidak kaku.'}

TOPIK UTAMA:
"${topic}"

GAYA PILIHAN: "${tone || 'Edukasi & Insight'}"

ATURAN OUTPUT:
1. Hasilkan 3 opsi draf postingan.
2. Draf 1: Ringkas & Direct (100-200 karakter)
3. Draf 2: Insight / Storytelling (300-450 karakter)
4. Draf 3: Utasan / Thread Panjang (> 500 karakter)
5. HANYA kembalikan JSON array valid tanpa penjelasan tambahan:
[
  { "id": 1, "title": "Ringkas & Direct", "content": "isi draf 1..." },
  { "id": 2, "title": "Insight & Storytelling", "content": "isi draf 2..." },
  { "id": 3, "title": "Format Utasan / Thread", "content": "isi draf 3..." }
]`;

    const result = await generateContentWithFallback(geminiApiKey, systemPrompt);

    if (!result.success || !result.data) {
      return new Response(
        JSON.stringify({ error: result.error }),
        { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    let rawText = result.data.candidates?.[0]?.content?.parts?.[0]?.text || "[]";
    rawText = rawText.replace(/```json/g, "").replace(/```/g, "").trim();

    let options = [];
    try {
      options = JSON.parse(rawText);
    } catch {
      options = [{ id: 1, title: "Draf Post", content: rawText }];
    }

    return new Response(
      JSON.stringify({ success: true, modelUsed: result.modelUsed, options }),
      { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );

  } catch (globalErr: any) {
    return new Response(
      JSON.stringify({ error: "Exception: " + globalErr.message }),
      { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
