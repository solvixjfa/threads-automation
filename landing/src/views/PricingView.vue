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
          <a href="/#fitur" class="hover:text-[var(--text-primary)] transition">{{ $t('nav.features') }}</a>
          <a href="/#contoh" class="hover:text-[var(--text-primary)] transition">{{ $t('nav.data') }}</a>
          <a href="/#cara-kerja" class="hover:text-[var(--text-primary)] transition">{{ $t('nav.how') }}</a>
          <a href="/pricing" class="text-[var(--text-primary)] transition">{{ $t('nav.pricing') }}</a>
          <a href="/#faq" class="hover:text-[var(--text-primary)] transition">{{ $t('nav.faq') }}</a>
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
          <a href="https://app.ixiera.id/login" class="text-sm font-medium text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition">{{ $t('nav.login') }}</a>
          <a href="https://app.ixiera.id/signup" class="btn-bd-primary" style="padding: 8px 16px;">{{ $t('nav.signup') }}</a>
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
        <a href="/#fitur" @click="mobileMenuOpen = false" class="hover:text-[var(--text-primary)] transition">{{ $t('nav.features') }}</a>
        <a href="/#contoh" @click="mobileMenuOpen = false" class="hover:text-[var(--text-primary)] transition">{{ $t('nav.data') }}</a>
        <a href="/#cara-kerja" @click="mobileMenuOpen = false" class="hover:text-[var(--text-primary)] transition">{{ $t('nav.how') }}</a>
        <a href="/pricing" @click="mobileMenuOpen = false" class="text-[var(--text-primary)] transition">{{ $t('nav.pricing') }}</a>
        <a href="/#faq" @click="mobileMenuOpen = false" class="hover:text-[var(--text-primary)] transition">{{ $t('nav.faq') }}</a>
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
        <a href="https://app.ixiera.id/signup" class="btn-bd-primary w-full text-center block">{{ $t('nav.signup') }}</a>
        <a href="https://app.ixiera.id/login" class="text-center block text-sm text-[var(--text-secondary)] py-1">{{ $t('nav.login') }}</a>
      </div>
    </div>

    <!-- MAIN CONTENT -->
    <main class="pt-16">
      
      <!-- HERO PRICING -->
      <section class="relative pt-24 pb-12">
        <div class="max-w-[1200px] mx-auto px-6 text-center relative z-10">
          <div class="pill-bd mb-6 mx-auto" style="width: fit-content;">
            <span class="w-1.5 h-1.5 rounded-full" style="background: var(--accent-mint);"></span>
            PUBLIC BETA
          </div>
          
          <h1 class="font-display text-[48px] md:text-[56px] leading-[1.0] mb-6 max-w-[800px] mx-auto text-[var(--text-primary)]">
            {{ $t('pricing.title') }} <br class="hidden md:block">
            <span class="italic text-[var(--accent-violet)]">{{ $t('pricing.subtitle') }}</span>
          </h1>
        </div>
      </section>

      <!-- PRICING CARDS -->
      <section class="pb-20 px-6">
        <div class="max-w-[1000px] mx-auto grid grid-cols-1 md:grid-cols-3 gap-6">
          
          <!-- TRIAL -->
          <div class="card-bd p-7 flex flex-col">
            <h3 class="text-[20px] font-semibold mb-1">{{ $t('pricing.p1_title') }}</h3>
            <p class="text-[13px] mb-6 text-[var(--text-secondary)]">{{ $t('pricing.p1_desc') }}</p>
            
            <div class="mb-6 flex items-baseline gap-1">
              <span class="text-[40px] font-bold leading-none">{{ $t('pricing.p1_price') }}</span>
              <span class="text-[14px] text-[var(--text-muted)]">{{ $t('pricing.p1_period') }}</span>
            </div>

            <ul class="space-y-3 mb-8 flex-1 text-[14px] text-[var(--text-secondary)]">
              <li class="flex items-start gap-2.5">
                <svg class="w-4 h-4 shrink-0 mt-0.5 text-[var(--accent-mint)]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                {{ $t('pricing.p1_f1') }}
              </li>
              <li class="flex items-start gap-2.5">
                <svg class="w-4 h-4 shrink-0 mt-0.5 text-[var(--accent-mint)]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                {{ $t('pricing.p1_f2') }}
              </li>
              <li class="flex items-start gap-2.5">
                <svg class="w-4 h-4 shrink-0 mt-0.5 text-[var(--accent-mint)]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                {{ $t('pricing.p1_f3') }}
              </li>
            </ul>
            <a href="https://app.ixiera.id/signup" class="btn-bd-ghost text-center mt-auto">{{ $t('pricing.p1_cta') }}</a>
          </div>

          <!-- PRO -->
          <div class="card-bd p-7 flex flex-col relative border-2 border-[var(--accent-violet)]">
            <div class="absolute -top-3 left-1/2 -translate-x-1/2 text-[10px] font-bold uppercase tracking-widest px-3 py-1 rounded-full text-white bg-[var(--accent-violet)]">{{ $t('pricing.popular') }}</div>
            <h3 class="text-[20px] font-semibold mb-1">{{ $t('pricing.p2_title') }}</h3>
            <p class="text-[13px] mb-6 text-[var(--text-secondary)]">{{ $t('pricing.p2_desc') }}</p>
            
            <div class="mb-6 flex items-baseline gap-1">
              <span class="text-[40px] font-bold leading-none">{{ $t('pricing.p2_price') }}</span>
              <span class="text-[14px] text-[var(--text-muted)]">{{ $t('pricing.p2_period') }}</span>
            </div>

            <ul class="space-y-3 mb-8 flex-1 text-[14px] text-[var(--text-secondary)]">
              <li class="flex items-start gap-2.5">
                <svg class="w-4 h-4 shrink-0 mt-0.5 text-[var(--accent-mint)]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                {{ $t('pricing.p2_f1') }}
              </li>
              <li class="flex items-start gap-2.5">
                <svg class="w-4 h-4 shrink-0 mt-0.5 text-[var(--accent-mint)]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                {{ $t('pricing.p2_f2') }}
              </li>
              <li class="flex items-start gap-2.5">
                <svg class="w-4 h-4 shrink-0 mt-0.5 text-[var(--accent-mint)]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                {{ $t('pricing.p2_f3') }}
              </li>
              <li class="flex items-start gap-2.5">
                <svg class="w-4 h-4 shrink-0 mt-0.5 text-[var(--accent-mint)]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                {{ $t('pricing.p2_f4') }}
              </li>
            </ul>
            <a href="https://app.ixiera.id/signup" class="btn-bd-primary text-center mt-auto">{{ $t('pricing.p2_cta') }}</a>
          </div>

          <!-- BYOK -->
          <div class="card-bd p-7 flex flex-col">
            <h3 class="text-[20px] font-semibold mb-1">{{ $t('pricing.p3_title') }}</h3>
            <p class="text-[13px] mb-6 text-[var(--text-secondary)]">{{ $t('pricing.p3_desc') }}</p>
            
            <div class="mb-6 flex items-baseline gap-1">
              <span class="text-[40px] font-bold leading-none">{{ $t('pricing.p3_price') }}</span>
              <span class="text-[14px] text-[var(--text-muted)]">{{ $t('pricing.p3_period') }}</span>
            </div>

            <ul class="space-y-3 mb-8 flex-1 text-[14px] text-[var(--text-secondary)]">
              <li class="flex items-start gap-2.5">
                <svg class="w-4 h-4 shrink-0 mt-0.5 text-[var(--accent-mint)]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                {{ $t('pricing.p3_f1') }}
              </li>
              <li class="flex items-start gap-2.5">
                <svg class="w-4 h-4 shrink-0 mt-0.5 text-[var(--accent-mint)]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                {{ $t('pricing.p3_f2') }}
              </li>
              <li class="flex items-start gap-2.5">
                <svg class="w-4 h-4 shrink-0 mt-0.5 text-[var(--accent-mint)]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                {{ $t('pricing.p3_f3') }}
              </li>
            </ul>
            <a href="https://app.ixiera.id/signup" class="btn-bd-ghost text-center mt-auto">{{ $t('pricing.p3_cta') }}</a>
          </div>

        </div>
        
        <div class="max-w-[1000px] mx-auto px-6 mt-10 text-center space-y-2">
          <p class="text-[12px] text-[var(--text-muted)]">{{ $t('pricing.note1') }}</p>
          <p class="text-[12px] font-medium text-[var(--text-secondary)]">{{ $t('pricing.note2') }}</p>
        </div>
      </section>

      <!-- FAQ HARGA -->
      <section class="py-20 border-t border-[var(--border)] bg-[var(--bg-secondary)]">
        <div class="max-w-[800px] mx-auto px-6">
          <h2 class="h2-bd">{{ $t('pricing.faq_title') }}</h2>
          <div class="border-t border-[var(--border)] mt-8">
            <details class="group border-b border-[var(--border)] py-5 cursor-pointer">
              <summary class="flex justify-between items-center text-[16px] font-semibold list-none text-[var(--text-primary)]">
                {{ $t('pricing.faq1_q') }}
                <span class="group-open:rotate-180 transition"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <p class="text-[14px] mt-3 leading-relaxed text-[var(--text-secondary)]">{{ $t('pricing.faq1_a') }}</p>
            </details>
            <details class="group border-b border-[var(--border)] py-5 cursor-pointer">
              <summary class="flex justify-between items-center text-[16px] font-semibold list-none text-[var(--text-primary)]">
                {{ $t('pricing.faq2_q') }}
                <span class="group-open:rotate-180 transition"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <p class="text-[14px] mt-3 leading-relaxed text-[var(--text-secondary)]">{{ $t('pricing.faq2_a') }}</p>
            </details>
            <details class="group border-b border-[var(--border)] py-5 cursor-pointer">
              <summary class="flex justify-between items-center text-[16px] font-semibold list-none text-[var(--text-primary)]">
                {{ $t('pricing.faq3_q') }}
                <span class="group-open:rotate-180 transition"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <p class="text-[14px] mt-3 leading-relaxed text-[var(--text-secondary)]">{{ $t('pricing.faq3_a') }}</p>
            </details>
            <details class="group border-b border-[var(--border)] py-5 cursor-pointer">
              <summary class="flex justify-between items-center text-[16px] font-semibold list-none text-[var(--text-primary)]">
                {{ $t('pricing.faq4_q') }}
                <span class="group-open:rotate-180 transition"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <p class="text-[14px] mt-3 leading-relaxed text-[var(--text-secondary)]">{{ $t('pricing.faq4_a') }}</p>
            </details>
          </div>
        </div>
      </section>

      <!-- FINAL CTA -->
      <section class="py-24 text-center border-t border-[var(--border)]">
        <div class="max-w-[800px] mx-auto px-6">
          <h2 class="font-display text-[40px] md:text-[56px] leading-[1.0] mb-8">{{ $t('cta.title') }}</h2>
          <a href="https://app.ixiera.id/signup" class="btn-bd-primary inline-block">{{ $t('cta.btn') }}</a>
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
