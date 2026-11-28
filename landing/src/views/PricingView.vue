<template>
  <div class="min-h-screen bg-[var(--bg)] text-[var(--text)] font-sans">
    <AppNavbar />
    <main class="pt-32 pb-24 px-6 max-w-[1160px] mx-auto">
      <div class="text-center mb-14">
        <div class="inline-flex items-center px-3 py-1 rounded-full border border-[var(--line)] text-xs font-bold tracking-widest text-[var(--muted)] uppercase mb-4">
          {{ locale === 'id' ? 'TRANSPARAN • TANPA AUTO-RENEW' : 'TRANSPARENT • NO AUTO-RENEW' }}
        </div>
        <h1 class="font-display text-5xl md:text-6xl mb-6">
          {{ locale === 'id' ? 'Harga jujur, ' : 'Honest pricing, ' }}
          <br><span class="italic">{{ locale === 'id' ? 'fitur lengkap.' : 'full firepower.' }}</span>
        </h1>
        <p class="text-lg text-[var(--muted)] max-w-2xl mx-auto">
          {{ locale === 'id'
            ? 'Mulai dengan trial 7 hari + 15.000 Token gratis. Tanpa kartu kredit. Setelahnya pilih paket 30 hari sesuai kebutuhanmu—tanpa perpanjangan otomatis tersembunyi.'
            : 'Start with a 7-day trial + 15,000 free Tokens. No credit card required. Afterward, pick a 30-day plan with zero hidden auto-renewals.' }}
        </p>
      </div>

      <!-- FREE TRIAL BANNER -->
      <div class="border border-[var(--line)] rounded-2xl p-6 md:p-7 bg-[var(--surface)] mb-8 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 text-left">
        <div>
          <div class="flex items-center gap-3 mb-1">
            <span class="text-xs font-mono font-bold uppercase tracking-wider px-2.5 py-0.5 rounded bg-[var(--surface-2)] text-[var(--text)]">
              {{ locale === 'id' ? 'MULAI GRATIS • 7 HARI' : 'FREE START • 7 DAYS' }}
            </span>
            <span class="text-xl font-bold">Rp 0</span>
          </div>
          <p class="text-sm text-[var(--muted)]">
            {{ locale === 'id'
              ? 'Termasuk 15.000 Token AI (Gemini & Groq), 1 Akun Threads, AI Planner, Smart Inbox, Trending Radar & Official Meta OAuth.'
              : 'Includes 15,000 AI Tokens (Gemini & Groq), 1 Threads Account, AI Planner, Smart Inbox, Trending Radar & Official Meta OAuth.' }}
          </p>
        </div>
        <a href="https://app.ixiera.online/login" class="w-full md:w-auto shrink-0 text-center px-7 py-3.5 rounded-full text-sm font-bold border border-[var(--line)] bg-[var(--bg)] hover:bg-[var(--surface-2)] transition">
          {{ locale === 'id' ? 'Mulai Trial Gratis' : 'Start Free Trial' }}
        </a>
      </div>

      <!-- 4 PRICING CARDS -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 text-left mb-20">
        <!-- Card 1: Starter -->
        <div class="border border-[var(--line)] rounded-2xl p-7 bg-[var(--surface)] flex flex-col">
          <div class="text-xs font-mono font-bold uppercase tracking-wider text-[var(--muted)] mb-2">
            {{ locale === 'id' ? 'KREATOR SOLO' : 'SOLO CREATOR' }}
          </div>
          <h3 class="text-2xl font-bold mb-1">Starter</h3>
          <p class="text-sm text-[var(--muted)] mb-5">
            {{ locale === 'id' ? 'Langsung jalan tanpa ribet setup API key.' : 'Plug-and-play automation with built-in AI.' }}
          </p>
          <div class="text-3xl font-bold mb-6">
            Rp 59rb<span class="text-sm text-[var(--muted)] font-normal"> / {{ locale === 'id' ? '30 hari' : '30 days' }}</span>
          </div>

          <ul class="space-y-3 text-sm text-[var(--muted)] mb-8 border-t border-[var(--line)] pt-5">
            <li class="flex items-start gap-2.5"><span class="text-[var(--text)] font-bold">✓</span> <span><strong class="text-[var(--text)]">{{ locale === 'id' ? '100.000 Token AI' : '100,000 AI Tokens' }}</strong> {{ locale === 'id' ? '/ bulan' : '/ month' }}</span></li>
            <li class="flex items-start gap-2.5"><span class="text-[var(--text)] font-bold">✓</span> <span><strong class="text-[var(--text)]">{{ locale === 'id' ? 'Maksimal 2 Akun' : 'Up to 2' }}</strong> {{ locale === 'id' ? 'Threads' : 'Threads Accounts' }}</span></li>
            <li class="flex items-start gap-2.5"><span class="text-[var(--text)] font-bold">✓</span> <span>{{ locale === 'id' ? 'Unlimited Jadwal Post & Thread Splitter' : 'Unlimited Post Scheduling & Thread Splitter' }}</span></li>
            <li class="flex items-start gap-2.5"><span class="text-[var(--text)] font-bold">✓</span> <span>Auto Reply, Location Tag & IG Cross-Post</span></li>
          </ul>

          <a href="https://app.ixiera.online/login" class="mt-auto block text-center py-3.5 rounded-full text-sm font-bold border border-[var(--line)] hover:bg-[var(--surface-2)] transition">
            {{ locale === 'id' ? 'Pilih Paket Starter' : 'Choose Starter' }}
          </a>
        </div>

        <!-- Card 2: Pro (Highlighted) -->
        <div class="border-2 border-[var(--text)] rounded-2xl p-7 bg-[var(--bg)] relative shadow-2xl flex flex-col">
          <div class="absolute -top-3 left-1/2 -translate-x-1/2 bg-[var(--text)] text-[var(--bg)] text-[10px] font-bold px-3.5 py-1 rounded-full uppercase tracking-wider">
            {{ locale === 'id' ? 'Paling Laris' : 'Most Popular' }}
          </div>
          <div class="text-xs font-mono font-bold uppercase tracking-wider text-[var(--muted)] mb-2">
            {{ locale === 'id' ? 'KREATOR AKTIF' : 'ACTIVE CREATOR' }}
          </div>
          <h3 class="text-2xl font-bold mb-1">Pro</h3>
          <p class="text-sm text-[var(--muted)] mb-5">
            {{ locale === 'id' ? 'Kuota token 3x lebih besar & multi-akun.' : '3x token quota & multi-account management.' }}
          </p>
          <div class="text-3xl font-bold mb-6">
            Rp 99rb<span class="text-sm text-[var(--muted)] font-normal"> / {{ locale === 'id' ? '30 hari' : '30 days' }}</span>
          </div>

          <ul class="space-y-3 text-sm text-[var(--muted)] mb-8 border-t border-[var(--line)] pt-5">
            <li class="flex items-start gap-2.5"><span class="text-[var(--text)] font-bold">✓</span> <span><strong class="text-[var(--text)]">{{ locale === 'id' ? '300.000 Token AI' : '300,000 AI Tokens' }}</strong> {{ locale === 'id' ? '/ bulan' : '/ month' }}</span></li>
            <li class="flex items-start gap-2.5"><span class="text-[var(--text)] font-bold">✓</span> <span><strong class="text-[var(--text)]">{{ locale === 'id' ? 'Maksimal 5 Akun' : 'Up to 5' }}</strong> {{ locale === 'id' ? 'Threads' : 'Threads Accounts' }}</span></li>
            <li class="flex items-start gap-2.5"><span class="text-[var(--text)] font-bold">✓</span> <span>Full Auto Reply + Custom Knowledge Base</span></li>
            <li class="flex items-start gap-2.5"><span class="text-[var(--text)] font-bold">✓</span> <span>Trending Radar, Discovery & Analytics</span></li>
          </ul>

          <a href="https://app.ixiera.online/login" class="mt-auto block text-center py-3.5 rounded-full text-sm font-bold bg-[var(--text)] text-[var(--bg)] hover:opacity-90 transition">
            {{ locale === 'id' ? 'Pilih Paket Pro' : 'Choose Pro' }}
          </a>
        </div>

        <!-- Card 3: Business -->
        <div class="border border-[var(--line)] rounded-2xl p-7 bg-[var(--surface)] flex flex-col">
          <div class="text-xs font-mono font-bold uppercase tracking-wider text-[var(--muted)] mb-2">
            {{ locale === 'id' ? 'BRAND & TIM' : 'BRAND & TEAM' }}
          </div>
          <h3 class="text-2xl font-bold mb-1">Business</h3>
          <p class="text-sm text-[var(--muted)] mb-5">
            {{ locale === 'id' ? 'Skala besar untuk bisnis & jaringan akun.' : 'High scale for brands & account networks.' }}
          </p>
          <div class="text-3xl font-bold mb-6">
            Rp 179rb<span class="text-sm text-[var(--muted)] font-normal"> / {{ locale === 'id' ? '30 hari' : '30 days' }}</span>
          </div>

          <ul class="space-y-3 text-sm text-[var(--muted)] mb-8 border-t border-[var(--line)] pt-5">
            <li class="flex items-start gap-2.5"><span class="text-[var(--text)] font-bold">✓</span> <span><strong class="text-[var(--text)]">{{ locale === 'id' ? '750.000 Token AI' : '750,000 AI Tokens' }}</strong> {{ locale === 'id' ? '/ bulan' : '/ month' }}</span></li>
            <li class="flex items-start gap-2.5"><span class="text-[var(--text)] font-bold">✓</span> <span><strong class="text-[var(--text)]">{{ locale === 'id' ? 'Maksimal 20 Akun' : 'Up to 20' }}</strong> {{ locale === 'id' ? 'Threads' : 'Threads Accounts' }}</span></li>
            <li class="flex items-start gap-2.5"><span class="text-[var(--text)] font-bold">✓</span> <span>Smart Inbox (Comments + Mentions)</span></li>
            <li class="flex items-start gap-2.5"><span class="text-[var(--text)] font-bold">✓</span> <span>Custom Knowledge Base & Deep Analytics</span></li>
          </ul>

          <a href="https://app.ixiera.online/login" class="mt-auto block text-center py-3.5 rounded-full text-sm font-bold border border-[var(--line)] hover:bg-[var(--surface-2)] transition">
            {{ locale === 'id' ? 'Pilih Paket Business' : 'Choose Business' }}
          </a>
        </div>

        <!-- Card 4: Agency BYOK -->
        <div class="border border-[var(--line)] rounded-2xl p-7 bg-[var(--surface)] flex flex-col">
          <div class="text-xs font-mono font-bold uppercase tracking-wider text-[var(--muted)] mb-2">
            {{ locale === 'id' ? 'UNLIMITED AI • AGENSI' : 'UNLIMITED AI • AGENCY' }}
          </div>
          <h3 class="text-2xl font-bold mb-1">Agency BYOK</h3>
          <p class="text-sm text-[var(--muted)] mb-5">
            {{ locale === 'id' ? 'Pakai API Key Gemini / Groq milikmu sendiri.' : 'Bring your own Gemini / Groq API keys.' }}
          </p>
          <div class="text-3xl font-bold mb-6">
            Rp 249rb<span class="text-sm text-[var(--muted)] font-normal"> / {{ locale === 'id' ? '30 hari' : '30 days' }}</span>
          </div>

          <ul class="space-y-3 text-sm text-[var(--muted)] mb-8 border-t border-[var(--line)] pt-5">
            <li class="flex items-start gap-2.5"><span class="text-[var(--text)] font-bold">✓</span> <span><strong class="text-[var(--text)]">{{ locale === 'id' ? 'Unlimited Token' : 'Unlimited Tokens' }}</strong> ({{ locale === 'id' ? 'pakai kuota API-mu' : 'use your own API quota' }})</span></li>
            <li class="flex items-start gap-2.5"><span class="text-[var(--text)] font-bold">✓</span> <span><strong class="text-[var(--text)]">{{ locale === 'id' ? 'Maksimal 50 Akun' : 'Up to 50' }}</strong> {{ locale === 'id' ? 'Threads' : 'Threads Accounts' }}</span></li>
            <li class="flex items-start gap-2.5"><span class="text-[var(--text)] font-bold">✓</span> <span>{{ locale === 'id' ? 'Semua fitur Composer, Scheduler & IG Cross-Post' : 'All Composer, Scheduler & IG Cross-Post features' }}</span></li>
            <li class="flex items-start gap-2.5"><span class="text-[var(--text)] font-bold">✓</span> <span>{{ locale === 'id' ? 'Cocok untuk Agensi & High-Volume' : 'Ideal for Agencies & High-Volume' }}</span></li>
          </ul>

          <a href="https://app.ixiera.online/login" class="mt-auto block text-center py-3.5 rounded-full text-sm font-bold border border-[var(--line)] hover:bg-[var(--surface-2)] transition">
            {{ locale === 'id' ? 'Pilih Agency BYOK' : 'Choose Agency BYOK' }}
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
                <th class="p-4 font-bold text-center">Starter (Rp59rb)</th>
                <th class="p-4 font-bold text-center">Pro (Rp99rb)</th>
                <th class="p-4 font-bold text-center">Business (Rp179rb)</th>
                <th class="p-4 font-bold text-center">Agency (Rp249rb)</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-[var(--line)]">
              <tr v-for="(row, idx) in comparisonRows" :key="idx">
                <td class="p-4 font-medium">{{ locale === 'id' ? row.feature.id : row.feature.en }}</td>
                <td class="p-4 text-center text-[var(--muted)]">{{ locale === 'id' ? row.trial.id : row.trial.en }}</td>
                <td class="p-4 text-center text-[var(--muted)]">{{ locale === 'id' ? row.starter.id : row.starter.en }}</td>
                <td class="p-4 text-center font-bold">{{ locale === 'id' ? row.pro.id : row.pro.en }}</td>
                <td class="p-4 text-center text-[var(--muted)]">{{ locale === 'id' ? row.business.id : row.business.en }}</td>
                <td class="p-4 text-center text-[var(--muted)]">{{ locale === 'id' ? row.agency.id : row.agency.en }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p class="text-xs text-[var(--muted)] mt-4 text-center">
          {{ locale === 'id'
            ? '* Pemakaian token dihitung transparan sesuai jumlah token AI aktual (prompt + output) per aksi. Template balasan manual & Quick Score dasar selalu GRATIS.'
            : '* Token usage is billed transparently based on actual AI tokens (prompt + output) per action. Manual reply templates & basic Quick Score are always FREE.' }}
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
    starter: { id: '30 Hari', en: '30 Days' },
    pro: { id: '30 Hari', en: '30 Days' },
    business: { id: '30 Hari', en: '30 Days' },
    agency: { id: '30 Hari', en: '30 Days' }
  },
  {
    feature: { id: 'Kuota Token AI (Gemini & Groq)', en: 'AI Token Quota (Gemini & Groq)' },
    trial: { id: '15.000 Token', en: '15,000 Tokens' },
    starter: { id: '100.000 Token', en: '100,000 Tokens' },
    pro: { id: '300.000 Token', en: '300,000 Tokens' },
    business: { id: '750.000 Token', en: '750,000 Tokens' },
    agency: { id: 'Unlimited (BYOK)', en: 'Unlimited (BYOK)' }
  },
  {
    feature: { id: 'Maksimal Akun Threads', en: 'Max Threads Accounts' },
    trial: { id: '1 Akun', en: '1 Account' },
    starter: { id: '2 Akun', en: '2 Accounts' },
    pro: { id: '5 Akun', en: '5 Accounts' },
    business: { id: '20 Akun', en: '20 Accounts' },
    agency: { id: '50 Akun', en: '50 Accounts' }
  },
  {
    feature: { id: 'AI 3-Day Planner & Repurpose', en: 'AI 3-Day Planner & Repurpose' },
    trial: { id: 'Termasuk', en: 'Included' },
    starter: { id: 'Termasuk', en: 'Included' },
    pro: { id: 'Termasuk', en: 'Included' },
    business: { id: 'Termasuk', en: 'Included' },
    agency: { id: 'Termasuk', en: 'Included' }
  },
  {
    feature: { id: 'Jadwal Post & Thread Splitter', en: 'Post Scheduling & Thread Splitter' },
    trial: { id: 'Termasuk', en: 'Included' },
    starter: { id: 'Unlimited', en: 'Unlimited' },
    pro: { id: 'Unlimited', en: 'Unlimited' },
    business: { id: 'Unlimited', en: 'Unlimited' },
    agency: { id: 'Unlimited', en: 'Unlimited' }
  },
  {
    feature: { id: 'Location Tagging & Cross-Post IG', en: 'Location Tagging & IG Cross-Post' },
    trial: { id: 'Termasuk', en: 'Included' },
    starter: { id: 'Termasuk', en: 'Included' },
    pro: { id: 'Termasuk', en: 'Included' },
    business: { id: 'Termasuk', en: 'Included' },
    agency: { id: 'Termasuk', en: 'Included' }
  },
  {
    feature: { id: 'Inbox Komentar & Public Mentions', en: 'Comments & Public Mentions Inbox' },
    trial: { id: 'Termasuk', en: 'Included' },
    starter: { id: 'Termasuk', en: 'Included' },
    pro: { id: 'Termasuk', en: 'Included' },
    business: { id: 'Termasuk', en: 'Included' },
    agency: { id: 'Termasuk', en: 'Included' }
  },
  {
    feature: { id: 'Trending Topics, Search & Discovery', en: 'Trending Topics, Search & Discovery' },
    trial: { id: 'Termasuk', en: 'Included' },
    starter: { id: 'Termasuk', en: 'Included' },
    pro: { id: 'Termasuk', en: 'Included' },
    business: { id: 'Termasuk', en: 'Included' },
    agency: { id: 'Termasuk', en: 'Included' }
  },
  {
    feature: { id: 'Knowledge Base (Gaya Bahasa Brand)', en: 'Knowledge Base (Brand Voice)' },
    trial: { id: 'Termasuk', en: 'Included' },
    starter: { id: 'Termasuk', en: 'Included' },
    pro: { id: 'Termasuk', en: 'Included' },
    business: { id: 'Termasuk', en: 'Included' },
    agency: { id: 'Termasuk', en: 'Included' }
  }
]
</script>
