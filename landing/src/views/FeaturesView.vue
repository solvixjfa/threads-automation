<template>
  <div class="min-h-screen bg-[var(--bg)] text-[var(--text)] font-sans">
    <AppNavbar />
    <main class="pt-32 pb-24 px-6 max-w-[1120px] mx-auto">
      <div class="text-center mb-20">
        <h1 class="font-display text-5xl md:text-6xl mb-6">Satu platform, <br><span class="italic">semua kendali.</span></h1>
        <p class="text-lg text-[var(--muted)] max-w-2xl mx-auto">Dari perencanaan konten hingga analitik mendalam, semua fitur yang kamu butuhkan untuk mengotomatisasi Threads ada di sini.</p>
      </div>
      
      <!-- Link ke sub-fitur -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <a href="/features/composer" class="border border-[var(--line)] bg-[var(--surface)] rounded-2xl p-8 hover:border-[var(--text)] transition group">
          <div class="w-12 h-12 rounded-lg bg-[var(--surface-2)] flex items-center justify-center mb-6 text-[var(--text)]">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
          </div>
          <h3 class="text-xl font-bold mb-3">Content Composer</h3>
          <p class="text-[var(--muted)] text-sm leading-relaxed">Generate rencana konten 3 hari, tulis draf dengan AI, dan jadwalkan postingan dalam satu layar.</p>
        </a>
        <a href="/features/inbox" class="border border-[var(--line)] bg-[var(--surface)] rounded-2xl p-8 hover:border-[var(--text)] transition group">
          <div class="w-12 h-12 rounded-lg bg-[var(--surface-2)] flex items-center justify-center mb-6 text-[var(--text)]">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path></svg>
          </div>
          <h3 class="text-xl font-bold mb-3">Smart Inbox</h3>
          <p class="text-[var(--muted)] text-sm leading-relaxed">Kelola komentar dengan sentuhan personal. Dijawab AI atau menggunakan template yang kamu atur sendiri.</p>
        </a>
        <a href="/features/analytics" class="border border-[var(--line)] bg-[var(--surface)] rounded-2xl p-8 hover:border-[var(--text)] transition group">
          <div class="w-12 h-12 rounded-lg bg-[var(--surface-2)] flex items-center justify-center mb-6 text-[var(--text)]">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
          </div>
          <h3 class="text-xl font-bold mb-3">Deep Analytics</h3>
          <p class="text-[var(--muted)] text-sm leading-relaxed">Ketahui jam terbaik untuk posting, tipe hook yang perform, dan tren topik dari akunmu sendiri.</p>
        </a>
      </div>
    </main>
    <AppFooter />
  </div>
</template>
<script setup lang="ts">
import AppNavbar from '../components/layouts/AppNavbar.vue'
import AppFooter from '../components/layouts/AppFooter.vue'
</script>
