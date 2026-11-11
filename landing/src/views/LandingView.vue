<template>
  <div class="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)] font-sans selection:bg-[#9984d8] selection:text-white">
    
    <!-- DESKTOP SIDEBAR (BALIK KE ASLINYA) -->
    <aside class="hidden md:flex flex-col fixed top-0 left-0 h-screen w-60 z-50 bg-[var(--bg-primary)] border-r border-[var(--border)]">
      <div class="h-16 px-5 flex items-center border-b border-[var(--border)]">
        <a href="/" class="flex items-center gap-2">
          <div class="w-8 h-8 flex items-center justify-center rounded-md text-sm font-bold bg-[var(--accent)] text-[var(--accent-text)]">IX</div>
          <span class="ml-2 font-bold text-xl text-[var(--text-primary)]" style="letter-spacing: -0.03em;">Ixiera</span>
        </a>
      </div>

      <nav class="flex-1 p-3 space-y-1 overflow-y-auto">
        <a href="/" class="nav-bd text-[var(--text-primary)] bg-[var(--bg-hover)]">Dashboard</a>
        
        <!-- Dropdown Fitur di Sidebar -->
        <div>
          <button @click="fiturOpen = !fiturOpen" class="nav-bd w-full flex items-center justify-between">
            Fitur
            <svg :class="{'rotate-180': fiturOpen}" class="w-3 h-3 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
          </button>
          <div v-show="fiturOpen" class="pl-4 py-1 space-y-1">
            <a href="/features/composer" class="nav-bd text-sm py-1.5">Content Composer</a>
            <a href="/features/inbox" class="nav-bd text-sm py-1.5">Smart Inbox</a>
            <a href="/features/analytics" class="nav-bd text-sm py-1.5">Deep Analytics</a>
          </div>
        </div>

        <a href="#cara-kerja" class="nav-bd">Cara Kerja</a>
        <a href="/pricing" class="nav-bd">Harga</a>
        <a href="#faq" class="nav-bd">FAQ</a>
      </nav>

      <div class="p-3 border-t border-[var(--border)] space-y-2">
        <div class="flex items-center gap-2">
          <button @click="toggleTheme" class="flex-1 flex items-center justify-center py-2 rounded-md border border-[var(--border)] text-[var(--text-muted)] hover:bg-[var(--bg-hover)] hover:text-[var(--text-primary)] transition">
            <Sun v-if="theme === 'dark'" class="w-4 h-4" />
            <Moon v-else class="w-4 h-4" />
          </button>
          <button @click="toggleLang" class="px-3 py-2 rounded-md border border-[var(--border)] text-[var(--text-muted)] text-xs font-bold hover:bg-[var(--bg-hover)] transition">
            {{ locale.toUpperCase() }}
          </button>
        </div>
        <a href="https://app.ixiera.id/signup" class="block text-center text-sm font-bold py-2.5 rounded-md bg-[var(--accent)] text-[var(--accent-text)] hover:opacity-90 transition">
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
          <a href="/" @click="mobileMenuOpen = false" class="nav-bd">Dashboard</a>
          <div>
            <button @click="fiturOpenMobile = !fiturOpenMobile" class="nav-bd w-full flex items-center justify-between">
              Fitur
              <svg :class="{'rotate-180': fiturOpenMobile}" class="w-3 h-3 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
            </button>
            <div v-show="fiturOpenMobile" class="pl-4 py-1 space-y-1">
              <a href="/features/composer" @click="mobileMenuOpen = false" class="nav-bd text-sm py-1.5">Content Composer</a>
              <a href="/features/inbox" @click="mobileMenuOpen = false" class="nav-bd text-sm py-1.5">Smart Inbox</a>
              <a href="/features/analytics" @click="mobileMenuOpen = false" class="nav-bd text-sm py-1.5">Deep Analytics</a>
            </div>
          </div>
          <a href="#cara-kerja" @click="mobileMenuOpen = false" class="nav-bd">Cara Kerja</a>
          <a href="/pricing" @click="mobileMenuOpen = false" class="nav-bd">Harga</a>
          <a href="#faq" @click="mobileMenuOpen = false" class="nav-bd">FAQ</a>
        </nav>

        <div class="p-4 border-t border-[var(--border)] space-y-3">
          <div class="flex gap-2">
            <button @click="toggleTheme" class="flex-1 flex items-center justify-center py-3 rounded-lg border border-[var(--border)] text-[var(--text-muted)]">
              <Sun v-if="theme === 'dark'" class="w-4 h-4" />
              <Moon v-else class="w-4 h-4" />
            </button>
            <button @click="toggleLang" class="flex-1 py-3 rounded-lg border border-[var(--border)] text-[var(--text-muted)] text-xs font-bold">
              {{ locale.toUpperCase() }}
            </button>
          </div>
          <a href="https://app.ixiera.id/signup" class="block text-center text-sm font-bold py-3 rounded-lg bg-[var(--accent)] text-[var(--accent-text)]">
            Minta Akses
          </a>
        </div>
      </aside>
    </div>

    <!-- MAIN CONTENT -->
    <main class="md:ml-60 pt-14 md:pt-0">
      
      <!-- HERO -->
      <section class="relative pt-24 pb-20">
        <div class="max-w-[1000px] mx-auto px-6 text-center relative z-10">
          <div class="pill-bd mb-6 mx-auto" style="width: fit-content;">
            <span class="w-1.5 h-1.5 rounded-full" style="background: var(--accent-mint);"></span>
            PUBLIC BETA
          </div>
          <h1 class="font-display text-[48px] md:text-[64px] leading-[1.0] mb-6 max-w-[800px] mx-auto text-[var(--text-primary)]">
            Posting yang belajar dari <br class="hidden md:block">
            <span class="italic text-[var(--accent-violet)]">akun kamu sendiri.</span>
          </h1>
          <p class="text-[16px] md:text-[18px] leading-[1.56] max-w-[640px] mx-auto mb-10 text-[var(--text-secondary)]">
            Ixiera membaca post kamu yang paling jalan (jam, hook, panjang, topik), lalu membantu bikin rencana konten dan membalas komentar dengan gayamu.
          </p>
          <div class="flex flex-col sm:flex-row items-center justify-center gap-3 mb-8">
            <a href="https://app.ixiera.id/signup" class="btn-bd-primary w-full sm:w-auto text-center">Minta Akses</a>
            <a href="/features/composer" class="btn-bd-ghost w-full sm:w-auto text-center">Lihat Fitur</a>
          </div>
        </div>
        
        <!-- Hero Mockup Dashboard -->
        <div class="max-w-[1000px] mx-auto px-6 pb-16 md:pb-24 relative mt-10">
          <div class="absolute inset-0 pointer-events-none" style="background: radial-gradient(ellipse 70% 60% at 50% 0%, rgba(153,132,216,0.35) 0%, transparent 70%);"></div>
          <div class="relative rounded-2xl border border-[var(--border)] overflow-hidden bg-[#050607] shadow-2xl">
            <div class="flex items-center gap-1.5 px-4 py-3 border-b border-[#1a1a1a]">
              <div class="w-2.5 h-2.5 rounded-full bg-[#1a1a1a]"></div>
              <div class="w-2.5 h-2.5 rounded-full bg-[#1a1a1a]"></div>
              <div class="w-2.5 h-2.5 rounded-full bg-[#1a1a1a]"></div>
              <div class="ml-auto text-[10px] font-mono text-[#555]">app.ixiera.id/dashboard</div>
            </div>
            <div class="p-5 md:p-7 space-y-5">
              <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
                <div class="bg-black border border-[#1a1a1a] rounded-xl p-3 md:p-4">
                  <p class="text-[10px] text-[#666] mb-1">Total Views</p>
                  <p class="text-lg md:text-2xl font-bold text-white tracking-tight">324.158</p>
                </div>
                <div class="bg-black border border-[#1a1a1a] rounded-xl p-3 md:p-4">
                  <p class="text-[10px] text-[#666] mb-1">Total Likes</p>
                  <p class="text-lg md:text-2xl font-bold text-white tracking-tight">3.691</p>
                </div>
                <div class="bg-black border border-[#1a1a1a] rounded-xl p-3 md:p-4">
                  <p class="text-[10px] text-[#666] mb-1">Published</p>
                  <p class="text-lg md:text-2xl font-bold text-white tracking-tight">82</p>
                </div>
                <div class="bg-black border border-[#1a1a1a] rounded-xl p-3 md:p-4">
                  <p class="text-[10px] text-[#666] mb-1">Avg Engagement</p>
                  <p class="text-lg md:text-2xl font-bold text-white tracking-tight">0.97%</p>
                </div>
              </div>
              <div class="bg-black border border-[#1a1a1a] rounded-xl p-4">
                <div class="flex justify-between items-center mb-3">
                  <span class="text-[10px] text-[#666] uppercase tracking-widest font-bold">Growth Harian</span>
                </div>
                <svg viewBox="0 0 400 80" class="w-full" preserveAspectRatio="none" style="height: 80px;">
                  <defs>
                    <linearGradient id="chartGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.2" />
                      <stop offset="100%" stop-color="#ffffff" stop-opacity="0" />
                    </linearGradient>
                  </defs>
                  <path d="M0,70 Q50,65 80,55 T160,45 T240,30 T320,20 L400,10 L400,80 L0,80 Z" fill="url(#chartGradient)" />
                  <path d="M0,70 Q50,65 80,55 T160,45 T240,30 T320,20 L400,10" stroke="#ffffff" stroke-width="1.5" fill="none" />
                </svg>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- MASALAH -->
      <section class="py-20 border-t border-[var(--border)]">
        <div class="max-w-[1000px] mx-auto px-6">
          <h2 class="h2-bd">Jadi admin akun sendiri itu melelahkan.</h2>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-5 mt-10">
            <div class="card-bd p-7 feature-card">
              <span class="font-display text-[32px] block mb-3 text-[var(--accent-violet)]">01</span>
              <h3 class="text-[17px] font-semibold mb-2">Bingung mau posting apa.</h3>
              <p class="text-[14px] leading-relaxed text-[var(--text-secondary)]">Ide habis padahal harus konsisten.</p>
            </div>
            <div class="card-bd p-7 feature-card">
              <span class="font-display text-[32px] block mb-3 text-[var(--accent-violet)]">02</span>
              <h3 class="text-[17px] font-semibold mb-2">Komentar numpuk.</h3>
              <p class="text-[14px] leading-relaxed text-[var(--text-secondary)]">Telat balas, interaksi dan momentum hilang.</p>
            </div>
            <div class="card-bd p-7 feature-card">
              <span class="font-display text-[32px] block mb-3 text-[var(--accent-violet)]">03</span>
              <h3 class="text-[17px] font-semibold mb-2">Nggak tahu apa yang jalan.</h3>
              <p class="text-[14px] leading-relaxed text-[var(--text-secondary)]">Post mana, jam berapa, hook seperti apa, semua cuma feeling.</p>
            </div>
          </div>
        </div>
      </section>

      <!-- FITUR OVERVIEW -->
      <section id="fitur" class="py-20 border-t border-[var(--border)] bg-[var(--bg-secondary)]">
        <div class="max-w-[1000px] mx-auto px-6">
          <h2 class="h2-bd">Bukan sekadar scheduler.</h2>
          <p class="text-center mb-14 text-[15px] text-[var(--text-secondary)]">Lima menu, satu alur: rencanakan, posting, balas, pelajari.</p>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
            <a href="/features/composer" class="card-bd p-7 hover:border-[#9984d8] transition group">
              <div class="w-10 h-10 rounded-lg bg-[#9984d8]/10 flex items-center justify-center mb-4 group-hover:scale-110 transition">
                <svg class="w-5 h-5 text-[#9984d8]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
              </div>
              <h3 class="text-[17px] font-semibold mb-2">Content Composer</h3>
              <p class="text-[14px] leading-relaxed text-[var(--text-secondary)]">Generate rencana konten 3 hari dengan AI cerdas.</p>
            </a>
            <a href="/features/inbox" class="card-bd p-7 hover:border-[#3fcb7f] transition group">
              <div class="w-10 h-10 rounded-lg bg-[#3fcb7f]/10 flex items-center justify-center mb-4 group-hover:scale-110 transition">
                <svg class="w-5 h-5 text-[#3fcb7f]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path></svg>
              </div>
              <h3 class="text-[17px] font-semibold mb-2">Smart Inbox</h3>
              <p class="text-[14px] leading-relaxed text-[var(--text-secondary)]">Balas komentar pakai AI atau template dengan mudah.</p>
            </a>
            <a href="/features/analytics" class="card-bd p-7 hover:border-white transition group">
              <div class="w-10 h-10 rounded-lg bg-white/10 flex items-center justify-center mb-4 group-hover:scale-110 transition">
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
              </div>
              <h3 class="text-[17px] font-semibold mb-2">Deep Analytics</h3>
              <p class="text-[14px] leading-relaxed text-[var(--text-secondary)]">Analisis jam, hook, dan topik terbaik dari data akunmu.</p>
            </a>
          </div>
        </div>
      </section>

      <!-- CARA KERJA -->
      <section id="cara-kerja" class="py-20 border-t border-[var(--border)]">
        <div class="max-w-[1000px] mx-auto px-6">
          <h2 class="h2-bd">Mulai dalam 3 langkah.</h2>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mt-10">
            <div class="space-y-3">
              <div class="w-10 h-10 rounded-full flex items-center justify-center font-display text-[18px] border border-[var(--border)] bg-[var(--bg-secondary)] text-[var(--accent-violet)]">1</div>
              <h3 class="text-[17px] font-semibold">Daftar dan minta akses.</h3>
              <p class="text-[14px] leading-relaxed text-[var(--text-secondary)]">Buat akun, lalu kirim @username Threads kamu. Akses disetujui manual dan kamu dikabari lewat email.</p>
            </div>
            <div class="space-y-3">
              <div class="w-10 h-10 rounded-full flex items-center justify-center font-display text-[18px] border border-[var(--border)] bg-[var(--bg-secondary)] text-[var(--accent-violet)]">2</div>
              <h3 class="text-[17px] font-semibold">Hubungkan dan ajari gayamu.</h3>
              <p class="text-[14px] leading-relaxed text-[var(--text-secondary)]">Setelah disetujui, terima undangan tester di Threads dan login lewat sistem resmi Meta. Tulis dokumen gaya dan aturanmu di Knowledge Base.</p>
            </div>
            <div class="space-y-3">
              <div class="w-10 h-10 rounded-full flex items-center justify-center font-display text-[18px] border border-[var(--border)] bg-[var(--bg-secondary)] text-[var(--accent-violet)]">3</div>
              <h3 class="text-[17px] font-semibold">Review dan jalan.</h3>
              <p class="text-[14px] leading-relaxed text-[var(--text-secondary)]">Setujui draf, atur mode balasan, dan pantau Analytics tiap minggu.</p>
            </div>
          </div>
        </div>
      </section>

      <!-- FAQ -->
      <section id="faq" class="py-20 border-t border-[var(--border)] bg-[var(--bg-secondary)]">
        <div class="max-w-[800px] mx-auto px-6">
          <h2 class="h2-bd">Pertanyaan Umum</h2>
          <div class="border-t border-[var(--border)] mt-8">
            <details class="group border-b border-[var(--border)] py-5 cursor-pointer">
              <summary class="flex justify-between items-center text-[16px] font-semibold list-none text-[var(--text-primary)]">
                Kenapa harus minta akses?
                <span class="group-open:rotate-180 transition"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <p class="text-[14px] mt-3 leading-relaxed text-[var(--text-secondary)]">Ixiera masih dalam tahap early access, jadi tiap akun ditambahkan manual dan perlu disetujui dulu.</p>
            </details>
            <details class="group border-b border-[var(--border)] py-5 cursor-pointer">
              <summary class="flex justify-between items-center text-[16px] font-semibold list-none text-[var(--text-primary)]">
                Apakah ini gratis?
                <span class="group-open:rotate-180 transition"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <p class="text-[14px] mt-3 leading-relaxed text-[var(--text-secondary)]">Trial 7 hari gratis dengan 20 kredit. Setelah itu, paket berbayar mulai dari Rp29.000 per bulan.</p>
            </details>
          </div>
        </div>
      </section>

      <!-- FINAL CTA -->
      <section class="py-24 text-center border-t border-[var(--border)]">
        <div class="max-w-[800px] mx-auto px-6">
          <h2 class="font-display text-[40px] md:text-[56px] leading-[1.0] mb-8">Siap berhenti nebak-nebak?</h2>
          <a href="https://app.ixiera.id/signup" class="btn-bd-primary inline-block">Minta Akses</a>
        </div>
      </section>

      <!-- FOOTER -->
      <footer class="border-t border-[var(--border)] py-8">
        <div class="max-w-[1000px] mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-5 text-[13px] text-[var(--text-muted)]">
          <div class="flex items-center gap-2">
            <div class="w-6 h-6 flex items-center justify-center rounded text-[10px] font-bold bg-[var(--accent)] text-[var(--accent-text)]">IX</div>
            <span>2026 Ixiera.</span>
          </div>
          <div class="flex gap-5 flex-wrap justify-center">
            <a href="mailto:contact@ixiera.id" class="hover:text-[var(--text-primary)] transition">Email</a>
            <a href="/privacy" class="hover:text-[var(--text-primary)] transition">Kebijakan Privasi</a>
            <a href="/terms" class="hover:text-[var(--text-primary)] transition">Syarat & Ketentuan</a>
          </div>
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
const fiturOpen = ref(false)
const fiturOpenMobile = ref(false)
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
