<template>
  <div class="min-h-screen bg-[var(--bg)] text-[var(--text)] font-sans">
    <AppNavbar />
    
    <main class="pt-32 pb-24 px-6 max-w-[1120px] mx-auto">
      <!-- Content based on slug -->
      
      <!-- COMPOSER -->
      <div v-if="slug === 'composer'">
        <div class="text-center mb-16 fade-in">
          <div class="pill-bd mb-4 mx-auto inline-block"><span class="w-1.5 h-1.5 rounded-full bg-[#9984d8]"></span> Content Composer</div>
          <h1 class="font-display text-5xl md:text-6xl mb-6">Dari ide singkat,<br/><span class="italic">jadi 3 hari konten.</span></h1>
          <p class="text-lg text-[var(--muted)] max-w-2xl mx-auto">Tulis draf, gunakan AI Planner, dan jadwalkan postingan dalam satu layar. Nggak perlu buka banyak tab lagi.</p>
        </div>
        
        <!-- Mockup Composer -->
        <div class="max-w-3xl mx-auto border border-[#222] rounded-xl overflow-hidden bg-[#050607] shadow-2xl">
          <div class="flex items-center gap-1.5 px-4 py-3 border-b border-[#1a1a1a] bg-[#0a0a0a]">
            <div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div><div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div><div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div>
            <span class="ml-2 text-[10px] text-[#666] font-mono">app.ixiera.id/content/create</span>
          </div>
          <div class="p-6">
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
                  <div class="w-full bg-[#000] border border-[#222] rounded-md px-3 py-2 text-[10px] text-white">Strategi konten Threads Q4</div>
                </div>
                <div>
                  <label class="text-[9px] text-[#666] block mb-1">Gaya Bahasa</label>
                  <div class="w-full bg-[#000] border border-[#222] rounded-md px-3 py-2 text-[10px] text-white flex justify-between items-center">
                    <span>Edukasi & Insight</span>
                    <svg class="w-3 h-3 text-[#666]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                  </div>
                </div>
              </div>
              <div class="flex justify-end mt-2">
                <button class="bg-white text-black text-[10px] font-bold px-4 py-2 rounded-md">Bikin Rencana 3 Hari</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- INBOX -->
      <div v-if="slug === 'inbox'">
        <div class="text-center mb-16 fade-in">
          <div class="pill-bd mb-4 mx-auto inline-block"><span class="w-1.5 h-1.5 rounded-full bg-[#3fcb7f]"></span> Smart Inbox</div>
          <h1 class="font-display text-5xl md:text-6xl mb-6">Komentar masuk,<br/><span class="italic text-[#3fcb7f]">langsung terpilah.</span></h1>
          <p class="text-lg text-[var(--muted)] max-w-2xl mx-auto">Balas komentar dengan AI atau template tanpa kehilangan sentuhan personal. Pilih mode Review Manual atau Full Auto.</p>
        </div>

        <!-- Mockup Inbox -->
        <div class="max-w-3xl mx-auto border border-[#222] rounded-xl overflow-hidden bg-[#050607] shadow-2xl">
          <div class="flex items-center gap-1.5 px-4 py-3 border-b border-[#1a1a1a] bg-[#0a0a0a]">
            <div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div><div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div><div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div>
            <span class="ml-2 text-[10px] text-[#666] font-mono">app.ixiera.id/comment</span>
          </div>
          <div class="p-6">
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
              <div class="bg-[#000] border border-[#222] rounded-lg p-3 text-[10px] text-white mb-3">
                Kontennya sangat membantu, kak! Ditunggu update selanjutnya.
              </div>
              <div class="border border-[#222] rounded-lg bg-[#000] p-3">
                <div class="flex justify-between items-center mb-2">
                  <span class="text-[9px] font-bold text-[#666]">DRAF BALASAN <span class="text-[#444]">| DARI TEMPLATE</span></span>
                  <button class="text-[9px] font-bold text-white bg-[#1a1a1a] px-2 py-1 rounded flex items-center gap-1 border border-[#333]">
                    Bikin Ulang AI
                  </button>
                </div>
                <div class="text-[10px] text-[#999] bg-[#111] border border-[#222] rounded p-3 h-12 mb-3">
                  Terima kasih banyak, kak! Senang bisa membantu.
                </div>
                <div class="flex justify-end gap-2">
                  <button class="text-[9px] font-bold text-[#666] px-2 py-1">Abaikan</button>
                  <button class="bg-white text-black text-[9px] font-bold px-3 py-1.5 rounded-md flex items-center gap-1">
                    Kirim ke Threads
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ANALYTICS -->
      <div v-if="slug === 'analytics'">
        <div class="text-center mb-16 fade-in">
          <div class="pill-bd mb-4 mx-auto inline-block"><span class="w-1.5 h-1.5 rounded-full bg-[#9984d8]"></span> Deep Analytics</div>
          <h1 class="font-display text-5xl md:text-6xl mb-6">Tahu persis<br/><span class="italic">apa yang jalan.</span></h1>
          <p class="text-lg text-[var(--muted)] max-w-2xl mx-auto">Ketahui jam terbaik, hook terbaik, dan tren performa akunmu. Semua data dihitung dari akunmu sendiri.</p>
        </div>

        <!-- Mockup Analytics -->
        <div class="max-w-3xl mx-auto border border-[#222] rounded-xl overflow-hidden bg-[#050607] shadow-2xl">
          <div class="flex items-center gap-1.5 px-4 py-3 border-b border-[#1a1a1a] bg-[#0a0a0a]">
            <div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div><div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div><div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div>
            <span class="ml-2 text-[10px] text-[#666] font-mono">app.ixiera.id/analytics/best-time</span>
          </div>
          <div class="p-6">
            <div class="border border-[#9984d8] rounded-xl p-5 bg-[#9984d8]/5 mb-6 relative overflow-hidden">
              <div class="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-[#9984d8] to-transparent"></div>
              <div class="text-[9px] text-[#9984d8] bg-[#9984d8]/20 px-2 py-0.5 rounded font-bold uppercase tracking-wider mb-2 inline-block">Waktu Terbaik Berikutnya</div>
              <div class="text-xl font-bold text-white mb-1">Selasa, 08:00–12:00 WIB</div>
              <div class="text-[10px] text-[#999] mb-4">3.20% Rata-rata ER • 8 post (Pagi)</div>
              <button class="bg-white text-black text-[10px] font-bold px-4 py-2 rounded-md">Jadwalkan Sekarang</button>
            </div>

            <div class="border border-[#222] rounded-xl p-5 bg-[#0a0a0a]">
              <div class="text-[10px] font-bold text-white mb-4">Waktu Terbaik Per Hari</div>
              <div class="space-y-2">
                <div class="flex items-center justify-between bg-[#111] p-3 rounded border border-[#222]">
                  <div class="flex items-center gap-3">
                    <span class="w-5 h-5 rounded-full bg-[#222] flex items-center justify-center text-[10px] text-white">3</span>
                    <span class="text-[11px] text-white">Selasa (11:00)</span>
                  </div>
                  <div class="flex items-center gap-4">
                    <span class="text-[11px] font-bold text-[#3fcb7f]">13.64%</span>
                    <button class="bg-[#222] text-white text-[9px] px-3 py-1.5 rounded">Jadwalkan</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

    </main>
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import AppNavbar from '../components/layouts/AppNavbar.vue'
import AppFooter from '../components/layouts/AppFooter.vue'

const route = useRoute()
const slug = computed(() => route.params.slug)
</script>
