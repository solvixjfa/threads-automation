<template>
  <Card>
    <template #header>
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-sm font-bold">Auto reply</h2>
          <p class="text-xs theme-text-muted mt-0.5">Operational rules and tone for automatic replies.</p>
        </div>
        <button
          type="button"
          @click="autoReply.enabled = !autoReply.enabled"
          class="relative inline-flex h-6 w-11 shrink-0 items-center rounded-full transition"
          :style="{ background: autoReply.enabled ? 'var(--accent)' : 'var(--bg-hover)' }"
        >
          <span
            class="inline-block h-5 w-5 rounded-full transition-transform"
            :style="{
              background: autoReply.enabled ? 'var(--accent-text)' : 'var(--text-muted)',
              transform: autoReply.enabled ? 'translateX(22px)' : 'translateX(2px)'
            }"
          ></span>
        </button>
      </div>
    </template>

    <div v-if="loading" class="space-y-3">
      <div class="h-10 skeleton"></div>
      <div class="h-20 skeleton"></div>
    </div>

    <template v-else>
    <div v-if="!autoReply.enabled" class="p-4 rounded-lg theme-bg-sec border theme-border text-xs theme-text-muted">
      Auto reply is disabled. Enable the toggle above to start generating replies.
    </div>

    <div v-else class="space-y-4">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="space-y-1">
          <label class="label">Operation mode</label>
          <select v-model="autoReply.mode" class="input">
            <option value="review">Review queue (approve manually)</option>
            <option value="auto">Full auto (reply immediately)</option>
          </select>
        </div>
        <div class="space-y-1">
          <label class="label">Max replies per hour</label>
          <input v-model.number="autoReply.max_per_hour" type="number" class="input" />
        </div>
      </div>

      <div class="space-y-1">
        <label class="label">Tone and instruction prompt</label>
        <textarea
          v-model="autoReply.tone_prompt"
          rows="3"
          placeholder="Example: Reply politely, concise, and helpful. Never lecture."
          class="textarea"
        ></textarea>
        <p class="text-[11px] theme-text-muted mt-1">Guides how the AI writes replies. Leave empty for default tone.</p>
      </div>
    </div>

    </template>

    <template #footer>
      <div class="flex justify-end">
        <Button @click="save" :disabled="saving || !accountId" :loading="saving">
          {{ saving ? 'Saving...' : 'Save' }}
        </Button>
      </div>
    </template>
  </Card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { supabase } from '../../lib/supabase'
import { useNotify } from '../../composables/useNotify'
import { Card, Button } from '../../components/ui'

const { showToast } = useNotify()
const loading = ref(true)
const accountId = ref<string | null>(null)
const saving = ref(false)

const autoReply = ref({
  enabled: true,
  mode: 'review',
  max_per_hour: 10,
  tone_prompt: ''
})

async function load() {
  loading.value = true
  try {
    await loadInternal()
  } finally {
    loading.value = false
  }
}

async function loadInternal() {
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) return
  const { data: account } = await supabase
    .schema('threads')
    .from('threads_accounts')
    .select('id')
    .eq('user_id', user.id)
    .maybeSingle()
  if (!account) return
  accountId.value = account.id

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

async function save() {
  if (!accountId.value) return
  saving.value = true
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
    saving.value = false
  }
}

onMounted(load)
</script>
