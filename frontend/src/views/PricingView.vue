<template>
  <div class="max-w-4xl mx-auto p-6 space-y-8 theme-bg theme-text min-h-screen">
    <div class="text-center space-y-2">
      <h1 class="text-3xl font-bold">Pilih Paket Kamu</h1>
      <p class="theme-text-muted">Upgrade instan untuk lanjut pakai fitur AI Ixiera tanpa batas.</p>
    </div>

    <div v-if="loading" class="text-center py-10 theme-text-muted animate-pulse">Memuat status...</div>

    <template v-else>
      <div v-if="paymentSuccess" class="p-4 rounded-xl border-2 border-emerald-500 bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 text-center space-y-1">
        <p class="font-bold">Pembayaran Diterima!</p>
        <p class="text-sm">Paket akun kamu otomatis diperbarui setelah konfirmasi pembayaran selesai.</p>
      </div>

      <div v-if="currentPlan && currentPlan !== 'free' && currentPlan !== 'none'" class="p-4 rounded-xl border border-emerald-500/40 bg-emerald-500/5 text-center">
        <p class="text-sm">Paket aktif saat ini: <b class="uppercase">{{ currentPlan.replace('paid_', 'Pro ') }}</b></p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Plan 1: Pro Credit -->
        <div class="card p-6 border-2 theme-border space-y-4 flex flex-col justify-between">
          <div>
            <h2 class="text-xl font-bold">Pro Credit</h2>
            <p class="text-2xl font-black mt-2">Rp 29.000 <span class="text-sm font-normal theme-text-muted">/ bulan</span></p>
            <ul class="mt-4 space-y-2 text-sm theme-text-muted">
              <li class="flex items-center gap-2">✓ 100 Kredit AI per bulan</li>
              <li class="flex items-center gap-2">✓ Akses semua fitur AI</li>
              <li class="flex items-center gap-2">✓ Tanpa perlu API Key sendiri</li>
            </ul>
          </div>
          <button @click="checkoutPlan('paid_credit')" :disabled="isProcessing" class="btn btn-primary w-full mt-6">
            {{ isProcessing && selectedPlan === 'paid_credit' ? 'Memproses...' : 'Bayar Sekarang (Pro Credit)' }}
          </button>
        </div>

        <!-- Plan 2: Pro BYOK -->
        <div class="card p-6 border-2 border-black dark:border-white space-y-4 flex flex-col justify-between relative">
          <div class="absolute top-0 right-0 bg-black text-white dark:bg-white dark:text-black text-[10px] font-bold px-3 py-1 rounded-bl-lg uppercase tracking-wider">Paling Hemat</div>
          <div>
            <h2 class="text-xl font-bold">Pro BYOK</h2>
            <p class="text-2xl font-black mt-2">Rp 19.000 <span class="text-sm font-normal theme-text-muted">/ bulan</span></p>
            <ul class="mt-4 space-y-2 text-sm theme-text-muted">
              <li class="flex items-center gap-2">✓ Unlimited AI (pakai API Key sendiri)</li>
              <li class="flex items-center gap-2">✓ Support Gemini & Groq</li>
              <li class="flex items-center gap-2">✓ Biaya API ditanggung sendiri</li>
            </ul>
          </div>
          <button @click="checkoutPlan('paid_byok')" :disabled="isProcessing" class="btn btn-primary w-full mt-6">
            {{ isProcessing && selectedPlan === 'paid_byok' ? 'Memproses...' : 'Bayar Sekarang (Pro BYOK)' }}
          </button>
        </div>
      </div>

      <p class="text-xs text-center theme-text-muted mt-6 italic">Pembayaran aman & otomatis diproses via Duitku Payment Gateway.</p>
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

const route = useRoute()
const { showToast } = useNotify()
const loading = ref(true)
const isProcessing = ref(false)
const selectedPlan = ref<string | null>(null)
const currentPlan = ref<string>('free')
const paymentSuccess = ref(false)

const API_BASE = (import.meta.env.VITE_API_URL || 'https://api.ixiera.online').replace(/\/$/, '')

onMounted(async () => {
  try {
    if (route.query.payment === 'success') {
      paymentSuccess.value = true
    }

    const { data: { user } } = await supabase.auth.getUser()
    if (!user) return

    const { data: acc } = await supabase.schema('threads').from('threads_accounts')
      .select('plan').eq('user_id', user.id).maybeSingle()

    if (acc?.plan && acc.plan !== 'none') {
      currentPlan.value = acc.plan
    } else {
      const { data: prof } = await supabase.schema('threads').from('profiles')
        .select('plan').eq('id', user.id).maybeSingle()
      if (prof?.plan) currentPlan.value = prof.plan
    }
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
