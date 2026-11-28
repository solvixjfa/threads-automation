<template>
  <div class="max-w-6xl mx-auto p-6 space-y-8 theme-bg theme-text min-h-screen">
    <div class="text-center space-y-2">
      <h1 class="text-3xl font-bold">Pilih Paket Kamu</h1>
      <p class="theme-text-muted">1 Credit = 1 Token AI. Pilih kapasitas kredit dan jumlah akun sesuai kebutuhanmu.</p>
    </div>

    <div v-if="loading" class="text-center py-10 theme-text-muted animate-pulse">Memuat status...</div>

    <template v-else>
      <div v-if="paymentSuccess" class="p-4 rounded-xl border-2 border-emerald-500 bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 text-center space-y-1">
        <p class="font-bold">Pembayaran Diterima!</p>
        <p class="text-sm">Paket akun kamu otomatis diperbarui setelah konfirmasi pembayaran selesai.</p>
      </div>

      <div v-if="currentPlan && currentPlan !== 'free' && currentPlan !== 'none'" class="p-4 rounded-xl border border-emerald-500/40 bg-emerald-500/5 text-center">
        <p class="text-sm">Paket aktif saat ini: <b class="uppercase">{{ formatPlanDisplay(currentPlan) }}</b></p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        <!-- 1. Starter -->
        <div class="card p-6 border-2 theme-border space-y-4 flex flex-col justify-between">
          <div>
            <h2 class="text-xl font-bold">Starter</h2>
            <p class="text-2xl font-black mt-2">Rp 59.000 <span class="text-xs font-normal theme-text-muted">/ bulan</span></p>
            <ul class="mt-4 space-y-2 text-sm theme-text-muted">
              <li class="flex items-center gap-2">✓ <b>100.000</b> Credits AI / bulan</li>
              <li class="flex items-center gap-2">✓ Maksimal <b>2 Akun</b> Threads</li>
              <li class="flex items-center gap-2">✓ Semua fitur AI & Analytics</li>
              <li class="flex items-center gap-2">✓ Tanpa perlu API Key sendiri</li>
            </ul>
          </div>
          <button @click="checkoutPlan('starter')" :disabled="isProcessing" class="btn btn-primary w-full mt-6">
            {{ isProcessing && selectedPlan === 'starter' ? 'Memproses...' : 'Pilih Starter' }}
          </button>
        </div>

        <!-- 2. Pro (Most Popular) -->
        <div class="card p-6 border-2 border-black dark:border-white space-y-4 flex flex-col justify-between relative shadow-lg">
          <div class="absolute top-0 right-0 bg-black text-white dark:bg-white dark:text-black text-[10px] font-bold px-3 py-1 rounded-bl-lg uppercase tracking-wider">Paling Populer</div>
          <div>
            <h2 class="text-xl font-bold">Pro</h2>
            <p class="text-2xl font-black mt-2">Rp 99.000 <span class="text-xs font-normal theme-text-muted">/ bulan</span></p>
            <ul class="mt-4 space-y-2 text-sm theme-text-muted">
              <li class="flex items-center gap-2">✓ <b>300.000</b> Credits AI / bulan</li>
              <li class="flex items-center gap-2">✓ Maksimal <b>5 Akun</b> Threads</li>
              <li class="flex items-center gap-2">✓ Semua fitur AI & Analytics</li>
              <li class="flex items-center gap-2">✓ Tanpa perlu API Key sendiri</li>
            </ul>
          </div>
          <button @click="checkoutPlan('pro')" :disabled="isProcessing" class="btn btn-primary w-full mt-6">
            {{ isProcessing && selectedPlan === 'pro' ? 'Memproses...' : 'Pilih Pro' }}
          </button>
        </div>

        <!-- 3. Business -->
        <div class="card p-6 border-2 theme-border space-y-4 flex flex-col justify-between">
          <div>
            <h2 class="text-xl font-bold">Business</h2>
            <p class="text-2xl font-black mt-2">Rp 179.000 <span class="text-xs font-normal theme-text-muted">/ bulan</span></p>
            <ul class="mt-4 space-y-2 text-sm theme-text-muted">
              <li class="flex items-center gap-2">✓ <b>750.000</b> Credits AI / bulan</li>
              <li class="flex items-center gap-2">✓ Maksimal <b>20 Akun</b> Threads</li>
              <li class="flex items-center gap-2">✓ Semua fitur AI & Analytics</li>
              <li class="flex items-center gap-2">✓ Tanpa perlu API Key sendiri</li>
            </ul>
          </div>
          <button @click="checkoutPlan('business')" :disabled="isProcessing" class="btn btn-primary w-full mt-6">
            {{ isProcessing && selectedPlan === 'business' ? 'Memproses...' : 'Pilih Business' }}
          </button>
        </div>

        <!-- 4. Agency (BYOK) -->
        <div class="card p-6 border-2 theme-border space-y-4 flex flex-col justify-between relative">
          <div class="absolute top-0 right-0 bg-emerald-600 text-white text-[10px] font-bold px-3 py-1 rounded-bl-lg uppercase tracking-wider">Unlimited BYOK</div>
          <div>
            <h2 class="text-xl font-bold">Agency (BYOK)</h2>
            <p class="text-2xl font-black mt-2">Rp 249.000 <span class="text-xs font-normal theme-text-muted">/ bulan</span></p>
            <ul class="mt-4 space-y-2 text-sm theme-text-muted">
              <li class="flex items-center gap-2">✓ <b>Unlimited</b> AI (API Key sendiri)</li>
              <li class="flex items-center gap-2">✓ Maksimal <b>50 Akun</b> Threads</li>
              <li class="flex items-center gap-2">✓ Support Gemini & Groq</li>
              <li class="flex items-center gap-2">✓ Biaya token ditanggung sendiri</li>
            </ul>
          </div>
          <button @click="checkoutPlan('agency')" :disabled="isProcessing" class="btn btn-primary w-full mt-6">
            {{ isProcessing && selectedPlan === 'agency' ? 'Memproses...' : 'Pilih Agency' }}
          </button>
        </div>
      </div>

      <p class="text-xs text-center theme-text-muted mt-6 italic">Pembayaran aman & otomatis diproses via Duitku Payment Gateway. Perpanjangan sebelum masa aktif habis akan mengakumulasi sisa kredit kamu.</p>
    </template>

    <div class="text-center pt-6">
      <RouterLink to="/profile/ai" class="text-sm font-bold underline hover:theme-text-muted">Kembali ke Pengaturan</RouterLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { supabase } from '../lib/supabase'
import { useNotify } from '../composables/useNotify'
import { useAccountStore } from '../stores/accounts'

const accountStore = useAccountStore()
const route = useRoute()
const { showToast } = useNotify()
const loading = ref(true)
const isProcessing = ref(false)
const selectedPlan = ref<string | null>(null)
const currentPlan = ref<string>('free')
const paymentSuccess = ref(false)

const API_BASE = (import.meta.env.VITE_API_URL || 'https://api.ixiera.online').replace(/\/$/, '')

function formatPlanDisplay(p: string) {
  const map: Record<string, string> = {
    starter: 'Starter',
    pro: 'Pro',
    business: 'Business',
    agency: 'Agency (BYOK)',
    paid_credit: 'Pro Credit (Beta)',
    paid_byok: 'Pro BYOK (Beta)',
    trial: 'Free Trial',
  }
  return map[p] || p
}

onMounted(async () => {
  try {
    if (route.query.payment === 'success') {
      paymentSuccess.value = true
    }
    await accountStore.fetchAccounts()
    currentPlan.value = accountStore.effectivePlan || 'free'
  } finally {
    loading.value = false
  }
})

async function checkoutPlan(planType: string) {
  isProcessing.value = true
  selectedPlan.value = planType
  try {
    const { data: { session } } = await supabase.auth.getSession()
    if (!session?.access_token) {
      throw new Error('Silakan login ulang terlebih dahulu')
    }

    const res = await fetch(`${API_BASE}/api/v1/payment/create-invoice`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${session.access_token}`
      },
      body: JSON.stringify({ plan_type: planType })
    })

    const data = await res.json()
    if (!res.ok) throw new Error(data.detail || 'Gagal membuat invoice')
    if (!data.paymentUrl) throw new Error('URL pembayaran tidak tersedia')

    window.location.href = data.paymentUrl
  } catch (err: any) {
    showToast('Gagal memulai pembayaran: ' + err.message, 'error')
  } finally {
    isProcessing.value = false
    selectedPlan.value = null
  }
}
</script>
