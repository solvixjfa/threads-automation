<template>
  <div class="max-w-4xl mx-auto p-6 space-y-8 theme-bg theme-text min-h-screen">
    <div class="text-center space-y-2">
      <h1 class="text-3xl font-bold">Pilih Paket Kamu</h1>
      <p class="theme-text-muted">Upgrade untuk lanjut pakai fitur AI Ixiera tanpa batas.</p>
    </div>

    <div v-if="loading" class="text-center py-10 theme-text-muted animate-pulse">Memuat status...</div>
    
    <template v-else>
      <!-- BANNER PENDING REQUEST -->
      <div v-if="pendingPlan" class="p-4 rounded-xl border-2 border-amber-500 bg-amber-500/10 text-amber-600 dark:text-amber-400 text-center space-y-2">
        <p class="font-bold">Permintaan Upgrade Sedang Diproses</p>
        <p class="text-sm">Kamu mengajukan paket <b>{{ getPlanName(pendingPlan) }}</b>. Silakan selesaikan pembayaran ke Admin via WhatsApp agar akun kamu segera diaktifkan.</p>
        <a :href="getWaLink('Halo Admin, saya sudah request paket ' + getPlanName(pendingPlan) + '. Mohon info pembayarannya.')" target="_blank" class="inline-block bg-[#25D366] text-white text-xs font-bold px-4 py-2 rounded-lg mt-2">
          Hubungi Admin (WhatsApp)
        </a>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6" :class="{'opacity-50 pointer-events-none': pendingPlan}">
        <!-- Plan 1: Pro Credit -->
        <div class="card p-6 border-2 theme-border space-y-4 flex flex-col justify-between">
          <div>
            <h2 class="text-xl font-bold">Pro Credit</h2>
            <p class="text-2xl font-black mt-2">Rp 49.000 <span class="text-sm font-normal theme-text-muted">/ bulan</span></p>
            <ul class="mt-4 space-y-2 text-sm theme-text-muted">
              <li class="flex items-center gap-2">✓ 100 Kredit AI per bulan</li>
              <li class="flex items-center gap-2">✓ Akses semua fitur AI</li>
              <li class="flex items-center gap-2">✓ Tanpa perlu API Key sendiri</li>
            </ul>
          </div>
          <button @click="requestPlan('paid_credit', 'Pro Credit')" :disabled="isProcessing" class="btn btn-primary w-full mt-6">
            Pilih Pro Credit
          </button>
        </div>

        <!-- Plan 2: Pro BYOK -->
        <div class="card p-6 border-2 border-black dark:border-white space-y-4 flex flex-col justify-between relative">
          <div class="absolute top-0 right-0 bg-black text-white dark:bg-white dark:text-black text-[10px] font-bold px-3 py-1 rounded-bl-lg uppercase tracking-wider">Paling Hemat</div>
          <div>
            <h2 class="text-xl font-bold">Pro BYOK</h2>
            <p class="text-2xl font-black mt-2">Rp 29.000 <span class="text-sm font-normal theme-text-muted">/ bulan</span></p>
            <ul class="mt-4 space-y-2 text-sm theme-text-muted">
              <li class="flex items-center gap-2">✓ Unlimited AI (pakai API Key sendiri)</li>
              <li class="flex items-center gap-2">✓ Support Gemini & Groq</li>
              <li class="flex items-center gap-2">✓ Biaya API ditanggung sendiri</li>
            </ul>
          </div>
          <button @click="requestPlan('paid_byok', 'Pro BYOK')" :disabled="isProcessing" class="btn btn-primary w-full mt-6">
            Pilih Pro BYOK
          </button>
        </div>
      </div>
    </template>

    <div class="text-center pt-6">
      <RouterLink to="/settings/ai" class="text-sm font-bold underline hover:theme-text-muted">Kembali ke Pengaturan</RouterLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { supabase } from '../lib/supabase'
import { useNotify } from '../composables/useNotify'

const { showToast } = useNotify()
const loading = ref(true)
const isProcessing = ref(false)
const accountId = ref<string | null>(null)
const userEmail = ref('')
const pendingPlan = ref<string | null>(null)

onMounted(async () => {
  try {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) return
    userEmail.value = user.email || ''

    const { data: acc } = await supabase.schema('threads').from('threads_accounts')
      .select('id, pending_plan').eq('user_id', user.id).maybeSingle()
    
    if (acc) {
      accountId.value = acc.id
      pendingPlan.value = acc.pending_plan
    }
  } finally {
    loading.value = false
  }
})

function getPlanName(plan: string) {
  return plan === 'paid_credit' ? 'Pro Credit (Rp 49.000)' : 'Pro BYOK (Rp 29.000)'
}

function getWaLink(message: string) {
  const phone = '6285702373412'
  return `https://wa.me/${phone}?text=${encodeURIComponent(message)}`
}

async function requestPlan(planType: string, planName: string) {
  if (!accountId.value) return
  isProcessing.value = true
  try {
    // 1. Simpan request ke DB
    const { error } = await supabase.schema('threads').from('threads_accounts')
      .update({ pending_plan: planType }).eq('id', accountId.value)
    
    if (error) throw error

    // 2. Update UI state
    pendingPlan.value = planType

    // 3. Buka WhatsApp
    const message = `Halo Admin Ixiera,\n\nSaya ingin upgrade ke paket *${planName}*.\nEmail akun saya: ${userEmail.value}\n\nMohon info instruksi pembayaran (Transfer/QRIS). Terima kasih!`
    window.open(getWaLink(message), '_blank')
    showToast('Permintaan tersimpan. Lanjutkan pembayaran via WhatsApp.', 'success')

  } catch (err: any) {
    showToast('Gagal memproses permintaan: ' + err.message, 'error')
  } finally {
    isProcessing.value = false
  }
}
</script>
