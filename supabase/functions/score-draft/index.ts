import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

serve(async (req) => {
  // 1. Handle CORS Preflight Request
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const { text, account_id } = await req.json()

    if (!text) {
      return new Response(JSON.stringify({ error: 'Text is required' }), {
        status: 400,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      })
    }

    // --- LOGIKA AI SEDERHANA (GANTI DENGAN CALL API GEMINI LU NANTI) ---
    // Di sini kita bikin dummy response dulu biar jalurnya lancar.
    const mockScore = Math.floor(Math.random() * 41) + 50 // Random 50-90
    const mockSuggestions = [
      'Gunakan pertanyaan di awal kalimat (Hook).',
      'Tambahkan jeda baris agar lebih mudah dibaca.',
    ]

    const responsePayload = {
      result: {
        score: mockScore,
        breakdown: { clarity: 80, engagement_potential: 75 },
        suggestions: mockSuggestions
      }
    }

    return new Response(JSON.stringify(responsePayload), {
      status: 200,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    })

  } catch (error) {
    console.error('Error di score-draft:', error)
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    })
  }
})
