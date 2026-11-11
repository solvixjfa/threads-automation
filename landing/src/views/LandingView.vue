<template>
  <div class="min-h-screen font-sans selection:bg-[var(--text)] selection:text-[var(--bg)] bg-[var(--bg)] text-[var(--text)] overflow-x-hidden">
    
    <!-- NAVBAR -->
    <AppNavbar />

    <main class="pt-24 md:pt-32">
      <!-- HERO -->
      <section class="max-w-[1120px] mx-auto px-6 pb-20 md:pb-32 flex flex-col md:flex-row items-center gap-12">
        <div class="flex-1 space-y-6 text-center md:text-left fade-in">
          <div class="inline-flex items-center px-3 py-1 rounded-full border border-[var(--line)] text-xs font-bold tracking-widest text-[var(--muted)] uppercase">{{ $t('landing.hero.badge') }}</div>
          
          <h1 class="font-display text-5xl md:text-7xl leading-[1.05]">
            {{ $t('landing.hero.title_1') }} <br class="hidden md:block"/>
            <span class="italic text-[var(--text)]">{{ $t('landing.hero.title_2') }}</span>
          </h1>
          
          <p class="text-lg text-[var(--muted)] leading-relaxed max-w-xl mx-auto md:mx-0">{{ $t('landing.hero.subtitle') }}</p>
          
          <div class="flex flex-col sm:flex-row items-center justify-center md:justify-start gap-4 pt-4">
            <a href="https://app.ixiera.id/login" class="w-full sm:w-auto px-8 py-3.5 rounded-full text-base font-bold bg-[var(--text)] text-[var(--bg)] hover:opacity-90 transition">{{ $t('landing.hero.cta_primary') }}</a>
            <a href="#contoh" class="w-full sm:w-auto px-8 py-3.5 rounded-full text-base font-bold border border-[var(--line)] hover:bg-[var(--surface-2)] transition">{{ $t('landing.hero.cta_secondary') }}</a>
          </div>
          
          <p class="text-xs text-[var(--muted)] pt-2">{{ $t('landing.hero.microcopy') }}</p>
          
          <div class="flex flex-col sm:flex-row gap-4 pt-8 text-xs text-[var(--muted)] justify-center md:justify-start">
            <span class="flex items-center gap-2"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg> {{ $t('landing.hero.trust_1') }}</span>
            <span class="flex items-center gap-2"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg> {{ $t('landing.hero.trust_2') }}</span>
            <span class="flex items-center gap-2"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg> {{ $t('landing.hero.trust_3') }}</span>
          </div>
        </div>

        <!-- MOCKUP HERO: DASHBOARD (PIXEL PERFECT) -->
        <div class="flex-1 w-full max-w-md mx-auto fade-in">
          <div class="border border-[#222] rounded-2xl overflow-hidden bg-[#050607] shadow-2xl">
            <div class="flex items-center gap-1.5 px-4 py-3 border-b border-[#1a1a1a] bg-[#0a0a0a]">
              <div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div>
              <div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div>
              <div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div>
              <div class="ml-auto text-[10px] font-mono text-[#666]">app.ixiera.id/dashboard</div>
            </div>
            <div class="p-5 space-y-4">
              <div class="grid grid-cols-2 gap-3">
                <div class="bg-[#000] border border-[#1a1a1a] rounded-xl p-3">
                  <p class="text-[10px] text-[#666] mb-1">TOTAL VIEWS</p>
                  <p class="text-xl font-bold text-white tracking-tight">324.158</p>
                </div>
                <div class="bg-[#000] border border-[#1a1a1a] rounded-xl p-3">
                  <p class="text-[10px] text-[#666] mb-1">AVG ENGAGEMENT</p>
                  <p class="text-xl font-bold text-white tracking-tight">0.97%</p>
                </div>
              </div>
              <div class="bg-[#000] border border-[#1a1a1a] rounded-xl p-4">
                <div class="flex justify-between items-center mb-3">
                  <span class="text-[10px] text-[#666] uppercase tracking-widest font-bold">Growth Harian</span>
                  <div class="flex gap-2 text-[9px] font-bold text-[#666]">
                    <span class="text-white">7D</span><span>14D</span><span>30D</span>
                  </div>
                </div>
                <svg viewBox="0 0 400 80" class="w-full" preserveAspectRatio="none" style="height: 60px;">
                  <defs>
                    <linearGradient id="chartGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.2" />
                      <stop offset="100%" stop-color="#ffffff" stop-opacity="0" />
                    </linearGradient>
                  </defs>
                  <path d="M0,60 Q50,55 80,45 T160,35 T240,20 T320,15 L400,10 L400,80 L0,80 Z" fill="url(#chartGradient)" />
                  <path d="M0,60 Q50,55 80,45 T160,35 T240,20 T320,15 L400,10" stroke="#ffffff" stroke-width="1.5" fill="none" />
                </svg>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- FITUR -->
      <section id="fitur" class="py-20 md:py-32 border-t border-[var(--line)]">
        <div class="max-w-[1120px] mx-auto px-6">
          <div class="text-center mb-20 fade-in">
            <h2 class="font-display text-4xl md:text-5xl">{{ $t('landing.features.title') }}</h2>
            <p class="text-lg text-[var(--muted)] mt-4">{{ $t('landing.features.subtitle') }}</p>
          </div>

          <div class="space-y-32">
            <!-- Fitur 1: Content (PIXEL PERFECT COMPOSER) -->
            <div class="flex flex-col md:flex-row items-center gap-12">
              <div class="flex-1 space-y-4 fade-in">
                <span class="text-xs font-bold uppercase tracking-widest text-[var(--muted)]">01 · Content</span>
                <h3 class="font-display text-3xl">{{ $t('landing.features.f1_title') }}</h3>
                <p class="text-[var(--muted)] leading-relaxed">{{ $t('landing.features.f1_desc') }}</p>
              </div>
              
              <div class="flex-1 w-full">
                <div class="border border-[#222] rounded-xl overflow-hidden bg-[#050607] shadow-2xl">
                  <div class="flex items-center gap-1.5 px-4 py-3 border-b border-[#1a1a1a] bg-[#0a0a0a]">
                    <div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div><div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div><div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div>
                    <span class="ml-2 text-[10px] text-[#666] font-mono">app.ixiera.id/content/create</span>
                  </div>
                  <div class="p-5">
                    <div class="mb-4">
                      <h3 class="text-sm font-bold text-white mb-1">Composer</h3>
                      <p class="text-[10px] text-[#666]">Tulis atau generate draf otomatis pakai AI, pecah utasan, dan jadwalkan postingan.</p>
                    </div>
                    
                    <div class="border border-[#222] rounded-xl p-4 bg-[#0a0a0a] mb-4">
                      <div class="text-[10px] font-bold text-white mb-3 flex items-center gap-2">
                        <span class="w-2 h-2 rounded-full bg-white"></span> AI CONTENT PLANNER
                      </div>
                      <div class="grid grid-cols-2 gap-3 mb-3">
                        <div>
                          <label class="text-[9px] text-[#666] block mb-1">Topik / Ide Singkat</label>
                          <div class="w-full bg-[#000] border border-[#222] rounded-md px-2 py-1.5 text-[10px] text-[#666]">Masukkan topik singkat...</div>
                        </div>
                        <div>
                          <label class="text-[9px] text-[#666] block mb-1">Gaya Bahasa</label>
                          <div class="w-full bg-[#000] border border-[#222] rounded-md px-2 py-1.5 text-[10px] text-white flex justify-between items-center">
                            <span>Edukasi & Insight</span>
                            <svg class="w-3 h-3 text-[#666]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                          </div>
                        </div>
                      </div>
                      <div class="flex justify-end mt-2">
                        <button class="bg-white text-black text-[10px] font-bold px-3 py-1.5 rounded-md">Bikin Rencana 3 Hari</button>
                      </div>
                    </div>

                    <div class="border border-[#222] rounded-xl p-4 bg-[#0a0a0a]">
                      <div class="text-[10px] font-bold text-white mb-3 flex justify-between">
                        <span>TEKS POSTINGAN UTAMA</span>
                        <span class="text-[#666] font-normal">0 Karakter</span>
                      </div>
                      <div class="w-full bg-[#000] border border-[#222] rounded-md p-2 text-[10px] text-[#666] h-16 mb-3">Tulis draf kamu di sini...</div>
                      <div class="flex justify-between items-center pt-3 border-t border-[#222]">
                        <div class="flex gap-2 text-[9px] text-[#666]">
                          <span class="bg-[#1a1a1a] px-2 py-1 rounded">Best time hari ini 17:00</span>
                          <span class="bg-[#1a1a1a] px-2 py-1 rounded">Pakai Insight</span>
                        </div>
                        <button class="bg-white text-black text-[10px] font-bold px-3 py-1.5 rounded-md">Jadwalkan</button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Fitur 2: Komentar (PIXEL PERFECT INBOX) -->
            <div class="flex flex-col md:flex-row-reverse items-center gap-12">
              <div class="flex-1 space-y-4 fade-in">
                <span class="text-xs font-bold uppercase tracking-widest text-[var(--muted)]">02 · Komentar</span>
                <h3 class="font-display text-3xl">{{ $t('landing.features.f2_title') }}</h3>
                <p class="text-[var(--muted)] leading-relaxed">{{ $t('landing.features.f2_desc') }}</p>
              </div>
              
              <div class="flex-1 w-full">
                <div class="border border-[#222] rounded-xl overflow-hidden bg-[#050607] shadow-2xl">
                  <div class="flex items-center gap-1.5 px-4 py-3 border-b border-[#1a1a1a] bg-[#0a0a0a]">
                    <div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div><div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div><div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div>
                    <span class="ml-2 text-[10px] text-[#666] font-mono">app.ixiera.id/comment</span>
                  </div>
                  <div class="p-5">
                    <div class="mb-4">
                      <h3 class="text-sm font-bold text-white mb-1">Komentar</h3>
                      <p class="text-[10px] text-[#666]">Balas komentar di postingan kamu pakai draf AI atau template.</p>
                    </div>

                    <div class="flex gap-4 border-b border-[#222] pb-2 mb-4 text-[10px] font-bold">
                      <span class="text-white border-b-2 border-white pb-2 -mb-[10px]">Review (1)</span>
                      <span class="text-[#666]">Prioritas (0)</span>
                      <span class="text-[#666]">Percakapan (1)</span>
                      <span class="text-[#666]">Riwayat (48)</span>
                    </div>

                    <div class="border border-[#222] rounded-xl p-4 bg-[#0a0a0a]">
                      <div class="flex items-center gap-2 mb-3">
                        <div class="w-5 h-5 rounded-full bg-[#222]"></div>
                        <span class="text-[10px] font-bold text-white">@username</span>
                        <span class="text-[9px] font-bold text-[#9984d8] bg-[#9984d8]/10 px-2 py-0.5 rounded border border-[#9984d8]/20">PRAISE</span>
                      </div>
                      
                      <div class="bg-[#000] border border-[#222] rounded-lg p-2 text-[10px] text-white mb-3">
                        Kontennya sangat membantu, kak! Ditunggu update selanjutnya.
                      </div>
                      
                      <div class="border border-[#222] rounded-lg bg-[#000] p-3">
                        <div class="flex justify-between items-center mb-2">
                          <span class="text-[9px] font-bold text-[#666]">DRAF BALASAN <span class="text-[#444]">| DARI TEMPLATE</span></span>
                          <button class="text-[9px] font-bold text-white bg-[#1a1a1a] px-2 py-1 rounded flex items-center gap-1 border border-[#333]">
                            <svg class="w-3 h-3 text-[#9984d8]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg> Bikin Ulang AI
                          </button>
                        </div>
                        <div class="text-[10px] text-[#999] bg-[#111] border border-[#222] rounded p-2 h-10 mb-3">
                          Terima kasih banyak, kak! Senang bisa membantu.
                        </div>
                        <div class="flex justify-end gap-2">
                          <button class="text-[9px] font-bold text-[#666] px-2 py-1">Abaikan</button>
                          <button class="bg-white text-black text-[9px] font-bold px-3 py-1.5 rounded-md flex items-center gap-1">
                            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path></svg> Kirim ke Threads
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Fitur 3: Analytics (PIXEL PERFECT BEST TIME) -->
            <div class="flex flex-col md:flex-row items-center gap-12">
              <div class="flex-1 space-y-4 fade-in">
                <span class="text-xs font-bold uppercase tracking-widest text-[var(--muted)]">03 · Analytics</span>
                <h3 class="font-display text-3xl">{{ $t('landing.features.f3_title') }}</h3>
                <p class="text-[var(--muted)] leading-relaxed">{{ $t('landing.features.f3_desc') }}</p>
              </div>
              
              <div class="flex-1 w-full">
                <div class="border border-[#222] rounded-xl overflow-hidden bg-[#050607] shadow-2xl">
                  <div class="flex items-center gap-1.5 px-4 py-3 border-b border-[#1a1a1a] bg-[#0a0a0a]">
                    <div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div><div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div><div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div>
                    <span class="ml-2 text-[10px] text-[#666] font-mono">app.ixiera.id/analytics/best-time</span>
                  </div>
                  <div class="p-5">
                    <div class="mb-4">
                      <h3 class="text-sm font-bold text-white mb-1">Waktu Terbaik</h3>
                      <p class="text-[10px] text-[#666]">Tren engagement berdasarkan jam (WIB).</p>
                    </div>

                    <!-- Best Time Card -->
                    <div class="border border-[#9984d8] rounded-xl p-4 bg-[#9984d8]/5 mb-4 relative overflow-hidden">
                      <div class="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-[#9984d8] to-transparent"></div>
                      <div class="text-[9px] text-[#9984d8] bg-[#9984d8]/20 px-2 py-0.5 rounded font-bold uppercase tracking-wider mb-2 inline-block">Waktu Terbaik Berikutnya</div>
                      <div class="text-lg font-bold text-white mb-1">Selasa, 08:00–12:00 WIB</div>
                      <div class="text-[10px] text-[#999] mb-3">3.20% Rata-rata ER • 8 post (Pagi)</div>
                      <button class="bg-white text-black text-[10px] font-bold px-3 py-1.5 rounded-md">Jadwalkan Sekarang</button>
                    </div>

                    <!-- Chart -->
                    <div class="border border-[#222] rounded-xl p-4 bg-[#0a0a0a] mb-4">
                      <div class="text-[10px] font-bold text-white mb-3 flex justify-between items-center">
                        <span>Waktu Terbaik untuk Posting</span>
                        <span class="text-[8px] bg-[#1a1a1a] text-[#666] px-1.5 py-0.5 rounded">DATA LENGKAP</span>
                      </div>
                      <svg viewBox="0 0 400 80" class="w-full" preserveAspectRatio="none" style="height: 60px;">
                        <defs>
                          <linearGradient id="chartGradient" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="0%" stop-color="#ffffff" stop-opacity="0.2" />
                            <stop offset="100%" stop-color="#ffffff" stop-opacity="0" />
                          </linearGradient>
                        </defs>
                        <path d="M0,60 Q50,55 80,45 T160,35 T240,20 T320,15 L400,10 L400,80 L0,80 Z" fill="url(#chartGradient)" />
                        <path d="M0,60 Q50,55 80,45 T160,35 T240,20 T320,15 L400,10" stroke="#ffffff" stroke-width="1.5" fill="none" />
                      </svg>
                      <div class="flex justify-between mt-2 text-[8px] text-[#666]">
                        <span>00:00</span><span>09:00</span><span>12:00</span><span>18:00</span><span>21:00</span>
                      </div>
                    </div>
                    
                    <!-- List -->
                    <div class="border border-[#222] rounded-xl p-4 bg-[#0a0a0a]">
                      <div class="text-[10px] font-bold text-white mb-3">Waktu Terbaik Per Hari</div>
                      <div class="space-y-2">
                        <div class="flex items-center justify-between bg-[#111] p-2 rounded border border-[#222]">
                          <div class="flex items-center gap-2">
                            <span class="w-4 h-4 rounded-full bg-[#222] flex items-center justify-center text-[8px] text-white">3</span>
                            <span class="text-[10px] text-white">Selasa (11:00)</span>
                          </div>
                          <div class="flex items-center gap-3">
                            <span class="text-[10px] font-bold text-[#3fcb7f]">13.64%</span>
                            <button class="bg-[#222] text-white text-[8px] px-2 py-1 rounded">Jadwalkan</button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- FAQ -->
      <section id="faq" class="py-20 md:py-32 bg-[var(--surface)] border-t border-[var(--line)]">
        <div class="max-w-3xl mx-auto px-6 fade-in">
          <h2 class="font-display text-4xl text-center mb-12">{{ $t('landing.faq.title') }}</h2>
          <div class="space-y-2">
            <div v-for="i in 9" :key="i" class="border border-[var(--line)] rounded-lg bg-[var(--bg)] overflow-hidden">
              <button @click="faqOpen = faqOpen === i ? null : i" class="w-full px-6 py-4 text-left flex justify-between items-center font-bold hover:bg-[var(--surface-2)] transition">
                <span>{{ $t('landing.faq.q' + i) }}</span>
                <svg class="w-5 h-5 transition-transform duration-300" :class="{'rotate-180': faqOpen === i}" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
              </button>
              <div v-if="faqOpen === i" class="px-6 pb-4 text-sm text-[var(--muted)] leading-relaxed">{{ $t('landing.faq.a' + i) }}</div>
            </div>
          </div>
        </div>
      </section>

    </main>

    <!-- FOOTER -->
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import AppNavbar from '../components/layouts/AppNavbar.vue'
import AppFooter from '../components/layouts/AppFooter.vue'
import { RouterLink } from 'vue-router'

const faqOpen = ref<number | null>(1)

const hookData = ref([
  { label: 'Question', er: 2.92, n: 6 },
  { label: 'Story', er: 1.36, n: 32 },
])
const lengthData = ref([
  { label: '300–500 char', er: 2.96, n: 10 },
  { label: '100–300 char', er: 1.12, n: 25 },
])

function getBarWidth(er: number) {
  const maxER = 3.5
  const pct = (er / maxER) * 100
  return `${Math.min(pct, 100)}%`
}



onMounted(() => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible')
        entry.target.querySelectorAll('.bar-grow').forEach(bar => {
          const width = (bar as HTMLElement).style.width
          ;(bar as HTMLElement).style.width = '0%'
          setTimeout(() => {
            (bar as HTMLElement).style.width = width
          }, 50)
        })
        observer.unobserve(entry.target)
      }
    })
  }, { threshold: 0.1 })
  document.querySelectorAll('.fade-in').forEach(el => observer.observe(el))
})
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&display=swap');

:root {
  --bg: #000000; --surface: #050607; --surface-2: #0A0A0A;
  --line: #222222; --text: #FFFFFF; --muted: #A3A3A3;
  --faint: #555555; --bar-dim: #404040;
}
html:not(.dark) {
  --bg: #FFFFFF; --surface: #FAFAFA; --surface-2: #F2F2F2;
  --line: #E5E5E5; --text: #0A0A0A; --muted: #525252;
  --faint: #A3A3A3; --bar-dim: #C4C4C4;
}

body {
  background-color: var(--bg);
  color: var(--text);
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  font-variant-numeric: tabular-nums;
  -webkit-font-smoothing: antialiased;
}

.font-display {
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-weight: 500;
  letter-spacing: -0.01em;
}

.fade-in {
  opacity: 0;
  transform: translateY(8px);
  transition: opacity 300ms ease-out, transform 300ms ease-out;
}
.fade-in.visible {
  opacity: 1;
  transform: translateY(0);
}
.bar-grow {
  transition: width 800ms cubic-bezier(0.4, 0, 0.2, 1);
}
@media (prefers-reduced-motion: reduce) {
  .fade-in, .bar-grow {
    transition: none !important;
    animation: none !important;
    opacity: 1 !important;
    transform: none !important;
  }
}
</style>
