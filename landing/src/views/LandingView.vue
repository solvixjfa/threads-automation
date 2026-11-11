<template>
  <div class="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)] font-sans selection:bg-[#9984d8] selection:text-white">
    <!-- TOP NAVBAR -->
    <nav class="fixed top-0 left-0 right-0 z-50 h-16 bg-[var(--bg-primary)]/80 backdrop-blur-md border-b border-[var(--border)] flex items-center">
      <div class="w-full max-w-[1200px] mx-auto px-6 flex items-center justify-between">
        <a href="/" class="flex items-center gap-2">
          <div class="w-7 h-7 flex items-center justify-center rounded text-xs font-bold bg-[var(--accent)] text-[var(--accent-text)]">IX</div>
          <span class="font-bold text-lg tracking-tight">Ixiera</span>
        </a>
        <div class="hidden md:flex items-center gap-8 text-sm font-medium text-[var(--text-secondary)]">
          <a href="/features" class="hover:text-[var(--text-primary)] transition">Fitur</a>
          <a href="#contoh" class="hover:text-[var(--text-primary)] transition">Contoh Data</a>
          <a href="#cara-kerja" class="hover:text-[var(--text-primary)] transition">Cara Kerja</a>
          <a href="/pricing" class="hover:text-[var(--text-primary)] transition">Harga</a>
          <a href="#faq" class="hover:text-[var(--text-primary)] transition">FAQ</a>
        </div>
        <div class="hidden md:flex items-center gap-4">
          <button @click="toggleTheme" class="p-2 text-[var(--text-muted)] hover:text-[var(--text-primary)] transition">
            <Sun v-if="theme === 'dark'" class="w-4 h-4" />
            <Moon v-else class="w-4 h-4" />
          </button>
          <button @click="toggleLang" class="text-xs font-bold text-[var(--text-muted)] hover:text-[var(--text-primary)] transition px-2 py-1 rounded border border-[var(--border)]">
            {{ locale.toUpperCase() }}
          </button>
          <div class="w-px h-4 bg-[var(--border)] mx-1"></div>
          <a href="https://app.ixiera.id/login" class="text-sm font-medium text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition">Log in</a>
          <a href="https://app.ixiera.id/signup" class="btn-bd-primary" style="padding: 8px 16px;">Sign up</a>
        </div>
        <button @click="mobileMenuOpen = true" class="md:hidden p-2 text-[var(--text-primary)]">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
        </button>
      </div>
    </nav>

    <!-- MOBILE DRAWER -->
    <div v-if="mobileMenuOpen" class="md:hidden fixed inset-0 z-[100] bg-[var(--bg-primary)]/95 backdrop-blur-lg flex flex-col p-6">
      <div class="flex justify-between items-center mb-10">
        <div class="flex items-center gap-2">
          <div class="w-7 h-7 flex items-center justify-center rounded text-xs font-bold bg-[var(--accent)] text-[var(--accent-text)]">IX</div>
          <span class="font-bold text-lg">Ixiera</span>
        </div>
        <button @click="mobileMenuOpen = false" class="p-2 text-[var(--text-primary)]">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
        </button>
      </div>
      <nav class="flex flex-col gap-6 text-[16px] font-medium text-[var(--text-secondary)]">
        <a href="/features" @click="mobileMenuOpen = false" class="hover:text-[var(--text-primary)] transition">Fitur</a>
        <a href="#contoh" @click="mobileMenuOpen = false" class="hover:text-[var(--text-primary)] transition">Contoh Data</a>
        <a href="#cara-kerja" @click="mobileMenuOpen = false" class="hover:text-[var(--text-primary)] transition">Cara Kerja</a>
        <a href="/pricing" @click="mobileMenuOpen = false" class="hover:text-[var(--text-primary)] transition">Harga</a>
        <a href="#faq" @click="mobileMenuOpen = false" class="hover:text-[var(--text-primary)] transition">FAQ</a>
      </nav>
      <div class="mt-auto pt-6 border-t border-[var(--border)] space-y-4">
        <div class="flex gap-2">
          <button @click="toggleTheme" class="flex-1 flex items-center justify-center py-2.5 rounded-md border border-[var(--border)] text-[var(--text-muted)]">
            <Sun v-if="theme === 'dark'" class="w-4 h-4" />
            <Moon v-else class="w-4 h-4" />
          </button>
          <button @click="toggleLang" class="flex-1 py-2.5 rounded-md border border-[var(--border)] text-[var(--text-muted)] text-xs font-bold">
            {{ locale.toUpperCase() }}
          </button>
        </div>
        <a href="https://app.ixiera.id/signup" class="btn-bd-primary w-full text-center block">Sign up</a>
        <a href="https://app.ixiera.id/login" class="text-center block text-sm text-[var(--text-secondary)] py-1">Log in</a>
      </div>
    </div>

    <main class="pt-16">
      <!-- HERO -->
      <section class="relative pt-24 pb-20">
        <div class="max-w-[1200px] mx-auto px-6 text-center relative z-10">
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
            <a href="/features" class="btn-bd-ghost w-full sm:w-auto text-center">Lihat Fitur</a>
          </div>
        </div>
        
        <!-- Hero Mockup (Dashboard Overview) -->
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

      <!-- CTA TO FEATURES -->
      <section class="py-24 text-center border-t border-[var(--border)] bg-[var(--bg-secondary)]">
        <div class="max-w-[800px] mx-auto px-6">
          <h2 class="font-display text-[40px] md:text-[56px] leading-[1.0] mb-6">Siap lihat lebih dalam?</h2>
          <p class="text-[16px] text-[var(--text-secondary)] mb-8">Jelajahi setiap fitur yang bikin Ixiera beda dari yang lain.</p>
          <a href="/features" class="btn-bd-primary inline-block">Lihat Semua Fitur</a>
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
