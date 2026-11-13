<template>
  <nav class="fixed top-0 w-full z-50 border-b border-[var(--line)] bg-[var(--bg)]/80 backdrop-blur-md">
    <div class="max-w-[1120px] mx-auto px-6 h-16 flex items-center justify-between">
      <!-- Logo -->
      <a href="/" class="flex items-center gap-2">
        <div class="w-8 h-8 flex items-center justify-center rounded-md text-sm font-bold bg-[var(--text)] text-[var(--bg)]">IX</div>
        <span class="font-bold text-xl tracking-tight">Ixiera</span>
      </a>

      <!-- Desktop Menu -->
      <div class="hidden md:flex items-center gap-8">
        <div class="relative group py-4">
          <a href="/features" class="text-sm font-medium text-[var(--muted)] hover:text-[var(--text)] transition-colors flex items-center gap-1">
            Fitur
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
          </a>
          <div class="absolute top-full left-0 mt-1 w-48 bg-[var(--bg)] border border-[var(--line)] rounded-xl p-2 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all shadow-xl z-50">
            <a href="/features" class="block px-3 py-2 text-sm font-bold text-[var(--text)] hover:bg-[var(--surface-2)] rounded-md transition">Semua Fitur</a>
            <a href="/features/composer" class="block px-3 py-2 text-sm text-[var(--muted)] hover:text-[var(--text)] hover:bg-[var(--surface-2)] rounded-md transition">Content Composer</a>
            <a href="/features/inbox" class="block px-3 py-2 text-sm text-[var(--muted)] hover:text-[var(--text)] hover:bg-[var(--surface-2)] rounded-md transition">Smart Inbox</a>
            <a href="/features/analytics" class="block px-3 py-2 text-sm text-[var(--muted)] hover:text-[var(--text)] hover:bg-[var(--surface-2)] rounded-md transition">Deep Analytics</a>
          </div>
        </div>
        
        <a href="/how-it-works" class="text-sm font-medium text-[var(--muted)] hover:text-[var(--text)] transition-colors">Cara Kerja</a>
        <a href="/pricing" class="text-sm font-medium text-[var(--muted)] hover:text-[var(--text)] transition-colors">Harga</a>
        <a href="/faq" class="text-sm font-medium text-[var(--muted)] hover:text-[var(--text)] transition-colors">FAQ</a>
      </div>

      <!-- Desktop Actions -->
      <div class="hidden md:flex items-center gap-4">
        <button @click="toggleTheme" class="p-2 rounded-full hover:bg-[var(--surface-2)] transition-colors">
          <Sun v-if="theme === 'dark'" class="w-5 h-5 text-[var(--text)]" />
          <Moon v-else class="w-5 h-5 text-[var(--text)]" />
        </button>
        <button @click="toggleLang" class="text-sm font-bold border border-[var(--line)] px-3 py-1.5 rounded-full hover:bg-[var(--surface-2)] transition">{{ locale.toUpperCase() }}</button>
        <a href="https://app.ixiera.id/login" class="text-sm font-bold bg-[var(--text)] text-[var(--bg)] px-6 py-2 rounded-full hover:opacity-90 transition">Minta Akses</a>
      </div>

      <!-- Mobile Hamburger -->
      <button @click="mobileMenuOpen = !mobileMenuOpen" class="md:hidden p-2">
        <svg v-if="!mobileMenuOpen" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
        <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
      </button>
    </div>

    <!-- Mobile Menu (Full Screen Overlay) -->
    <div v-if="mobileMenuOpen" class="md:hidden fixed inset-0 top-16 bg-[var(--bg)] z-40 overflow-y-auto">
      <div class="px-6 py-6 flex flex-col gap-2 min-h-full">
        
        <!-- Dropdown Fitur Accordion -->
        <div class="border-b border-[var(--line)] pb-2 mb-2">
          <button @click="mobileFiturOpen = !mobileFiturOpen" class="w-full flex items-center justify-between py-2 text-base font-bold text-[var(--text)]">
            Fitur
            <svg :class="{'rotate-180': mobileFiturOpen}" class="w-5 h-5 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
          </button>
          
          <!-- Sub-menu -->
          <div v-show="mobileFiturOpen" class="mt-2 space-y-1 pl-3 border-l-2 border-[var(--surface-2)]">
            <a href="/features" @click="mobileMenuOpen=false" class="block py-2 text-sm font-bold text-[var(--text)]">Semua Fitur</a>
            <a href="/features/composer" @click="mobileMenuOpen=false" class="block py-2 text-sm text-[var(--muted)] hover:text-[var(--text)]">Content Composer</a>
            <a href="/features/inbox" @click="mobileMenuOpen=false" class="block py-2 text-sm text-[var(--muted)] hover:text-[var(--text)]">Smart Inbox</a>
            <a href="/features/analytics" @click="mobileMenuOpen=false" class="block py-2 text-sm text-[var(--muted)] hover:text-[var(--text)]">Deep Analytics</a>
          </div>
        </div>

        <!-- Link Biasa -->
        <a href="/how-it-works" @click="mobileMenuOpen=false" class="block py-3 text-base font-bold text-[var(--text)] border-b border-[var(--line)]">Cara Kerja</a>
        <a href="/pricing" @click="mobileMenuOpen=false" class="block py-3 text-base font-bold text-[var(--text)] border-b border-[var(--line)]">Harga</a>
        <a href="/faq" @click="mobileMenuOpen=false" class="block py-3 text-base font-bold text-[var(--text)] border-b border-[var(--line)]">FAQ</a>
        
        <!-- Bottom Actions -->
        <div class="mt-auto pt-8 pb-4 flex flex-col gap-4">
          <div class="flex items-center justify-between bg-[var(--surface)] p-3 rounded-xl border border-[var(--line)]">
            <button @click="toggleTheme" class="flex items-center gap-2 text-sm font-bold text-[var(--text)]">
              <Sun v-if="theme === 'dark'" class="w-5 h-5" />
              <Moon v-else class="w-5 h-5" />
              <span>{{ theme === 'dark' ? 'Light Mode' : 'Dark Mode' }}</span>
            </button>
            <button @click="toggleLang" class="text-sm font-bold border border-[var(--line)] px-4 py-1.5 rounded-md bg-[var(--bg)]">{{ locale === 'id' ? 'EN' : 'ID' }}</button>
          </div>
          <a href="https://app.ixiera.id/login" class="block text-center text-base font-bold bg-[var(--text)] text-[var(--bg)] py-4 rounded-full shadow-lg">Minta Akses</a>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useTheme } from '../../composables/useTheme'
import { Sun, Moon } from 'lucide-vue-next'

const { locale } = useI18n()
const { theme, toggle: toggleTheme } = useTheme()
const mobileMenuOpen = ref(false)
const mobileFiturOpen = ref(false)

// Otomatis tutup menu kalau layar di-resize ke desktop
watch(mobileMenuOpen, (isOpen) => {
  if (isOpen) {
    document.body.style.overflow = 'hidden' // Kunci scroll body
  } else {
    document.body.style.overflow = 'auto'
    mobileFiturOpen.value = false // Reset dropdown
  }
})

function toggleLang() {
  locale.value = locale.value === 'id' ? 'en' : 'id'
  localStorage.setItem('app_lang', locale.value)
}
</script>
