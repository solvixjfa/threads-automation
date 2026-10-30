<template>
  <div class="min-h-screen theme-bg theme-text font-sans selection:bg-[var(--accent)] selection:text-white">
    
    <!-- NAVBAR (Diperbaiki, solid gak transparan) -->
    <nav class="fixed top-0 w-full z-50 border-b theme-border bg-[var(--bg)] shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <!-- Logo -->
          <div class="flex-shrink-0 flex items-center gap-2">
            <div class="w-8 h-8 flex items-center justify-center rounded-lg text-sm font-black theme-accent">IX</div>
            <span class="font-bold text-xl tracking-tight">Ixiera</span>
          </div>
          
          <!-- Desktop Menu -->
          <div class="hidden md:flex items-center space-x-8">
            <a href="#fitur" class="text-sm font-medium theme-text-muted hover:theme-text transition-colors">Fitur</a>
            <a href="#cara-kerja" class="text-sm font-medium theme-text-muted hover:theme-text transition-colors">Cara Kerja</a>
            <a href="#faq" class="text-sm font-medium theme-text-muted hover:theme-text transition-colors">FAQ</a>
          </div>

          <!-- Actions -->
          <div class="hidden md:flex items-center space-x-4">
            <button @click="toggleTheme" class="p-2 rounded-lg theme-text-muted hover:theme-text hover:bg-[var(--bg-sec)] transition">
              <Sun v-if="theme === 'dark'" class="w-5 h-5" />
              <Moon v-else class="w-5 h-5" />
            </button>
            <div class="flex items-center bg-[var(--bg-sec)] rounded-lg p-1 border theme-border">
              <button @click="changeLang('id')" :class="locale === 'id' ? 'theme-text font-bold bg-[var(--bg)] shadow-sm' : 'theme-text-muted'" class="px-2 py-1 text-xs rounded transition-all">ID</button>
              <button @click="changeLang('en')" :class="locale === 'en' ? 'theme-text font-bold bg-[var(--bg)] shadow-sm' : 'theme-text-muted'" class="px-2 py-1 text-xs rounded transition-all">EN</button>
            </div>
            <RouterLink to="/login" class="text-sm font-medium theme-text-muted hover:theme-text transition-colors">{{ $t('landing.nav.login') }}</RouterLink>
            <button @click="showAccessModal = true" class="btn btn-primary btn-sm rounded-full px-5">{{ $t('landing.nav.start_free') }}</button>
          </div>

          <!-- Mobile Menu Button -->
          <div class="flex md:hidden items-center gap-2">
             <button @click="toggleTheme" class="p-2 rounded-lg theme-text-muted hover:theme-text transition">
              <Sun v-if="theme === 'dark'" class="w-5 h-5" />
              <Moon v-else class="w-5 h-5" />
            </button>
            <div class="flex items-center bg-[var(--bg-sec)] rounded-lg p-1 border theme-border">
              <button @click="changeLang('id')" :class="locale === 'id' ? 'theme-text font-bold bg-[var(--bg)] shadow-sm' : 'theme-text-muted'" class="px-2 py-1 text-[10px] rounded transition-all">ID</button>
              <button @click="changeLang('en')" :class="locale === 'en' ? 'theme-text font-bold bg-[var(--bg)] shadow-sm' : 'theme-text-muted'" class="px-2 py-1 text-[10px] rounded transition-all">EN</button>
            </div>
            <button @click="mobileMenuOpen = !mobileMenuOpen" class="theme-text-muted hover:theme-text p-2">
              <Menu v-if="!mobileMenuOpen" class="w-6 h-6" />
              <X v-else class="w-6 h-6" />
            </button>
          </div>
        </div>
      </div>

      <!-- Mobile Menu Dropdown -->
      <div v-if="mobileMenuOpen" class="md:hidden border-t theme-border bg-[var(--bg)]">
        <div class="px-4 pt-2 pb-4 space-y-1">
          <a href="#fitur" @click="mobileMenuOpen = false" class="block px-3 py-2 rounded-md text-base font-medium theme-text-muted hover:theme-text hover:bg-[var(--bg-sec)]">Fitur</a>
          <a href="#cara-kerja" @click="mobileMenuOpen = false" class="block px-3 py-2 rounded-md text-base font-medium theme-text-muted hover:theme-text hover:bg-[var(--bg-sec)]">Cara Kerja</a>
          <a href="#faq" @click="mobileMenuOpen = false" class="block px-3 py-2 rounded-md text-base font-medium theme-text-muted hover:theme-text hover:bg-[var(--bg-sec)]">FAQ</a>
          <div class="pt-4 border-t theme-border mt-2 flex flex-col gap-2">
            <RouterLink to="/login" class="btn btn-secondary w-full">{{ $t('landing.nav.login') }}</RouterLink>
            <button @click="showAccessModal = true" class="btn btn-primary w-full">{{ $t('landing.nav.start_free') }}</button>
          </div>
        </div>
      </div>
    </nav>

    <!-- HERO SECTION (Fokus USP & Pain Point) -->
    <section class="pt-32 pb-20 lg:pt-40 lg:pb-28 px-4 sm:px-6 lg:px-8 relative overflow-hidden flex flex-col items-center text-center">
      
      <!-- Background Glow Elegan (Bukan kotak-kotak) -->
      <div class="absolute top-1/4 left-1/2 -translate-x-1/2 w-[800px] h-[500px] rounded-full blur-[120px] opacity-20 pointer-events-none" style="background: radial-gradient(circle, var(--accent) 0%, transparent 70%);"></div>
      
      <div class="max-w-4xl mx-auto relative z-10 space-y-6">
        <div class="inline-flex items-center px-3 py-1 rounded-full border theme-border text-xs font-medium theme-text-muted" style="background: var(--bg-sec);">
          {{ $t('landing.hero.badge') }}
        </div>
        
        <h1 class="text-4xl sm:text-5xl lg:text-7xl font-extrabold tracking-tight leading-tight">
          Berhenti Menghabiskan 3 Jam Sehari<br/>
          <span style="color: var(--accent);">Hanya untuk Mengurus Threads.</span>
        </h1>
        
        <p class="mt-4 text-lg sm:text-xl theme-text-muted max-w-2xl mx-auto leading-relaxed">
          Ixiera adalah asisten AI yang menjadwalkan konten, membalas komentar dengan sopan, dan menganalisis audiens Anda secara otomatis. Fokus pada karyamu, biarkan sistem yang bekerja.
        </p>

        <div class="mt-8 flex flex-col sm:flex-row gap-4 justify-center">
          <button @click="showAccessModal = true" class="btn btn-primary px-8 py-3 rounded-xl text-base shadow-lg hover:shadow-xl hover:-translate-y-0.5 transition-all flex items-center justify-center gap-2">
            {{ $t('landing.hero.cta_primary') }}
            <ArrowRight class="w-4 h-4" />
          </button>
          <a href="#fitur" class="btn btn-secondary px-8 py-3 rounded-xl text-base flex items-center justify-center">
            {{ $t('landing.hero.cta_secondary') }}
          </a>
        </div>
        
        <div class="flex items-center justify-center gap-6 pt-6 text-xs theme-text-muted">
          <span class="flex items-center gap-2"><CheckCircle class="w-4 h-4 text-green-500"/> Tanpa Kartu Kredit</span>
          <span class="flex items-center gap-2"><CheckCircle class="w-4 h-4 text-green-500"/> Setup 2 Menit</span>
          <span class="flex items-center gap-2"><CheckCircle class="w-4 h-4 text-green-500"/> Aman</span>
        </div>
      </div>
    </section>

    <!-- FITUR SECTION (Fokus Manfaat / Benefit, Bukan Jargon) -->
    <section id="fitur" class="py-20 border-t theme-border" style="background: var(--bg-sec);">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center max-w-3xl mx-auto mb-16">
          <h2 class="text-3xl sm:text-4xl font-bold tracking-tight">Kenapa Anda Harus Pakai Ixiera?</h2>
          <p class="mt-4 text-lg theme-text-muted">Bukan sekadar penjadwal. Ini adalah tim CS dan Copywriter AI pribadi Anda.</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <!-- Benefit 1 -->
          <div class="p-8 rounded-2xl border theme-border hover:border-[var(--accent)] transition-colors bg-[var(--bg)] shadow-sm">
            <div class="w-12 h-12 rounded-lg flex items-center justify-center mb-6" style="background: color-mix(in srgb, var(--accent) 15%, transparent); color: var(--accent);">
              <PenTool class="w-6 h-6" />
            </div>
            <h3 class="text-xl font-bold mb-3">Ide Konten 30 Hari ke Depan</h3>
            <p class="theme-text-muted leading-relaxed text-sm">
              Berhenti pusing memikirkan mau posting apa. Cukup berikan satu topik, AI kami akan membuat rencana konten (Content Plan) yang terstruktur dan tidak membosankan.
            </p>
          </div>

          <!-- Benefit 2 -->
          <div class="p-8 rounded-2xl border theme-border hover:border-[var(--success)] transition-colors bg-[var(--bg)] shadow-sm">
            <div class="w-12 h-12 rounded-lg flex items-center justify-center mb-6" style="background: color-mix(in srgb, var(--success) 15%, transparent); color: var(--success);">
              <MessageCircle class="w-6 h-6" />
            </div>
            <h3 class="text-xl font-bold mb-3">Balas Komentar 24/7 Tanpa Terdengar Kaku</h3>
            <p class="theme-text-muted leading-relaxed text-sm">
              Pelanggan atau audiens yang komplain bisa langsung ditangani. AI kami mempelajari gaya bahasa brand Anda, sehingga balasannya terasa manusiawi dan sopan.
            </p>
          </div>

          <!-- Benefit 3 -->
          <div class="p-8 rounded-2xl border theme-border hover:border-[var(--warning)] transition-colors bg-[var(--bg)] shadow-sm">
            <div class="w-12 h-12 rounded-lg flex items-center justify-center mb-6" style="background: color-mix(in srgb, var(--warning) 15%, transparent); color: var(--warning);">
              <BarChart3 class="w-6 h-6" />
            </div>
            <h3 class="text-xl font-bold mb-3">Posting di Jam Emas (Best Time)</h3>
            <p class="theme-text-muted leading-relaxed text-sm">
              Tidak semua jam efektif. Sistem Machine Learning kami mempelajari kapan audiens Anda paling aktif, sehingga konten Anda mendapatkan tayangan (views) maksimal.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- CARA KERJA SECTION -->
    <section id="cara-kerja" class="py-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center max-w-2xl mx-auto mb-16">
          <h2 class="text-3xl sm:text-4xl font-bold tracking-tight">Mulai dalam 3 Langkah Sederhana</h2>
          <p class="mt-4 text-lg theme-text-muted">Tanpa perlu keahlian teknis. Anda bisa langsung menghemat waktu dalam hitungan menit.</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 relative">
          <div class="text-center relative">
            <div class="w-16 h-16 mx-auto rounded-full flex items-center justify-center text-2xl font-bold mb-6 border-4" style="background: var(--bg-sec); border-color: var(--bg); color: var(--accent); z-index: 10; position: relative;">1</div>
            <h3 class="text-lg font-bold mb-2">{{ $t('landing.how.s1_title') }}</h3>
            <p class="theme-text-muted text-sm px-4">{{ $t('landing.how.s1_desc') }}</p>
          </div>
          <div class="text-center relative">
            <div class="w-16 h-16 mx-auto rounded-full flex items-center justify-center text-2xl font-bold mb-6 border-4" style="background: var(--bg-sec); border-color: var(--bg); color: var(--accent); z-index: 10; position: relative;">2</div>
            <h3 class="text-lg font-bold mb-2">{{ $t('landing.how.s2_title') }}</h3>
            <p class="theme-text-muted text-sm px-4">{{ $t('landing.how.s2_desc') }}</p>
          </div>
          <div class="text-center relative">
            <div class="w-16 h-16 mx-auto rounded-full flex items-center justify-center text-2xl font-bold mb-6 border-4" style="background: var(--bg-sec); border-color: var(--bg); color: var(--accent); z-index: 10; position: relative;">3</div>
            <h3 class="text-lg font-bold mb-2">{{ $t('landing.how.s3_title') }}</h3>
            <p class="theme-text-muted text-sm px-4">{{ $t('landing.how.s3_desc') }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- FAQ SECTION -->
    <section id="faq" class="py-20 border-t theme-border bg-[var(--bg-sec)]">
      <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold tracking-tight">{{ $t('landing.faq.title') }}</h2>
        </div>
        <div class="space-y-4">
          <!-- Q1 -->
          <div class="border theme-border rounded-xl overflow-hidden bg-[var(--bg)]">
            <button @click="faqOpen = faqOpen === 1 ? null : 1" class="w-full px-6 py-4 text-left flex justify-between items-center font-bold">
              <span>{{ $t('landing.faq.q1') }}</span>
              <ChevronDown class="w-5 h-5 transition-transform" :class="{'rotate-180': faqOpen === 1}" />
            </button>
            <div v-if="faqOpen === 1" class="px-6 pb-4 text-sm theme-text-muted leading-relaxed">
              {{ $t('landing.faq.a1') }}
            </div>
          </div>
          <!-- Q2 -->
          <div class="border theme-border rounded-xl overflow-hidden bg-[var(--bg)]">
            <button @click="faqOpen = faqOpen === 2 ? null : 2" class="w-full px-6 py-4 text-left flex justify-between items-center font-bold">
              <span>{{ $t('landing.faq.q2') }}</span>
              <ChevronDown class="w-5 h-5 transition-transform" :class="{'rotate-180': faqOpen === 2}" />
            </button>
            <div v-if="faqOpen === 2" class="px-6 pb-4 text-sm theme-text-muted leading-relaxed">
              {{ $t('landing.faq.a2') }}
            </div>
          </div>
          <!-- Q3 -->
          <div class="border theme-border rounded-xl overflow-hidden bg-[var(--bg)]">
            <button @click="faqOpen = faqOpen === 3 ? null : 3" class="w-full px-6 py-4 text-left flex justify-between items-center font-bold">
              <span>{{ $t('landing.faq.q3') }}</span>
              <ChevronDown class="w-5 h-5 transition-transform" :class="{'rotate-180': faqOpen === 3}" />
            </button>
            <div v-if="faqOpen === 3" class="px-6 pb-4 text-sm theme-text-muted leading-relaxed">
              {{ $t('landing.faq.a3') }}
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA SECTION -->
    <section class="py-24 text-center px-4">
      <div class="max-w-3xl mx-auto space-y-8">
        <h2 class="text-3xl sm:text-4xl font-bold tracking-tight">{{ $t('landing.cta.title') }}</h2>
        <p class="text-lg theme-text-muted max-w-xl mx-auto">{{ $t('landing.cta.subtitle') }}</p>
        <button @click="showAccessModal = true" class="btn btn-primary inline-flex items-center gap-2 px-10 py-4 rounded-xl text-lg font-bold shadow-lg hover:-translate-y-1 transition-transform">
          {{ $t('landing.cta.button') }}
          <ArrowRight class="w-5 h-5" />
        </button>
      </div>
    </section>

    <!-- FOOTER -->
    <footer class="py-6 border-t theme-border text-center">
      <p class="text-sm theme-text-muted">&copy; 2026 Ixiera.</p>
    </footer>

    <!-- MODAL DEVELOPER MODE / EARLY ACCESS -->
    <Teleport to="body">
      <div v-if="showAccessModal" class="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
        <div class="card max-w-md w-full p-6 space-y-4 shadow-2xl bg-[var(--bg)]">
          <div class="flex justify-between items-center">
            <h3 class="text-lg font-bold">{{ $t('landing.modal.title') }}</h3>
            <button @click="showAccessModal = false" class="theme-text-muted hover:theme-text"><X class="w-5 h-5" /></button>
          </div>
          <p class="text-sm theme-text-muted leading-relaxed">{{ $t('landing.modal.desc') }}</p>
          <div class="pt-2 flex justify-end gap-3">
            <button @click="showAccessModal = false" class="btn btn-secondary">Batal</button>
            <RouterLink to="/login" class="btn btn-primary">{{ $t('landing.modal.cta') }}</RouterLink>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useTheme } from '../composables/useTheme'
import { Menu, X, ArrowRight, PenTool, MessageCircle, BarChart3, Sun, Moon, ChevronDown, CheckCircle } from 'lucide-vue-next'

const mobileMenuOpen = ref(false)
const showAccessModal = ref(false)
const faqOpen = ref<number | null>(1)
const { locale } = useI18n()
const { theme, toggle: toggleTheme } = useTheme()

function changeLang(lang: string) {
  locale.value = lang
  localStorage.setItem('app_lang', lang)
}
</script>
