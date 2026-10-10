import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'

serve(async (req) => {
  // Langsung bypass semua pengecekan header/JWT di dalam kode
  const clientId = Deno.env.get('THREADS_APP_ID')
  const redirectUri = Deno.env.get('THREADS_REDIRECT_URI')

  if (!clientId || !redirectUri) {
    return new Response(JSON.stringify({ error: 'Missing env variables' }), { 
      status: 500, 
      headers: { 'Content-Type': 'application/json' } 
    })
  }

  // Bikin URL Login Threads Meta
  const scope = 'threads_basic,threads_content_publish' // Sesuaikan scope jika perlu
  const authUrl = `https://www.threads.net/oauth/authorize?client_id=${clientId}&redirect_uri=${encodeURIComponent(redirectUri)}&scope=${scope}&response_type=code`

  // Redirect otomatis browser ke halaman login Meta
  return Response.redirect(authUrl, 302)
})
