import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'

serve(async (req) => {
  const url = new URL(req.url)

  // Webhook Verification Request from Meta (GET)
  if (req.method === 'GET') {
    const mode = url.searchParams.get('hub.mode')
    const token = url.searchParams.get('hub.verify_token')
    const challenge = url.searchParams.get('hub.challenge')
    const expectedToken = Deno.env.get('THREADS_WEBHOOK_VERIFY_TOKEN')

    if (mode === 'subscribe' && token === expectedToken) {
      return new Response(challenge, {
        status: 200,
        headers: { 'Content-Type': 'text/plain' }
      })
    }
    return new Response('Forbidden', { status: 403 })
  }

  // Webhook Event Ingestion (POST)
  if (req.method === 'POST') {
    return new Response(JSON.stringify({ status: 'ok' }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    })
  }

  return new Response('Method Not Allowed', { status: 405 })
})
