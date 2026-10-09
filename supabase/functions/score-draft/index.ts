import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { corsHeaders } from "../_shared/cors.ts";

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    const { text, account_id, scheduled_post_id } = await req.json();

    if (!text || !account_id) {
      return new Response(JSON.stringify({ error: "Missing text or account_id" }), {
        status: 400,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    // 1. Analisis Heuristik Dasar
    let heuristicScore = 50;
    const suggestions: string[] = [];
    
    // Check Hook & Length
    if (text.length >= 100 && text.length <= 350) {
      heuristicScore += 15;
    } else if (text.length < 50) {
      heuristicScore -= 10;
      suggestions.push("Teks terlalu pendek, tambahkan detail atau kalimat pembuka yang menarik.");
    }

    // Check Question / Engagement Trigger
    if (text.includes("?")) {
      heuristicScore += 15;
    } else {
      suggestions.push("Tambahkan pertanyaan di akhir postingan untuk memicu diskusi/komentar.");
    }

    // Check Formatting / Paragraph Breaks
    if (text.includes("\n")) {
      heuristicScore += 10;
    } else {
      suggestions.push("Gunakan pemisah baris (enter) agar postingan lebih enak dibaca.");
    }

    const finalScore = Math.min(Math.max(heuristicScore, 10), 100);

    const breakdown = {
      heuristic_score: heuristicScore,
      length: text.length,
      has_question: text.includes("?"),
      has_line_breaks: text.includes("\n")
    };

    // 2. Simpan Skor ke DB (opsional jika dikirim scheduled_post_id)
    const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
    const serviceRoleKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
    const supabase = createClient(supabaseUrl, serviceRoleKey);

    const { data: scoreRecord, error: dbErr } = await supabase
      .schema("threads")
      .from("content_scores")
      .insert({
        account_id,
        scheduled_post_id: scheduled_post_id || null,
        score: finalScore,
        breakdown,
        suggestions,
        model_version: "v1.0-heuristic"
      })
      .select("*")
      .single();

    if (dbErr) throw dbErr;

    return new Response(JSON.stringify({ success: true, result: scoreRecord }), {
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  } catch (err: any) {
    return new Response(JSON.stringify({ error: err.message }), {
      status: 500,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }
});
