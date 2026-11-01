<template>
  <Card>
    <template #header>
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-sm font-bold">{{ $t('settings.auto_reply.title') }}</h2>
          <p class="text-xs theme-text-muted mt-0.5">{{ $t('settings.auto_reply.subtitle') }}</p>
        </div>
        <button type="button" @click="autoReply.enabled = !autoReply.enabled" class="relative inline-flex h-6 w-11 shrink-0 items-center rounded-full transition" :style="{ background: autoReply.enabled ? 'var(--accent)' : 'var(--bg-hover)' }">
          <span class="inline-block h-5 w-5 rounded-full transition-transform" :style="{ background: autoReply.enabled ? 'var(--accent-text)' : 'var(--text-muted)', transform: autoReply.enabled ? 'translateX(22px)' : 'translateX(2px)' }"></span>
        </button>
      </div>
    </template>

    <div v-if="loading" class="space-y-3">
      <div class="h-10 skeleton"></div>
      <div class="h-20 skeleton"></div>
    </div>

    <template v-else>
    <div v-if="!autoReply.enabled" class="p-4 rounded-lg theme-bg-sec border theme-border text-xs theme-text-muted">
      {{ $t('settings.auto_reply.disabled_msg') }}
    </div>

    <div v-else class="space-y-4">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Select 
          v-model="autoReply.mode" 
          :label="$t('settings.auto_reply.mode_label')" 
          :options="[
            { label: $t('settings.auto_reply.mode_review'), value: 'review' },
            { label: $t('settings.auto_reply.mode_auto'), value: 'auto' }
          ]" 
        />
        
        <div class="space-y-1">
          <label class="label">{{ $t('settings.auto_reply.max_replies') }}</label>
          <input v-model.number="autoReply.max_per_hour" type="number" class="input" min="1" max="100" />
          <p class="text-[10px] theme-text-muted">{{ $t('settings.auto_reply.max_replies_desc') }}</p>
        </div>
      </div>

      <div v-if="autoReply.mode === 'auto'" class="p-3 rounded-lg bg-amber-500/10 border border-amber-500/20 text-amber-500 text-[11px]">
        <strong>{{ $t('settings.auto_reply.warning') }}</strong>
      </div>

      <div class="space-y-1">
        <label class="label">{{ $t('settings.auto_reply.tone_label') }}</label>
        <textarea v-model="autoReply.tone_prompt" rows="3" :placeholder="$t('settings.auto_reply.tone_ph')" class="textarea"></textarea>
        <p class="text-[11px] theme-text-muted mt-1">{{ $t('settings.auto_reply.tone_desc') }}</p>
      </div>
    </div>
    </template>

    <template #footer>
      <div class="flex justify-end">
        <Button @click="save" :disabled="saving || !accountId" :loading="saving">
          {{ saving ? $t('common.processing') : $t('settings.auto_reply.save_btn') }}
        </Button>
      </div>
    </template>
  </Card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { supabase } from '../../lib/supabase'
import { useNotify } from '../../composables/useNotify'
import { Card, Button, Select } from '../../components/ui'

const { showToast } = useNotify()
const loading = ref(true)
const accountId = ref<string | null>(null)
const saving = ref(false)
const autoReply = ref({ enabled: true, mode: 'review', max_per_hour: 10, tone_prompt: '' })

async function load() {
  loading.value = true
  try {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) return
    const { data: account } = await supabase.schema('threads').from('threads_accounts').select('id').eq('user_id', user.id).maybeSingle()
    if (!account) return
    accountId.value = account.id

    const { data: settings } = await supabase.schema('threads').from('auto_reply_settings').select('*').eq('account_id', account.id).maybeSingle()
    if (settings) {
      autoReply.value.enabled = settings.enabled ?? true
      autoReply.value.mode = settings.mode || 'review'
      autoReply.value.max_per_hour = settings.max_per_hour || 10
      autoReply.value.tone_prompt = settings.tone_prompt || ''
    }
  } finally { loading.value = false }
}

async function save() {
  if (!accountId.value) return
  saving.value = true
  try {
    const { error } = await supabase.schema('threads').from('auto_reply_settings').upsert({
      account_id: accountId.value, enabled: autoReply.value.enabled, mode: autoReply.value.mode, max_per_hour: autoReply.value.max_per_hour, tone_prompt: autoReply.value.tone_prompt
    })
    if (error) throw error
    showToast('Settings saved.', 'success')
  } catch (err: any) {
    showToast('Failed to save: ' + err.message, 'error')
  } finally { saving.value = false }
}

onMounted(load)
</script>
