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

  // Verbose Logger Helper
  const log = (step: string, details?: any) => {
    console.log(`[GENERATE-POST] [${step}]`, details ? JSON.stringify(details) : '');
  };

  try {
    log("1_START_REQUEST");

    const authHeader = req.headers.get("Authorization");
    const supabaseUrl = Deno.env.get("SUPABASE_URL");
    const serviceRoleKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
    const geminiApiKey = Deno.env.get("GEMINI_API_KEY");

    if (!supabaseUrl || !serviceRoleKey) {
      log("ERR_MISSING_SUPABASE_ENV");
      return new Response(
        JSON.stringify({ error: "Environment SUPABASE_URL / SERVICE_ROLE_KEY belum terpasang." }),
        { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    if (!geminiApiKey) {
      log("ERR_MISSING_GEMINI_KEY");
      return new Response(
        JSON.stringify({ error: "GEMINI_API_KEY belum terpasang di Supabase Secrets." }),
        { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    // Parse Body
    let body;
    try {
      body = await req.json();
    } catch (parseErr: any) {
      log("ERR_BAD_JSON_BODY", parseErr.message);
      return new Response(
        JSON.stringify({ error: "Format request JSON tidak valid." }),
        { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const { topic, tone } = body || {};
    log("2_BODY_PARSED", { topicLength: topic?.length, tone });

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

    // Fetch Tenant Context & RAG Data
    if (authHeader) {
      log("3_FETCH_TENANT_CONTEXT");
      const userClient = createClient(supabaseUrl, Deno.env.get("SUPABASE_ANON_KEY")!, {
        global: { headers: { Authorization: authHeader } }
      });
      const { data: { user }, error: userErr } = await userClient.auth.getUser();

      if (userErr) {
        log("WARN_AUTH_USER_FAILED", userErr.message);
      }

      if (user) {
        const { data: account, error: accErr } = await supabase
          .schema("threads")
          .from("threads_accounts")
          .select("id")
          .eq("user_id", user.id)
          .limit(1)
          .maybeSingle();

        if (accErr) log("WARN_ACC_FETCH_ERR", accErr.message);

        if (account) {
          // Fetch Auto Reply Settings Context
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

          // Fetch RAG Documents dari tabel brand_knowledge
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

    log("4_BUILD_PROMPT", { ragDocsCount: ragDocs.length });

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

    log("5_CALL_GEMINI_API");
    const geminiRes = await fetch(
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

    const geminiData = await geminiRes.json();

    if (!geminiRes.ok || geminiData.error) {
      log("ERR_GEMINI_API_RESPONSE", geminiData.error || geminiRes.statusText);
      return new Response(
        JSON.stringify({ error: geminiData.error?.message || "Gemini API mengembalikan respons error." }),
        { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    log("6_PARSE_GEMINI_OUTPUT");
    let rawText = geminiData.candidates?.[0]?.content?.parts?.[0]?.text || "[]";
    rawText = rawText.replace(/```json/g, "").replace(/```/g, "").trim();

    let options = [];
    try {
      options = JSON.parse(rawText);
    } catch (jsonErr: any) {
      log("WARN_JSON_PARSE_FALLBACK", jsonErr.message);
      options = [{ id: 1, title: "Draf Post", content: rawText }];
    }

    log("7_SUCCESS_FINISH");
    return new Response(
      JSON.stringify({ success: true, options }),
      { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );

  } catch (globalErr: any) {
    console.error("[CRITICAL_EDGE_FUNCTION_CRASH]", globalErr.stack || globalErr.message || globalErr);
    return new Response(
      JSON.stringify({ 
        error: "Uncaught Edge Function Exception: " + (globalErr.message || "Unknown error"),
        stack: globalErr.stack 
      }),
      { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
