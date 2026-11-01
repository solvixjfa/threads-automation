<template>
  <div class="min-h-screen theme-bg theme-text font-sans selection:bg-black selection:text-white dark:selection:bg-white dark:selection:text-black">
    
    <!-- NAVBAR -->
    <nav class="fixed top-0 w-full z-50 border-b theme-border bg-[var(--bg)] shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <div class="flex-shrink-0 flex items-center gap-2">
            <div class="w-8 h-8 flex items-center justify-center rounded-lg text-sm font-black bg-black text-white dark:bg-white dark:text-black">IX</div>
            <span class="font-bold text-xl tracking-tight">Ixiera</span>
          </div>
          
          <div class="hidden md:flex items-center space-x-8">
            <a href="#fitur" class="text-sm font-medium theme-text-muted hover:theme-text transition-colors">{{ $t('landing.nav.features') }}</a>
            <a href="#cara-kerja" class="text-sm font-medium theme-text-muted hover:theme-text transition-colors">{{ $t('landing.nav.how_it_works') }}</a>
            <a href="#faq" class="text-sm font-medium theme-text-muted hover:theme-text transition-colors">{{ $t('landing.nav.faq') }}</a>
          </div>

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
            <RouterLink to="/login" class="px-5 py-2 rounded-full text-sm font-bold bg-black text-white hover:bg-gray-800 dark:bg-white dark:text-black dark:hover:bg-gray-200 transition">{{ $t('landing.nav.start_free') }}</RouterLink>
          </div>

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

      <!-- Mobile Menu -->
      <div v-if="mobileMenuOpen" class="md:hidden border-t theme-border bg-[var(--bg)]">
        <div class="px-4 pt-2 pb-4 space-y-1">
          <a href="#fitur" @click="mobileMenuOpen = false" class="block px-3 py-2 rounded-md text-base font-medium theme-text-muted hover:theme-text hover:bg-[var(--bg-sec)]">{{ $t('landing.nav.features') }}</a>
          <a href="#cara-kerja" @click="mobileMenuOpen = false" class="block px-3 py-2 rounded-md text-base font-medium theme-text-muted hover:theme-text hover:bg-[var(--bg-sec)]">{{ $t('landing.nav.how_it_works') }}</a>
          <a href="#faq" @click="mobileMenuOpen = false" class="block px-3 py-2 rounded-md text-base font-medium theme-text-muted hover:theme-text hover:bg-[var(--bg-sec)]">{{ $t('landing.nav.faq') }}</a>
          <div class="pt-4 border-t theme-border mt-2 flex flex-col gap-2">
            <RouterLink to="/login" class="block text-center px-3 py-2 rounded-md text-sm font-medium border theme-border">{{ $t('landing.nav.login') }}</RouterLink>
            <RouterLink to="/login" class="block text-center px-3 py-2 rounded-md text-sm font-bold bg-black text-white dark:bg-white dark:text-black">{{ $t('landing.nav.start_free') }}</RouterLink>
          </div>
        </div>
      </div>
    </nav>

    <!-- HERO -->
    <section class="pt-32 pb-20 lg:pt-40 lg:pb-28 px-4 sm:px-6 lg:px-8 relative overflow-hidden flex flex-col items-center text-center">
      <div class="max-w-4xl mx-auto relative z-10 space-y-6">
        <div class="inline-flex items-center px-3 py-1 rounded-full border theme-border text-xs font-medium theme-text-muted bg-[var(--bg-sec)]">
          {{ $t('landing.hero.badge') }}
        </div>
        
        <h1 class="text-4xl sm:text-5xl lg:text-7xl font-extrabold tracking-tight leading-tight">
          {{ $t('landing.hero.title_1') }}<br/>
          <span class="underline decoration-4 underline-offset-8">{{ $t('landing.hero.title_2') }}</span>
        </h1>
        
        <p class="mt-4 text-lg sm:text-xl theme-text-muted max-w-2xl mx-auto leading-relaxed">
          {{ $t('landing.hero.subtitle') }}
        </p>

        <div class="mt-8 flex flex-col sm:flex-row gap-4 justify-center">
          <RouterLink to="/login" class="px-8 py-3 rounded-xl text-base font-bold bg-black text-white hover:bg-gray-800 dark:bg-white dark:text-black dark:hover:bg-gray-200 transition-all flex items-center justify-center gap-2">
            {{ $t('landing.hero.cta_primary') }}
            <ArrowRight class="w-4 h-4" />
          </RouterLink>
          <a href="#contoh-nyata" class="px-8 py-3 rounded-xl text-base font-bold border theme-border hover:bg-[var(--bg-sec)] transition-colors flex items-center justify-center">
            {{ $t('landing.hero.cta_secondary') }}
          </a>
        </div>
        
        <div class="flex flex-col sm:flex-row items-center justify-center gap-4 sm:gap-6 pt-8 text-xs theme-text-muted">
          <span class="flex items-center gap-2"><CheckCircle class="w-4 h-4 shrink-0"/> {{ $t('landing.hero.trust_1') }}</span>
          <span class="flex items-center gap-2"><CheckCircle class="w-4 h-4 shrink-0"/> {{ $t('landing.hero.trust_2') }}</span>
          <span class="flex items-center gap-2"><CheckCircle class="w-4 h-4 shrink-0"/> {{ $t('landing.hero.trust_3') }}</span>
        </div>
      </div>
    </section>

    <!-- MASALAH -->
    <section class="py-20 border-t theme-border bg-[var(--bg-sec)]">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center max-w-3xl mx-auto mb-16">
          <h2 class="text-3xl sm:text-4xl font-bold tracking-tight">{{ $t('landing.problems.title') }}</h2>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="p-6 text-center space-y-2">
            <div class="w-12 h-12 mx-auto rounded-full flex items-center justify-center mb-4 border theme-border"><X class="w-6 h-6" /></div>
            <h3 class="text-lg font-bold">{{ $t('landing.problems.p1_title') }}</h3>
            <p class="theme-text-muted text-sm">{{ $t('landing.problems.p1_desc') }}</p>
          </div>
          <div class="p-6 text-center space-y-2">
            <div class="w-12 h-12 mx-auto rounded-full flex items-center justify-center mb-4 border theme-border"><X class="w-6 h-6" /></div>
            <h3 class="text-lg font-bold">{{ $t('landing.problems.p2_title') }}</h3>
            <p class="theme-text-muted text-sm">{{ $t('landing.problems.p2_desc') }}</p>
          </div>
          <div class="p-6 text-center space-y-2">
            <div class="w-12 h-12 mx-auto rounded-full flex items-center justify-center mb-4 border theme-border"><X class="w-6 h-6" /></div>
            <h3 class="text-lg font-bold">{{ $t('landing.problems.p3_title') }}</h3>
            <p class="theme-text-muted text-sm">{{ $t('landing.problems.p3_desc') }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- FITUR -->
    <section id="fitur" class="py-20 border-t theme-border">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center max-w-3xl mx-auto mb-16">
          <h2 class="text-3xl sm:text-4xl font-bold tracking-tight">{{ $t('landing.features.title') }}</h2>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div class="p-8 rounded-2xl border theme-border bg-[var(--bg)] shadow-sm flex gap-4">
            <PenTool class="w-8 h-8 shrink-0" />
            <div>
              <h3 class="text-lg font-bold mb-2">{{ $t('landing.features.f1_title') }}</h3>
              <p class="theme-text-muted text-sm leading-relaxed">{{ $t('landing.features.f1_desc') }}</p>
            </div>
          </div>
          <div class="p-8 rounded-2xl border theme-border bg-[var(--bg)] shadow-sm flex gap-4">
            <MessageCircle class="w-8 h-8 shrink-0" />
            <div>
              <h3 class="text-lg font-bold mb-2">{{ $t('landing.features.f2_title') }}</h3>
              <p class="theme-text-muted text-sm leading-relaxed">{{ $t('landing.features.f2_desc') }}</p>
            </div>
          </div>
          <div class="p-8 rounded-2xl border theme-border bg-[var(--bg)] shadow-sm flex gap-4">
            <BarChart3 class="w-8 h-8 shrink-0" />
            <div>
              <h3 class="text-lg font-bold mb-2">{{ $t('landing.features.f3_title') }}</h3>
              <p class="theme-text-muted text-sm leading-relaxed">{{ $t('landing.features.f3_desc') }}</p>
            </div>
          </div>
          <div class="p-8 rounded-2xl border theme-border bg-[var(--bg)] shadow-sm flex gap-4">
            <RotateCcw class="w-8 h-8 shrink-0" />
            <div>
              <h3 class="text-lg font-bold mb-2">{{ $t('landing.features.f4_title') }}</h3>
              <p class="theme-text-muted text-sm leading-relaxed">{{ $t('landing.features.f4_desc') }}</p>
            </div>
          </div>
        </div>
        
        <div class="mt-12 flex flex-wrap justify-center gap-4 text-sm theme-text-muted">
          <span class="flex items-center gap-2"><CheckCircle class="w-4 h-4"/> {{ $t('landing.features.small_1') }}</span>
          <span class="flex items-center gap-2"><CheckCircle class="w-4 h-4"/> {{ $t('landing.features.small_2') }}</span>
          <span class="flex items-center gap-2"><CheckCircle class="w-4 h-4"/> {{ $t('landing.features.small_3') }}</span>
        </div>
      </div>
    </section>

    <!-- CONTOH NYATA -->
    <section id="contoh-nyata" class="py-20 border-t theme-border bg-[var(--bg-sec)]">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-3xl sm:text-4xl font-bold tracking-tight mb-2">{{ $t('landing.examples.title') }}</h2>
          <p class="text-xs theme-text-muted italic">{{ $t('landing.examples.label') }}</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="p-6 rounded-2xl border theme-border bg-[var(--bg)] shadow-lg space-y-4">
            <h3 class="font-bold flex items-center gap-2 text-sm uppercase tracking-wide">
              <Star class="w-4 h-4" /> {{ $t('landing.examples.insight_title') }}
            </h3>
            <p class="text-sm leading-relaxed">{{ $t('landing.examples.insight_desc') }}</p>
          </div>

          <div class="p-6 rounded-2xl border theme-border bg-[var(--bg)] shadow-lg space-y-4">
            <h3 class="font-bold flex items-center gap-2 text-sm uppercase tracking-wide">
              <MessageCircle class="w-4 h-4" /> {{ $t('landing.examples.reply_title') }}
            </h3>
            <div class="space-y-3">
              <p class="text-xs theme-text-muted p-3 rounded-lg bg-[var(--bg-sec)] border theme-border">{{ $t('landing.examples.reply_incoming') }}</p>
              <p class="text-xs p-3 rounded-lg bg-[var(--bg-sec)] border theme-border">{{ $t('landing.examples.reply_outgoing') }}</p>
            </div>
          </div>

          <div class="p-6 rounded-2xl border theme-border bg-[var(--bg)] shadow-lg space-y-4">
            <h3 class="font-bold flex items-center gap-2 text-sm uppercase tracking-wide">
              <RotateCcw class="w-4 h-4" /> {{ $t('landing.examples.repurpose_title') }}
            </h3>
            <p class="text-sm leading-relaxed">{{ $t('landing.examples.repurpose_desc') }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CARA KERJA -->
    <section id="cara-kerja" class="py-20 border-t theme-border">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center max-w-2xl mx-auto mb-16">
          <h2 class="text-3xl sm:text-4xl font-bold tracking-tight">{{ $t('landing.how.title') }}</h2>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="text-center relative">
            <div class="w-16 h-16 mx-auto rounded-full flex items-center justify-center text-2xl font-bold mb-6 border-2 theme-border bg-[var(--bg)] z-10 relative">1</div>
            <h3 class="text-lg font-bold mb-2">{{ $t('landing.how.s1_title') }}</h3>
            <p class="theme-text-muted text-sm px-4">{{ $t('landing.how.s1_desc') }}</p>
          </div>
          <div class="text-center relative">
            <div class="w-16 h-16 mx-auto rounded-full flex items-center justify-center text-2xl font-bold mb-6 border-2 theme-border bg-[var(--bg)] z-10 relative">2</div>
            <h3 class="text-lg font-bold mb-2">{{ $t('landing.how.s2_title') }}</h3>
            <p class="theme-text-muted text-sm px-4">{{ $t('landing.how.s2_desc') }}</p>
          </div>
          <div class="text-center relative">
            <div class="w-16 h-16 mx-auto rounded-full flex items-center justify-center text-2xl font-bold mb-6 border-2 theme-border bg-[var(--bg)] z-10 relative">3</div>
            <h3 class="text-lg font-bold mb-2">{{ $t('landing.how.s3_title') }}</h3>
            <p class="theme-text-muted text-sm px-4">{{ $t('landing.how.s3_desc') }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- KEAMANAN -->
    <section class="py-16 bg-[var(--bg-sec)] border-t theme-border">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 class="text-2xl font-bold mb-8">{{ $t('landing.security.title') }}</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="flex flex-col items-center text-center space-y-2">
            <CheckCircle class="w-8 h-8" />
            <p class="text-sm theme-text-muted">{{ $t('landing.security.s1') }}</p>
          </div>
          <div class="flex flex-col items-center text-center space-y-2">
            <CheckCircle class="w-8 h-8" />
            <p class="text-sm theme-text-muted">{{ $t('landing.security.s2') }}</p>
          </div>
          <div class="flex flex-col items-center text-center space-y-2">
            <CheckCircle class="w-8 h-8" />
            <p class="text-sm theme-text-muted">{{ $t('landing.security.s3') }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- BETA -->
    <section class="py-20 text-center px-4 border-t theme-border">
      <div class="max-w-3xl mx-auto space-y-6">
        <h2 class="text-3xl sm:text-4xl font-bold tracking-tight">{{ $t('landing.beta.title') }}</h2>
        <p class="text-lg theme-text-muted max-w-xl mx-auto">{{ $t('landing.beta.desc') }}</p>
        <RouterLink to="/login" class="inline-flex items-center gap-2 px-10 py-4 rounded-xl text-lg font-bold bg-black text-white hover:bg-gray-800 dark:bg-white dark:text-black dark:hover:bg-gray-200 transition-all mt-4">
          {{ $t('landing.beta.cta') }}
          <ArrowRight class="w-5 h-5" />
        </RouterLink>
      </div>
    </section>

    <!-- FAQ -->
    <section id="faq" class="py-20 border-t theme-border bg-[var(--bg-sec)]">
      <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold tracking-tight">{{ $t('landing.faq.title') }}</h2>
        </div>
        <div class="space-y-4">
          <div v-for="i in 7" :key="i" class="border theme-border rounded-xl overflow-hidden bg-[var(--bg)]">
            <button @click="faqOpen = faqOpen === i ? null : i" class="w-full px-6 py-4 text-left flex justify-between items-center font-bold">
              <span>{{ $t('landing.faq.q' + i) }}</span>
              <ChevronDown class="w-5 h-5 transition-transform" :class="{'rotate-180': faqOpen === i}" />
            </button>
            <div v-if="faqOpen === i" class="px-6 pb-4 text-sm theme-text-muted leading-relaxed">
              {{ $t('landing.faq.a' + i) }}
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA PENUTUP -->
    <section class="py-24 text-center px-4">
      <div class="max-w-3xl mx-auto space-y-8">
        <h2 class="text-3xl sm:text-4xl font-bold tracking-tight">{{ $t('landing.cta.title') }}</h2>
        <RouterLink to="/login" class="inline-flex items-center gap-2 px-10 py-4 rounded-xl text-lg font-bold bg-black text-white hover:bg-gray-800 dark:bg-white dark:text-black dark:hover:bg-gray-200 transition-all">
          {{ $t('landing.cta.button') }}
          <ArrowRight class="w-5 h-5" />
        </RouterLink>
      </div>
    </section>

    <!-- FOOTER -->
    <footer class="py-12 border-t theme-border text-center space-y-4">
      <div class="flex flex-wrap justify-center gap-4 text-xs theme-text-muted">
        <a href="mailto:contact@ixiera.id" class="hover:theme-text transition">Email</a>
        <RouterLink to="/privacy" class="hover:theme-text transition">{{ $t('landing.footer.privacy') }}</RouterLink>
        <RouterLink to="/terms" class="hover:theme-text transition">{{ $t('landing.footer.terms') }}</RouterLink>
        <RouterLink to="/data-deletion" class="hover:theme-text transition">{{ $t('landing.footer.delete') }}</RouterLink>
      </div>
      <p class="text-xs theme-text-muted">&copy; 2026 Ixiera.</p>
      <p class="text-[10px] theme-text-muted max-w-xl mx-auto">{{ $t('landing.footer.copy') }}</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useTheme } from '../composables/useTheme'
import { 
  Menu, X, ArrowRight, Sun, Moon, ChevronDown, CheckCircle,
  PenTool, MessageCircle, BarChart3, RotateCcw, Star
} from 'lucide-vue-next'

const mobileMenuOpen = ref(false)
const faqOpen = ref<number | null>(1)
const { locale } = useI18n()
const { theme, toggle: toggleTheme } = useTheme()

function changeLang(lang: string) {
  locale.value = lang
  localStorage.setItem('app_lang', lang)
}
</script>
