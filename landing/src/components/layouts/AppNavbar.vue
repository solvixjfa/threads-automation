<template>
  <nav class="fixed top-0 w-full z-50 border-b border-[var(--line)] bg-[var(--bg)]/90 backdrop-blur-md">
    <div class="max-w-[1120px] mx-auto px-6 h-16 flex items-center justify-between">
      <a href="/" class="flex items-center gap-2">
        <div class="w-8 h-8 flex items-center justify-center rounded-md text-sm font-bold bg-[var(--text)] text-[var(--bg)]">IX</div>
        <span class="font-bold text-xl tracking-tight">Ixiera</span>
      </a>

      <div class="hidden md:flex items-center gap-7">
        <div class="relative group py-4">
          <a href="/features" class="text-sm font-medium text-[var(--muted)] hover:text-[var(--text)] transition-colors flex items-center gap-1">
            {{ $t("landing.nav.features") }}
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
          </a>
          <div class="absolute top-full left-0 mt-1 w-52 bg-[var(--bg)] border border-[var(--line)] rounded-xl p-2 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all shadow-xl z-50">
            <a href="/features" class="block px-3 py-2 text-sm font-bold text-[var(--text)] hover:bg-[var(--surface-2)] rounded-md transition">{{ locale === "id" ? "Semua Fitur" : "All Features" }}</a>
            <a href="/features/composer" class="block px-3 py-2 text-sm text-[var(--muted)] hover:text-[var(--text)] hover:bg-[var(--surface-2)] rounded-md transition">AI Composer & IG Cross-Post</a>
            <a href="/features/inbox" class="block px-3 py-2 text-sm text-[var(--muted)] hover:text-[var(--text)] hover:bg-[var(--surface-2)] rounded-md transition">Smart Inbox & Mentions</a>
            <a href="/features/analytics" class="block px-3 py-2 text-sm text-[var(--muted)] hover:text-[var(--text)] hover:bg-[var(--surface-2)] rounded-md transition">Trending & Deep Analytics</a>
          </div>
        </div>

        <a href="/how-it-works" class="text-sm font-medium text-[var(--muted)] hover:text-[var(--text)] transition-colors">{{ $t("landing.nav.how_it_works") }}</a>
        <a href="/pricing" class="text-sm font-medium text-[var(--muted)] hover:text-[var(--text)] transition-colors">{{ locale === "id" ? "Harga" : "Pricing" }}</a>
        <a href="/blog" class="text-sm font-medium text-[var(--muted)] hover:text-[var(--text)] transition-colors">Blog</a>
        <a href="/faq" class="text-sm font-medium text-[var(--muted)] hover:text-[var(--text)] transition-colors">{{ $t("landing.nav.faq") }}</a>
      </div>

      <div class="hidden md:flex items-center gap-4">
        <button @click="toggleTheme" type="button" aria-label="Toggle theme" class="p-2 rounded-full hover:bg-[var(--surface-2)] transition-colors">
          <Sun v-if="theme === 'dark'" class="w-5 h-5 text-[var(--text)]" />
          <Moon v-else class="w-5 h-5 text-[var(--text)]" />
        </button>
        <button @click="toggleLang" type="button" class="text-sm font-bold border border-[var(--line)] px-3 py-1.5 rounded-full hover:bg-[var(--surface-2)] transition">{{ locale.toUpperCase() }}</button>
        <a href="https://app.ixiera.online/login" class="text-sm font-bold bg-[var(--text)] text-[var(--bg)] px-6 py-2 rounded-full hover:opacity-90 transition">{{ locale === "id" ? "Mulai Gratis" : "Start Free" }}</a>
      </div>

      <button @click="toggleMobileMenu" type="button" aria-label="Toggle menu" class="md:hidden p-2">
        <svg v-if="!mobileMenuOpen" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
        <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
      </button>
    </div>

    <!-- Mobile Dropdown Panel -->
    <div v-if="mobileMenuOpen" class="md:hidden border-t border-[var(--line)] bg-[var(--bg)] px-6 py-4 space-y-3 shadow-2xl max-h-[calc(100vh-4rem)] overflow-y-auto">
      <div>
        <button @click="mobileFiturOpen = !mobileFiturOpen" type="button" class="w-full flex items-center justify-between py-1.5 text-sm font-medium text-[var(--text)]">
          <span>{{ $t("landing.nav.features") }}</span>
          <svg :class="{'rotate-180': mobileFiturOpen}" class="w-4 h-4 text-[var(--muted)] transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
        </button>
        <div v-show="mobileFiturOpen" class="mt-2 space-y-2.5 pl-3 border-l border-[var(--line)]">
          <a href="/features" @click="closeMenu" class="block text-sm font-medium text-[var(--text)]">{{ locale === "id" ? "Semua Fitur" : "All Features" }}</a>
          <a href="/features/composer" @click="closeMenu" class="block text-sm font-medium text-[var(--muted)]">AI Composer & IG Cross-Post</a>
          <a href="/features/inbox" @click="closeMenu" class="block text-sm font-medium text-[var(--muted)]">Smart Inbox & Mentions</a>
          <a href="/features/analytics" @click="closeMenu" class="block text-sm font-medium text-[var(--muted)]">Trending & Deep Analytics</a>
        </div>
      </div>

      <a href="/how-it-works" @click="closeMenu" class="block text-sm font-medium pt-3 border-t border-[var(--line)]">{{ $t("landing.nav.how_it_works") }}</a>
      <a href="/pricing" @click="closeMenu" class="block text-sm font-medium py-1">{{ locale === "id" ? "Harga" : "Pricing" }}</a>
      <a href="/blog" @click="closeMenu" class="block text-sm font-medium py-1">Blog & Resources</a>
      <a href="/faq" @click="closeMenu" class="block text-sm font-medium py-1">{{ $t("landing.nav.faq") }}</a>

      <div class="pt-3 border-t border-[var(--line)] flex flex-col gap-4">
        <div class="flex items-center justify-between">
          <button @click="toggleTheme" type="button" class="flex items-center gap-2 text-sm font-medium text-[var(--muted)]">
            <Sun v-if="theme === 'dark'" class="w-5 h-5" />
            <Moon v-else class="w-5 h-5" />
            <span>{{ theme === 'dark' ? "Light Mode" : "Dark Mode" }}</span>
          </button>
          <button @click="toggleLang" type="button" class="text-sm font-bold border border-[var(--line)] px-3 py-1.5 rounded-md">{{ locale === 'id' ? 'EN' : 'ID' }}</button>
        </div>
        <a href="https://app.ixiera.online/login" class="block text-center text-sm font-bold bg-[var(--text)] text-[var(--bg)] py-3 rounded-full">{{ locale === "id" ? "Mulai Gratis 7 Hari" : "Start 7-Day Free Trial" }}</a>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref } from "vue"
import { useI18n } from "vue-i18n"
import { useTheme } from "../../composables/useTheme"
import { Sun, Moon } from "lucide-vue-next"

const { locale } = useI18n({ useScope: "global" })
const { theme, toggle: toggleTheme } = useTheme()
const mobileMenuOpen = ref(false)
const mobileFiturOpen = ref(false)

function toggleMobileMenu() {
  mobileMenuOpen.value = !mobileMenuOpen.value
  if (!mobileMenuOpen.value) mobileFiturOpen.value = false
}

function closeMenu() {
  mobileMenuOpen.value = false
  mobileFiturOpen.value = false
}

function toggleLang() {
  const next = locale.value === "id" ? "en" : "id"
  locale.value = next
  localStorage.setItem("app_lang", next)
  document.documentElement.lang = next
}
</script>
