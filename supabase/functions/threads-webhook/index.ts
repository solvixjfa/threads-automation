import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'

serve(async (req) => {
  const url = new URL(req.url)

  // Handshake Verifikasi dari Meta Portal (GET)
  if (req.method === 'GET') {
    const mode = url.searchParams.get('hub.mode')
    const token = url.searchParams.get('hub.verify_token')
    const challenge = url.searchParams.get('hub.challenge')
    
    const EXPECTED_TOKEN = 'IXIERA_WH_SEC_9f8a2b1c4e7d3056_2026_xT'

    if (mode === 'subscribe' && token === EXPECTED_TOKEN) {
      return new Response(challenge, {
        status: 200,
        headers: { 'Content-Type': 'text/plain' }
      })
    }
    
    return new Response('Forbidden', { status: 403 })
  }

  // Event Ingestion dari Threads (POST)
  if (req.method === 'POST') {
    return new Response(JSON.stringify({ status: 'ok' }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    })
  }

  return new Response('Method Not Allowed', { status: 405 })
})
