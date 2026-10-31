<template>
  <div class="space-y-6">
    <Card>
      <template #header>
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-sm font-bold">AI & Billing</h2>
            <p class="text-xs theme-text-muted mt-0.5">Manage your plan and API keys.</p>
          </div>
          <Badge :variant="plan !== 'none' ? 'success' : 'danger'">
            {{ planName }}
          </Badge>
        </div>
      </template>

      <div v-if="loading" class="space-y-3">
        <div class="h-10 skeleton"></div>
        <div class="h-20 skeleton"></div>
      </div>

      <template v-else>
        <!-- PLAN STATUS -->
        <div class="p-4 rounded-xl border theme-border bg-[var(--bg-sec)] space-y-3 mb-6">
          <div class="flex justify-between items-center">
            <h3 class="text-sm font-bold">Current Plan</h3>
            <span v-if="planExpiresAt" class="text-xs theme-text-muted">Expires: {{ formatDate(planExpiresAt) }}</span>
          </div>
          
          <div class="flex items-center justify-between">
            <div>
              <div class="text-2xl font-black">{{ planName }}</div>
              <div v-if="plan === 'trial' || plan === 'paid_credit'" class="text-sm theme-text-muted mt-1">
                {{ creditBalance }} Credits Remaining
              </div>
              <div v-else-if="plan === 'paid_byok'" class="text-sm theme-text-muted mt-1">
                Unlimited (BYOK Active)
              </div>
            </div>
            <RouterLink to="/pricing" class="btn btn-primary btn-sm">Upgrade Plan</RouterLink>
          </div>
        </div>

        <!-- BYOK SECTION -->
        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <h3 class="text-sm font-bold">API Keys (BYOK)</h3>
            <Badge v-if="plan !== 'paid_byok'" variant="danger">Locked</Badge>
          </div>
          <p class="text-xs theme-text-muted">
            Gunakan API Key sendiri agar tidak memotong kredit. Fitur ini khusus untuk paket <strong>Pro BYOK</strong>.
          </p>
          
          <div v-if="plan !== 'paid_byok'" class="p-4 rounded-lg border border-red-500/20 bg-red-500/5 text-red-500 text-xs text-center">
            Fitur ini terkunci. Silakan upgrade ke Pro BYOK untuk mengaktifkan.
          </div>

          <div v-else class="space-y-4">
            <!-- GEMINI -->
            <div class="space-y-1">
              <label class="label">Gemini API Key</label>
              <div class="flex gap-2">
                <input v-model="geminiKey" type="password" placeholder="AIzaSy..." class="input flex-1" />
                <Button @click="saveKey('gemini')" :disabled="saving" :loading="saving">Save</Button>
              </div>
              <p class="text-[10px] theme-text-muted">Digunakan untuk Embedding RAG & Generate Text.</p>
            </div>
            <!-- GROQ -->
            <div class="space-y-1">
              <label class="label">Groq API Key</label>
              <div class="flex gap-2">
                <input v-model="groqKey" type="password" placeholder="gsk_..." class="input flex-1" />
                <Button @click="saveKey('groq')" :disabled="saving" :loading="saving">Save</Button>
              </div>
              <p class="text-[10px] theme-text-muted">Digunakan untuk Generate Text super cepat.</p>
            </div>
          </div>
        </div>
      </template>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { supabase } from '../../lib/supabase'
import { useNotify } from '../../composables/useNotify'
import { Card, Button, Badge } from '../../components/ui'

const { showToast } = useNotify()
const loading = ref(true)
const saving = ref(false)
const accountId = ref<string | null>(null)

const plan = ref('none')
const planExpiresAt = ref<string | null>(null)
const creditBalance = ref(0)
const geminiKey = ref('')
const groqKey = ref('')

const planName = computed(() => {
  if (plan.value === 'trial') return 'Trial'
  if (plan.value === 'paid_credit') return 'Pro Credit'
  if (plan.value === 'paid_byok') return 'Pro BYOK'
  return 'Free'
})

function formatDate(iso: string) {
  if (!iso) return ''
  return new Date(iso).toLocaleDateString('id-ID', { dateStyle: 'medium' })
}

async function load() {
  loading.value = true
  try {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) return

    const { data: account, error } = await supabase
      .schema('threads').from('threads_accounts')
      .select('id, plan, plan_expires_at, credit_balance, custom_gemini_key, custom_groq_key')
      .eq('user_id', user.id).maybeSingle()

    if (error) throw error

    if (account) {
      accountId.value = account.id
      plan.value = account.plan || 'none'
      planExpiresAt.value = account.plan_expires_at
      creditBalance.value = account.credit_balance || 0
      geminiKey.value = account.custom_gemini_key || ''
      groqKey.value = account.custom_groq_key || ''
    }
  } catch (err: any) {
    showToast('Failed to load settings: ' + err.message, 'error')
  } finally {
    loading.value = false
  }
}

async function saveKey(provider: 'gemini' | 'groq') {
  if (!accountId.value) return
  const keyToSave = provider === 'gemini' ? geminiKey.value.trim() : groqKey.value.trim()
  
  if (!keyToSave) {
    showToast('Key tidak boleh kosong', 'error')
    return
  }

  saving.value = true
  try {
    // Validasi API Key (Sederhana)
    const url = provider === 'gemini' 
      ? `https://generativelanguage.googleapis.com/v1beta/models?key=${keyToSave}`
      : 'https://api.groq.com/openai/v1/models'
    
    const headers: any = provider === 'groq' ? { 'Authorization': `Bearer ${keyToSave}` } : {}
    const res = await fetch(url, { headers })

    if (!res.ok) throw new Error('API Key tidak valid atau limit tercapai.')

    // Simpan ke DB
    const updateData = provider === 'gemini' 
      ? { custom_gemini_key: keyToSave }
      : { custom_groq_key: keyToSave }

    const { error } = await supabase
      .schema('threads').from('threads_accounts')
      .update(updateData)
      .eq('id', accountId.value)

    if (error) throw error
    showToast(`${provider.toUpperCase()} Key berhasil disimpan!`, 'success')
  } catch (err: any) {
    showToast('Gagal: ' + err.message, 'error')
  } finally {
    saving.value = false
  }
}

onMounted(load)
</script>
