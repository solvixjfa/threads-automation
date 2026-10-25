<template>
  <div class="space-y-6">
    <Card>
      <template #header>
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-sm font-bold">AI & Billing</h2>
            <p class="text-xs theme-text-muted mt-0.5">Manage your AI credits and personal API keys.</p>
          </div>
          <!-- BADGE DINAMIS -->
          <Badge v-if="hasCustomKey" variant="success">Own API Key</Badge>
          <Badge v-else :variant="credits > 0 ? 'success' : 'danger'">
            {{ credits }} SaaS Credits
          </Badge>
        </div>
      </template>

      <div v-if="loading" class="space-y-3">
        <div class="h-10 skeleton"></div>
        <div class="h-20 skeleton"></div>
      </div>

      <template v-else>
        <!-- STATUS BAR: Nunjukin lu lagi pake yang mana -->
        <div 
          class="p-4 rounded-lg border theme-border space-y-2 mb-6"
          :style="hasCustomKey ? 'background: var(--bg-sec);' : 'background: var(--bg-sec);'"
        >
          <div class="flex items-center gap-2">
            <span 
              class="w-2.5 h-2.5 rounded-full" 
              :style="hasCustomKey ? 'background: var(--success);' : 'background: var(--accent);'"
            ></span>
            <h3 class="text-sm font-bold">
              {{ hasCustomKey ? 'Using Your Own Gemini API Key' : 'Using SaaS AI Credits' }}
            </h3>
          </div>
          <p v-if="!hasCustomKey" class="text-xs theme-text-muted">
            You have <strong>{{ credits }}</strong> credits left. 1 credit is used per Content Plan generation.
          </p>
          <p v-else class="text-xs theme-text-muted">
            Unlimited generation. Your SaaS credits ({{ credits }}) will NOT be deducted.
          </p>
        </div>

        <!-- BYOK INPUT -->
        <div class="space-y-3">
          <h3 class="text-sm font-bold">Bring Your Own Key (BYOK)</h3>
          <p class="text-xs theme-text-muted">
            Use your own Google Gemini API Key to generate unlimited content for free.
          </p>
          <div class="space-y-1">
            <label class="label">Gemini API Key</label>
            <input 
              v-model="customKey" 
              type="password" 
              placeholder="AIzaSy..." 
              class="input" 
            />
            <p class="text-[11px] theme-text-muted mt-1">
              Get your free API key at <a href="https://aistudio.google.com/app/apikey" target="_blank" class="font-bold theme-text hover:underline">Google AI Studio</a>.
            </p>
          </div>
        </div>
      </template>

      <template #footer>
        <div class="flex justify-between items-center gap-3">
          <!-- TOMBOL REMOVE (KIRI) -->
          <button 
            v-if="hasCustomKey" 
            @click="confirmRemove" 
            class="text-xs font-bold px-3 py-2 rounded-lg border theme-border theme-text-muted hover:theme-text transition-colors"
          >
            Remove API Key
          </button>
          <div v-else></div>

          <!-- TOMBOL SAVE (KANAN) -->
          <Button @click="saveKey" :disabled="saving || !accountId || !customKey.trim()" :loading="saving">
            {{ saving ? 'Saving...' : 'Save API Key' }}
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

const { showToast, askConfirm } = useNotify()
const loading = ref(true)
const saving = ref(false)
const accountId = ref<string | null>(null)

const credits = ref(0)
const customKey = ref('')
const hasCustomKey = ref(false)

async function load() {
  loading.value = true
  try {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) return

    const { data: account, error } = await supabase
      .schema('threads')
      .from('threads_accounts')
      .select('id, ai_credits, custom_gemini_key')
      .eq('user_id', user.id)
      .maybeSingle()

    if (error) throw error

    if (account) {
      accountId.value = account.id
      credits.value = account.ai_credits ?? 20
      customKey.value = account.custom_gemini_key || ''
      hasCustomKey.value = !!account.custom_gemini_key
    }
  } catch (err: any) {
    showToast('Failed to load settings: ' + err.message, 'error')
  } finally {
    loading.value = false
  }
}

async function saveKey() {
  if (!accountId.value || !customKey.value.trim()) return
  saving.value = true
  try {
    const keyToSave = customKey.value.trim()
    const { error } = await supabase
      .schema('threads')
      .from('threads_accounts')
      .update({ custom_gemini_key: keyToSave })
      .eq('id', accountId.value)

    if (error) throw error
    
    hasCustomKey.value = true
    showToast('API Key saved. You are now on Unlimited mode.', 'success')
  } catch (err: any) {
    showToast('Failed to save API Key: ' + err.message, 'error')
  } finally {
    saving.value = false
  }
}

function confirmRemove() {
  askConfirm({
    title: 'Remove API Key',
    message: 'Are you sure? Your account will switch back to using SaaS Credits.',
    confirmText: 'Remove',
    onConfirm: () => removeKey()
  })
}

async function removeKey() {
  if (!accountId.value) return
  saving.value = true
  try {
    const { error } = await supabase
      .schema('threads')
      .from('threads_accounts')
      .update({ custom_gemini_key: null })
      .eq('id', accountId.value)

    if (error) throw error
    
    customKey.value = ''
    hasCustomKey.value = false
    showToast('API Key removed. Switched back to SaaS Credits.', 'info')
  } catch (err: any) {
    showToast('Failed to remove API Key: ' + err.message, 'error')
  } finally {
    saving.value = false
  }
}

onMounted(load)
</script>
