<template>
  <div class="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)] font-sans selection:bg-[#9984d8] selection:text-white">
    <!-- TOP NAVBAR -->
    <nav class="fixed top-0 left-0 right-0 z-50 h-16 bg-[var(--bg-primary)]/80 backdrop-blur-md border-b border-[var(--border)] flex items-center">
      <div class="w-full max-w-[1200px] mx-auto px-6 flex items-center justify-between">
        <a href="/" class="flex items-center gap-2">
          <div class="w-7 h-7 flex items-center justify-center rounded text-xs font-bold bg-[var(--accent)] text-[var(--accent-text)]">IX</div>
          <span class="font-bold text-lg tracking-tight">Ixiera</span>
        </a>
        <div class="hidden md:flex items-center gap-8 text-sm font-medium text-[var(--text-secondary)]">
          <a href="/features" class="text-[var(--text-primary)] transition">Fitur</a>
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
      <div class="text-center mb-20">
        <h1 class="font-display text-[48px] md:text-[64px] leading-[1.0] mb-6">Satu platform,<br/><span class="italic text-[var(--accent-violet)]">semua kendali.</span></h1>
        <p class="text-[18px] text-[var(--text-secondary)] max-w-[600px] mx-auto">Dari perencanaan konten hingga analitik mendalam, semua yang kamu butuhkan ada di sini.</p>
      </div>

      <!-- FEATURE 1: COMPOSER -->
      <div class="mb-32">
        <div class="mb-8 text-center">
          <h2 class="text-2xl font-semibold mb-2">Content Composer</h2>
          <p class="text-[var(--text-secondary)]">Tulis draf, gunakan AI Planner, dan jadwalkan postingan dalam satu layar.</p>
        </div>
        
        <!-- Mockup Composer -->
        <div class="rounded-2xl border border-[#222] bg-[#050607] overflow-hidden shadow-2xl">
          <div class="h-10 bg-[#0a0a0a] border-b border-[#222] flex items-center px-4 gap-2">
            <div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div>
            <div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div>
            <div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div>
            <div class="ml-auto text-[10px] font-mono text-[#555]">app.ixiera.id/content/create</div>
          </div>
          <div class="p-6">
            <h3 class="text-lg font-bold mb-1">Composer</h3>
            <p class="text-xs text-gray-500 mb-6">Tulis atau generate draf otomatis pakai AI, pecah utasan, dan jadwalkan postingan.</p>
            
            <div class="border border-[#222] rounded-xl p-5 bg-[#0a0a0a] mb-6">
              <div class="text-[11px] font-bold text-white mb-4 flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-white"></span> AI CONTENT PLANNER
              </div>
              <div class="grid grid-cols-2 gap-4 mb-4">
                <div>
                  <label class="text-[10px] text-gray-500 block mb-1">Topik / Ide Singkat</label>
                  <input type="text" placeholder="Masukkan topik singkat..." class="w-full bg-[#000] border border-[#222] rounded-md px-3 py-2 text-sm text-white focus:outline-none">
                </div>
                <div>
                  <label class="text-[10px] text-gray-500 block mb-1">Gaya Bahasa</label>
                  <div class="w-full bg-[#000] border border-[#222] rounded-md px-3 py-2 text-sm text-white flex justify-between items-center">
                    <span>Edukasi & Insight</span>
                    <svg class="w-3 h-3 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                  </div>
                </div>
              </div>
              <div class="flex justify-end mt-4">
                <button class="bg-white text-black text-xs font-semibold px-4 py-2 rounded-md">Bikin Rencana 3 Hari</button>
              </div>
            </div>

            <div class="border border-[#222] rounded-xl p-5 bg-[#0a0a0a]">
              <div class="text-[11px] font-bold text-white mb-4 flex items-center justify-between">
                <span>TEKS POSTINGAN UTAMA</span>
                <span class="text-gray-500 font-normal">0 Karakter</span>
              </div>
              <textarea placeholder="Tulis draf kamu di sini..." class="w-full bg-[#000] border border-[#222] rounded-md p-3 text-sm text-white h-32 resize-none focus:outline-none"></textarea>
              
              <div class="flex justify-between items-center mt-4 pt-4 border-t border-[#222]">
                <div class="flex gap-2 text-[10px] text-gray-500">
                  <span class="bg-[#222] px-2 py-1 rounded">Best time hari ini 17:00</span>
                  <span class="bg-[#222] px-2 py-1 rounded">Pakai Insight</span>
                </div>
                <div class="flex gap-2">
                  <div class="bg-[#111] border border-[#222] rounded-md px-3 py-2 text-sm text-white">11/11/2026, 14:00</div>
                  <button class="bg-white text-black text-xs font-semibold px-4 py-2 rounded-md">Jadwalkan</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- FEATURE 2: INBOX -->
      <div class="mb-32">
        <div class="mb-8 text-center">
          <h2 class="text-2xl font-semibold mb-2">Smart Inbox</h2>
          <p class="text-[var(--text-secondary)]">Balas komentar dengan AI atau template tanpa kehilangan sentuhan personal.</p>
        </div>
        
        <!-- Mockup Inbox -->
        <div class="rounded-2xl border border-[#222] bg-[#050607] overflow-hidden shadow-2xl">
          <div class="h-10 bg-[#0a0a0a] border-b border-[#222] flex items-center px-4 gap-2">
            <div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div>
            <div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div>
            <div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div>
            <div class="ml-auto text-[10px] font-mono text-[#555]">app.ixiera.id/comment</div>
          </div>
          <div class="p-6">
            <h3 class="text-lg font-bold mb-1">Komentar</h3>
            <p class="text-xs text-gray-500 mb-6">Balas komentar di postingan kamu pakai draf AI atau template.</p>
            
            <div class="flex justify-between items-center mb-6 border-b border-[#222] pb-3">
              <div class="flex gap-6 text-xs font-semibold">
                <span class="text-white border-b-2 border-white pb-3 -mb-[13px]">Review (1)</span>
                <span class="text-gray-500">Prioritas (0)</span>
                <span class="text-gray-500">Percakapan (1)</span>
                <span class="text-gray-500">Riwayat (48)</span>
              </div>
              <div class="w-4 h-4 border border-gray-600 rounded bg-[#111]"></div>
            </div>

            <div class="border border-[#222] rounded-xl p-5 bg-[#0a0a0a]">
              <div class="flex items-center gap-2 mb-4">
                <div class="w-5 h-5 rounded-full bg-gray-700"></div>
                <span class="text-xs font-bold text-white">@ONEZEROWW</span>
                <span class="text-[10px] font-bold text-[#9984d8] bg-[#9984d8]/10 px-2 py-0.5 rounded">PRAISE</span>
              </div>
              <div class="bg-[#000] border border-[#222] rounded-lg p-3 text-sm text-gray-300 mb-4">
                itulah rakyat, wkwk mental ngemis wehh
              </div>
              
              <div class="border border-[#222] rounded-lg bg-[#000] p-3">
                <div class="flex justify-between items-center mb-2">
                  <span class="text-[10px] font-bold text-gray-500">DRAF BALASAN <span class="text-gray-600">| DARI TEMPLATE</span></span>
                  <button class="text-[10px] font-semibold text-white flex items-center gap-1 bg-[#222] px-2 py-1 rounded">
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg> Bikin Ulang AI
                  </button>
                </div>
                <textarea class="w-full bg-transparent text-sm text-gray-300 resize-none focus:outline-none h-16">terimakasih</textarea>
              </div>
              
              <div class="flex justify-end gap-3 mt-4">
                <button class="text-xs text-gray-500 hover:text-white px-2">Abaikan</button>
                <button class="bg-white text-black text-xs font-semibold px-4 py-2 rounded-md flex items-center gap-2">
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path></svg>
                  Kirim ke Threads
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- FEATURE 3: ANALYTICS -->
      <div class="mb-20">
        <div class="mb-8 text-center">
          <h2 class="text-2xl font-semibold mb-2">Deep Analytics</h2>
          <p class="text-[var(--text-secondary)]">Ketahui jam terbaik, hook terbaik, dan tren performa akunmu.</p>
        </div>
        
        <!-- Mockup Analytics -->
        <div class="rounded-2xl border border-[#222] bg-[#050607] overflow-hidden shadow-2xl">
          <div class="h-10 bg-[#0a0a0a] border-b border-[#222] flex items-center px-4 gap-2">
            <div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div>
            <div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div>
            <div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div>
            <div class="ml-auto text-[10px] font-mono text-[#555]">app.ixiera.id/analytics/best-time</div>
          </div>
          <div class="p-6">
            <h3 class="text-lg font-bold mb-1">Waktu Terbaik</h3>
            <p class="text-xs text-gray-500 mb-6">Tren engagement berdasarkan jam (WIB).</p>
            
            <div class="border border-[#9984d8] rounded-xl p-5 bg-[#9984d8]/5 mb-6 relative overflow-hidden">
              <div class="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-[#9984d8] to-transparent"></div>
              <div class="flex items-center gap-2 mb-2">
                <span class="text-[10px] text-[#9984d8] bg-[#9984d8]/20 px-2 py-0.5 rounded font-bold uppercase tracking-wider">Waktu Terbaik Berikutnya</span>
              </div>
              <div class="text-2xl font-bold text-white mb-1">Selasa, 08:00–12:00 WIB</div>
              <div class="text-xs text-gray-400 mb-4">3.20% Rata-rata ER • 8 post (Pagi)</div>
              <button class="bg-white text-black text-xs font-semibold px-4 py-2 rounded-md">Jadwalkan Sekarang</button>
            </div>

            <div class="border border-[#222] rounded-xl p-5 bg-[#0a0a0a] mb-6">
              <div class="text-[11px] font-bold text-white mb-4">Waktu Terbaik untuk Posting</div>
              <div class="flex items-end h-32 gap-2">
                <div class="w-full bg-[#222] rounded-t-sm" style="height: 20%"></div>
                <div class="w-full bg-[#222] rounded-t-sm" style="height: 30%"></div>
                <div class="w-full bg-[#222] rounded-t-sm" style="height: 25%"></div>
                <div class="w-full bg-white rounded-t-sm" style="height: 90%"></div>
                <div class="w-full bg-[#222] rounded-t-sm" style="height: 40%"></div>
                <div class="w-full bg-[#222] rounded-t-sm" style="height: 60%"></div>
                <div class="w-full bg-[#222] rounded-t-sm" style="height: 35%"></div>
              </div>
              <div class="flex justify-between mt-2 text-[10px] text-gray-500">
                <span>00:00</span><span>06:00</span><span>12:00</span><span>18:00</span>
              </div>
            </div>
            
            <div class="border border-[#222] rounded-xl p-5 bg-[#0a0a0a]">
              <div class="text-[11px] font-bold text-white mb-4">Waktu Terbaik Per Hari</div>
              <div class="space-y-2">
                <div class="flex items-center justify-between p-2 rounded hover:bg-[#111] transition">
                  <div class="flex items-center gap-3">
                    <span class="w-5 h-5 rounded-full bg-[#111] border border-[#222] flex items-center justify-center text-[10px] text-gray-400">1</span>
                    <span class="text-xs text-white">Minggu (08:00)</span>
                  </div>
                  <div class="flex items-center gap-4">
                    <div class="w-32 h-1.5 bg-[#222] rounded-full overflow-hidden"><div class="h-full bg-white" style="width: 30%"></div></div>
                    <span class="text-xs font-bold text-white">3.02%</span>
                  </div>
                </div>
                <div class="flex items-center justify-between p-2 rounded hover:bg-[#111] transition">
                  <div class="flex items-center gap-3">
                    <span class="w-5 h-5 rounded-full bg-[#111] border border-[#222] flex items-center justify-center text-[10px] text-gray-400">3</span>
                    <span class="text-xs text-white">Selasa (11:00)</span>
                  </div>
                  <div class="flex items-center gap-4">
                    <div class="w-32 h-1.5 bg-[#222] rounded-full overflow-hidden"><div class="h-full bg-white" style="width: 85%"></div></div>
                    <span class="text-xs font-bold text-[#3fcb7f]">13.64%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>
