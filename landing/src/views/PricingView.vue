<template>
  <div class="min-h-screen">

    <!-- DESKTOP SIDEBAR (SAMA SEPERTI LANDING) -->
    <aside class="hidden md:flex flex-col fixed top-0 left-0 h-screen w-60 z-50 bg-[var(--bg-primary)] border-r border-[var(--border)]">
      <div class="h-16 px-5 flex items-center border-b border-[var(--border)]">
        <a href="/" class="flex items-center gap-2">
          <div class="w-8 h-8 flex items-center justify-center rounded-md text-sm font-bold bg-[var(--accent)] text-[var(--accent-text)]">IX</div>
          <span class="ml-2 font-bold text-xl text-[var(--text-primary)]" style="letter-spacing: -0.03em;">Ixiera</span>
        </a>
      </div>

      <nav class="flex-1 p-3 space-y-1 overflow-y-auto">
        <a href="/#fitur" class="nav-bd">Fitur</a>
        <a href="/#contoh" class="nav-bd">Contoh Data</a>
        <a href="/#cara-kerja" class="nav-bd">Cara Kerja</a>
        <a href="/pricing" class="nav-bd" style="color: var(--text-primary); background: var(--bg-hover);">Harga</a>
        <a href="/#faq" class="nav-bd">FAQ</a>
      </nav>

      <div class="p-3 border-t border-[var(--border)] space-y-2">
        <div class="flex items-center gap-2">
          <button @click="toggleTheme" class="flex-1 flex items-center justify-center py-2 rounded-md border border-[var(--border)] text-[var(--text-muted)] hover:bg-[var(--bg-hover)] hover:text-[var(--text-primary)] transition">
            <Sun v-if="theme === 'dark'" class="w-4 h-4" />
            <Moon v-else class="w-4 h-4" />
          </button>
          <button @click="toggleLang" class="px-3 py-2 rounded-md border border-[var(--border)] text-[var(--text-muted)] text-xs font-bold hover:bg-[var(--bg-hover)] transition" style="letter-spacing: -0.03em;">
            {{ locale.toUpperCase() }}
          </button>
        </div>
        <a href="https://app.ixiera.id/login" class="block text-center text-sm font-bold py-2.5 rounded-md bg-[var(--accent)] text-[var(--accent-text)] hover:opacity-90 transition" style="letter-spacing: -0.03em;">
          Minta Akses
        </a>
      </div>
    </aside>

    <!-- MOBILE TOP BAR -->
    <nav class="md:hidden fixed top-0 left-0 right-0 z-40 h-14 bg-[var(--bg-primary)]/95 backdrop-blur-md border-b border-[var(--border)] flex items-center px-4 justify-between">
      <a href="/" class="flex items-center gap-2">
        <div class="w-7 h-7 flex items-center justify-center rounded-md text-xs font-bold bg-[var(--accent)] text-[var(--accent-text)]">IX</div>
        <span class="font-bold text-lg text-[var(--text-primary)]" style="letter-spacing: -0.03em;">Ixiera</span>
      </a>
      <button @click="mobileMenuOpen = true" class="p-2 text-[var(--text-primary)]">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
      </button>
    </nav>

    <!-- MOBILE DRAWER -->
    <div v-if="mobileMenuOpen" class="md:hidden fixed inset-0 z-[100]" style="display: flex;">
      <div class="absolute inset-0 bg-black/60" @click="mobileMenuOpen = false"></div>
      <aside class="drawer-slide relative w-72 max-w-[80%] h-full flex flex-col shadow-2xl bg-[var(--bg-primary)] border-r border-[var(--border)]">
        <div class="h-16 px-5 flex items-center justify-between border-b border-[var(--border)]">
          <a href="/" class="flex items-center gap-2">
            <div class="w-8 h-8 flex items-center justify-center rounded-md text-sm font-bold bg-[var(--accent)] text-[var(--accent-text)]">IX</div>
            <span class="font-bold text-xl text-[var(--text-primary)]" style="letter-spacing: -0.03em;">Ixiera</span>
          </a>
          <button @click="mobileMenuOpen = false" class="p-2 text-[var(--text-primary)]">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
          </button>
        </div>

        <nav class="flex-1 p-4 space-y-1 overflow-y-auto">
          <a href="/#fitur" @click="mobileMenuOpen = false" class="nav-bd">Fitur</a>
          <a href="/#contoh" @click="mobileMenuOpen = false" class="nav-bd">Contoh Data</a>
          <a href="/#cara-kerja" @click="mobileMenuOpen = false" class="nav-bd">Cara Kerja</a>
          <a href="/pricing" @click="mobileMenuOpen = false" class="nav-bd" style="color: var(--text-primary); background: var(--bg-hover);">Harga</a>
          <a href="/#faq" @click="mobileMenuOpen = false" class="nav-bd">FAQ</a>
        </nav>

        <div class="p-4 border-t border-[var(--border)] space-y-3">
          <div class="flex gap-2">
            <button @click="toggleTheme" class="flex-1 flex items-center justify-center py-3 rounded-lg border border-[var(--border)] text-[var(--text-muted)]">
              <Sun v-if="theme === 'dark'" class="w-4 h-4" />
              <Moon v-else class="w-4 h-4" />
            </button>
            <button @click="toggleLang" class="flex-1 py-3 rounded-lg border border-[var(--border)] text-[var(--text-muted)] text-xs font-bold" style="letter-spacing: -0.03em;">
              {{ locale.toUpperCase() }}
            </button>
          </div>
          <a href="https://app.ixiera.id/login" class="block text-center text-sm font-bold py-3 rounded-lg bg-[var(--accent)] text-[var(--accent-text)]" style="letter-spacing: -0.03em;">
            Minta Akses
          </a>
        </div>
      </aside>
    </div>

    <!-- MAIN CONTENT -->
    <main class="md:ml-60 pt-14 md:pt-0">
      
      <!-- HERO PRICING -->
      <section class="relative">
        <div class="container-bd text-center relative z-10" style="padding-top: 48px; padding-bottom: 48px;">
          <div class="pill-bd mb-6">
            <span class="w-1.5 h-1.5 rounded-full" style="background: #3fcb7f;"></span>
            HARGA BETA
          </div>
          <h1 class="font-display text-[40px] md:text-[56px] leading-[1.1] mb-4 max-w-3xl mx-auto text-[var(--text-primary)]">
            Harga transparan, <span class="italic" style="color: #9984d8;">tanpa jebakan.</span>
          </h1>
          <p class="text-[16px] md:text-[18px] leading-relaxed max-w-2xl mx-auto text-[var(--text-secondary)]" style="letter-spacing: -0.03em;">
            Mulai dengan trial 7 hari. Kalau cocok, lanjutkan dengan paket bulanan. Harga beta ini terkunci selama kamu berlangganan.
          </p>
        </div>
      </section>

      <!-- PRICING CARDS -->
      <section class="container-bd pb-20">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 md:gap-4 lg:gap-6">
          
          <!-- TRIAL -->
          <div class="card-bd p-7 flex flex-col">
            <h3 class="text-[20px] font-semibold mb-1 text-[var(--text-primary)]" style="letter-spacing: -0.03em;">Trial 7 Hari</h3>
            <p class="text-[13px] mb-6 text-[var(--text-secondary)]" style="letter-spacing: -0.03em;">Coba semua fitur tanpa bayar di awal.</p>
            
            <div class="mb-6">
              <span class="text-[40px] font-bold text-[var(--text-primary)]" style="letter-spacing: -0.03em;">Rp 0</span>
              <span class="text-[14px] text-[var(--text-muted)]">/ 7 hari</span>
            </div>

            <ul class="space-y-3 mb-8 flex-1 text-[14px] text-[var(--text-secondary)]" style="letter-spacing: -0.03em;">
              <li class="flex items-start gap-2.5">
                <svg class="w-4 h-4 shrink-0 mt-0.5" style="color: #3fcb7f;" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                20 kredit AI gratis
              </li>
              <li class="flex items-start gap-2.5">
                <svg class="w-4 h-4 shrink-0 mt-0.5" style="color: #3fcb7f;" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                Akses ke semua fitur inti
              </li>
              <li class="flex items-start gap-2.5">
                <svg class="w-4 h-4 shrink-0 mt-0.5" style="color: #3fcb7f;" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                Tanpa perlu kartu kredit
              </li>
            </ul>
            <a href="https://app.ixiera.id/login" class="btn-bd-ghost text-center">Mulai Trial</a>
          </div>

          <!-- PRO -->
          <div class="card-bd p-7 flex flex-col relative" style="border: 2px solid #9984d8; box-shadow: 0 0 40px rgba(153,132,216,0.15);">
            <div class="absolute -top-3 left-1/2 -translate-x-1/2 text-[10px] font-bold uppercase tracking-widest px-3 py-1 rounded-full text-white" style="background: #9984d8;">Paling Populer</div>
            <h3 class="text-[20px] font-semibold mb-1 text-[var(--text-primary)]" style="letter-spacing: -0.03em;">Paket 30 Hari</h3>
            <p class="text-[13px] mb-6 text-[var(--text-secondary)]" style="letter-spacing: -0.03em;">Buat yang serius ngejalanin otomatisasi.</p>
            
            <div class="mb-6">
              <span class="text-[40px] font-bold text-[var(--text-primary)]" style="letter-spacing: -0.03em;">Rp 29rb</span>
              <span class="text-[14px] text-[var(--text-muted)]">/ bulan</span>
            </div>

            <ul class="space-y-3 mb-8 flex-1 text-[14px] text-[var(--text-secondary)]" style="letter-spacing: -0.03em;">
              <li class="flex items-start gap-2.5">
                <svg class="w-4 h-4 shrink-0 mt-0.5" style="color: #3fcb7f;" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                100 kredit AI per bulan
              </li>
              <li class="flex items-start gap-2.5">
                <svg class="w-4 h-4 shrink-0 mt-0.5" style="color: #3fcb7f;" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                Auto-reply engine penuh
              </li>
              <li class="flex items-start gap-2.5">
                <svg class="w-4 h-4 shrink-0 mt-0.5" style="color: #3fcb7f;" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                Analytics tanpa batas
              </li>
              <li class="flex items-start gap-2.5">
                <svg class="w-4 h-4 shrink-0 mt-0.5" style="color: #3fcb7f;" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                Tanpa auto-renew (manual perpanjang)
              </li>
            </ul>
            <a href="https://app.ixiera.id/login" class="btn-bd-primary text-center">Pilih Pro</a>
          </div>

          <!-- BYOK -->
          <div class="card-bd p-7 flex flex-col">
            <h3 class="text-[20px] font-semibold mb-1 text-[var(--text-primary)]" style="letter-spacing: -0.03em;">Paket + API Key</h3>
            <p class="text-[13px] mb-6 text-[var(--text-secondary)]" style="letter-spacing: -0.03em;">Pakai API key Gemini/Groq milikmu sendiri.</p>
            
            <div class="mb-6">
              <span class="text-[40px] font-bold text-[var(--text-primary)]" style="letter-spacing: -0.03em;">Rp 19rb</span>
              <span class="text-[14px] text-[var(--text-muted)]">/ bulan</span>
            </div>

            <ul class="space-y-3 mb-8 flex-1 text-[14px] text-[var(--text-secondary)]" style="letter-spacing: -0.03em;">
              <li class="flex items-start gap-2.5">
                <svg class="w-4 h-4 shrink-0 mt-0.5" style="color: #3fcb7f;" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                Tanpa batasan kredit dari kami
              </li>
              <li class="flex items-start gap-2.5">
                <svg class="w-4 h-4 shrink-0 mt-0.5" style="color: #3fcb7f;" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                Biaya API langsung ke provider
              </li>
              <li class="flex items-start gap-2.5">
                <svg class="w-4 h-4 shrink-0 mt-0.5" style="color: #3fcb7f;" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                Kontrol penuh atas model AI
              </li>
            </ul>
            <a href="https://app.ixiera.id/login" class="btn-bd-ghost text-center">Pilih BYOK</a>
          </div>

        </div>

        <div class="mt-10 text-center text-[12px] text-[var(--text-muted)]" style="letter-spacing: -0.03em;">
          <p>1 kredit = 1 aksi AI (generate, balasan AI, repurpose, analisis lanjutan). Template balasan dan Quick Score gratis.</p>
          <p class="mt-1">API key sendiri hanya tersedia di paket berbayar.</p>
        </div>
      </section>

      <!-- PRICING FAQ -->
      <section class="section-bd" style="background: var(--bg-secondary);">
        <div class="container-bd" style="max-width: 800px;">
          <h2 class="h2-bd">Pertanyaan soal Harga</h2>
          <div class="border-t border-[var(--border)] mt-8">
            <details class="group border-b border-[var(--border)] py-5 cursor-pointer">
              <summary class="flex justify-between items-center text-[16px] font-semibold list-none text-[var(--text-primary)]" style="letter-spacing: -0.03em;">
                Apakah ada biaya tersembunyi?
                <span class="group-open:rotate-180 transition"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <p class="text-[14px] mt-3 leading-relaxed text-[var(--text-secondary)]" style="letter-spacing: -0.03em;">Tidak. Harga yang tertera adalah harga final. Tidak ada biaya setup, biaya tersembunyi, atau auto-renew diam-diam.</p>
            </details>
            <details class="group border-b border-[var(--border)] py-5 cursor-pointer">
              <summary class="flex justify-between items-center text-[16px] font-semibold list-none text-[var(--text-primary)]" style="letter-spacing: -0.03em;">
                Kenapa paketnya tidak auto-renew?
                <span class="group-open:rotate-180 transition"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <p class="text-[14px] mt-3 leading-relaxed text-[var(--text-secondary)]" style="letter-spacing: -0.03em;">Supaya kamu punya kendali penuh. Kami tidak mau uangmu kepotong otomatis saat kamu sedang tidak aktif. Kamu bisa perpanjang manual kapan saja.</p>
            </details>
            <details class="group border-b border-[var(--border)] py-5 cursor-pointer">
              <summary class="flex justify-between items-center text-[16px] font-semibold list-none text-[var(--text-primary)]" style="letter-spacing: -0.03em;">
                Kalau kredit habis di tengah bulan, gimana?
                <span class="group-open:rotate-180 transition"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <p class="text-[14px] mt-3 leading-relaxed text-[var(--text-secondary)]" style="letter-spacing: -0.03em;">Kamu bisa upgrade ke paket BYOK, atau top-up kredit tambahan (akan hadir segera). Fitur template dan Quick Score tetap bisa dipakai tanpa kredit.</p>
            </details>
            <details class="group border-b border-[var(--border)] py-5 cursor-pointer">
              <summary class="flex justify-between items-center text-[16px] font-semibold list-none text-[var(--text-primary)]" style="letter-spacing: -0.03em;">
                Apakah harga beta akan naik?
                <span class="group-open:rotate-180 transition"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <p class="text-[14px] mt-3 leading-relaxed text-[var(--text-secondary)]" style="letter-spacing: -0.03em;">Harga bisa naik untuk pengguna baru nanti. Tapi untuk kamu yang berlangganan sekarang, harga beta ini terkunci selamanya selama langgananmu tidak terputus.</p>
            </details>
          </div>
        </div>
      </section>

      <!-- FINAL CTA -->
      <section class="section-bd text-center">
        <div class="container-bd">
          <h2 class="font-display text-[36px] md:text-[48px] leading-[1.1] mb-6 text-[var(--text-primary)]">Masih ragu?</h2>
          <p class="text-[15px] text-[var(--text-secondary)] mb-8" style="letter-spacing: -0.03em;">Coba dulu trial 7 hari. Kalau tidak cocok, tidak perlu bayar apa-apa.</p>
          <a href="https://app.ixiera.id/login" class="btn-bd-primary inline-block">Mulai Trial Gratis</a>
        </div>
      </section>

      <!-- FOOTER -->
      <footer class="border-t border-[var(--border)] py-8">
        <div class="container-bd flex flex-col md:flex-row justify-between items-center gap-5 text-[13px] text-[var(--text-muted)]" style="letter-spacing: -0.03em;">
          <div class="flex items-center gap-2">
            <div class="w-6 h-6 flex items-center justify-center rounded text-[10px] font-bold bg-[var(--accent)] text-[var(--accent-text)]">IX</div>
            <span>2026 Ixiera.</span>
          </div>
          <div class="flex gap-5 flex-wrap justify-center">
            <a href="mailto:contact@ixiera.id" class="hover:text-[var(--text-primary)] transition">Email</a>
            <a href="/privacy" class="hover:text-[var(--text-primary)] transition">Kebijakan Privasi</a>
            <a href="/terms" class="hover:text-[var(--text-primary)] transition">Syarat &amp; Ketentuan</a>
            <a href="/data-deletion" class="hover:text-[var(--text-primary)] transition">Hapus Data</a>
          </div>
        </div>
        <div class="container-bd text-center mt-5 text-[10px] text-[var(--text-muted)]" style="letter-spacing: -0.03em;">
          Ixiera adalah produk independen dan tidak berafiliasi dengan Meta Platforms. Threads adalah merek dagang Meta.
        </div>
      </footer>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Sun, Moon } from 'lucide-vue-next'
import { useI18n } from 'vue-i18n'

const { locale } = useI18n()
const mobileMenuOpen = ref(false)
const theme = ref<'light' | 'dark'>('dark')

function toggleTheme() {
  theme.value = theme.value === 'dark' ? 'light' : 'dark'
  document.documentElement.classList.toggle('dark', theme.value === 'dark')
}

function toggleLang() {
  locale.value = locale.value === 'id' ? 'en' : 'id'
}

onMounted(() => {
  theme.value = document.documentElement.classList.contains('dark') ? 'dark' : 'light'
})
</script>
