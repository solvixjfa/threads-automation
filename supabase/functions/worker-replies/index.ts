import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { corsHeaders } from "../_shared/cors.ts";

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
    const serviceRoleKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
    const supabase = createClient(supabaseUrl, serviceRoleKey);

    // Ambil balasan yang belum terklasifikasi
    const { data: unclassified, error: fetchErr } = await supabase
      .schema("threads")
      .from("replies")
      .select("*")
      .eq("classification", "unclassified")
      .limit(20);

    if (fetchErr) throw fetchErr;

    let processedCount = 0;

    for (const reply of unclassified || []) {
      const txt = (reply.text || "").toLowerCase();
      let classification = "neutral";

      // Logika Klasifikasi Sederhana/Rule-Based Baseline
      if (txt.includes("?") || txt.startsWith("gimana") || txt.startsWith("apa") || txt.startsWith("kenapa")) {
        classification = "question";
      } else if (txt.includes("keren") || txt.includes("mantap") || txt.includes("top") || txt.includes("🔥") || txt.includes("👍")) {
        classification = "praise";
      } else if (txt.includes("http://") || txt.includes("https://") || txt.includes("slot") || txt.includes("gacor")) {
        classification = "spam";
      } else if (txt.includes("anjing") || txt.includes("babi") || txt.includes("goblok")) {
        classification = "toxic";
      }

      await supabase
        .schema("threads")
        .from("replies")
        .update({
          classification,
          processed_at: new Date().toISOString()
        })
        .eq("id", reply.id);

      processedCount++;
    }

    return new Response(JSON.stringify({ success: true, processed: processedCount }), {
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  } catch (err: any) {
    return new Response(JSON.stringify({ error: err.message }), {
      status: 500,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }
});
