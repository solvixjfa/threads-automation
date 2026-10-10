import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

async function getEmbedding(text: string, apiKey: string): Promise<number[]> {
  const res = await fetch(
    `https://generativelanguage.googleapis.com/v1beta/models/text-embedding-004:embedContent?key=${apiKey}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model: "models/text-embedding-004",
        content: { parts: [{ text }] }
      }),
    }
  );

  const data = await res.json();
  if (!res.ok || data.error) {
    throw new Error(data.error?.message || "Gagal membuat vector embedding.");
  }

  return data.embedding.values;
}

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
    const serviceRoleKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
    const geminiApiKey = Deno.env.get("GEMINI_API_KEY")!;

    const { id, content } = await req.json();

    if (!id || !content) {
      return new Response(
        JSON.stringify({ error: "Parameter ID dan content wajib diisi." }),
        { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    // Generate vector 768 dimensi via Gemini
    const vector = await getEmbedding(content, geminiApiKey);

    const supabase = createClient(supabaseUrl, serviceRoleKey);
    const { error } = await supabase
      .schema("threads")
      .from("brand_knowledge")
      .update({ embedding: JSON.stringify(vector) })
      .eq("id", id);

    if (error) throw error;

    return new Response(
      JSON.stringify({ success: true, message: "Vector embedding berhasil dibuat & disimpan." }),
      { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (err: any) {
    return new Response(
      JSON.stringify({ error: err.message }),
      { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
