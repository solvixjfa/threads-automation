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
            <!-- Language Switcher Desktop -->
            <div class="flex items-center bg-[var(--bg-sec)] rounded-lg p-1 border theme-border mr-2">
              <button @click="changeLang('id')" :class="locale === 'id' ? 'theme-text font-bold bg-[var(--bg)] shadow-sm' : 'theme-text-muted'" class="px-2 py-1 text-xs rounded transition-all">ID</button>
              <button @click="changeLang('en')" :class="locale === 'en' ? 'theme-text font-bold bg-[var(--bg)] shadow-sm' : 'theme-text-muted'" class="px-2 py-1 text-xs rounded transition-all">EN</button>
            </div>
            <RouterLink to="/login" class="text-sm font-medium theme-text-muted hover:theme-text transition-colors">{{ $t('landing.nav.login') }}</RouterLink>
            <RouterLink to="/login" class="btn btn-primary btn-sm rounded-full px-5">{{ $t('landing.nav.start_free') }}</RouterLink>
          </div>

          <!-- Mobile Menu Button -->
          <div class="flex md:hidden items-center gap-3">
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
            <RouterLink to="/login" class="btn btn-primary w-full">{{ $t('landing.nav.start_free') }}</RouterLink>
          </div>
        </div>
      </div>
    </nav>

    <!-- HERO SECTION -->
    <section class="pt-32 pb-20 lg:pt-40 lg:pb-28 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
      <div class="absolute inset-0 z-0 opacity-[0.03]" style="background-image: radial-gradient(var(--text) 1px, transparent 1px); background-size: 32px 32px;"></div>
      
      <div class="max-w-7xl mx-auto relative z-10">
        <div class="lg:grid lg:grid-cols-12 lg:gap-8 items-center">
          
          <!-- Text Content -->
          <div class="lg:col-span-6 text-center lg:text-left space-y-6">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full border theme-border text-xs font-medium theme-text-muted" style="background: var(--bg-sec);">
              <span class="relative flex h-2 w-2">
                <span class="animate-ping absolute inline-flex h-full w-full rounded-full opacity-75" style="background: var(--success);"></span>
                <span class="relative inline-flex rounded-full h-2 w-2" style="background: var(--success);"></span>
              </span>
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
              <RouterLink to="/login" class="btn btn-primary px-8 py-3 rounded-xl text-base shadow-lg hover:shadow-xl transition-all flex items-center justify-center gap-2">
                {{ $t('landing.hero.cta_primary') }}
                <ArrowRight class="w-4 h-4" />
              </RouterLink>
              <a href="#fitur" class="btn btn-secondary px-8 py-3 rounded-xl text-base flex items-center justify-center">
                {{ $t('landing.hero.cta_secondary') }}
              </a>
            </div>
            
            <p class="text-sm theme-text-muted mt-4">{{ $t('landing.hero.no_cc') }}</p>
          </div>

          <!-- Mockup Visual -->
          <div class="mt-16 lg:mt-0 lg:col-span-6 relative">
            <div class="absolute -inset-1 rounded-2xl blur-2xl opacity-20" style="background: linear-gradient(90deg, var(--accent), var(--success));"></div>
            <div class="relative rounded-2xl border theme-border shadow-2xl overflow-hidden" style="background: var(--bg-sec);">
              <div class="h-10 border-b theme-border flex items-center px-4 gap-2" style="background: var(--bg);">
                <div class="w-3 h-3 rounded-full bg-red-400"></div>
                <div class="w-3 h-3 rounded-full bg-amber-400"></div>
                <div class="w-3 h-3 rounded-full bg-green-400"></div>
              </div>
              <div class="flex h-[350px] sm:h-[450px]">
                <div class="w-16 md:w-48 border-r theme-border p-3 sm:p-4 space-y-4 hidden sm:block" style="background: var(--bg);">
                  <div class="flex items-center gap-2 opacity-50">
                    <div class="w-6 h-6 rounded bg-[var(--text)]"></div>
                    <div class="h-3 w-16 rounded bg-[var(--text)]"></div>
                  </div>
                  <div class="space-y-2 pt-4">
                    <div class="h-8 w-full rounded bg-[var(--accent)] opacity-10"></div>
                    <div class="h-8 w-full rounded bg-[var(--bg-sec)]"></div>
                    <div class="h-8 w-full rounded bg-[var(--bg-sec)]"></div>
                  </div>
                </div>
                <div class="flex-1 p-4 sm:p-6 flex flex-col gap-4">
                  <div class="flex justify-between items-center">
                    <div class="h-4 w-24 rounded bg-[var(--text)] opacity-20"></div>
                    <div class="h-6 w-20 rounded bg-[var(--accent)] opacity-80"></div>
                  </div>
                  <div class="grid grid-cols-2 gap-3">
                    <div class="p-3 rounded-lg border theme-border" style="background: var(--bg);">
                      <div class="h-2 w-10 rounded bg-[var(--text)] opacity-20 mb-2"></div>
                      <div class="h-5 w-16 rounded bg-[var(--text)] opacity-60"></div>
                    </div>
                    <div class="p-3 rounded-lg border theme-border" style="background: var(--bg);">
                      <div class="h-2 w-10 rounded bg-[var(--text)] opacity-20 mb-2"></div>
                      <div class="h-5 w-16 rounded bg-[var(--text)] opacity-60"></div>
                    </div>
                  </div>
                  <div class="flex-1 rounded-xl border theme-border p-3 flex items-end gap-1.5" style="background: var(--bg);">
                     <div v-for="i in 15" :key="i" class="flex-1 rounded-t bg-[var(--accent)] opacity-40 hover:opacity-100 transition-opacity" :style="{ height: (15 + Math.random() * 85) + '%' }"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </section>

    <!-- FITUR SECTION -->
    <section id="fitur" class="py-20 border-t theme-border" style="background: var(--bg-sec);">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center max-w-3xl mx-auto mb-16">
          <h2 class="text-3xl sm:text-4xl font-bold tracking-tight">{{ $t('landing.features.title') }}</h2>
          <p class="mt-4 text-lg theme-text-muted">{{ $t('landing.features.subtitle') }}</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="p-8 rounded-2xl border theme-border hover:border-current transition-colors" style="background: var(--bg);">
            <div class="w-12 h-12 rounded-lg flex items-center justify-center mb-6" style="background: color-mix(in srgb, var(--accent) 15%, transparent); color: var(--accent);">
              <PenTool class="w-6 h-6" />
            </div>
            <h3 class="text-xl font-bold mb-3">{{ $t('landing.features.f1_title') }}</h3>
            <p class="theme-text-muted leading-relaxed">{{ $t('landing.features.f1_desc') }}</p>
          </div>

          <div class="p-8 rounded-2xl border theme-border hover:border-current transition-colors" style="background: var(--bg);">
            <div class="w-12 h-12 rounded-lg flex items-center justify-center mb-6" style="background: color-mix(in srgb, var(--success) 15%, transparent); color: var(--success);">
              <MessageCircle class="w-6 h-6" />
            </div>
            <h3 class="text-xl font-bold mb-3">{{ $t('landing.features.f2_title') }}</h3>
            <p class="theme-text-muted leading-relaxed">{{ $t('landing.features.f2_desc') }}</p>
          </div>

          <div class="p-8 rounded-2xl border theme-border hover:border-current transition-colors" style="background: var(--bg);">
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

    <!-- CTA SECTION -->
    <section class="py-24 text-center px-4" style="background: var(--bg-sec); border-top: 1px solid var(--border);">
      <div class="max-w-3xl mx-auto space-y-8">
        <h2 class="text-3xl sm:text-4xl font-bold tracking-tight">{{ $t('landing.cta.title') }}</h2>
        <p class="text-lg theme-text-muted max-w-xl mx-auto">{{ $t('landing.cta.subtitle') }}</p>
        <RouterLink to="/login" class="btn btn-primary inline-flex items-center gap-2 px-10 py-4 rounded-xl text-lg font-bold shadow-lg hover:-translate-y-1 transition-transform">
          {{ $t('landing.cta.button') }}
          <ArrowRight class="w-5 h-5" />
        </RouterLink>
      </div>
    </section>

    <!-- FOOTER -->
    <footer class="py-12 border-t theme-border" style="background: var(--bg);">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row justify-between items-center gap-4">
        <div class="flex items-center gap-2">
          <div class="w-6 h-6 flex items-center justify-center rounded text-[10px] font-black theme-accent">IX</div>
          <span class="font-bold">Ixiera</span>
        </div>
        <p class="text-sm theme-text-muted">&copy; {{ new Date().getFullYear() }} Ixiera. {{ $t('landing.footer.copy') }}</p>
        <div class="flex gap-4 text-sm theme-text-muted">
          <a href="#" class="hover:theme-text transition">{{ $t('landing.footer.privacy') }}</a>
          <a href="#" class="hover:theme-text transition">{{ $t('landing.footer.terms') }}</a>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { Menu, X, ArrowRight, PenTool, MessageCircle, BarChart3 } from 'lucide-vue-next'

const mobileMenuOpen = ref(false)
const { locale } = useI18n()

function changeLang(lang: string) {
  locale.value = lang
  localStorage.setItem('app_lang', lang)
}
</script>
