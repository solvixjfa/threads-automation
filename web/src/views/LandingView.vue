<template>
  <div class="min-h-screen theme-bg theme-text font-sans selection:bg-[var(--accent)] selection:text-white">
    
    <!-- NAVBAR -->
    <nav class="fixed top-0 w-full z-50 border-b theme-border backdrop-blur-md" style="background: color-mix(in srgb, var(--bg) 90%, transparent);">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <!-- Logo -->
          <div class="flex-shrink-0 flex items-center gap-2">
            <div class="w-8 h-8 flex items-center justify-center rounded-lg text-sm font-black theme-accent">IX</div>
            <span class="font-bold text-xl tracking-tight">Ixiera</span>
          </div>
          
          <!-- Desktop Menu -->
          <div class="hidden md:flex items-center space-x-8">
            <a href="#fitur" class="text-sm font-medium theme-text-muted hover:theme-text transition-colors">{{ $t('landing.nav.features') }}</a>
            <a href="#cara-kerja" class="text-sm font-medium theme-text-muted hover:theme-text transition-colors">{{ $t('landing.nav.how_it_works') }}</a>
            <a href="#faq" class="text-sm font-medium theme-text-muted hover:theme-text transition-colors">{{ $t('landing.nav.faq') }}</a>
          </div>

          <!-- Actions -->
          <div class="hidden md:flex items-center space-x-4">
            <!-- Theme Toggle -->
            <button @click="toggleTheme" class="p-2 rounded-lg theme-text-muted hover:theme-text hover:bg-[var(--bg-sec)] transition">
              <Sun v-if="theme === 'dark'" class="w-5 h-5" />
              <Moon v-else class="w-5 h-5" />
            </button>

            <!-- Language Switcher Desktop -->
            <div class="flex items-center bg-[var(--bg-sec)] rounded-lg p-1 border theme-border">
              <button @click="changeLang('id')" :class="locale === 'id' ? 'theme-text font-bold bg-[var(--bg)] shadow-sm' : 'theme-text-muted'" class="px-2 py-1 text-xs rounded transition-all">ID</button>
              <button @click="changeLang('en')" :class="locale === 'en' ? 'theme-text font-bold bg-[var(--bg)] shadow-sm' : 'theme-text-muted'" class="px-2 py-1 text-xs rounded transition-all">EN</button>
            </div>
            <RouterLink to="/login" class="text-sm font-medium theme-text-muted hover:theme-text transition-colors">{{ $t('landing.nav.login') }}</RouterLink>
            <button @click="showAccessModal = true" class="btn btn-primary btn-sm rounded-full px-5">{{ $t('landing.nav.start_free') }}</button>
          </div>

          <!-- Mobile Menu Button -->
          <div class="flex md:hidden items-center gap-2">
             <!-- Theme Toggle Mobile -->
             <button @click="toggleTheme" class="p-2 rounded-lg theme-text-muted hover:theme-text transition">
              <Sun v-if="theme === 'dark'" class="w-5 h-5" />
              <Moon v-else class="w-5 h-5" />
            </button>

            <!-- Lang Switcher Mobile -->
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
      <div v-if="mobileMenuOpen" class="md:hidden border-t theme-border" style="background: var(--bg);">
        <div class="px-4 pt-2 pb-4 space-y-1">
          <a href="#fitur" @click="mobileMenuOpen = false" class="block px-3 py-2 rounded-md text-base font-medium theme-text-muted hover:theme-text hover:theme-bg-sec">{{ $t('landing.nav.features') }}</a>
          <a href="#cara-kerja" @click="mobileMenuOpen = false" class="block px-3 py-2 rounded-md text-base font-medium theme-text-muted hover:theme-text hover:theme-bg-sec">{{ $t('landing.nav.how_it_works') }}</a>
          <a href="#faq" @click="mobileMenuOpen = false" class="block px-3 py-2 rounded-md text-base font-medium theme-text-muted hover:theme-text hover:theme-bg-sec">{{ $t('landing.nav.faq') }}</a>
          <div class="pt-4 border-t theme-border mt-2 flex flex-col gap-2">
            <RouterLink to="/login" class="btn btn-secondary w-full">{{ $t('landing.nav.login') }}</RouterLink>
            <button @click="showAccessModal = true" class="btn btn-primary w-full">{{ $t('landing.nav.start_free') }}</button>
          </div>
        </div>
      </div>
    </nav>

    <!-- HERO SECTION (Diperbaiki padding top-nya) -->
    <section class="pt-40 pb-20 lg:pt-48 lg:pb-28 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
      <div class="absolute inset-0 z-0 opacity-[0.03]" style="background-image: radial-gradient(var(--text) 1px, transparent 1px); background-size: 32px 32px;"></div>
      
      <div class="max-w-7xl mx-auto relative z-10">
        <div class="lg:grid lg:grid-cols-12 lg:gap-8 items-center">
          
          <!-- Text Content -->
          <div class="lg:col-span-6 text-center lg:text-left space-y-6">
            <!-- BADGE SIMPEL -->
            <div class="inline-flex items-center px-3 py-1 rounded-full border theme-border text-xs font-medium theme-text-muted" style="background: var(--bg-sec);">
              {{ $t('landing.hero.badge') }}
            </div>
            
            <h1 class="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight leading-tight">
              {{ $t('landing.hero.title_1') }}<br/>
              <span style="color: var(--accent);">{{ $t('landing.hero.title_2') }}</span>
            </h1>
            
            <p class="mt-4 text-lg sm:text-xl theme-text-muted max-w-2xl mx-auto lg:mx-0">
              {{ $t('landing.hero.subtitle') }}
            </p>

            <div class="mt-8 flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
              <button @click="showAccessModal = true" class="btn btn-primary px-8 py-3 rounded-xl text-base shadow-lg hover:shadow-xl transition-all flex items-center justify-center gap-2">
                {{ $t('landing.hero.cta_primary') }}
                <ArrowRight class="w-4 h-4" />
              </button>
              <a href="#fitur" class="btn btn-secondary px-8 py-3 rounded-xl text-base flex items-center justify-center">
                {{ $t('landing.hero.cta_secondary') }}
              </a>
            </div>
            
            <p class="text-sm theme-text-muted mt-4">{{ $t('landing.hero.no_cc') }}</p>
          </div>

          <!-- Mockup Visual (DIPERBAIKI BIAR GAK RUSAK) -->
          <div class="mt-16 lg:mt-0 lg:col-span-6 relative">
            <div class="absolute -inset-1 rounded-2xl blur-2xl opacity-10" style="background: var(--accent);"></div>
            <div class="relative rounded-2xl border theme-border shadow-2xl overflow-hidden bg-[var(--bg-sec)]">
              <!-- Window Bar -->
              <div class="h-10 border-b theme-border flex items-center px-4 gap-2 bg-[var(--bg)]">
                <div class="w-3 h-3 rounded-full bg-red-400"></div>
                <div class="w-3 h-3 rounded-full bg-amber-400"></div>
                <div class="w-3 h-3 rounded-full bg-green-400"></div>
              </div>
              
              <!-- Mockup Content -->
              <div class="flex h-[350px] sm:h-[450px]">
                <!-- Fake Sidebar -->
                <div class="w-16 md:w-48 border-r theme-border p-3 sm:p-4 space-y-4 hidden sm:block bg-[var(--bg)]">
                  <div class="flex items-center gap-2 opacity-40">
                    <div class="w-6 h-6 rounded bg-black dark:bg-white"></div>
                    <div class="h-3 w-16 rounded bg-black dark:bg-white"></div>
                  </div>
                  <div class="space-y-2 pt-4">
                    <div class="h-8 w-full rounded bg-black dark:bg-white opacity-10"></div>
                    <div class="h-8 w-full rounded bg-black dark:bg-white opacity-[0.03]"></div>
                    <div class="h-8 w-full rounded bg-black dark:bg-white opacity-[0.03]"></div>
                  </div>
                </div>
                
                <!-- Fake Main Content -->
                <div class="flex-1 p-4 sm:p-6 flex flex-col gap-4 bg-[var(--bg-sec)]">
                  <div class="flex justify-between items-center">
                    <div class="h-4 w-24 rounded bg-black dark:bg-white opacity-20"></div>
                    <div class="h-6 w-20 rounded bg-[var(--accent)] opacity-80"></div>
                  </div>
                  <div class="grid grid-cols-2 gap-3">
                    <div class="p-3 rounded-lg border theme-border bg-[var(--bg)]">
                      <div class="h-2 w-10 rounded bg-black dark:bg-white opacity-20 mb-2"></div>
                      <div class="h-5 w-16 rounded bg-black dark:bg-white opacity-60"></div>
                    </div>
                    <div class="p-3 rounded-lg border theme-border bg-[var(--bg)]">
                      <div class="h-2 w-10 rounded bg-black dark:bg-white opacity-20 mb-2"></div>
                      <div class="h-5 w-16 rounded bg-black dark:bg-white opacity-60"></div>
                    </div>
                  </div>
                  <div class="flex-1 rounded-xl border theme-border p-3 flex items-end gap-1.5 bg-[var(--bg)]">
                     <div v-for="i in 15" :key="i" class="flex-1 rounded-t bg-[var(--accent)] opacity-60 hover:opacity-100 transition-opacity" :style="{ height: (15 + Math.random() * 85) + '%' }"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </section>

    <!-- FITUR SECTION -->
    <section id="fitur" class="py-20 border-t theme-border bg-[var(--bg-sec)]">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center max-w-3xl mx-auto mb-16">
          <h2 class="text-3xl sm:text-4xl font-bold tracking-tight">{{ $t('landing.features.title') }}</h2>
          <p class="mt-4 text-lg theme-text-muted">{{ $t('landing.features.subtitle') }}</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="p-8 rounded-2xl border theme-border hover:border-current transition-colors bg-[var(--bg)]">
            <div class="w-12 h-12 rounded-lg flex items-center justify-center mb-6" style="background: color-mix(in srgb, var(--accent) 15%, transparent); color: var(--accent);">
              <PenTool class="w-6 h-6" />
            </div>
            <h3 class="text-xl font-bold mb-3">{{ $t('landing.features.f1_title') }}</h3>
            <p class="theme-text-muted leading-relaxed">{{ $t('landing.features.f1_desc') }}</p>
          </div>

          <div class="p-8 rounded-2xl border theme-border hover:border-current transition-colors bg-[var(--bg)]">
            <div class="w-12 h-12 rounded-lg flex items-center justify-center mb-6" style="background: color-mix(in srgb, var(--success) 15%, transparent); color: var(--success);">
              <MessageCircle class="w-6 h-6" />
            </div>
            <h3 class="text-xl font-bold mb-3">{{ $t('landing.features.f2_title') }}</h3>
            <p class="theme-text-muted leading-relaxed">{{ $t('landing.features.f2_desc') }}</p>
          </div>

          <div class="p-8 rounded-2xl border theme-border hover:border-current transition-colors bg-[var(--bg)]">
            <div class="w-12 h-12 rounded-lg flex items-center justify-center mb-6" style="background: color-mix(in srgb, var(--warning) 15%, transparent); color: var(--warning);">
              <BarChart3 class="w-6 h-6" />
            </div>
            <h3 class="text-xl font-bold mb-3">{{ $t('landing.features.f3_title') }}</h3>
            <p class="theme-text-muted leading-relaxed">{{ $t('landing.features.f3_desc') }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CARA KERJA SECTION -->
    <section id="cara-kerja" class="py-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center max-w-2xl mx-auto mb-16">
          <h2 class="text-3xl sm:text-4xl font-bold tracking-tight">{{ $t('landing.how.title') }}</h2>
          <p class="mt-4 text-lg theme-text-muted">{{ $t('landing.how.subtitle') }}</p>
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

    <!-- FOOTER (DIBERSIHKAN) -->
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
import { Menu, X, ArrowRight, PenTool, MessageCircle, BarChart3, Sun, Moon, ChevronDown } from 'lucide-vue-next'

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
