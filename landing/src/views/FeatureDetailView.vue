<template>
  <div class="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)] font-sans selection:bg-[#9984d8] selection:text-white">
    <!-- NAVBAR (Sama) -->
    <nav class="fixed top-0 left-0 right-0 z-50 h-16 bg-[var(--bg-primary)]/80 backdrop-blur-md border-b border-[var(--border)] flex items-center">
      <div class="w-full max-w-[1200px] mx-auto px-6 flex items-center justify-between">
        <a href="/" class="flex items-center gap-2">
          <div class="w-7 h-7 flex items-center justify-center rounded text-xs font-bold bg-[var(--accent)] text-[var(--accent-text)]">IX</div>
          <span class="font-bold text-lg tracking-tight">Ixiera</span>
        </a>
        <!-- Dropdown Desktop -->
        <div class="hidden md:flex items-center gap-8 text-sm font-medium text-[var(--text-secondary)]">
          <div class="relative group py-4">
            <button class="hover:text-[var(--text-primary)] flex items-center gap-1 transition">
              Fitur <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
            </button>
            <div class="absolute top-full left-0 mt-1 w-48 bg-[#050607] border border-[#333] rounded-xl p-2 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all shadow-xl">
              <a href="/features/composer" class="block px-3 py-2 text-sm text-gray-400 hover:text-white hover:bg-[#111] rounded-md transition">Content Composer</a>
              <a href="/features/inbox" class="block px-3 py-2 text-sm text-gray-400 hover:text-white hover:bg-[#111] rounded-md transition">Smart Inbox</a>
              <a href="/features/analytics" class="block px-3 py-2 text-sm text-gray-400 hover:text-white hover:bg-[#111] rounded-md transition">Deep Analytics</a>
            </div>
          </div>
          <a href="/#cara-kerja" class="hover:text-[var(--text-primary)] transition">Cara Kerja</a>
          <a href="/pricing" class="hover:text-[var(--text-primary)] transition">Harga</a>
          <a href="/#faq" class="hover:text-[var(--text-primary)] transition">FAQ</a>
        </div>
        <div class="hidden md:flex items-center gap-4">
          <a href="https://app.ixiera.id/login" class="text-sm font-medium text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition">Log in</a>
          <a href="https://app.ixiera.id/signup" class="btn-bd-primary" style="padding: 8px 16px;">Sign up</a>
        </div>
      </div>
    </nav>

    <main class="pt-32 pb-24 px-6 max-w-[1000px] mx-auto">
      <!-- Content based on slug -->
      
      <!-- COMPOSER -->
      <div v-if="slug === 'composer'">
        <div class="text-center mb-16">
          <div class="pill-bd mb-4 mx-auto inline-block"><span class="w-1.5 h-1.5 rounded-full bg-[#9984d8]"></span> Content Composer</div>
          <h1 class="font-display text-[48px] md:text-[56px] leading-[1.0] mb-6">Dari ide singkat,<br/><span class="italic text-[var(--accent-violet)]">jadi 3 hari konten.</span></h1>
          <p class="text-[18px] text-[var(--text-secondary)] max-w-[600px] mx-auto">Tulis draf, gunakan AI Planner, dan jadwalkan postingan dalam satu layar.</p>
        </div>
        <!-- Mockup Composer (Sama kayak sebelumnya) -->
        <div class="rounded-2xl border border-[#222] bg-[#050607] overflow-hidden shadow-2xl">
          <div class="h-10 bg-[#0a0a0a] border-b border-[#222] flex items-center px-4 gap-2">
            <div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div>
            <div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div>
            <div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div>
            <div class="ml-auto text-[10px] font-mono text-[#555]">app.ixiera.id/content/create</div>
          </div>
          <div class="p-6">
            <h3 class="text-lg font-bold mb-1">Composer</h3>
            <p class="text-xs text-gray-500 mb-6">Tulis atau generate draf otomatis pakai AI.</p>
            <div class="border border-[#222] rounded-xl p-5 bg-[#0a0a0a] mb-6">
              <div class="text-[11px] font-bold text-white mb-4">AI CONTENT PLANNER</div>
              <div class="grid grid-cols-2 gap-4 mb-4">
                <div><label class="text-[10px] text-gray-500 mb-1 block">Topik / Ide Singkat</label><input type="text" placeholder="Masukkan topik..." class="w-full bg-[#000] border border-[#222] rounded-md px-3 py-2 text-sm text-white"></div>
                <div><label class="text-[10px] text-gray-500 mb-1 block">Gaya Bahasa</label><div class="w-full bg-[#000] border border-[#222] rounded-md px-3 py-2 text-sm text-white">Edukasi & Insight</div></div>
              </div>
              <div class="flex justify-end mt-4"><button class="bg-white text-black text-xs font-semibold px-4 py-2 rounded-md">Bikin Rencana 3 Hari</button></div>
            </div>
          </div>
        </div>
      </div>

      <!-- INBOX -->
      <div v-if="slug === 'inbox'">
        <div class="text-center mb-16">
          <div class="pill-bd mb-4 mx-auto inline-block"><span class="w-1.5 h-1.5 rounded-full bg-[#3fcb7f]"></span> Smart Inbox</div>
          <h1 class="font-display text-[48px] md:text-[56px] leading-[1.0] mb-6">Komentar masuk,<br/><span class="italic text-[#3fcb7f]">langsung terpilah.</span></h1>
          <p class="text-[18px] text-[var(--text-secondary)] max-w-[600px] mx-auto">Balas komentar dengan AI atau template tanpa kehilangan sentuhan personal.</p>
        </div>
        <!-- Mockup Inbox (Sama) -->
        <div class="rounded-2xl border border-[#222] bg-[#050607] overflow-hidden shadow-2xl">
          <div class="h-10 bg-[#0a0a0a] border-b border-[#222] flex items-center px-4 gap-2">
            <div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div><div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div><div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div>
            <div class="ml-auto text-[10px] font-mono text-[#555]">app.ixiera.id/comment</div>
          </div>
          <div class="p-6">
            <div class="flex justify-between items-center mb-6 border-b border-[#222] pb-3">
              <div class="flex gap-6 text-xs font-semibold">
                <span class="text-white border-b-2 border-white pb-3 -mb-[13px]">Review (1)</span>
                <span class="text-gray-500">Prioritas (0)</span><span class="text-gray-500">Percakapan (1)</span>
              </div>
            </div>
            <div class="border border-[#222] rounded-xl p-5 bg-[#0a0a0a]">
              <div class="flex items-center gap-2 mb-4"><span class="text-xs font-bold text-white">@ONEZEROWW</span><span class="text-[10px] font-bold text-[#9984d8] bg-[#9984d8]/10 px-2 py-0.5 rounded">PRAISE</span></div>
              <div class="bg-[#000] border border-[#222] rounded-lg p-3 text-sm text-gray-300 mb-4">itulah rakyat, wkwk mental ngemis wehh</div>
              <div class="border border-[#222] rounded-lg bg-[#000] p-3">
                <div class="flex justify-between items-center mb-2"><span class="text-[10px] font-bold text-gray-500">DRAF BALASAN</span></div>
                <textarea class="w-full bg-transparent text-sm text-gray-300 resize-none h-16">terimakasih</textarea>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ANALYTICS -->
      <div v-if="slug === 'analytics'">
        <div class="text-center mb-16">
          <div class="pill-bd mb-4 mx-auto inline-block"><span class="w-1.5 h-1.5 rounded-full bg-[#9984d8]"></span> Deep Analytics</div>
          <h1 class="font-display text-[48px] md:text-[56px] leading-[1.0] mb-6">Tahu persis<br/><span class="italic text-[var(--accent-violet)]">apa yang jalan.</span></h1>
          <p class="text-[18px] text-[var(--text-secondary)] max-w-[600px] mx-auto">Ketahui jam terbaik, hook terbaik, dan tren performa akunmu.</p>
        </div>
        <!-- Mockup Analytics (Sama) -->
        <div class="rounded-2xl border border-[#222] bg-[#050607] overflow-hidden shadow-2xl">
          <div class="h-10 bg-[#0a0a0a] border-b border-[#222] flex items-center px-4 gap-2">
            <div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div><div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div><div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div>
            <div class="ml-auto text-[10px] font-mono text-[#555]">app.ixiera.id/analytics/best-time</div>
          </div>
          <div class="p-6">
            <div class="border border-[#9984d8] rounded-xl p-5 bg-[#9984d8]/5 mb-6 relative overflow-hidden">
              <div class="text-[10px] text-[#9984d8] bg-[#9984d8]/20 px-2 py-0.5 rounded font-bold uppercase tracking-wider mb-2 inline-block">Waktu Terbaik</div>
              <div class="text-2xl font-bold text-white mb-4">Selasa, 08:00–12:00 WIB</div>
              <button class="bg-white text-black text-xs font-semibold px-4 py-2 rounded-md">Jadwalkan Sekarang</button>
            </div>
            <div class="border border-[#222] rounded-xl p-5 bg-[#0a0a0a]">
              <div class="text-[11px] font-bold text-white mb-4">Waktu Terbaik Per Hari</div>
              <div class="space-y-2">
                <div class="flex justify-between items-center p-2"><span class="text-xs text-white">Selasa (11:00)</span><div class="flex items-center gap-4"><div class="w-32 h-1.5 bg-[#222] rounded-full overflow-hidden"><div class="h-full bg-white" style="width: 85%"></div></div><span class="text-xs font-bold text-[#3fcb7f]">13.64%</span></div></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const slug = computed(() => route.params.slug)
</script>
