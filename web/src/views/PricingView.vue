<template>
  <div class="max-w-4xl mx-auto p-6 space-y-8 theme-bg theme-text min-h-screen">
    <div class="text-center space-y-2">
      <h1 class="text-3xl font-bold">Pilih Paket Kamu</h1>
      <p class="theme-text-muted">Upgrade untuk lanjut pakai fitur AI Ixiera.</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- Plan 1: Pro Credit -->
      <div class="card p-6 border-2 theme-border space-y-4 flex flex-col justify-between">
        <div>
          <h2 class="text-xl font-bold">Pro Credit</h2>
          <p class="text-2xl font-black mt-2">Rp 49.000 <span class="text-sm font-normal theme-text-muted">/ bulan</span></p>
          <ul class="mt-4 space-y-2 text-sm theme-text-muted">
            <li class="flex items-center gap-2">✓ 100 Kredit AI per bulan</li>
            <li class="flex items-center gap-2">✓ Akses semua fitur AI (Generate, Reply, Repurpose)</li>
            <li class="flex items-center gap-2">✓ Tanpa perlu API Key sendiri</li>
          </ul>
        </div>
        <button @click="handleUpgrade('Pro Credit')" class="btn btn-primary w-full mt-6">Pilih Pro Credit</button>
      </div>

      <!-- Plan 2: Pro BYOK -->
      <div class="card p-6 border-2 border-black dark:border-white space-y-4 flex flex-col justify-between relative">
        <div class="absolute top-0 right-0 bg-black text-white dark:bg-white dark:text-black text-xs font-bold px-3 py-1 rounded-bl-lg">Paling Hemat</div>
        <div>
          <h2 class="text-xl font-bold">Pro BYOK</h2>
          <p class="text-2xl font-black mt-2">Rp 29.000 <span class="text-sm font-normal theme-text-muted">/ bulan</span></p>
          <ul class="mt-4 space-y-2 text-sm theme-text-muted">
            <li class="flex items-center gap-2">✓ Unlimited AI (pakai API Key sendiri)</li>
            <li class="flex items-center gap-2">✓ Support Gemini & Groq</li>
            <li class="flex items-center gap-2">✓ Biaya API ditanggung sendiri</li>
          </ul>
        </div>
        <button @click="handleUpgrade('Pro BYOK')" class="btn btn-primary w-full mt-6">Pilih Pro BYOK</button>
      </div>
    </div>

    <div class="p-4 rounded-xl border theme-border bg-[var(--bg-sec)] text-center space-y-2">
      <p class="text-sm font-bold">Cara Upgrade:</p>
      <p class="text-xs theme-text-muted">Klik tombol paket di atas, lalu hubungi Admin via WhatsApp/Email untuk instruksi pembayaran (Transfer/QRIS). Admin akan mengaktifkan paket kamu secara manual.</p>
      <p class="text-sm font-bold mt-2">contact@ixiera.id</p>
    </div>

    <div class="text-center">
      <RouterLink to="/settings/ai" class="text-sm font-bold underline">Kembali ke Pengaturan</RouterLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useNotify } from '../composables/useNotify'

const { showToast } = useNotify()

function handleUpgrade(planName: string) {
  showToast(`Silakan hubungi Admin untuk upgrade ke ${planName}`, 'info')
}
</script>
