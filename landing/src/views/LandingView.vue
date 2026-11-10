<template>
  <div class="min-h-screen font-sans bg-[var(--bg)] text-[var(--text)]">

    <!-- SIDEBAR DESKTOP -->
    <aside class="hidden md:flex fixed left-0 top-0 h-screen w-60 border-r border-[var(--line)] bg-[var(--bg)] flex-col z-50">
      <div class="h-16 px-5 flex items-center border-b border-[var(--line)]">
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 flex items-center justify-center rounded-md text-sm font-bold bg-[var(--text)] text-[var(--bg)]">IX</div>
          <span class="font-bold text-xl tracking-tight">Ixiera</span>
        </div>
      </div>

      <nav class="flex-1 p-3 space-y-1 overflow-y-auto">
        <a href="#fitur" class="block px-3 py-2.5 rounded-md text-sm font-medium text-[var(--muted)] hover:text-[var(--text)] hover:bg-[var(--surface-2)] transition">Fitur</a>
        <a href="#contoh" class="block px-3 py-2.5 rounded-md text-sm font-medium text-[var(--muted)] hover:text-[var(--text)] hover:bg-[var(--surface-2)] transition">Contoh Data</a>
        <a href="#cara-kerja" class="block px-3 py-2.5 rounded-md text-sm font-medium text-[var(--muted)] hover:text-[var(--text)] hover:bg-[var(--surface-2)] transition">Cara Kerja</a>
        <a href="#harga" class="block px-3 py-2.5 rounded-md text-sm font-medium text-[var(--muted)] hover:text-[var(--text)] hover:bg-[var(--surface-2)] transition">Harga</a>
        <a href="#faq" class="block px-3 py-2.5 rounded-md text-sm font-medium text-[var(--muted)] hover:text-[var(--text)] hover:bg-[var(--surface-2)] transition">FAQ</a>
      </nav>

      <div class="p-3 border-t border-[var(--line)] space-y-2">
        <div class="flex items-center gap-2">
          <button @click="toggleTheme" class="flex-1 flex items-center justify-center gap-2 px-2 py-2 rounded-md text-xs font-bold text-[var(--muted)] border border-[var(--line)] hover:bg-[var(--surface-2)] hover:text-[var(--text)] transition">
            <Sun v-if="theme === 'dark'" class="w-4 h-4" />
            <Moon v-else class="w-4 h-4" />
          </button>
          <button @click="toggleLang" class="px-3 py-2 rounded-md text-xs font-bold text-[var(--muted)] border border-[var(--line)] hover:bg-[var(--surface-2)] hover:text-[var(--text)] transition">
            {{ locale.toUpperCase() }}
          </button>
        </div>
        <a href="https://app.ixiera.id/login" class="block text-center text-sm font-bold bg-[var(--text)] text-[var(--bg)] py-2.5 rounded-md hover:opacity-90 transition">Minta Akses</a>
      </div>
    </aside>

    <!-- MOBILE TOP BAR -->
    <nav class="md:hidden fixed top-0 w-full z-40 border-b border-[var(--line)] bg-[var(--bg)]/90 backdrop-blur-md">
      <div class="h-16 px-4 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 flex items-center justify-center rounded-md text-sm font-bold bg-[var(--text)] text-[var(--bg)]">IX</div>
          <span class="font-bold text-lg tracking-tight">Ixiera</span>
        </div>
        <button @click="mobileMenuOpen = true" class="p-2 rounded-md hover:bg-[var(--surface-2)] transition">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
        </button>
      </div>
    </nav>

    <!-- MOBILE DRAWER -->
    <Teleport to="body">
      <div v-if="mobileMenuOpen" class="md:hidden fixed inset-0 z-[100] flex">
        <div class="absolute inset-0 bg-black/60 backdrop-blur-sm" @click="mobileMenuOpen = false"></div>
        <aside class="relative w-72 max-w-[80%] h-full bg-[var(--bg)] border-r border-[var(--line)] flex flex-col shadow-2xl" style="animation: slideIn 0.2s ease-out forwards;">
          <div class="h-16 px-5 flex items-center justify-between border-b border-[var(--line)]">
            <div class="flex items-center gap-2">
              <div class="w-8 h-8 flex items-center justify-center rounded-md text-sm font-bold bg-[var(--text)] text-[var(--bg)]">IX</div>
              <span class="font-bold text-xl tracking-tight">Ixiera</span>
            </div>
            <button @click="mobileMenuOpen = false" class="p-2 text-[var(--muted)] hover:text-[var(--text)]">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
            </button>
          </div>
          <nav class="flex-1 p-4 space-y-2 overflow-y-auto">
            <a href="#fitur" @click="mobileMenuOpen=false" class="block px-4 py-3 rounded-lg text-sm font-medium text-[var(--muted)] hover:text-[var(--text)] hover:bg-[var(--surface-2)]">Fitur</a>
            <a href="#contoh" @click="mobileMenuOpen=false" class="block px-4 py-3 rounded-lg text-sm font-medium text-[var(--muted)] hover:text-[var(--text)] hover:bg-[var(--surface-2)]">Contoh Data</a>
            <a href="#cara-kerja" @click="mobileMenuOpen=false" class="block px-4 py-3 rounded-lg text-sm font-medium text-[var(--muted)] hover:text-[var(--text)] hover:bg-[var(--surface-2)]">Cara Kerja</a>
            <a href="#harga" @click="mobileMenuOpen=false" class="block px-4 py-3 rounded-lg text-sm font-medium text-[var(--muted)] hover:text-[var(--text)] hover:bg-[var(--surface-2)]">Harga</a>
            <a href="#faq" @click="mobileMenuOpen=false" class="block px-4 py-3 rounded-lg text-sm font-medium text-[var(--muted)] hover:text-[var(--text)] hover:bg-[var(--surface-2)]">FAQ</a>
          </nav>
          <div class="p-4 border-t border-[var(--line)] space-y-3">
            <div class="flex gap-2">
              <button @click="toggleTheme" class="flex-1 flex items-center justify-center gap-2 px-3 py-3 rounded-lg text-xs font-bold text-[var(--muted)] border border-[var(--line)]">
                <Sun v-if="theme === 'dark'" class="w-4 h-4" />
                <Moon v-else class="w-4 h-4" />
              </button>
              <button @click="toggleLang" class="flex-1 px-3 py-3 rounded-lg text-xs font-bold text-[var(--muted)] border border-[var(--line)]">
                {{ locale.toUpperCase() }}
              </button>
            </div>
            <a href="https://app.ixiera.id/login" class="block text-center text-sm font-bold bg-[var(--text)] text-[var(--bg)] py-3 rounded-lg">Minta Akses</a>
          </div>
        </aside>
      </div>
    </Teleport>

    <style>
      @keyframes slideIn {
        from { transform: translateX(-100%); }
        to { transform: translateX(0); }
      }
    </style>

    <!-- MAIN CONTENT -->
    <main class="md:ml-60 pt-16 md:pt-0">
      
      <!-- HERO -->
      <section class="max-w-[1000px] mx-auto px-6 pb-20 md:pb-32 flex flex-col items-center text-center pt-12 md:pt-24">
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-[var(--line)] mb-8">
          <span class="w-1.5 h-1.5 rounded-full bg-[#3fcb7f]"></span>
          <span class="text-[13px] font-medium tracking-[-0.03em] text-[var(--muted)]">PUBLIC BETA</span>
        </div>

        <h1 class="font-serif-display text-[44px] md:text-[56px] leading-[1.1] md:leading-[1.05] tracking-normal mb-6 max-w-4xl mx-auto text-[var(--text)]">
          Posting yang belajar dari <br class="hidden md:block"/>
          <span class="italic text-[#9984d8]">akun kamu sendiri.</span>
        </h1>

        <p class="text-[16px] md:text-[18px] text-[var(--muted)] tracking-[-0.03em] leading-[1.6] max-w-2xl mx-auto mb-10">
          Ixiera membaca post kamu yang paling jalan (jam, hook, panjang, topik), lalu membantu bikin rencana konten dan membalas komentar dengan gayamu.
        </p>

        <div class="flex flex-col sm:flex-row items-center gap-4 mb-8 w-full sm:w-auto">
          <a href="https://app.ixiera.id/login" class="w-full sm:w-auto px-8 py-3.5 rounded-md text-[15px] font-medium tracking-[-0.03em] bg-[var(--text)] text-[var(--bg)] hover:opacity-90 transition">Minta Akses</a>
          <a href="#contoh" class="w-full sm:w-auto px-8 py-3.5 rounded-md text-[15px] font-medium tracking-[-0.03em] text-[var(--text)] border border-[var(--line)] hover:bg-[var(--surface-2)] transition">Lihat contohnya</a>
        </div>

        <p class="text-[13px] text-[var(--muted)] tracking-[-0.03em] mb-8">Trial 7 hari · 20 kredit gratis · Tanpa bayar di awal</p>
        
        <div class="flex flex-wrap justify-center gap-4 text-xs text-[var(--muted)]">
          <span>Login resmi Meta, tanpa simpan password</span>
          <span>Kill Switch kapan saja</span>
          <span>Data terpisah per user</span>
        </div>
      </section>

      <!-- HERO MOCKUP (DASHBOARD) -->
      <section class="max-w-[900px] mx-auto px-4 md:px-0 mb-20 md:mb-32">
        <div class="relative w-full rounded-2xl overflow-hidden border border-[var(--line)] bg-[#050607] shadow-2xl">
          <div class="flex items-center gap-1.5 px-4 py-3 border-b border-[var(--line)]">
            <div class="w-2.5 h-2.5 rounded-full bg-[var(--line)]"></div>
            <div class="w-2.5 h-2.5 rounded-full bg-[var(--line)]"></div>
            <div class="w-2.5 h-2.5 rounded-full bg-[var(--line)]"></div>
            <span class="ml-2 text-[10px] text-[var(--muted)] uppercase tracking-widest font-bold">Dashboard</span>
          </div>
          <div class="p-6 md:p-8 grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="bg-[var(--bg)] border border-[var(--line)] rounded-xl p-5">
              <p class="text-[12px] text-[var(--muted)] mb-1">Total Views</p>
              <p class="text-[32px] font-semibold text-[var(--text)] tracking-[-0.03em] mb-2">311,781</p>
              <p class="text-[12px] text-[#3fcb7f] tracking-[-0.03em]">up 126 percent</p>
            </div>
            <div class="bg-[var(--bg)] border border-[var(--line)] rounded-xl p-5">
              <p class="text-[12px] text-[var(--muted)] mb-1">Followers</p>
              <p class="text-[32px] font-semibold text-[var(--text)] tracking-[-0.03em] mb-2">2,592</p>
              <p class="text-[12px] text-[#3fcb7f] tracking-[-0.03em]">up 15 this week</p>
            </div>
            <div class="bg-[var(--bg)] border border-[var(--line)] rounded-xl p-5">
              <p class="text-[12px] text-[var(--muted)] mb-1">Engagement Rate</p>
              <p class="text-[32px] font-semibold text-[var(--text)] tracking-[-0.03em] mb-2">4.8 percent</p>
              <p class="text-[12px] text-[#3fcb7f] tracking-[-0.03em]">up 0.3 percent</p>
            </div>
          </div>
        </div>
      </section>

      <!-- MASALAH -->
      <section class="py-20 md:py-32 bg-[var(--surface)] border-t border-[var(--line)]">
        <div class="max-w-[1000px] mx-auto px-6">
          <h2 class="font-serif-display text-[36px] md:text-[48px] leading-[1.1] mb-12 text-center text-[var(--text)]">
            Jadi admin akun sendiri itu melelahkan.
          </h2>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="bg-[#050607] border border-[var(--line)] rounded-2xl p-8">
              <span class="font-serif-display text-[32px] text-[#9984d8] block mb-4">01</span>
              <h3 class="text-[18px] font-semibold text-[var(--text)] mb-2">Bingung mau posting apa.</h3>
              <p class="text-[14px] text-[var(--muted)] leading-[1.6]">Ide habis padahal harus konsisten.</p>
            </div>
            <div class="bg-[#050607] border border-[var(--line)] rounded-2xl p-8">
              <span class="font-serif-display text-[32px] text-[#9984d8] block mb-4">02</span>
              <h3 class="text-[18px] font-semibold text-[var(--text)] mb-2">Komentar numpuk.</h3>
              <p class="text-[14px] text-[var(--muted)] leading-[1.6]">Telat balas, interaksi dan momentum hilang.</p>
            </div>
            <div class="bg-[#050607] border border-[var(--line)] rounded-2xl p-8">
              <span class="font-serif-display text-[32px] text-[#9984d8] block mb-4">03</span>
              <h3 class="text-[18px] font-semibold text-[var(--text)] mb-2">Nggak tahu apa yang jalan.</h3>
              <p class="text-[14px] text-[var(--muted)] leading-[1.6]">Post mana, jam berapa, hook seperti apa, semua cuma feeling.</p>
            </div>
          </div>
        </div>
      </section>

      <!-- FITUR -->
      <section id="fitur" class="py-20 md:py-32 bg-[var(--bg)] border-t border-[var(--line)]">
        <div class="max-w-[1000px] mx-auto px-6">
          <h2 class="font-serif-display text-[36px] md:text-[48px] leading-[1.1] mb-4 text-center text-[var(--text)]">
            Bukan sekadar scheduler.
          </h2>
          <p class="text-center text-[var(--muted)] mb-16 tracking-[-0.03em]">Lima menu, satu alur: rencanakan, posting, balas, pelajari.</p>

          <div class="space-y-12">
            <!-- Fitur 1 -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
              <div>
                <span class="text-[14px] text-[#9984d8] font-bold tracking-widest uppercase mb-2 block">01 · Content</span>
                <h3 class="text-[24px] font-semibold text-[var(--text)] mb-4">Dari satu topik jadi rencana 3 hari.</h3>
                <p class="text-[15px] text-[var(--muted)] leading-[1.6]">Tulis topik dan pilih gaya, Ixiera menyusun rencana post. Cek Quick Score gratis sebelum menjadwalkan, dan ubah post lama yang ramai jadi Listicle, Opini, atau Cerita.</p>
              </div>
              <div class="bg-[#050607] border border-[var(--line)] rounded-2xl p-6">
                <div class="space-y-3">
                  <div class="text-xs font-bold text-[var(--muted)] uppercase tracking-widest">AI Content Planner</div>
                  <div class="bg-[var(--bg)] border border-[var(--line)] p-3 rounded-lg text-sm text-[var(--text)]">Topik / Short Idea: AI</div>
                  <div class="bg-[var(--bg)] border border-[var(--line)] p-3 rounded-lg text-sm text-[var(--text)]">Tone / Style: Storytelling</div>
                  <div class="bg-white text-black text-center py-2 rounded-md font-bold text-sm">Generate 3-Day Plan</div>
                  <div class="bg-[var(--bg)] border border-[var(--line)] p-4 rounded-lg space-y-2">
                    <div class="text-[10px] font-bold text-[#9984d8]">DAY 1: KOMPLEKSITAS MODEL VS KEBUTUHAN NYATA</div>
                    <p class="text-xs text-[var(--muted)]">Awal-awal ngulik AI, bawaannya pengen bikin arsitektur yang keliatan paling rumit...</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Fitur 2 -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
              <div class="order-2 md:order-1 bg-[#050607] border border-[var(--line)] rounded-2xl p-6">
                <div class="flex gap-2 mb-4">
                  <div class="px-3 py-1 bg-white text-black text-xs font-bold rounded-md">Review Manual</div>
                  <div class="px-3 py-1 bg-[var(--bg)] text-[var(--muted)] border border-[var(--line)] text-xs font-bold rounded-md">Full Auto</div>
                </div>
                <div class="space-y-3 text-sm">
                  <div class="flex justify-between items-center bg-[var(--bg)] p-3 rounded-lg border border-[var(--line)]">
                    <span class="text-[var(--text)]">Pertanyaan</span>
                    <span class="text-[#3fcb7f] font-bold text-xs">Balasan AI</span>
                  </div>
                  <div class="flex justify-between items-center bg-[var(--bg)] p-3 rounded-lg border border-[var(--line)]">
                    <span class="text-[var(--text)]">Pujian</span>
                    <span class="text-[#9984d8] font-bold text-xs">Template</span>
                  </div>
                  <div class="flex justify-between items-center bg-[var(--bg)] p-3 rounded-lg border border-[var(--line)]">
                    <span class="text-[var(--text)]">Spam / Toxic</span>
                    <span class="text-[#b3b3b3] font-bold text-xs">Template</span>
                  </div>
                </div>
              </div>
              <div class="order-1 md:order-2">
                <span class="text-[14px] text-[#9984d8] font-bold tracking-widest uppercase mb-2 block">02 · Komentar</span>
                <h3 class="text-[24px] font-semibold text-[var(--text)] mb-4">Komentar masuk, sudah terpilah.</h3>
                <p class="text-[15px] text-[var(--muted)] leading-[1.6]">Setiap komentar dikategorikan: pertanyaan, pujian, netral, spam, toxic. Atur tiap kategori: dijawab AI atau pakai template. Pilih Review Manual atau Full Auto, dengan batas balasan per jam.</p>
              </div>
            </div>

            <!-- Fitur 3 -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
              <div>
                <span class="text-[14px] text-[#9984d8] font-bold tracking-widest uppercase mb-2 block">03 · Analytics</span>
                <h3 class="text-[24px] font-semibold text-[var(--text)] mb-4">Tahu apa yang jalan, bukan cuma feeling.</h3>
                <p class="text-[15px] text-[var(--muted)] leading-[1.6]">Jam dengan engagement tertinggi, tipe hook, panjang post, dan topik, semuanya dihitung dari data akunmu sendiri.</p>
              </div>
              <div class="bg-[#050607] border border-[var(--line)] rounded-2xl p-6">
                 <div class="flex gap-4 mb-4 text-xs font-bold text-[var(--muted)] border-b border-[var(--line)] pb-2">
                   <span class="text-[var(--text)] border-b-2 border-[#9984d8] pb-2 -mb-[9px]">Best Time</span>
                   <span>Hook</span>
                   <span>Length</span>
                 </div>
                 <div class="grid grid-cols-7 gap-1 mt-4">
                   <div v-for="i in 21" :key="i" class="h-6 rounded-sm bg-[var(--bg)] border border-[var(--line)]" :class="i % 4 === 0 ? 'bg-[#9984d8]/40' : ''"></div>
                 </div>
              </div>
            </div>

            <!-- Fitur 4 -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
              <div class="order-2 md:order-1 bg-[#050607] border border-[var(--line)] rounded-2xl p-6">
                <div class="bg-[var(--bg)] border border-[var(--line)] p-4 rounded-lg space-y-3">
                  <div class="flex justify-between items-center">
                    <span class="text-xs font-bold text-[var(--text)]">Gaya Bahasa</span>
                    <span class="text-[10px] bg-[#3fcb7f]/20 text-[#3fcb7f] px-2 py-0.5 rounded-full font-bold">Dipakai AI</span>
                  </div>
                  <div class="text-xs text-[var(--muted)]">Santai, singkat, hindari jargon. Selalu sapa dengan "kak".</div>
                </div>
              </div>
              <div class="order-1 md:order-2">
                <span class="text-[14px] text-[#9984d8] font-bold tracking-widest uppercase mb-2 block">04 · Pengetahuan</span>
                <h3 class="text-[24px] font-semibold text-[var(--text)] mb-4">Ajari sekali, dipakai di semua balasan.</h3>
                <p class="text-[15px] text-[var(--muted)] leading-[1.6]">Tulis fakta, aturan, dan gaya bahasamu di Knowledge Base. AI memakainya setiap kali menyusun draf atau membalas komentar, jadi hasilnya nggak pernah generic.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- CONTOH DATA -->
      <section id="contoh" class="py-20 md:py-32 bg-[var(--surface)] border-t border-[var(--line)]">
        <div class="max-w-[1000px] mx-auto px-6">
          <h2 class="font-serif-display text-[36px] md:text-[48px] leading-[1.1] mb-4 text-center text-[var(--text)]">
            Contoh dari data nyata.
          </h2>
          <p class="text-center text-[var(--muted)] mb-16 tracking-[-0.03em]">Hasil Analytics dari 50 post akun pembuat Ixiera. Sampel kecil, dan hasil tiap akun akan berbeda.</p>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Hook -->
            <div class="bg-[#050607] border border-[var(--line)] rounded-2xl p-6">
              <h3 class="text-sm font-bold text-[var(--text)] mb-6">Hook Performance</h3>
              <div class="space-y-4">
                <div>
                  <div class="flex justify-between text-xs mb-1"><span class="font-bold text-[var(--text)]">Question</span><span class="text-[var(--text)]">2.92%</span></div>
                  <div class="w-full bg-[var(--bg)] h-2 rounded-full overflow-hidden"><div class="bg-white h-full w-[85%]"></div></div>
                </div>
                <div>
                  <div class="flex justify-between text-xs mb-1"><span class="font-bold text-[var(--text)]">Story</span><span class="text-[var(--text)]">1.36%</span></div>
                  <div class="w-full bg-[var(--bg)] h-2 rounded-full overflow-hidden"><div class="bg-[#b3b3b3] h-full w-[40%]"></div></div>
                </div>
                <div>
                  <div class="flex justify-between text-xs mb-1"><span class="font-bold text-[var(--text)]">Statement</span><span class="text-[var(--text)]">0.90%</span></div>
                  <div class="w-full bg-[var(--bg)] h-2 rounded-full overflow-hidden"><div class="bg-[#808080] h-full w-[25%]"></div></div>
                </div>
              </div>
            </div>

            <!-- Length -->
            <div class="bg-[#050607] border border-[var(--line)] rounded-2xl p-6">
              <h3 class="text-sm font-bold text-[var(--text)] mb-6">Post Length</h3>
              <div class="space-y-4">
                <div>
                  <div class="flex justify-between text-xs mb-1"><span class="font-bold text-[var(--text)]">300–500 char</span><span class="text-[var(--text)]">2.96%</span></div>
                  <div class="w-full bg-[var(--bg)] h-2 rounded-full overflow-hidden"><div class="bg-white h-full w-[85%]"></div></div>
                </div>
                <div>
                  <div class="flex justify-between text-xs mb-1"><span class="font-bold text-[var(--text)]">100–300 char</span><span class="text-[var(--text)]">1.12%</span></div>
                  <div class="w-full bg-[var(--bg)] h-2 rounded-full overflow-hidden"><div class="bg-[#b3b3b3] h-full w-[35%]"></div></div>
                </div>
              </div>
            </div>
          </div>
          <p class="text-[11px] text-[var(--muted)] text-center mt-6">ER = engagement rate. Jumlah post per kategori ditampilkan di tiap bar.</p>
        </div>
      </section>

      <!-- CARA KERJA -->
      <section id="cara-kerja" class="py-20 md:py-32 bg-[var(--bg)] border-t border-[var(--line)]">
        <div class="max-w-[1000px] mx-auto px-6">
          <h2 class="font-serif-display text-[36px] md:text-[48px] leading-[1.1] mb-16 text-center text-[var(--text)]">
            Mulai dalam 3 langkah.
          </h2>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div class="space-y-4">
              <div class="w-10 h-10 rounded-full bg-[#050607] border border-[var(--line)] flex items-center justify-center font-serif-display text-[#9984d8] text-xl">1</div>
              <h3 class="text-[18px] font-semibold text-[var(--text)]">Daftar dan minta akses.</h3>
              <p class="text-[14px] text-[var(--muted)] leading-[1.6]">Buat akun, lalu kirim @username Threads kamu. Akses disetujui manual dan kamu dikabari lewat email.</p>
            </div>
            <div class="space-y-4">
              <div class="w-10 h-10 rounded-full bg-[#050607] border border-[var(--line)] flex items-center justify-center font-serif-display text-[#9984d8] text-xl">2</div>
              <h3 class="text-[18px] font-semibold text-[var(--text)]">Hubungkan dan ajari gayamu.</h3>
              <p class="text-[14px] text-[var(--muted)] leading-[1.6]">Setelah disetujui, terima undangan tester di Threads dan login lewat sistem resmi Meta. Tulis dokumen gaya dan aturanmu di Knowledge Base.</p>
            </div>
            <div class="space-y-4">
              <div class="w-10 h-10 rounded-full bg-[#050607] border border-[var(--line)] flex items-center justify-center font-serif-display text-[#9984d8] text-xl">3</div>
              <h3 class="text-[18px] font-semibold text-[var(--text)]">Review dan jalan.</h3>
              <p class="text-[14px] text-[var(--muted)] leading-[1.6]">Setujui draf, atur mode balasan, dan pantau Analytics tiap minggu.</p>
            </div>
          </div>
        </div>
      </section>

      <!-- KEAMANAN -->
      <section class="py-20 md:py-32 bg-[var(--surface)] border-t border-[var(--line)]">
        <div class="max-w-[1000px] mx-auto px-6 grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
          <div>
            <h2 class="font-serif-display text-[36px] md:text-[48px] leading-[1.1] mb-8 text-[var(--text)]">
              Kamu yang pegang kendali.
            </h2>
            <ul class="space-y-6">
              <li class="flex items-start gap-3">
                <svg class="w-5 h-5 text-[#3fcb7f] shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                <span class="text-[14px] text-[var(--text)] leading-[1.6]">Password Threads tidak pernah disimpan. Login hanya lewat OAuth resmi Meta.</span>
              </li>
              <li class="flex items-start gap-3">
                <svg class="w-5 h-5 text-[#3fcb7f] shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                <span class="text-[14px] text-[var(--text)] leading-[1.6]">Data analitik dan dokumen gayamu terpisah dari user lain.</span>
              </li>
              <li class="flex items-start gap-3">
                <svg class="w-5 h-5 text-[#3fcb7f] shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                <span class="text-[14px] text-[var(--text)] leading-[1.6]">Teks yang diproses AI dikirim ke penyedia model (Gemini/Groq). Detailnya ada di Kebijakan Privasi.</span>
              </li>
              <li class="flex items-start gap-3">
                <svg class="w-5 h-5 text-[#3fcb7f] shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                <span class="text-[14px] text-[var(--text)] leading-[1.6]">Matikan otomatisasi atau putus koneksi kapan saja lewat Kill Switch.</span>
              </li>
            </ul>
          </div>
          <div class="bg-[#050607] border border-[var(--line)] rounded-2xl p-8 aspect-square flex items-center justify-center relative overflow-hidden hidden md:flex">
             <div class="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(153,132,216,0.1)_0,transparent_70%)]"></div>
             <div class="w-24 h-24 rounded-full border-2 border-[#9984d8]/30 flex items-center justify-center">
               <div class="w-16 h-16 rounded-full border-2 border-[#9984d8]/60 flex items-center justify-center">
                 <div class="w-8 h-8 rounded-full bg-[#3fcb7f] shadow-[0_0_20px_#3fcb7f]"></div>
               </div>
             </div>
          </div>
        </div>
      </section>

      <!-- HARGA -->
      <section id="harga" class="py-20 md:py-32 bg-[var(--bg)] border-t border-[var(--line)]">
        <div class="max-w-[1000px] mx-auto px-6">
          <div class="text-center mb-16">
            <h2 class="font-serif-display text-[36px] md:text-[48px] leading-[1.1] mb-4 text-[var(--text)]">Mulai dari sini.</h2>
            <p class="text-[16px] text-[var(--muted)]">Pilih paket yang sesuai. Kami terus berbenah dari masukanmu.</p>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="bg-[var(--surface)] border border-[var(--line)] rounded-2xl p-8 flex flex-col">
              <h3 class="text-[18px] font-semibold text-[var(--text)] mb-2">Trial 7 Hari</h3>
              <p class="text-[13px] text-[var(--muted)] mb-6 h-10">7 hari · 20 kredit gratis · semua fitur</p>
              <a href="https://app.ixiera.id/login" class="block text-center w-full py-3 rounded-md border border-[var(--line)] text-[14px] font-medium hover:bg-[#111] transition mt-auto">Start free</a>
            </div>
            <div class="bg-[#050607] border border-[#9984d8] rounded-2xl p-8 flex flex-col relative shadow-[0_0_30px_rgba(153,132,216,0.15)]">
              <h3 class="text-[18px] font-semibold text-white mb-2">Paket 30 hari</h3>
              <p class="text-[13px] text-[#b3b3b3] mb-6 h-10">Rp29.000 · 100 kredit per bulan · tanpa auto-renew</p>
              <a href="https://app.ixiera.id/login" class="block text-center w-full py-3 rounded-md bg-white text-black text-[14px] font-medium hover:bg-gray-200 transition mt-auto">Pilih Pro</a>
            </div>
            <div class="bg-[var(--surface)] border border-[var(--line)] rounded-2xl p-8 flex flex-col">
              <h3 class="text-[18px] font-semibold text-[var(--text)] mb-2">BYOK</h3>
              <p class="text-[13px] text-[var(--muted)] mb-6 h-10">Rp19.000 · pakai API key milikmu · tanpa kredit</p>
              <a href="https://app.ixiera.id/login" class="block text-center w-full py-3 rounded-md border border-[var(--line)] text-[14px] font-medium hover:bg-[#111] transition mt-auto">Pilih BYOK</a>
            </div>
          </div>
          <div class="text-center mt-8 space-y-2">
            <p class="text-[12px] text-[var(--muted)]">1 kredit = 1 aksi AI (generate, balasan AI, repurpose, analisis lanjutan). Template balasan dan Quick Score gratis.</p>
            <p class="text-[12px] text-[var(--muted)]">Harga beta, terkunci selama kamu berlangganan.</p>
          </div>
        </div>
      </section>

      <!-- FAQ -->
      <section id="faq" class="py-20 md:py-32 bg-[var(--surface)] border-t border-[var(--line)]">
        <div class="max-w-[800px] mx-auto px-6">
          <h2 class="font-serif-display text-[36px] md:text-[48px] leading-[1.1] mb-12 text-center text-[var(--text)]">
            Pertanyaan Umum
          </h2>
          <div class="space-y-0 border-t border-[var(--line)]">
            <details class="group border-b border-[var(--line)] py-5 cursor-pointer">
              <summary class="flex justify-between items-center text-[16px] font-semibold text-[var(--text)] list-none">
                Kenapa harus minta akses?
                <span class="group-open:rotate-180 transition"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <p class="text-[14px] text-[var(--muted)] mt-3 leading-relaxed">Ixiera masih dalam tahap early access, jadi tiap akun ditambahkan manual dan perlu disetujui dulu. Kabar lewat email.</p>
            </details>
            <details class="group border-b border-[var(--line)] py-5 cursor-pointer">
              <summary class="flex justify-between items-center text-[16px] font-semibold text-[var(--text)] list-none">
                Apakah ini gratis?
                <span class="group-open:rotate-180 transition"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <p class="text-[14px] text-[var(--muted)] mt-3 leading-relaxed">Trial 7 hari gratis dengan 20 kredit. Setelah itu ada paket berbayar.</p>
            </details>
            <details class="group border-b border-[var(--line)] py-5 cursor-pointer">
              <summary class="flex justify-between items-center text-[16px] font-semibold text-[var(--text)] list-none">
                Apa itu kredit?
                <span class="group-open:rotate-180 transition"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <p class="text-[14px] text-[var(--muted)] mt-3 leading-relaxed">1 kredit = 1 aksi AI. Template dan Quick Score tidak pakai kredit.</p>
            </details>
          </div>
        </div>
      </section>

      <!-- FINAL CTA & FOOTER -->
      <section class="py-24 md:py-32 border-t border-[var(--line)] text-center px-6 bg-[var(--bg)]">
        <h2 class="font-serif-display text-[40px] md:text-[56px] leading-[1.1] text-[var(--text)] mb-8 max-w-2xl mx-auto">
          Siap berhenti nebak-nebak?
        </h2>
        <a href="https://app.ixiera.id/login" class="inline-block px-8 py-4 rounded-md bg-white text-black text-[16px] font-bold hover:bg-gray-200 transition">
          Minta Akses
        </a>
      </section>

      <footer class="border-t border-[var(--line)] py-10 px-6">
        <div class="max-w-[1000px] mx-auto flex flex-col md:flex-row justify-between items-center gap-6 text-sm text-[var(--muted)]">
          <div class="flex items-center gap-2">
            <div class="w-6 h-6 flex items-center justify-center rounded text-[10px] font-bold bg-[var(--text)] text-[var(--bg)]">IX</div>
            <span>© 2026 Ixiera.</span>
          </div>
          <div class="flex gap-6">
            <a href="/privacy" class="hover:text-[var(--text)] transition">Kebijakan Privasi</a>
            <a href="/terms" class="hover:text-[var(--text)] transition">Syarat & Ketentuan</a>
            <a href="/data-deletion" class="hover:text-[var(--text)] transition">Hapus Data</a>
          </div>
        </div>
        <div class="max-w-[1000px] mx-auto text-center mt-6 text-[10px] text-[var(--muted)]">
          Ixiera adalah produk independen dan tidak berafiliasi dengan Meta Platforms. Threads adalah merek dagang Meta.
        </div>
      </footer>

    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Sun, Moon } from 'lucide-vue-next'
import { useI18n } from 'vue-i18n'

const { locale } = useI18n()
const mobileMenuOpen = ref(false)
const theme = ref<'light' | 'dark'>('dark')

function toggleTheme() {
  theme.value = theme.value === 'dark' ? 'light' : 'dark'
  document.documentElement.classList.toggle('dark', theme.value === 'dark')
}

function toggleLang() {
  locale.value = locale.value === 'id' ? 'en' : 'id'
}

onMounted(() => {
  if (document.documentElement.classList.contains('dark')) {
    theme.value = 'dark'
  } else {
    theme.value = 'light'
  }
})
</script>
