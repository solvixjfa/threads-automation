<template>
  <div class="min-h-screen bg-[var(--bg)] text-[var(--text)] font-sans">
    <AppNavbar />
    <main class="pt-32 pb-24 px-6 max-w-3xl mx-auto">
      <div class="text-center mb-16">
        <h1 class="font-display text-5xl md:text-6xl mb-4">Pertanyaan Umum</h1>
        <p class="text-[var(--muted)]">Semua yang perlu kamu tahu tentang Ixiera.</p>
      </div>

      <div class="space-y-3">
        <div v-for="i in 9" :key="i" class="border border-[var(--line)] rounded-xl bg-[var(--surface)] overflow-hidden">
          <button @click="faqOpen = faqOpen === i ? null : i" class="w-full px-6 py-5 text-left flex justify-between items-center font-bold hover:bg-[var(--surface-2)] transition">
            <span>{{ $t('landing.faq.q' + i) }}</span>
            <svg class="w-5 h-5 transition-transform duration-300" :class="{'rotate-180': faqOpen === i}" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
          </button>
          <div v-if="faqOpen === i" class="px-6 pb-5 text-[var(--muted)] leading-relaxed">{{ $t('landing.faq.a' + i) }}</div>
        </div>
      </div>
    </main>
    <AppFooter />
  </div>
</template>
<script setup lang="ts">
import { ref } from 'vue'
import AppNavbar from '../components/layouts/AppNavbar.vue'
import AppFooter from '../components/layouts/AppFooter.vue'
const faqOpen = ref<number | null>(1)
</script>
