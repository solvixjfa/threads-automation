<template>
  <div class="space-y-6">
    <Card>
      <template #header>
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-sm font-bold">Connected account</h2>
            <p class="text-xs theme-text-muted mt-0.5">Meta Threads API connection.</p>
          </div>
          <Badge :variant="accountConnected ? 'success' : 'default'">
            {{ accountConnected ? 'Connected' : 'Not connected' }}
          </Badge>
        </div>
      </template>

      <div v-if="loading" class="space-y-2">
        <div class="h-4 w-32 skeleton"></div>
        <div class="h-3 w-48 skeleton"></div>
      </div>

      <div v-else class="flex items-center justify-between gap-4">
        <div>
          <p class="text-sm font-bold">{{ accountUsername ? '@' + accountUsername : 'No active account' }}</p>
          <p class="text-xs theme-text-muted mt-0.5">
            {{ accountConnected
              ? 'Ready to publish posts and read interactions.'
              : 'Connect your Threads account to start automation.' }}
          </p>
        </div>
        <Button @click="connectThreads" size="sm">
          {{ accountConnected ? 'Reconnect' : 'Connect' }}
        </Button>
      </div>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { supabase } from '../../lib/supabase'
import { useNotify } from '../../composables/useNotify'
import { Card, Button, Badge } from '../../components/ui'

const { showToast } = useNotify()
const loading = ref(true)
const accountConnected = ref(false)
const accountUsername = ref('')

async function initAccount() {
  loading.value = true
  try {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) return
    const { data: account } = await supabase
      .schema('threads')
      .from('threads_accounts')
      .select('username, connection_status')
      .eq('user_id', user.id)
      .maybeSingle()
    if (account) {
      accountConnected.value = account.connection_status === 'connected'
      accountUsername.value = account.username || ''
    }
  } finally {
    loading.value = false
  }
}

async function connectThreads() {
  try {
    const { data, error } = await supabase.functions.invoke('threads-oauth-start')
    if (error) throw error
    if (data?.error) throw new Error(data.error)
    if (data?.url) window.location.href = data.url
  } catch (err: any) {
    showToast('Failed to load OAuth URL: ' + err.message, 'error')
  }
}

onMounted(initAccount)
</script>
