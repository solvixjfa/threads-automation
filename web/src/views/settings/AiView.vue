<template>
  <div class="space-y-6">
    <Card>
      <template #header>
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-sm font-bold">AI & Billing</h2>
            <p class="text-xs theme-text-muted mt-0.5">Manage your plan and API keys.</p>
          </div>
          <div class="flex items-center gap-2">
            <button @click="load" :disabled="loading" class="text-xs font-bold theme-text-muted hover:theme-text underline">
              Refresh
            </button>
            <Badge :variant="plan !== 'none' ? 'success' : 'danger'">
              {{ planName }}
            </Badge>
          </div>
        </div>
      </template>

      <div v-if="loading" class="space-y-3">
        <div class="h-10 skeleton"></div>
        <div class="h-20 skeleton"></div>
      </div>

      <template v-else>
        <!-- BANNER PENDING REQUEST -->
        <div v-if="pendingPlan" class="p-4 rounded-xl border border-amber-500/30 bg-amber-500/5 text-amber-600 dark:text-amber-400 space-y-2 mb-6">
          <p class="text-sm font-bold">Menunggu Konfirmasi Admin</p>
          <p class="text-xs">Kamu sudah request paket <b>{{ getPlanLabel(pendingPlan) }}</b>. Admin akan mengaktifkan setelah pembayaran.</p>
          <a :href="getWaLink('Halo Admin, saya sudah transfer untuk paket ' + getPlanLabel(pendingPlan) + '.')" target="_blank" class="inline-block bg-[#25D366] text-white text-xs font-bold px-3 py-1.5 rounded-md mt-1">
            Hubungi Admin (WA)
          </a>
        </div>

        <!-- PLAN STATUS -->
        <div class="p-4 rounded-xl border theme-border bg-[var(--bg-sec)] space-y-3 mb-6">
          <div class="flex justify-between items-center">
            <h3 class="text-sm font-bold">Current Plan</h3>
            <span v-if="planExpiresAt" class="text-xs theme-text-muted">Expires: {{ formatDate(planExpiresAt) }}</span>
          </div>
          
          <div class="flex items-center justify-between">
            <div>
              <div class="text-2xl font-black">{{ planName }}</div>
              
              <!-- LOGIKA TEGAS: PAID_BYOK = UNLIMITED, SELAIN ITU = KREDIT -->
              <div v-if="plan === 'paid_byok'" class="text-sm font-bold text-[var(--success)] mt-1">
                Unlimited (BYOK Active)
              </div>
              <div v-else class="text-sm theme-text-muted mt-1">
                {{ creditBalance }} Credits Remaining
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
          
          <!-- KALAU BUKAN PAID_BYOK, TAMPILIN PESAN TERKUNCI -->
          <div v-if="plan !== 'paid_byok'" class="p-4 rounded-lg border border-red-500/20 bg-red-500/5 text-red-500 text-xs text-center">
            Fitur ini terkunci. Upgrade ke <b>Pro BYOK</b> untuk menggunakan API Key sendiri.
          </div>

          <!-- KALAU PAID_BYOK, BARU MUNCULIN INPUT -->
          <div v-else class="space-y-4 pt-2">
            <p class="text-xs theme-text-muted mb-2">Gunakan API Key sendiri agar tidak memotong kredit.</p>
            
            <!-- GEMINI -->
            <div class="space-y-1">
              <label class="label">Gemini API Key</label>
              <div class="flex gap-2">
                <input v-model="geminiKey" type="password" placeholder="AIzaSy..." class="input flex-1" />
                <Button v-if="!hasGeminiKey" @click="saveKey('gemini')" :disabled="saving">Save</Button>
                <Button v-else variant="danger" @click="removeKey('gemini')">Remove</Button>
              </div>
            </div>
            <!-- GROQ -->
            <div class="space-y-1">
              <label class="label">Groq API Key</label>
              <div class="flex gap-2">
                <input v-model="groqKey" type="password" placeholder="gsk_..." class="input flex-1" />
                <Button v-if="!hasGroqKey" @click="saveKey('groq')" :disabled="saving">Save</Button>
                <Button v-else variant="danger" @click="removeKey('groq')">Remove</Button>
              </div>
            </div>
          </div>
        </div>
      </template>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { supabase } from '../../lib/supabase'
import { useNotify } from '../../composables/useNotify'
import { Card, Button, Badge } from '../../components/ui'

const { showToast } = useNotify()
const loading = ref(true)
const saving = ref(false)
const accountId = ref<string | null>(null)
let pollInterval: any = null

const plan = ref('none')
const pendingPlan = ref<string | null>(null)
const planExpiresAt = ref<string | null>(null)
const creditBalance = ref(0)
const geminiKey = ref('')
const groqKey = ref('')
const hasGeminiKey = ref(false)
const hasGroqKey = ref(false)

const planName = computed(() => getPlanLabel(plan.value))

function getPlanLabel(p: string) {
  if (p === 'trial') return 'Trial'
  if (p === 'paid_credit') return 'Pro Credit'
  if (p === 'paid_byok') return 'Pro BYOK'
  return 'Free'
}

function formatDate(iso: string) {
  if (!iso) return ''
  return new Date(iso).toLocaleDateString('id-ID', { dateStyle: 'medium' })
}

function getWaLink(msg: string) {
  return `https://wa.me/6285702373412?text=${encodeURIComponent(msg)}`
}

async function load(isSilent = false) {
  if (!isSilent) loading.value = true
  try {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) return

    const { data: account, error } = await supabase
      .schema('threads').from('threads_accounts')
      .select('id, plan, pending_plan, plan_expires_at, credit_balance, custom_gemini_key, custom_groq_key')
      .eq('user_id', user.id).maybeSingle()

    if (error) throw error

    if (account) {
      const oldPlan = plan.value
      accountId.value = account.id
      plan.value = account.plan || 'none'
      pendingPlan.value = account.pending_plan
      planExpiresAt.value = account.plan_expires_at
      creditBalance.value = account.credit_balance || 0
      
      // Cek keberadaan key
      hasGeminiKey.value = !!account.custom_gemini_key
      hasGroqKey.value = !!account.custom_groq_key
      
      // Jangan timpa input kalau user lagi ngetik
      if (!isSilent) {
        geminiKey.value = account.custom_gemini_key ? '********' : ''
        groqKey.value = account.custom_groq_key ? '********' : ''
      }

      // Notifikasi kalau plan berubah jadi paid
      if (isSilent && oldPlan !== plan.value && (plan.value === 'paid_credit' || plan.value === 'paid_byok')) {
        showToast('Upgrade Berhasil! Paket kamu sudah aktif.', 'success')
        // Stop polling kalau udah sukses upgrade
        if (pollInterval) clearInterval(pollInterval)
      }
    }
  } catch (err: any) {
    if (!isSilent) showToast('Failed to load: ' + err.message, 'error')
  } finally {
    if (!isSilent) loading.value = false
  }
}

async function saveKey(provider: 'gemini' | 'groq') {
  if (!accountId.value) return
  const keyToSave = provider === 'gemini' ? geminiKey.value.trim() : groqKey.value.trim()
  
  if (!keyToSave || keyToSave === '********') { 
    showToast('Masukkan API Key baru', 'error'); 
    return 
  }

  saving.value = true
  try {
    const url = provider === 'gemini' 
      ? `https://generativelanguage.googleapis.com/v1beta/models?key=${keyToSave}`
      : 'https://api.groq.com/openai/v1/models'
    const headers: any = provider === 'groq' ? { 'Authorization': `Bearer ${keyToSave}` } : {}
    const res = await fetch(url, { headers })
    if (!res.ok) throw new Error('API Key tidak valid atau limit tercapai.')

    const updateData = provider === 'gemini' ? { custom_gemini_key: keyToSave } : { custom_groq_key: keyToSave }
    const { error } = await supabase.schema('threads').from('threads_accounts').update(updateData).eq('id', accountId.value)
    if (error) throw error
    
    showToast(`${provider.toUpperCase()} Key berhasil disimpan!`, 'success')
    if (provider === 'gemini') { hasGeminiKey.value = true; geminiKey.value = '********'; }
    if (provider === 'groq') { hasGroqKey.value = true; groqKey.value = '********'; }
    
  } catch (err: any) {
    showToast('Gagal: ' + err.message, 'error')
  } finally {
    saving.value = false
  }
}

async function removeKey(provider: 'gemini' | 'groq') {
  if (!accountId.value) return
  saving.value = true
  try {
    const updateData = provider === 'gemini' ? { custom_gemini_key: null } : { custom_groq_key: null }
    const { error } = await supabase.schema('threads').from('threads_accounts').update(updateData).eq('id', accountId.value)
    if (error) throw error
    showToast(`${provider.toUpperCase()} Key dihapus.`, 'info')
    if (provider === 'gemini') { hasGeminiKey.value = false; geminiKey.value = ''; }
    if (provider === 'groq') { hasGroqKey.value = false; groqKey.value = ''; }
  } catch (err: any) {
    showToast('Gagal hapus: ' + err.message, 'error')
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  load()
  // Polling 60 detik. Kalau udah Pro, gak perlu polling lagi.
  pollInterval = setInterval(() => {
    if (plan.value !== 'paid_credit' && plan.value !== 'paid_byok') {
      load(true)
    }
  }, 60000)
})

onUnmounted(() => {
  if (pollInterval) clearInterval(pollInterval)
})
</script>
EOEF
cd ~/threads-automation
cat > web/src/views/settings/AiView.vue << 'EOF'
<template>
  <div class="space-y-6">
    <Card>
      <template #header>
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-sm font-bold">AI & Billing</h2>
            <p class="text-xs theme-text-muted mt-0.5">Manage your plan and API keys.</p>
          </div>
          <div class="flex items-center gap-2">
            <button @click="load" :disabled="loading" class="text-xs font-bold theme-text-muted hover:theme-text underline">
              Refresh
            </button>
            <Badge :variant="plan !== 'none' ? 'success' : 'danger'">
              {{ planName }}
            </Badge>
          </div>
        </div>
      </template>

      <div v-if="loading" class="space-y-3">
        <div class="h-10 skeleton"></div>
        <div class="h-20 skeleton"></div>
      </div>

      <template v-else>
        <!-- BANNER PENDING REQUEST -->
        <div v-if="pendingPlan" class="p-4 rounded-xl border border-amber-500/30 bg-amber-500/5 text-amber-600 dark:text-amber-400 space-y-2 mb-6">
          <p class="text-sm font-bold">Menunggu Konfirmasi Admin</p>
          <p class="text-xs">Kamu sudah request paket <b>{{ getPlanLabel(pendingPlan) }}</b>. Admin akan mengaktifkan setelah pembayaran.</p>
          <a :href="getWaLink('Halo Admin, saya sudah transfer untuk paket ' + getPlanLabel(pendingPlan) + '.')" target="_blank" class="inline-block bg-[#25D366] text-white text-xs font-bold px-3 py-1.5 rounded-md mt-1">
            Hubungi Admin (WA)
          </a>
        </div>

        <!-- PLAN STATUS -->
        <div class="p-4 rounded-xl border theme-border bg-[var(--bg-sec)] space-y-3 mb-6">
          <div class="flex justify-between items-center">
            <h3 class="text-sm font-bold">Current Plan</h3>
            <span v-if="planExpiresAt" class="text-xs theme-text-muted">Expires: {{ formatDate(planExpiresAt) }}</span>
          </div>
          
          <div class="flex items-center justify-between">
            <div>
              <div class="text-2xl font-black">{{ planName }}</div>
              
              <!-- LOGIKA TEGAS: PAID_BYOK = UNLIMITED, SELAIN ITU = KREDIT -->
              <div v-if="plan === 'paid_byok'" class="text-sm font-bold text-[var(--success)] mt-1">
                Unlimited (BYOK Active)
              </div>
              <div v-else class="text-sm theme-text-muted mt-1">
                {{ creditBalance }} Credits Remaining
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
          
          <!-- KALAU BUKAN PAID_BYOK, TAMPILIN PESAN TERKUNCI -->
          <div v-if="plan !== 'paid_byok'" class="p-4 rounded-lg border border-red-500/20 bg-red-500/5 text-red-500 text-xs text-center">
            Fitur ini terkunci. Upgrade ke <b>Pro BYOK</b> untuk menggunakan API Key sendiri.
          </div>

          <!-- KALAU PAID_BYOK, BARU MUNCULIN INPUT -->
          <div v-else class="space-y-4 pt-2">
            <p class="text-xs theme-text-muted mb-2">Gunakan API Key sendiri agar tidak memotong kredit.</p>
            
            <!-- GEMINI -->
            <div class="space-y-1">
              <label class="label">Gemini API Key</label>
              <div class="flex gap-2">
                <input v-model="geminiKey" type="password" placeholder="AIzaSy..." class="input flex-1" />
                <Button v-if="!hasGeminiKey" @click="saveKey('gemini')" :disabled="saving">Save</Button>
                <Button v-else variant="danger" @click="removeKey('gemini')">Remove</Button>
              </div>
            </div>
            <!-- GROQ -->
            <div class="space-y-1">
              <label class="label">Groq API Key</label>
              <div class="flex gap-2">
                <input v-model="groqKey" type="password" placeholder="gsk_..." class="input flex-1" />
                <Button v-if="!hasGroqKey" @click="saveKey('groq')" :disabled="saving">Save</Button>
                <Button v-else variant="danger" @click="removeKey('groq')">Remove</Button>
              </div>
            </div>
          </div>
        </div>
      </template>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { supabase } from '../../lib/supabase'
import { useNotify } from '../../composables/useNotify'
import { Card, Button, Badge } from '../../components/ui'

const { showToast } = useNotify()
const loading = ref(true)
const saving = ref(false)
const accountId = ref<string | null>(null)
let pollInterval: any = null

const plan = ref('none')
const pendingPlan = ref<string | null>(null)
const planExpiresAt = ref<string | null>(null)
const creditBalance = ref(0)
const geminiKey = ref('')
const groqKey = ref('')
const hasGeminiKey = ref(false)
const hasGroqKey = ref(false)

const planName = computed(() => getPlanLabel(plan.value))

function getPlanLabel(p: string) {
  if (p === 'trial') return 'Trial'
  if (p === 'paid_credit') return 'Pro Credit'
  if (p === 'paid_byok') return 'Pro BYOK'
  return 'Free'
}

function formatDate(iso: string) {
  if (!iso) return ''
  return new Date(iso).toLocaleDateString('id-ID', { dateStyle: 'medium' })
}

function getWaLink(msg: string) {
  return `https://wa.me/6285702373412?text=${encodeURIComponent(msg)}`
}

async function load(isSilent = false) {
  if (!isSilent) loading.value = true
  try {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) return

    const { data: account, error } = await supabase
      .schema('threads').from('threads_accounts')
      .select('id, plan, pending_plan, plan_expires_at, credit_balance, custom_gemini_key, custom_groq_key')
      .eq('user_id', user.id).maybeSingle()

    if (error) throw error

    if (account) {
      const oldPlan = plan.value
      accountId.value = account.id
      plan.value = account.plan || 'none'
      pendingPlan.value = account.pending_plan
      planExpiresAt.value = account.plan_expires_at
      creditBalance.value = account.credit_balance || 0
      
      // Cek keberadaan key
      hasGeminiKey.value = !!account.custom_gemini_key
      hasGroqKey.value = !!account.custom_groq_key
      
      // Jangan timpa input kalau user lagi ngetik
      if (!isSilent) {
        geminiKey.value = account.custom_gemini_key ? '********' : ''
        groqKey.value = account.custom_groq_key ? '********' : ''
      }

      // Notifikasi kalau plan berubah jadi paid
      if (isSilent && oldPlan !== plan.value && (plan.value === 'paid_credit' || plan.value === 'paid_byok')) {
        showToast('Upgrade Berhasil! Paket kamu sudah aktif.', 'success')
        // Stop polling kalau udah sukses upgrade
        if (pollInterval) clearInterval(pollInterval)
      }
    }
  } catch (err: any) {
    if (!isSilent) showToast('Failed to load: ' + err.message, 'error')
  } finally {
    if (!isSilent) loading.value = false
  }
}

async function saveKey(provider: 'gemini' | 'groq') {
  if (!accountId.value) return
  const keyToSave = provider === 'gemini' ? geminiKey.value.trim() : groqKey.value.trim()
  
  if (!keyToSave || keyToSave === '********') { 
    showToast('Masukkan API Key baru', 'error'); 
    return 
  }

  saving.value = true
  try {
    const url = provider === 'gemini' 
      ? `https://generativelanguage.googleapis.com/v1beta/models?key=${keyToSave}`
      : 'https://api.groq.com/openai/v1/models'
    const headers: any = provider === 'groq' ? { 'Authorization': `Bearer ${keyToSave}` } : {}
    const res = await fetch(url, { headers })
    if (!res.ok) throw new Error('API Key tidak valid atau limit tercapai.')

    const updateData = provider === 'gemini' ? { custom_gemini_key: keyToSave } : { custom_groq_key: keyToSave }
    const { error } = await supabase.schema('threads').from('threads_accounts').update(updateData).eq('id', accountId.value)
    if (error) throw error
    
    showToast(`${provider.toUpperCase()} Key berhasil disimpan!`, 'success')
    if (provider === 'gemini') { hasGeminiKey.value = true; geminiKey.value = '********'; }
    if (provider === 'groq') { hasGroqKey.value = true; groqKey.value = '********'; }
    
  } catch (err: any) {
    showToast('Gagal: ' + err.message, 'error')
  } finally {
    saving.value = false
  }
}

async function removeKey(provider: 'gemini' | 'groq') {
  if (!accountId.value) return
  saving.value = true
  try {
    const updateData = provider === 'gemini' ? { custom_gemini_key: null } : { custom_groq_key: null }
    const { error } = await supabase.schema('threads').from('threads_accounts').update(updateData).eq('id', accountId.value)
    if (error) throw error
    showToast(`${provider.toUpperCase()} Key dihapus.`, 'info')
    if (provider === 'gemini') { hasGeminiKey.value = false; geminiKey.value = ''; }
    if (provider === 'groq') { hasGroqKey.value = false; groqKey.value = ''; }
  } catch (err: any) {
    showToast('Gagal hapus: ' + err.message, 'error')
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  load()
  // Polling 60 detik. Kalau udah Pro, gak perlu polling lagi.
  pollInterval = setInterval(() => {
    if (plan.value !== 'paid_credit' && plan.value !== 'paid_byok') {
      load(true)
    }
  }, 60000)
})

onUnmounted(() => {
  if (pollInterval) clearInterval(pollInterval)
})
</script>
