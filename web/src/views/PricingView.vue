<template>
  <div class="max-w-4xl mx-auto p-6 space-y-8 theme-bg theme-text min-h-screen">
    <div class="text-center space-y-2">
      <h1 class="text-3xl font-bold">Pilih Paket Kamu</h1>
      <p class="theme-text-muted">Upgrade untuk lanjut pakai fitur AI Ixiera tanpa batas.</p>
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
        <button @click="requestUpgrade('Pro Credit (Rp 49.000)')" class="btn btn-primary w-full mt-6">
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
        <button @click="requestUpgrade('Pro BYOK (Rp 29.000)')" class="btn btn-primary w-full mt-6">
          Pilih Pro BYOK
        </button>
      </div>
    </div>

    <!-- CARA UPGRADE -->
    <div class="p-6 rounded-xl border theme-border bg-[var(--bg-sec)] text-center space-y-4">
      <div>
        <h3 class="text-sm font-bold">Bagaimana cara upgrade?</h3>
        <p class="text-xs theme-text-muted mt-1">
          Klik tombol paket di atas. Kamu akan diarahkan ke WhatsApp Admin dengan pesan otomatis. 
          Setelah pembayaran dikonfirmasi, Admin akan mengaktifkan paket kamu secara manual (maks. 1x24 jam).
        </p>
      </div>
      
      <div class="flex flex-wrap justify-center gap-4 pt-2">
        <a :href="getWaLink('Halo Admin, saya mau tanya-tanya dulu soal paket Ixiera.')" target="_blank" class="flex items-center gap-2 text-xs font-bold px-4 py-2 rounded-lg bg-[#25D366] text-white hover:opacity-90 transition">
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>
          WhatsApp
        </a>
        <a href="https://www.threads.net/@ixiera.id" target="_blank" class="flex items-center gap-2 text-xs font-bold px-4 py-2 rounded-lg border theme-border hover:bg-[var(--bg)] transition">
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.477 2 2 6.477 2 12c0 5.523 4.477 10 10 10s10-4.477 10-10c0-5.523-4.477-10-10-10zm0 17.5a7.5 7.5 0 110-15 7.5 7.5 0 010 15z"/></svg>
          Threads
        </a>
      </div>
    </div>

    <div class="text-center">
      <RouterLink to="/settings/ai" class="text-sm font-bold underline hover:theme-text-muted">Kembali ke Pengaturan</RouterLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { supabase } from '../lib/supabase'
import { useNotify } from '../composables/useNotify'

const { showToast } = useNotify()
const userEmail = ref('')

onMounted(async () => {
  const { data: { user } } = await supabase.auth.getUser()
  if (user?.email) userEmail.value = user.email
})

function getWaLink(message: string) {
  // Nomor WA Admin (Format Internasional tanpa +)
  const phone = '6285702373412'
  return `https://wa.me/${phone}?text=${encodeURIComponent(message)}`
}

function requestUpgrade(planName: string) {
  const message = `Halo Admin Ixiera,\n\nSaya ingin upgrade ke paket *${planName}*.\nEmail akun saya: ${userEmail.value}\n\nMohon info instruksi pembayaran (Transfer/QRIS). Terima kasih!`
  
  // Buka link WhatsApp
  window.open(getWaLink(message), '_blank')
  showToast('Membuka WhatsApp Admin...', 'info')
}
</script>
