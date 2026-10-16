<template>
  <div class="space-y-6">
    <Card>
      <template #header>
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-sm font-bold">Connected Account</h2>
            <p class="text-xs theme-text-muted mt-0.5">Meta Threads API connection status.</p>
          </div>
          <Badge :variant="accountConnected ? 'success' : 'default'">
            {{ accountConnected ? 'Connected' : 'Not connected' }}
          </Badge>
        </div>
      </template>

      <div class="flex items-center justify-between gap-4">
        <div>
          <p class="text-sm font-bold">{{ accountUsername ? '@' + accountUsername : 'No active account' }}</p>
          <p class="text-xs theme-text-muted mt-0.5">
            {{ accountConnected
              ? 'Ready to publish posts and read interactions.'
              : 'Connect your Threads account to start automation.' }}
          </p>
        </div>
        <Button @click="connectThreads" size="sm">
          {{ accountConnected ? 'Reconnect' : 'Connect Threads' }}
        </Button>
      </div>
    </Card>

    <Card>
      <template #header>
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-sm font-bold">Auto Reply</h2>
            <p class="text-xs theme-text-muted mt-0.5">Operational rules and language style for replies.</p>
          </div>
          <label class="relative inline-flex items-center cursor-pointer">
            <input type="checkbox" v-model="autoReply.enabled" class="sr-only peer">
            <div class="w-11 h-6 rounded-full transition theme-bg-hover peer-checked:theme-accent after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:rounded-full after:h-5 after:w-5 after:transition-all after:theme-bg peer-checked:after:translate-x-full"></div>
          </label>
        </div>
      </template>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="space-y-1">
          <label class="label">Operation Mode</label>
          <select v-model="autoReply.mode" class="input">
            <option value="review">Review queue (approve manually)</option>
            <option value="auto">Full auto (reply immediately)</option>
          </select>
        </div>
        <div class="space-y-1">
          <label class="label">Max per hour</label>
          <input v-model.number="autoReply.max_per_hour" type="number" class="input" />
        </div>
      </div>

      <div class="space-y-1 mt-4">
        <label class="label">Tone and instruction prompt</label>
        <textarea
          v-model="autoReply.tone_prompt"
          rows="3"
          placeholder="Example: Reply politely, concise, and helpful. Never lecture."
          class="textarea"
        ></textarea>
      </div>

      <template #footer>
        <div class="flex justify-end">
          <Button @click="saveAutoReplySettings" :disabled="isSavingSettings" :loading="isSavingSettings">
            {{ isSavingSettings ? 'Saving...' : 'Save settings' }}
          </Button>
        </div>
      </template>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { supabase } from '../../lib/supabase'
import { useNotify } from '../../composables/useNotify'
import { Card, Button, Badge } from '../../components/ui'

const { showToast } = useNotify()

const accountConnected = ref(false)
const accountUsername = ref('')
const accountId = ref<string | null>(null)
const isSavingSettings = ref(false)

const autoReply = ref({
  enabled: true,
  mode: 'review',
  max_per_hour: 10,
  tone_prompt: ''
})

async function initAccountAndSettings() {
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) return

  const { data: account } = await supabase
    .schema('threads')
    .from('threads_accounts')
    .select('*')
    .eq('user_id', user.id)
    .maybeSingle()

  if (account) {
    accountId.value = account.id
    accountConnected.value = account.connection_status === 'connected'
    accountUsername.value = account.username || ''

    const { data: settings } = await supabase
      .schema('threads')
      .from('auto_reply_settings')
      .select('*')
      .eq('account_id', account.id)
      .maybeSingle()

    if (settings) {
      autoReply.value.enabled = settings.enabled ?? true
      autoReply.value.mode = settings.mode || 'review'
      autoReply.value.max_per_hour = settings.max_per_hour || 10
      autoReply.value.tone_prompt = settings.tone_prompt || ''
    }
  }
}

async function connectThreads() {
  try {
    const { data, error } = await supabase.functions.invoke('threads-oauth-start')
    if (error) throw error
    if (data?.error) throw new Error(data.error)
    if (data?.url) {
      window.location.href = data.url
    }
  } catch (err: any) {
    showToast('Failed to load OAuth URL: ' + err.message, 'error')
  }
}

async function saveAutoReplySettings() {
  if (!accountId.value) return showToast('Connect a Threads account first.', 'error')
  isSavingSettings.value = true
  try {
    const { error } = await supabase
      .schema('threads')
      .from('auto_reply_settings')
      .upsert({
        account_id: accountId.value,
        enabled: autoReply.value.enabled,
        mode: autoReply.value.mode,
        max_per_hour: autoReply.value.max_per_hour,
        tone_prompt: autoReply.value.tone_prompt
      })
    if (error) throw error
    showToast('Settings saved.', 'success')
  } catch (err: any) {
    showToast('Failed to save: ' + err.message, 'error')
  } finally {
    isSavingSettings.value = false
  }
}

onMounted(initAccountAndSettings)
</script>
