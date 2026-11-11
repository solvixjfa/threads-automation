<template>
  <nav class="fixed top-0 w-full z-50 border-b border-[var(--line)] bg-[var(--bg)]/80 backdrop-blur-md">
    <div class="max-w-[1120px] mx-auto px-6 h-16 flex items-center justify-between">
      <a href="/" class="flex items-center gap-2">
        <div class="w-8 h-8 flex items-center justify-center rounded-md text-sm font-bold bg-[var(--text)] text-[var(--bg)]">IX</div>
        <span class="font-bold text-xl tracking-tight">Ixiera</span>
      </a>

      <div class="hidden md:flex items-center gap-8">
        <div class="relative group py-4">
          <a href="/features" class="text-sm font-medium text-[var(--muted)] hover:text-[var(--text)] transition-colors flex items-center gap-1">
            Fitur
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
          </a>
          <div class="absolute top-full left-0 mt-1 w-48 bg-[var(--bg)] border border-[var(--line)] rounded-xl p-2 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all shadow-xl z-50">
            <a href="/features/composer" class="block px-3 py-2 text-sm text-[var(--muted)] hover:text-[var(--text)] hover:bg-[var(--surface-2)] rounded-md transition">Content Composer</a>
            <a href="/features/inbox" class="block px-3 py-2 text-sm text-[var(--muted)] hover:text-[var(--text)] hover:bg-[var(--surface-2)] rounded-md transition">Smart Inbox</a>
            <a href="/features/analytics" class="block px-3 py-2 text-sm text-[var(--muted)] hover:text-[var(--text)] hover:bg-[var(--surface-2)] rounded-md transition">Deep Analytics</a>
          </div>
        </div>
        
        <a href="/how-it-works" class="text-sm font-medium text-[var(--muted)] hover:text-[var(--text)] transition-colors">Cara Kerja</a>
        <a href="/pricing" class="text-sm font-medium text-[var(--muted)] hover:text-[var(--text)] transition-colors">Harga</a>
        <a href="/faq" class="text-sm font-medium text-[var(--muted)] hover:text-[var(--text)] transition-colors">FAQ</a>
      </div>

      <div class="hidden md:flex items-center gap-4">
        <button @click="toggleTheme" class="p-2 rounded-full hover:bg-[var(--surface-2)] transition-colors">
          <Sun v-if="theme === 'dark'" class="w-5 h-5 text-[var(--text)]" />
          <Moon v-else class="w-5 h-5 text-[var(--text)]" />
        </button>
        <button @click="toggleLang" class="text-sm font-bold border border-[var(--line)] px-3 py-1.5 rounded-full hover:bg-[var(--surface-2)] transition">{{ locale.toUpperCase() }}</button>
        <a href="https://app.ixiera.id/login" class="text-sm font-bold bg-[var(--text)] text-[var(--bg)] px-6 py-2 rounded-full hover:opacity-90 transition">Minta Akses</a>
      </div>

      <button @click="mobileMenuOpen = !mobileMenuOpen" class="md:hidden p-2">
        <svg v-if="!mobileMenuOpen" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
        <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
      </button>
    </div>

    <div v-if="mobileMenuOpen" class="md:hidden border-t border-[var(--line)] bg-[var(--bg)] px-6 py-4 space-y-4 shadow-xl">
      <div class="space-y-2">
        <span class="block text-xs font-bold text-[var(--muted)] uppercase tracking-wider">Fitur</span>
        <a href="/features" @click="mobileMenuOpen=false" class="block text-sm font-medium pl-2">Semua Fitur</a>
        <a href="/features/composer" @click="mobileMenuOpen=false" class="block text-sm font-medium pl-2 text-[var(--muted)]">Content Composer</a>
        <a href="/features/inbox" @click="mobileMenuOpen=false" class="block text-sm font-medium pl-2 text-[var(--muted)]">Smart Inbox</a>
        <a href="/features/analytics" @click="mobileMenuOpen=false" class="block text-sm font-medium pl-2 text-[var(--muted)]">Deep Analytics</a>
      </div>
      <a href="/how-it-works" @click="mobileMenuOpen=false" class="block text-sm font-medium pt-2 border-t border-[var(--line)]">Cara Kerja</a>
      <a href="/pricing" @click="mobileMenuOpen=false" class="block text-sm font-medium">Harga</a>
      <a href="/faq" @click="mobileMenuOpen=false" class="block text-sm font-medium">FAQ</a>
      
      <div class="pt-4 border-t border-[var(--line)] flex flex-col gap-4">
        <div class="flex items-center justify-between">
          <button @click="toggleTheme" class="flex items-center gap-2 text-sm font-medium text-[var(--muted)]">
            <Sun v-if="theme === 'dark'" class="w-5 h-5" />
            <Moon v-else class="w-5 h-5" />
            <span>{{ theme === 'dark' ? 'Light Mode' : 'Dark Mode' }}</span>
          </button>
          <button @click="toggleLang" class="text-sm font-bold border border-[var(--line)] px-3 py-1.5 rounded-md">{{ locale === 'id' ? 'EN' : 'ID' }}</button>
        </div>
        <a href="https://app.ixiera.id/login" class="block text-center text-sm font-bold bg-[var(--text)] text-[var(--bg)] py-3 rounded-full">Minta Akses</a>
      </div>
    </div>
  </nav>
</template>
<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useTheme } from '../../composables/useTheme'
import { Sun, Moon } from 'lucide-vue-next'
const { locale } = useI18n()
const { theme, toggle: toggleTheme } = useTheme()
const mobileMenuOpen = ref(false)
function toggleLang() {
  locale.value = locale.value === 'id' ? 'en' : 'id'
  localStorage.setItem('app_lang', locale.value)
}
</script>
