<template>
  <div class="min-h-screen bg-[var(--bg)] text-[var(--text)] font-sans">
    <AppNavbar />
    <main class="pt-32 pb-24 px-6 max-w-[1120px] mx-auto">
      <div class="text-center mb-16">
        <div class="inline-flex items-center px-3 py-1 rounded-full border border-[var(--line)] text-xs font-bold tracking-widest text-[var(--muted)] uppercase mb-4">
          {{ locale === 'id' ? 'TRANSPARAN • TANPA AUTO-RENEW' : 'TRANSPARENT • NO AUTO-RENEW' }}
        </div>
        <h1 class="font-display text-5xl md:text-6xl mb-6">
          {{ locale === 'id' ? 'Harga jujur, ' : 'Honest pricing, ' }}
          <br><span class="italic">{{ locale === 'id' ? 'fitur lengkap.' : 'full firepower.' }}</span>
        </h1>
        <p class="text-lg text-[var(--muted)] max-w-2xl mx-auto">
          {{ locale === 'id'
            ? 'Mulai dengan trial 7 hari + 20 kredit gratis. Tanpa kartu kredit. Setelahnya pilih paket 30 hari sesuai kebutuhanmu—tanpa perpanjangan otomatis tersembunyi.'
            : 'Start with a 7-day trial + 20 free credits. No credit card required. Afterward, pick a 30-day plan with zero hidden auto-renewals.' }}
        </p>
      </div>

      <!-- 3 PRICING CARDS -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto text-left mb-20">
        <!-- Card 1: Trial -->
        <div class="border border-[var(--line)] rounded-2xl p-8 bg-[var(--surface)] flex flex-col">
          <div class="text-xs font-mono font-bold uppercase tracking-wider text-[var(--muted)] mb-2">
            {{ locale === 'id' ? 'MULAI GRATIS' : 'FREE START' }}
          </div>
          <h3 class="text-2xl font-bold mb-1">Trial</h3>
          <p class="text-sm text-[var(--muted)] mb-6">
            {{ locale === 'id' ? 'Uji seluruh alur kerja Ixiera di akunmu.' : 'Test the full Ixiera workflow on your account.' }}
          </p>
          <div class="text-4xl font-bold mb-6">
            Rp 0<span class="text-sm text-[var(--muted)] font-normal"> / {{ locale === 'id' ? '7 hari' : '7 days' }}</span>
          </div>

          <ul class="space-y-3 text-sm text-[var(--muted)] mb-8 border-t border-[var(--line)] pt-6">
            <li class="flex items-start gap-2.5"><span class="text-[var(--text)] font-bold">✓</span> <span><strong class="text-[var(--text)]">20 Kredit AI</strong> (Gemini & Groq)</span></li>
            <li class="flex items-start gap-2.5"><span class="text-[var(--text)] font-bold">✓</span> <span>AI 3-Day Content Planner & Quick Score</span></li>
            <li class="flex items-start gap-2.5"><span class="text-[var(--text)] font-bold">✓</span> <span>Smart Inbox (Komentar & Public Mentions)</span></li>
            <li class="flex items-start gap-2.5"><span class="text-[var(--text)] font-bold">✓</span> <span>Trending Topics & Keyword Search</span></li>
            <li class="flex items-start gap-2.5"><span class="text-[var(--text)] font-bold">✓</span> <span>Official Meta OAuth + Kill Switch</span></li>
          </ul>

          <a href="https://app.ixiera.online/login" class="mt-auto block text-center py-3.5 rounded-full font-bold border border-[var(--line)] hover:bg-[var(--surface-2)] transition">
            {{ locale === 'id' ? 'Mulai Trial Gratis' : 'Start Free Trial' }}
          </a>
        </div>

        <!-- Card 2: Pro (Highlighted) -->
        <div class="border-2 border-[var(--text)] rounded-2xl p-8 bg-[var(--bg)] relative shadow-2xl flex flex-col">
          <div class="absolute -top-3 left-1/2 -translate-x-1/2 bg-[var(--text)] text-[var(--bg)] text-[10px] font-bold px-3.5 py-1 rounded-full uppercase tracking-wider">
            {{ locale === 'id' ? 'Paling Laris' : 'Most Popular' }}
          </div>
          <div class="text-xs font-mono font-bold uppercase tracking-wider text-[var(--muted)] mb-2">
            {{ locale === 'id' ? 'SIAP PAKAI • ALL-IN-ONE' : 'READY TO USE • ALL-IN-ONE' }}
          </div>
          <h3 class="text-2xl font-bold mb-1">Pro</h3>
          <p class="text-sm text-[var(--muted)] mb-6">
            {{ locale === 'id' ? 'Langsung jalan tanpa ribet setup API key.' : 'Plug-and-play automation with built-in AI.' }}
          </p>
          <div class="text-4xl font-bold mb-6">
            Rp 29rb<span class="text-sm text-[var(--muted)] font-normal"> / {{ locale === 'id' ? '30 hari' : '30 days' }}</span>
          </div>

          <ul class="space-y-3 text-sm text-[var(--muted)] mb-8 border-t border-[var(--line)] pt-6">
            <li class="flex items-start gap-2.5"><span class="text-[var(--text)] font-bold">✓</span> <span><strong class="text-[var(--text)]">100 Kredit AI / bulan</strong> (Gemini + Groq)</span></li>
            <li class="flex items-start gap-2.5"><span class="text-[var(--text)] font-bold">✓</span> <span><strong class="text-[var(--text)]">Unlimited</strong> Jadwal Post & Thread Splitter</span></li>
            <li class="flex items-start gap-2.5"><span class="text-[var(--text)] font-bold">✓</span> <span><strong class="text-[var(--text)]">Location Tagging</strong> & Cross-Post Instagram</span></li>
            <li class="flex items-start gap-2.5"><span class="text-[var(--text)] font-bold">✓</span> <span>Full Auto Reply + Rate Limit & Kill Switch</span></li>
            <li class="flex items-start gap-2.5"><span class="text-[var(--text)] font-bold">✓</span> <span>Custom Knowledge Base (Gaya Bahasa & FAQ)</span></li>
            <li class="flex items-start gap-2.5"><span class="text-[var(--text)] font-bold">✓</span> <span>Trending Radar, Profile Discovery & Analytics</span></li>
          </ul>

          <a href="https://app.ixiera.online/login" class="mt-auto block text-center py-3.5 rounded-full font-bold bg-[var(--text)] text-[var(--bg)] hover:opacity-90 transition">
            {{ locale === 'id' ? 'Pilih Paket Pro' : 'Choose Pro Plan' }}
          </a>
        </div>

        <!-- Card 3: BYOK -->
        <div class="border border-[var(--line)] rounded-2xl p-8 bg-[var(--surface)] flex flex-col">
          <div class="text-xs font-mono font-bold uppercase tracking-wider text-[var(--muted)] mb-2">
            {{ locale === 'id' ? 'HEMAT • POWER USER' : 'SAVER • POWER USER' }}
          </div>
          <h3 class="text-2xl font-bold mb-1">BYOK</h3>
          <p class="text-sm text-[var(--muted)] mb-6">
            {{ locale === 'id' ? 'Pakai API Key Gemini / Groq milikmu sendiri.' : 'Bring your own Gemini / Groq API keys.' }}
          </p>
          <div class="text-4xl font-bold mb-6">
            Rp 19rb<span class="text-sm text-[var(--muted)] font-normal"> / {{ locale === 'id' ? '30 hari' : '30 days' }}</span>
          </div>

          <ul class="space-y-3 text-sm text-[var(--muted)] mb-8 border-t border-[var(--line)] pt-6">
            <li class="flex items-start gap-2.5"><span class="text-[var(--text)] font-bold">✓</span> <span><strong class="text-[var(--text)]">Tanpa Batas Kredit</strong> (pakai kuota API-mu)</span></li>
            <li class="flex items-start gap-2.5"><span class="text-[var(--text)] font-bold">✓</span> <span>Semua fitur Composer, Scheduler & IG Cross-Post</span></li>
            <li class="flex items-start gap-2.5"><span class="text-[var(--text)] font-bold">✓</span> <span>Smart Inbox (Comments + Mentions) & Auto-Reply</span></li>
            <li class="flex items-start gap-2.5"><span class="text-[var(--text)] font-bold">✓</span> <span>Trending Topics, Keyword Search & Discovery</span></li>
            <li class="flex items-start gap-2.5"><span class="text-[var(--text)] font-bold">✓</span> <span>Custom Knowledge Base & Deep Analytics</span></li>
          </ul>

          <a href="https://app.ixiera.online/login" class="mt-auto block text-center py-3.5 rounded-full font-bold border border-[var(--line)] hover:bg-[var(--surface-2)] transition">
            {{ locale === 'id' ? 'Pilih Paket BYOK' : 'Choose BYOK Plan' }}
          </a>
        </div>
      </div>

      <!-- DETAILED FEATURE COMPARISON TABLE -->
      <div class="max-w-5xl mx-auto mb-20">
        <h2 class="font-display text-3xl md:text-4xl text-center mb-8">
          {{ locale === 'id' ? 'Perbandingan Lengkap Fitur' : 'Full Feature Comparison' }}
        </h2>
        <div class="border border-[var(--line)] rounded-2xl overflow-x-auto bg-[var(--surface)]">
          <table class="w-full text-left text-sm border-collapse">
            <thead>
              <tr class="border-b border-[var(--line)] bg-[var(--surface-2)]">
                <th class="p-4 font-bold">{{ locale === 'id' ? 'Fitur & Kapasitas' : 'Features & Limits' }}</th>
                <th class="p-4 font-bold text-center">Trial (Rp0)</th>
                <th class="p-4 font-bold text-center">BYOK (Rp19rb)</th>
                <th class="p-4 font-bold text-center">Pro (Rp29rb)</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-[var(--line)]">
              <tr v-for="(row, idx) in comparisonRows" :key="idx">
                <td class="p-4 font-medium">{{ locale === 'id' ? row.feature.id : row.feature.en }}</td>
                <td class="p-4 text-center text-[var(--muted)]">{{ locale === 'id' ? row.trial.id : row.trial.en }}</td>
                <td class="p-4 text-center text-[var(--muted)]">{{ locale === 'id' ? row.byok.id : row.byok.en }}</td>
                <td class="p-4 text-center font-bold">{{ locale === 'id' ? row.pro.id : row.pro.en }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p class="text-xs text-[var(--muted)] mt-4 text-center">
          {{ locale === 'id'
            ? '* 1 Kredit = 1 aksi generasi AI (3-Day Plan, Deep AI Score, Repurpose, atau Balasan AI). Template balasan manual & Quick Score dasar selalu GRATIS.'
            : '* 1 Credit = 1 AI action (3-Day Plan, Deep AI Score, Repurpose, or AI Reply). Manual reply templates & basic Quick Score are always FREE.' }}
        </p>
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

const comparisonRows = [
  {
    feature: { id: 'Masa Aktif', en: 'Duration' },
    trial: { id: '7 Hari', en: '7 Days' },
    byok: { id: '30 Hari (No Auto-Renew)', en: '30 Days (No Auto-Renew)' },
    pro: { id: '30 Hari (No Auto-Renew)', en: '30 Days (No Auto-Renew)' }
  },
  {
    feature: { id: 'Kuota Aksi AI (Gemini & Groq)', en: 'AI Action Quota (Gemini & Groq)' },
    trial: { id: '20 Kredit Gratis', en: '20 Free Credits' },
    byok: { id: 'Unlimited (API Key Sendiri)', en: 'Unlimited (Own API Key)' },
    pro: { id: '100 Kredit AI Bawaan', en: '100 Built-in AI Credits' }
  },
  {
    feature: { id: 'AI 3-Day Planner & Repurpose', en: 'AI 3-Day Planner & Repurpose' },
    trial: { id: 'Termasuk', en: 'Included' },
    byok: { id: 'Termasuk', en: 'Included' },
    pro: { id: 'Termasuk', en: 'Included' }
  },
  {
    feature: { id: 'Jadwal Post & Thread Splitter', en: 'Post Scheduling & Thread Splitter' },
    trial: { id: 'Termasuk', en: 'Included' },
    byok: { id: 'Unlimited', en: 'Unlimited' },
    pro: { id: 'Unlimited', en: 'Unlimited' }
  },
  {
    feature: { id: 'Location Tagging & Cross-Post IG', en: 'Location Tagging & IG Cross-Post' },
    trial: { id: 'Termasuk', en: 'Included' },
    byok: { id: 'Termasuk', en: 'Included' },
    pro: { id: 'Termasuk', en: 'Included' }
  },
  {
    feature: { id: 'Inbox Komentar & Public Mentions', en: 'Comments & Public Mentions Inbox' },
    trial: { id: 'Termasuk', en: 'Included' },
    byok: { id: 'Termasuk', en: 'Included' },
    pro: { id: 'Termasuk', en: 'Included' }
  },
  {
    feature: { id: 'Trending Topics, Search & Profile Discovery', en: 'Trending Topics, Search & Profile Discovery' },
    trial: { id: 'Termasuk', en: 'Included' },
    byok: { id: 'Termasuk', en: 'Included' },
    pro: { id: 'Termasuk', en: 'Included' }
  },
  {
    feature: { id: 'Custom Knowledge Base (RAG Persona)', en: 'Custom Knowledge Base (RAG Persona)' },
    trial: { id: 'Termasuk', en: 'Included' },
    byok: { id: 'Termasuk', en: 'Included' },
    pro: { id: 'Termasuk', en: 'Included' }
  }
]
</script>
