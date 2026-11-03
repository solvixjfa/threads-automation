<template>
  <div class="space-y-10 w-full max-w-3xl mx-auto pb-8">
    <!-- HERO -->
    <div class="text-center space-y-3 pt-2">
      <div class="inline-flex items-center justify-center w-14 h-14 rounded-2xl theme-bg-sec border theme-border mb-2">
        <BookOpen class="w-7 h-7 theme-text-muted" />
      </div>
      <h1 class="text-3xl font-black tracking-tight">{{ txt.heroTitle }}</h1>
      <p class="text-sm theme-text-muted max-w-lg mx-auto">{{ txt.heroSub }}</p>
    </div>

    <!-- QUICK START CARD -->
    <div class="card p-6 border-2 border-current">
      <div class="flex items-center gap-2 mb-4">
        <Zap class="w-5 h-5 theme-text-muted" />
        <h2 class="text-base font-bold">{{ txt.quickStartTitle }}</h2>
      </div>
      <ol class="space-y-3 text-sm">
        <li v-for="(step, i) in txt.quickStart" :key="i" class="flex gap-3">
          <span class="shrink-0 w-6 h-6 rounded-full flex items-center justify-center text-xs font-black" style="background:#e5e5e5;color:#0f0f0f;">{{ i + 1 }}</span>
          <span class="theme-text-sec leading-relaxed">{{ step }}</span>
        </li>
      </ol>
    </div>

    <!-- SECTIONS -->
    <div v-for="(section, idx) in txt.sections" :key="idx" class="space-y-4">
      <div class="flex items-center gap-3 pb-3 border-b theme-border">
        <div class="w-10 h-10 rounded-xl flex items-center justify-center theme-bg-sec border theme-border shrink-0">
          <component :is="section.icon" class="w-5 h-5 theme-text-muted" />
        </div>
        <div>
          <h2 class="text-lg font-bold">{{ section.title }}</h2>
          <p class="text-xs theme-text-muted">{{ section.sub }}</p>
        </div>
      </div>
      <div class="space-y-4 pl-1">
        <div v-for="(item, i) in section.items" :key="i" class="flex gap-3">
          <div class="w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-black shrink-0 mt-0.5 theme-bg-sec border theme-border">
            {{ i + 1 }}
          </div>
          <div class="space-y-1 min-w-0">
            <p class="text-sm font-bold">{{ item.title }}</p>
            <p class="text-xs theme-text-muted leading-relaxed">{{ item.desc }}</p>
          </div>
        </div>
      </div>
      <RouterLink v-if="section.cta" :to="section.cta.path" class="inline-flex items-center gap-1.5 text-xs font-bold theme-text-muted hover:theme-text transition px-3 py-1.5 rounded-md hover:theme-bg-hover">
        {{ section.cta.label }}
        <ChevronRight class="w-3 h-3" />
      </RouterLink>
    </div>

    <!-- FAQ -->
    <div class="space-y-4">
      <div class="flex items-center gap-3 pb-3 border-b theme-border">
        <div class="w-10 h-10 rounded-xl flex items-center justify-center theme-bg-sec border theme-border shrink-0">
          <HelpCircle class="w-5 h-5 theme-text-muted" />
        </div>
        <h2 class="text-lg font-bold">{{ txt.faqTitle }}</h2>
      </div>
      <div class="space-y-2">
        <details v-for="(faq, i) in txt.faqs" :key="i" class="card p-4 group">
          <summary class="flex items-center justify-between cursor-pointer list-none">
            <span class="text-sm font-bold pr-4">{{ faq.q }}</span>
            <ChevronDown class="w-4 h-4 theme-text-muted shrink-0 transition group-open:rotate-180" />
          </summary>
          <p class="text-xs theme-text-muted mt-3 leading-relaxed">{{ faq.a }}</p>
        </details>
      </div>
    </div>

    <!-- CONTACT -->
    <div class="card p-6 text-center space-y-3">
      <div class="inline-flex items-center justify-center w-10 h-10 rounded-xl theme-bg-sec border theme-border">
        <Mail class="w-5 h-5 theme-text-muted" />
      </div>
      <h3 class="text-base font-bold">{{ txt.contactTitle }}</h3>
      <p class="text-xs theme-text-muted max-w-md mx-auto">{{ txt.contactSub }}</p>
      <a href="mailto:contact@ixiera.id" class="inline-flex items-center gap-2 text-sm font-bold underline underline-offset-4 hover:opacity-80 transition">
        contact@ixiera.id
      </a>
    </div>

    <!-- FINAL CTA -->
    <div class="text-center pt-4">
      <RouterLink to="/content/create" class="inline-flex items-center gap-2 px-6 py-3 rounded-lg font-bold text-sm" style="background:#000;color:#fff;">
        <Plus class="w-4 h-4" />
        {{ txt.finalCta }}
      </RouterLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { RouterLink } from 'vue-router'
import {
  BookOpen, Zap, ChevronRight, ChevronDown, HelpCircle, Mail, Plus,
  LayoutDashboard, FileText, MessageCircle, BarChart3, User, Link2, Coins
} from 'lucide-vue-next'

const { locale } = useI18n()

const content = {
  id: {
    heroTitle: 'Panduan Ixiera',
    heroSub: 'Semua yang kamu butuhkan untuk mulai mengelola Threads dengan AI — dalam 5 menit.',
    quickStartTitle: 'Mulai Cepat (5 Langkah)',
    quickStart: [
      'Hubungkan akun Threads kamu di menu Profile → Account',
      'Buat post pertama di menu Content → Create (atau pakai AI generate)',
      'Jadwalkan post atau publish langsung',
      'Balas komentar di menu Comments (atau biarkan AI auto-reply)',
      'Pantau performa di menu Analytics',
    ],
    sections: [
      {
        title: 'Dashboard',
        sub: 'Ringkasan harian akun kamu',
        icon: LayoutDashboard,
        items: [
          { title: 'Action cards', desc: 'Kartu peringatan muncul kalau ada komentar menunggu balasan, trial hampir habis, atau waktu posting terbaik hari ini.' },
          { title: 'Stats singkat', desc: 'Queue, published, failed, dan avg engagement rate dalam 1 pandangan.' },
          { title: 'Top posts & grafik', desc: 'Lihat post terbaik (by views, likes, atau ER) dan tren 14 hari terakhir.' },
        ],
        cta: { label: 'Buka Dashboard', path: '/dashboard' },
      },
      {
        title: 'Content',
        sub: 'Buat, remix, dan jadwalkan post',
        icon: FileText,
        items: [
          { title: 'Create', desc: 'Tulis post manual atau generate 3-day plan dengan AI. Pilih tone, provider AI, dan knowledge base yang dipakai RAG.' },
          { title: 'Variant', desc: 'Remix post lama jadi variasi baru dengan AI — ubah angle tanpa kehilangan inti konten.' },
          { title: 'Queue', desc: 'Lihat semua post terjadwal dan riwayat yang udah publish. Retry post gagal langsung dari sini.' },
        ],
        cta: { label: 'Buka Content', path: '/content' },
      },
      {
        title: 'Comments',
        sub: 'Kelola interaksi dengan audiens',
        icon: MessageCircle,
        items: [
          { title: 'Auto-sync', desc: 'Komentar baru otomatis ditarik dari Threads setiap 10 menit. Bisa sync manual kapan aja.' },
          { title: 'AI classification', desc: 'Komentar dikelompokkan jadi priority, question, praise, neutral, spam, atau toxic.' },
          { title: 'Auto-reply', desc: 'Aktifkan AI auto-reply untuk balas komentar otomatis — atau review dulu sebelum kirim.' },
          { title: 'Bulk actions', desc: 'Pilih banyak komentar sekaligus untuk diproses bareng biar hemat waktu.' },
        ],
        cta: { label: 'Buka Comments', path: '/comment' },
      },
      {
        title: 'Analytics',
        sub: 'Insight berbasis data akun kamu',
        icon: BarChart3,
        items: [
          { title: 'Best Time', desc: 'Waktu posting terbaik per hari berdasarkan ER historis. Klik slot untuk langsung jadwalkan post di jam itu.' },
          { title: 'Hook', desc: 'Tipe hook mana yang paling performan (Data-Point, Contrarian, Confession, dll).' },
          { title: 'Length', desc: 'Panjang post optimal untuk engagement. Dapatkan rekomendasi + tombol buat post dengan panjang itu.' },
          { title: 'Topic', desc: 'Cluster topik paling performan di akun kamu. Klik topik untuk buat post serupa.' },
        ],
        cta: { label: 'Buka Analytics', path: '/analytics' },
      },
      {
        title: 'Profile',
        sub: 'Semua pengaturan akun',
        icon: User,
        items: [
          { title: 'Account', desc: 'Koneksi Threads, appearance (dark/light mode), dan bahasa (EN/ID).' },
          { title: 'Auto-Reply', desc: 'Aktif/nonaktifkan AI auto-reply, atur mode review vs auto, dan kustomisasi template.' },
          { title: 'Knowledge Base', desc: 'Upload dokumen brand voice, guidelines, atau fakta produk — AI pakai ini sebagai konteks RAG.' },
          { title: 'AI & Billing', desc: 'Pilih provider AI, pakai API key sendiri (BYOK), atau top up credits. Lihat riwayat transaksi.' },
        ],
        cta: { label: 'Buka Profile', path: '/profile' },
      },
      {
        title: 'Credits & Trial',
        sub: 'Cara kerja biaya AI',
        icon: Coins,
        items: [
          { title: 'Trial 7 hari', desc: 'Setiap akun baru dapat 20 credits gratis. Coba semua fitur tanpa bayar.' },
          { title: 'Hemat credit', desc: 'Setiap generate/analyze pakai 1 credit. Pakai API key sendiri di Settings → AI untuk unlimited, tanpa potong credits.' },
          { title: 'Auto-refund', desc: 'Kalau AI gagal proses, credit otomatis balik. Gak ada credit hangus.' },
        ],
        cta: { label: 'Lihat Plan', path: '/profile/ai' },
      },
    ],
    faqTitle: 'Pertanyaan Umum',
    faqs: [
      { q: 'Apakah data Threads saya aman?', a: 'Ya. Kami pakai OAuth resmi dari Meta — kami tidak pernah menyimpan password. Access token disimpan terenkripsi di Supabase dan hanya dipakai untuk sync/post atas izin kamu.' },
      { q: 'Berapa lama sync data dari Threads?', a: 'Auto-sync berjalan setiap 10 menit di background. Kalau mau langsung update, klik tombol "Sync" di halaman Comments atau "Refresh" di Dashboard.' },
      { q: 'Bisa pakai API key sendiri?', a: 'Bisa. Buka Profile → AI & Billing, masukkan Groq atau Gemini API key kamu. Semua generate tidak akan memotong credits.' },
      { q: 'Auto-reply bikin spam?', a: 'Tidak. Ada dua mode: review (kamu approve dulu sebelum terkirim) dan auto (langsung kirim). Default-nya review biar kamu tetap kontrol.' },
      { q: 'Kalau trial habis, data hilang?', a: 'Tidak. Semua data tetap aman. Kamu cuma perlu top-up credits atau pakai API key sendiri untuk lanjut generate konten.' },
      { q: 'Bisa disconnect Threads?', a: 'Bisa kapan aja di Profile → Account → Disconnect. Semua data auto-sync akan berhenti.' },
    ],
    contactTitle: 'Butuh bantuan?',
    contactSub: 'Kalau ada pertanyaan atau masalah, langsung email kami. Kami balas di hari kerja (biasanya <24 jam).',
    finalCta: 'Buat Post Pertama',
  },
  en: {
    heroTitle: 'Ixiera Guide',
    heroSub: 'Everything you need to start managing Threads with AI — in 5 minutes.',
    quickStartTitle: 'Quick Start (5 Steps)',
    quickStart: [
      'Connect your Threads account in Profile → Account',
      'Create your first post in Content → Create (or use AI generate)',
      'Schedule the post or publish directly',
      'Reply to comments in Comments menu (or let AI auto-reply)',
      'Track performance in Analytics menu',
    ],
    sections: [
      {
        title: 'Dashboard',
        sub: 'Daily summary of your account',
        icon: LayoutDashboard,
        items: [
          { title: 'Action cards', desc: 'Alert cards appear when comments need replies, trial is ending soon, or it\'s the best time to post today.' },
          { title: 'Quick stats', desc: 'Queue, published, failed, and avg engagement rate at a glance.' },
          { title: 'Top posts & charts', desc: 'See your best posts (by views, likes, or ER) and 14-day trends.' },
        ],
        cta: { label: 'Open Dashboard', path: '/dashboard' },
      },
      {
        title: 'Content',
        sub: 'Create, remix, and schedule posts',
        icon: FileText,
        items: [
          { title: 'Create', desc: 'Write manually or generate a 3-day plan with AI. Pick tone, AI provider, and which knowledge base to use for RAG.' },
          { title: 'Variant', desc: 'Remix old posts into new variations with AI — change the angle without losing core content.' },
          { title: 'Queue', desc: 'See all scheduled and published posts. Retry failed posts right from here.' },
        ],
        cta: { label: 'Open Content', path: '/content' },
      },
      {
        title: 'Comments',
        sub: 'Manage audience interactions',
        icon: MessageCircle,
        items: [
          { title: 'Auto-sync', desc: 'New comments are pulled from Threads every 10 minutes. You can manually sync anytime.' },
          { title: 'AI classification', desc: 'Comments are tagged as priority, question, praise, neutral, spam, or toxic.' },
          { title: 'Auto-reply', desc: 'Enable AI auto-reply to respond automatically — or review first before sending.' },
          { title: 'Bulk actions', desc: 'Select multiple comments and process together to save time.' },
        ],
        cta: { label: 'Open Comments', path: '/comment' },
      },
      {
        title: 'Analytics',
        sub: 'Data-driven insights for your account',
        icon: BarChart3,
        items: [
          { title: 'Best Time', desc: 'Best posting time per day based on historical ER. Click a slot to schedule a post at that time.' },
          { title: 'Hook', desc: 'Which hook types perform best (Data-Point, Contrarian, Confession, etc).' },
          { title: 'Length', desc: 'Optimal post length for engagement. Get a recommendation + a button to create a post that length.' },
          { title: 'Topic', desc: 'Top performing topic clusters on your account. Click a topic to create a similar post.' },
        ],
        cta: { label: 'Open Analytics', path: '/analytics' },
      },
      {
        title: 'Profile',
        sub: 'All account settings',
        icon: User,
        items: [
          { title: 'Account', desc: 'Threads connection, appearance (dark/light mode), and language (EN/ID).' },
          { title: 'Auto-Reply', desc: 'Enable/disable AI auto-reply, set review vs auto mode, and customize templates.' },
          { title: 'Knowledge Base', desc: 'Upload brand voice docs, guidelines, or product facts — AI uses these as RAG context.' },
          { title: 'AI & Billing', desc: 'Choose AI provider, use your own API key (BYOK), or top up credits. View transaction history.' },
        ],
        cta: { label: 'Open Profile', path: '/profile' },
      },
      {
        title: 'Credits & Trial',
        sub: 'How AI billing works',
        icon: Coins,
        items: [
          { title: '7-day trial', desc: 'Every new account gets 20 free credits. Try everything without paying.' },
          { title: 'Save credits', desc: 'Each generate/analyze costs 1 credit. Use your own API key in Settings → AI for unlimited, no credit charges.' },
          { title: 'Auto-refund', desc: 'If AI fails, credits are automatically refunded. No lost credits.' },
        ],
        cta: { label: 'View Plan', path: '/profile/ai' },
      },
    ],
    faqTitle: 'Frequently Asked Questions',
    faqs: [
      { q: 'Is my Threads data safe?', a: 'Yes. We use official OAuth from Meta — we never store your password. Access tokens are stored encrypted in Supabase and only used to sync/post with your permission.' },
      { q: 'How often does data sync?', a: 'Auto-sync runs every 10 minutes in the background. For instant update, click "Sync" in Comments or "Refresh" in Dashboard.' },
      { q: 'Can I use my own API key?', a: 'Yes. Open Profile → AI & Billing, enter your Groq or Gemini API key. All generate calls will not charge credits.' },
      { q: 'Does auto-reply spam people?', a: 'No. There are two modes: review (you approve before sending) and auto (sent instantly). Default is review so you stay in control.' },
      { q: 'If trial ends, is my data lost?', a: 'No. All data stays safe. You just need to top up credits or use your own API key to continue generating content.' },
      { q: 'Can I disconnect Threads?', a: 'Yes, anytime in Profile → Account → Disconnect. All auto-sync activity will stop.' },
    ],
    contactTitle: 'Need help?',
    contactSub: 'Got a question or issue? Email us directly. We reply within business days (usually <24h).',
    finalCta: 'Create First Post',
  }
}

const txt = computed(() => content[locale.value as 'id' | 'en'] || content.id)
</script>
