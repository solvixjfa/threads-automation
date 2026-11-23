<template>
  <div class="min-h-screen bg-[var(--bg)] text-[var(--text)] font-sans">
    <AppNavbar />
    <main class="pt-32 pb-24 px-6 max-w-[1120px] mx-auto">
      <div class="text-center mb-20">
        <div class="inline-flex items-center px-3 py-1 rounded-full border border-[var(--line)] text-xs font-bold tracking-widest text-[var(--muted)] uppercase mb-4">
          PUBLIC BETA
        </div>
        <h1 class="font-display text-5xl md:text-6xl mb-6">
          {{ locale === 'id' ? 'Satu platform, ' : 'One platform, ' }}
          <br><span class="italic">{{ locale === 'id' ? 'semua kendali.' : 'complete control.' }}</span>
        </h1>
        <p class="text-lg text-[var(--muted)] max-w-2xl mx-auto">
          {{ locale === 'id'
            ? 'Dari riset topik trending, penulisan draf berbasis gaya bahasamu, cross-post ke Instagram, hingga balasan komentar & mention otomatis.'
            : 'From live trending research and persona-matched drafting to Instagram cross-posting and automated comment & mention replies.' }}
        </p>
      </div>

      <!-- 6 Feature Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <a href="/features/composer" class="border border-[var(--line)] bg-[var(--surface)] rounded-2xl p-8 hover:border-[var(--text)] transition group">
          <div class="w-12 h-12 rounded-lg bg-[var(--surface-2)] flex items-center justify-center mb-6 text-[var(--text)]">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
          </div>
          <h3 class="text-xl font-bold mb-3">AI Content Composer</h3>
          <p class="text-[var(--muted)] text-sm leading-relaxed">
            {{ locale === 'id'
              ? 'Rencana konten 3 hari (Gemini), cek Quick Score gratis, pecah utasan otomatis, dan jadwalkan post di jam prime-time.'
              : '3-day content plans (Gemini), free Quick Score checks, automatic thread splitting, and prime-time scheduling.' }}
          </p>
        </a>

        <a href="/features/composer" class="border border-[var(--line)] bg-[var(--surface)] rounded-2xl p-8 hover:border-[var(--text)] transition group">
          <div class="w-12 h-12 rounded-lg bg-[var(--surface-2)] flex items-center justify-center mb-6 text-[var(--text)]">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
          </div>
          <h3 class="text-xl font-bold mb-3">Location Tag & IG Cross-Post</h3>
          <p class="text-[var(--muted)] text-sm leading-relaxed">
            {{ locale === 'id'
              ? 'Sematkan tag lokasi terverifikasi Meta dan distribusikan konten Threads langsung ke Instagram Feed dalam satu klik.'
              : 'Attach verified Meta location tags and cross-post your Threads content directly to your Instagram Feed in one toggle.' }}
          </p>
        </a>

        <a href="/features/inbox" class="border border-[var(--line)] bg-[var(--surface)] rounded-2xl p-8 hover:border-[var(--text)] transition group">
          <div class="w-12 h-12 rounded-lg bg-[var(--surface-2)] flex items-center justify-center mb-6 text-[var(--text)]">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path></svg>
          </div>
          <h3 class="text-xl font-bold mb-3">Smart Inbox & Mentions</h3>
          <p class="text-[var(--muted)] text-sm leading-relaxed">
            {{ locale === 'id'
              ? 'Kelola komentar post sekaligus public @mentions. Klasifikasi otomatis & balasan instan Groq dengan mode Manual atau Full Auto.'
              : 'Manage post comments alongside public @mentions. Instant Groq classification & reply drafts with Manual or Full Auto modes.' }}
          </p>
        </a>

        <a href="/features/composer" class="border border-[var(--line)] bg-[var(--surface)] rounded-2xl p-8 hover:border-[var(--text)] transition group">
          <div class="w-12 h-12 rounded-lg bg-[var(--surface-2)] flex items-center justify-center mb-6 text-[var(--text)]">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
          </div>
          <h3 class="text-xl font-bold mb-3">Trending Radar & Discovery</h3>
          <p class="text-[var(--muted)] text-sm leading-relaxed">
            {{ locale === 'id'
              ? 'Pantau Threads Trending Topics real-time, cari postingan berdasarkan kata kunci, dan intip profil kreator di niche kamu.'
              : 'Track real-time Threads Trending Topics, search public posts by keyword, and inspect creator profiles in your niche.' }}
          </p>
        </a>

        <a href="/features/inbox" class="border border-[var(--line)] bg-[var(--surface)] rounded-2xl p-8 hover:border-[var(--text)] transition group">
          <div class="w-12 h-12 rounded-lg bg-[var(--surface-2)] flex items-center justify-center mb-6 text-[var(--text)]">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path></svg>
          </div>
          <h3 class="text-xl font-bold mb-3">Custom Knowledge Base</h3>
          <p class="text-[var(--muted)] text-sm leading-relaxed">
            {{ locale === 'id'
              ? 'Simpan katalog produk, FAQ, harga, dan aturan gaya bahasamu agar setiap draf dan balasan AI terdengar seperti kamu.'
              : 'Store product facts, FAQs, pricing, and brand voice rules so every AI draft and reply sounds unmistakably like you.' }}
          </p>
        </a>

        <a href="/features/analytics" class="border border-[var(--line)] bg-[var(--surface)] rounded-2xl p-8 hover:border-[var(--text)] transition group">
          <div class="w-12 h-12 rounded-lg bg-[var(--surface-2)] flex items-center justify-center mb-6 text-[var(--text)]">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
          </div>
          <h3 class="text-xl font-bold mb-3">Deep Analytics & Heatmap</h3>
          <p class="text-[var(--muted)] text-sm leading-relaxed">
            {{ locale === 'id'
              ? 'Ketahui jam terbaik posting (WIB), tipe hook paling efektif, dan panjang karakter ideal langsung dari data akunmu sendiri.'
              : 'Discover your best posting hours, highest-converting hooks, and ideal character length computed from your own account.' }}
          </p>
        </a>
      </div>
    </main>
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import AppNavbar from '../components/layouts/AppNavbar.vue'
import AppFooter from '../components/layouts/AppFooter.vue'

const { locale } = useI18n({ useScope: 'global' })
</script>
