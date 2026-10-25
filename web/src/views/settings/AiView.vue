<template>
  <div class="space-y-6">
    <Card>
      <template #header>
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-sm font-bold">AI & Billing</h2>
            <p class="text-xs theme-text-muted mt-0.5">Manage your AI providers and keys.</p>
          </div>
          <Badge v-if="hasCustomKey || hasGroqKey" variant="success">BYOK Active</Badge>
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
        <!-- DEFAULT PROVIDER -->
        <div class="p-4 rounded-lg border theme-border space-y-3 mb-6" style="background: var(--bg-sec);">
          <h3 class="text-sm font-bold">Default AI Provider</h3>
          <div class="flex gap-4">
            <label class="flex items-center gap-2 text-sm cursor-pointer">
              <input type="radio" v-model="aiProvider" value="groq" class="w-4 h-4" />
              <span class="font-bold">Groq (Llama 3.3) - Fast</span>
            </label>
            <label class="flex items-center gap-2 text-sm cursor-pointer">
              <input type="radio" v-model="aiProvider" value="gemini" class="w-4 h-4" />
              <span class="font-bold">Gemini (Google) - Smart</span>
            </label>
          </div>
        </div>

        <!-- CREDITS -->
        <div v-if="!hasCustomKey && !hasGroqKey" class="p-4 rounded-lg theme-bg-sec border theme-border space-y-2 mb-6">
          <p class="text-xs theme-text-muted">
            You have <strong>{{ credits }}</strong> SaaS credits left. 1 credit is used per generation.
          </p>
        </div>

        <!-- BYOK GROQ -->
        <div class="space-y-3 mb-6">
          <h3 class="text-sm font-bold">Groq API Key</h3>
          <div class="space-y-1">
            <input v-model="groqKey" type="password" placeholder="gsk_..." class="input" />
            <p class="text-[11px] theme-text-muted mt-1">
              Get your free key at <a href="https://console.groq.com/keys" target="_blank" class="font-bold theme-text hover:underline">Groq Console</a>.
            </p>
          </div>
        </div>

        <!-- BYOK GEMINI -->
        <div class="space-y-3">
          <h3 class="text-sm font-bold">Gemini API Key <span class="text-xs font-normal theme-text-muted">(Wajib untuk RAG Embedding)</span></h3>
          <div class="space-y-1">
            <input v-model="geminiKey" type="password" placeholder="AIzaSy..." class="input" />
            <p class="text-[11px] theme-text-muted mt-1">
              Get your free key at <a href="https://aistudio.google.com/app/apikey" target="_blank" class="font-bold theme-text hover:underline">Google AI Studio</a>.
            </p>
          </div>
        </div>
      </template>

      <template #footer>
        <div class="flex justify-between items-center gap-3">
          <button v-if="hasCustomKey || hasGroqKey" @click="confirmRemove" class="text-xs font-bold px-3 py-2 rounded-lg border theme-border theme-text-muted hover:theme-text transition-colors">
            Remove All Keys
          </button>
          <div v-else></div>
          <Button @click="saveSettings" :disabled="saving || !accountId" :loading="saving">
            {{ saving ? 'Saving...' : 'Save Settings' }}
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
const aiProvider = ref('groq')
const geminiKey = ref('')
const groqKey = ref('')
const hasCustomKey = ref(false)
const hasGroqKey = ref(false)

async function load() {
  loading.value = true
  try {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) return
    const { data: account, error } = await supabase
      .schema('threads').from('threads_accounts')
      .select('id, ai_credits, custom_gemini_key, custom_groq_key, ai_provider')
      .eq('user_id', user.id).maybeSingle()
    if (error) throw error
    if (account) {
      accountId.value = account.id
      credits.value = account.ai_credits ?? 20
      geminiKey.value = account.custom_gemini_key || ''
      groqKey.value = account.custom_groq_key || ''
      aiProvider.value = account.ai_provider || 'groq'
      hasCustomKey.value = !!account.custom_gemini_key
      hasGroqKey.value = !!account.custom_groq_key
    }
  } catch (err: any) {
    showToast('Failed to load: ' + err.message, 'error')
  } finally {
    loading.value = false
  }
}

async function saveSettings() {
  if (!accountId.value) return
  saving.value = true
  try {
    // Validasi Groq Key kalau diisi
    if (groqKey.value.trim()) {
      const res = await fetch('https://api.groq.com/openai/v1/models', {
        headers: { 'Authorization': `Bearer ${groqKey.value.trim()}` }
      })
      if (!res.ok) throw new Error('Invalid Groq API Key.')
    }
    
    // Validasi Gemini Key kalau diisi
    if (geminiKey.value.trim()) {
      const res = await fetch(`https://generativelanguage.googleapis.com/v1beta/models?key=${geminiKey.value.trim()}`)
      if (!res.ok) throw new Error('Invalid Gemini API Key.')
    }

    const { error } = await supabase.schema('threads').from('threads_accounts').update({
      custom_gemini_key: geminiKey.value.trim() || null,
      custom_groq_key: groqKey.value.trim() || null,
      ai_provider: aiProvider.value
    }).eq('id', accountId.value)

    if (error) throw error
    hasCustomKey.value = !!geminiKey.value.trim()
    hasGroqKey.value = !!groqKey.value.trim()
    showToast('AI settings saved.', 'success')
  } catch (err: any) {
    showToast(err.message, 'error')
  } finally {
    saving.value = false
  }
}

function confirmRemove() {
  askConfirm({
    title: 'Remove Keys',
    message: 'Remove all custom API keys and revert to SaaS Credits?',
    confirmText: 'Remove',
    onConfirm: () => removeKeys()
  })
}

async function removeKeys() {
  if (!accountId.value) return
  saving.value = true
  try {
    await supabase.schema('threads').from('threads_accounts').update({
      custom_gemini_key: null, custom_groq_key: null
    }).eq('id', accountId.value)
    geminiKey.value = ''; groqKey.value = ''
    hasCustomKey.value = false; hasGroqKey.value = false
    showToast('Keys removed.', 'info')
  } catch (err: any) {
    showToast('Failed: ' + err.message, 'error')
  } finally {
    saving.value = false
  }
}

onMounted(load)
</script>
