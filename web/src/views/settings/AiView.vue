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
          <Badge v-if="hasCustomKey" variant="success">Unlimited (Own Key)</Badge>
          <Badge v-else :variant="credits > 0 ? 'success' : 'danger'">
            {{ credits }} Credits Left
          </Badge>
        </div>
      </template>

      <div v-if="loading" class="space-y-3">
        <div class="h-10 skeleton"></div>
        <div class="h-20 skeleton"></div>
      </div>

      <template v-else>
        <!-- SaaS Credits (Sembunyiin kalau pake custom key) -->
        <div v-if="!hasCustomKey" class="p-4 rounded-lg theme-bg-sec border theme-border space-y-2 mb-6">
          <h3 class="text-sm font-bold">SaaS AI Credits</h3>
          <p class="text-xs theme-text-muted">
            You have <strong>{{ credits }}</strong> credits left. 1 credit is used every time you generate a Content Plan.
            If you run out, you can either top up or use your own Gemini API Key below.
          </p>
          <Button size="sm" @click="showToast('Top up feature coming soon.', 'info')">Top Up Credits</Button>
        </div>

        <!-- BYOK -->
        <div class="space-y-3">
          <h3 class="text-sm font-bold">Bring Your Own Key (BYOK)</h3>
          <p class="text-xs theme-text-muted">
            Use your own Google Gemini API Key to generate unlimited content for free (you pay Google directly). 
            When a custom key is set, your SaaS credits will <strong>not</strong> be deducted.
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
        <div class="flex justify-end items-center gap-3">
          <button v-if="hasCustomKey" @click="removeKey" class="text-xs font-bold theme-text-muted hover:theme-text">Remove API Key</button>
          <Button @click="saveKey" :disabled="saving || !accountId" :loading="saving">
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

const { showToast } = useNotify()
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
  if (!accountId.value) return
  saving.value = true
  try {
    const keyToSave = customKey.value.trim() || null
    const { error } = await supabase
      .schema('threads')
      .from('threads_accounts')
      .update({ custom_gemini_key: keyToSave })
      .eq('id', accountId.value)

    if (error) throw error
    
    hasCustomKey.value = !!keyToSave
    showToast('API Key saved successfully.', 'success')
  } catch (err: any) {
    showToast('Failed to save API Key: ' + err.message, 'error')
  } finally {
    saving.value = false
  }
}

async function removeKey() {
  customKey.value = ''
  await saveKey()
}

onMounted(load)
</script>
