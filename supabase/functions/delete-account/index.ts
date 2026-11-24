import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const authHeader = req.headers.get('Authorization')
    if (!authHeader) {
      return new Response(JSON.stringify({ error: 'Unauthorized' }), {
        status: 401,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      })
    }

    const supabaseUrl = Deno.env.get('SUPABASE_URL') ?? ''
    const supabaseAnonKey = Deno.env.get('SUPABASE_ANON_KEY') ?? ''
    const supabaseServiceKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''

    const userClient = createClient(supabaseUrl, supabaseAnonKey, {
      global: { headers: { Authorization: authHeader } },
    })

    const { data: { user }, error: userError } = await userClient.auth.getUser()
    if (userError || !user) {
      return new Response(JSON.stringify({ error: 'Invalid user session' }), {
        status: 401,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      })
    }

    const adminClient = createClient(supabaseUrl, supabaseServiceKey)
    const body = await req.json()
    const mode = body?.mode as string

    if (mode === 'disconnect_account') {
      const accountId = body?.account_id as string
      if (!accountId) {
        return new Response(JSON.stringify({ error: 'account_id is required' }), {
          status: 400,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        })
      }

      const { error: delError } = await adminClient
        .schema('threads')
        .from('threads_accounts')
        .delete()
        .eq('id', accountId)
        .eq('user_id', user.id)

      if (delError) throw delError

      return new Response(JSON.stringify({ success: true, mode: 'disconnect_account' }), {
        status: 200,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      })
    }

    if (mode === 'account_only' || mode === 'full_data') {
      const { data: userAccounts } = await adminClient
        .schema('threads')
        .from('threads_accounts')
        .select('id')
        .eq('user_id', user.id)

      const accountIds = (userAccounts ?? []).map((a: { id: string }) => a.id)

      if (mode === 'full_data') {
        const accountTables = [
          'scheduled_posts',
          'post_queue',
          'reply_logs',
          'auto_reply_rules',
          'knowledge_base',
          'analytics_snapshots',
          'ai_logs',
        ]
        if (accountIds.length > 0) {
          for (const table of accountTables) {
            try {
              await adminClient
                .schema('threads')
                .from(table)
                .delete()
                .in('account_id', accountIds)
            } catch (_) {
              // Abaikan jika tabel tidak ada
            }
          }
        }

        const userTables = ['credit_transactions', 'payments']
        for (const table of userTables) {
          try {
            await adminClient
              .schema('threads')
              .from(table)
              .delete()
              .eq('user_id', user.id)
          } catch (_) {
            // Abaikan jika tabel tidak ada
          }
        }
      }

      const { error: accDelError } = await adminClient
        .schema('threads')
        .from('threads_accounts')
        .delete()
        .eq('user_id', user.id)

      if (accDelError && mode === 'account_only') {
        await adminClient
          .schema('threads')
          .from('threads_accounts')
          .update({
            access_token: 'REVOKED',
            custom_gemini_key: null,
            custom_groq_key: null,
          })
          .eq('user_id', user.id)
      }

      try {
        await adminClient
          .schema('threads')
          .from('profiles')
          .delete()
          .eq('id', user.id)
      } catch (_) {
        // Lanjut hapus auth user
      }

      const { error: authDelError } = await adminClient.auth.admin.deleteUser(user.id)
      if (authDelError) throw authDelError

      return new Response(JSON.stringify({ success: true, mode }), {
        status: 200,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      })
    }

    return new Response(JSON.stringify({ error: 'Invalid mode' }), {
      status: 400,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    })
  } catch (err) {
    return new Response(JSON.stringify({ error: (err as Error).message || 'Server error' }), {
      status: 500,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    })
  }
})
