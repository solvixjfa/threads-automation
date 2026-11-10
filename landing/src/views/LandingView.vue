<template>
  <div class="min-h-screen font-sans" style="background: var(--bg-primary); color: var(--text-primary);">

    <!-- SIDEBAR DESKTOP (STICKY, BUKAN FIXED) -->
    <aside class="hidden md:flex flex-col sticky top-0 h-screen w-60 shrink-0 border-r z-50"
           style="background: var(--bg-primary); border-color: var(--border);">
      <div class="h-16 px-5 flex items-center border-b" style="border-color: var(--border);">
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 flex items-center justify-center rounded-md text-sm font-bold"
               style="background: var(--accent); color: var(--accent-text);">IX</div>
          <span class="font-bold text-xl tracking-tight">Ixiera</span>
        </div>
      </div>

      <nav class="flex-1 p-3 space-y-1 overflow-y-auto">
        <a href="#fitur" class="block px-3 py-2.5 rounded-md text-sm font-medium transition nav-link">Fitur</a>
        <a href="#contoh" class="block px-3 py-2.5 rounded-md text-sm font-medium transition nav-link">Contoh Data</a>
        <a href="#cara-kerja" class="block px-3 py-2.5 rounded-md text-sm font-medium transition nav-link">Cara Kerja</a>
        <a href="#harga" class="block px-3 py-2.5 rounded-md text-sm font-medium transition nav-link">Harga</a>
        <a href="#faq" class="block px-3 py-2.5 rounded-md text-sm font-medium transition nav-link">FAQ</a>
      </nav>

      <div class="p-3 border-t space-y-2" style="border-color: var(--border);">
        <div class="flex items-center gap-2">
          <button @click="toggleTheme" class="flex-1 flex items-center justify-center gap-2 px-2 py-2 rounded-md text-xs font-bold border transition"
                  style="color: var(--text-muted); border-color: var(--border);">
            <Sun v-if="theme === 'dark'" class="w-4 h-4" />
            <Moon v-else class="w-4 h-4" />
          </button>
          <button @click="toggleLang" class="px-3 py-2 rounded-md text-xs font-bold border transition"
                  style="color: var(--text-muted); border-color: var(--border);">
            {{ locale.toUpperCase() }}
          </button>
        </div>
        <a href="https://app.ixiera.id/login" class="block text-center text-sm font-bold py-2.5 rounded-md transition hover:opacity-90"
           style="background: var(--accent); color: var(--accent-text);">Minta Akses</a>
      </div>
    </aside>

    <!-- MOBILE TOP BAR (STICKY) -->
    <nav class="md:hidden sticky top-0 z-40 border-b backdrop-blur-md"
         style="background: color-mix(in srgb, var(--bg-primary) 85%, transparent); border-color: var(--border);">
      <div class="h-16 px-4 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 flex items-center justify-center rounded-md text-sm font-bold"
               style="background: var(--accent); color: var(--accent-text);">IX</div>
          <span class="font-bold text-lg tracking-tight">Ixiera</span>
        </div>
        <button @click="mobileMenuOpen = true" class="p-2 rounded-md transition">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
        </button>
      </div>
    </nav>

    <!-- MOBILE DRAWER (SLIDE FROM LEFT) -->
    <Teleport to="body">
      <div v-if="mobileMenuOpen" class="md:hidden fixed inset-0 z-[100] flex">
        <div class="absolute inset-0 bg-black/60" @click="mobileMenuOpen = false"></div>
        <aside class="relative w-72 max-w-[80%] h-full border-r flex flex-col shadow-2xl"
               style="background: var(--bg-primary); border-color: var(--border); animation: slideIn 0.25s ease-out forwards;">
          <div class="h-16 px-5 flex items-center justify-between border-b" style="border-color: var(--border);">
            <div class="flex items-center gap-2">
              <div class="w-8 h-8 flex items-center justify-center rounded-md text-sm font-bold"
                   style="background: var(--accent); color: var(--accent-text);">IX</div>
              <span class="font-bold text-xl tracking-tight">Ixiera</span>
            </div>
            <button @click="mobileMenuOpen = false" class="p-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
            </button>
          </div>
          <nav class="flex-1 p-4 space-y-2 overflow-y-auto">
            <a href="#fitur" @click="mobileMenuOpen=false" class="block px-4 py-3 rounded-lg text-sm font-medium nav-link">Fitur</a>
            <a href="#contoh" @click="mobileMenuOpen=false" class="block px-4 py-3 rounded-lg text-sm font-medium nav-link">Contoh Data</a>
            <a href="#cara-kerja" @click="mobileMenuOpen=false" class="block px-4 py-3 rounded-lg text-sm font-medium nav-link">Cara Kerja</a>
            <a href="#harga" @click="mobileMenuOpen=false" class="block px-4 py-3 rounded-lg text-sm font-medium nav-link">Harga</a>
            <a href="#faq" @click="mobileMenuOpen=false" class="block px-4 py-3 rounded-lg text-sm font-medium nav-link">FAQ</a>
          </nav>
          <div class="p-4 border-t space-y-3" style="border-color: var(--border);">
            <div class="flex gap-2">
              <button @click="toggleTheme" class="flex-1 flex items-center justify-center gap-2 px-3 py-3 rounded-lg text-xs font-bold border" style="border-color: var(--border);">
                <Sun v-if="theme === 'dark'" class="w-4 h-4" />
                <Moon v-else class="w-4 h-4" />
              </button>
              <button @click="toggleLang" class="flex-1 px-3 py-3 rounded-lg text-xs font-bold border" style="border-color: var(--border);">
                {{ locale.toUpperCase() }}
              </button>
            </div>
            <a href="https://app.ixiera.id/login" class="block text-center text-sm font-bold py-3 rounded-lg" style="background: var(--accent); color: var(--accent-text);">Minta Akses</a>
          </div>
        </aside>
      </div>
    </Teleport>

    <style>
      @keyframes slideIn { from { transform: translateX(-100%); } to { transform: translateX(0); } }
      .nav-link { color: var(--text-secondary); }
      .nav-link:hover { color: var(--text-primary); background: var(--bg-hover); }
    </style>

    <!-- WRAPPER FLEX (SIDEBAR + MAIN) -->
    <div class="md:flex">
      <!-- Spacer untuk sidebar di desktop -->
      <div class="hidden md:block w-60 shrink-0"></div>

      <main class="flex-1 min-w-0">
      <!-- HERO -->
      <section class="max-w-[900px] mx-auto px-6 pb-16 md:pb-24 pt-10 md:pt-20 flex flex-col items-center text-center">
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full border mb-8" style="border-color: var(--border);">
          <span class="w-1.5 h-1.5 rounded-full" style="background: var(--accent-mint);"></span>
          <span class="text-[13px] font-medium tracking-tight" style="color: var(--text-muted);">PUBLIC BETA</span>
        </div>

        <h1 class="font-display text-[44px] md:text-[56px] leading-[1.1] mb-6 max-w-3xl mx-auto">
          Posting yang belajar dari <br class="hidden md:block"/>
          <span class="italic" style="color: var(--accent-violet);">akun kamu sendiri.</span>
        </h1>

        <p class="text-[16px] md:text-[18px] leading-[1.6] max-w-2xl mx-auto mb-10" style="color: var(--text-secondary);">
          Ixiera membaca post kamu yang paling jalan (jam, hook, panjang, topik), lalu membantu bikin rencana konten dan membalas komentar dengan gayamu.
        </p>

        <div class="flex flex-col sm:flex-row items-center gap-4 mb-8 w-full sm:w-auto">
          <a href="https://app.ixiera.id/login" class="w-full sm:w-auto px-8 py-3.5 rounded-md text-[15px] font-medium transition hover:opacity-90" style="background: var(--accent); color: var(--accent-text);">Minta Akses</a>
          <a href="#contoh" class="w-full sm:w-auto px-8 py-3.5 rounded-md text-[15px] font-medium border transition" style="color: var(--text-primary); border-color: var(--border);">Lihat contohnya</a>
        </div>

        <p class="text-[13px] mb-8" style="color: var(--text-muted);">Trial 7 hari · 20 kredit gratis · Tanpa bayar di awal</p>

        <div class="flex flex-wrap justify-center gap-4 text-xs" style="color: var(--text-muted);">
          <span>Login resmi Meta, tanpa simpan password</span>
          <span>Kill Switch kapan saja</span>
          <span>Data terpisah per user</span>
        </div>
      </section>

      <!-- HERO MOCKUP: HOOK PERFORMANCE -->
      <section class="max-w-[700px] mx-auto px-4 md:px-0 mb-16 md:mb-24">
        <div class="rounded-xl overflow-hidden border" style="background: var(--bg-secondary); border-color: var(--border);">
          <div class="flex items-center justify-between px-5 py-3 border-b" style="border-color: var(--border);">
            <span class="text-[11px] font-bold uppercase tracking-widest" style="color: var(--text-muted);">Hook Performance</span>
            <span class="text-[10px] font-bold px-2 py-0.5 rounded" style="color: var(--accent-mint); background: color-mix(in srgb, var(--accent-mint) 15%, transparent);">Data nyata</span>
          </div>
          <div class="p-5 space-y-4">
            <div>
              <div class="flex justify-between text-xs mb-1.5"><span class="font-bold">Question</span><span>2.92%</span></div>
              <div class="w-full h-2 rounded-full overflow-hidden" style="background: var(--bg-hover);"><div class="h-full rounded-full" style="width: 92%; background: var(--accent-violet);"></div></div>
              <div class="text-[10px] mt-1 text-right" style="color: var(--text-muted);">n=6</div>
            </div>
            <div>
              <div class="flex justify-between text-xs mb-1.5"><span class="font-bold">Story</span><span>1.36%</span></div>
              <div class="w-full h-2 rounded-full overflow-hidden" style="background: var(--bg-hover);"><div class="h-full rounded-full" style="width: 43%; background: var(--accent-mint);"></div></div>
              <div class="text-[10px] mt-1 text-right" style="color: var(--text-muted);">n=32</div>
            </div>
            <div>
              <div class="flex justify-between text-xs mb-1.5"><span class="font-bold">Statement</span><span>0.90%</span></div>
              <div class="w-full h-2 rounded-full overflow-hidden" style="background: var(--bg-hover);"><div class="h-full rounded-full" style="width: 28%; background: var(--text-secondary);"></div></div>
              <div class="text-[10px] mt-1 text-right" style="color: var(--text-muted);">n=10</div>
            </div>
            <div>
              <div class="flex justify-between text-xs mb-1.5"><span class="font-bold">List</span><span>0.00%</span></div>
              <div class="w-full h-2 rounded-full overflow-hidden" style="background: var(--bg-hover);"><div class="h-full rounded-full" style="width: 2%; background: var(--text-muted);"></div></div>
              <div class="text-[10px] mt-1 text-right" style="color: var(--text-muted);">n=2</div>
            </div>
          </div>
        </div>
      </section>

      <!-- MASALAH -->
      <section class="py-16 md:py-24 border-t" style="border-color: var(--border);">
        <div class="max-w-[1000px] mx-auto px-6">
          <h2 class="font-display text-[32px] md:text-[48px] leading-[1.1] mb-12 text-center">
            Jadi admin akun sendiri itu melelahkan.
          </h2>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
            <div class="rounded-2xl p-7 border" style="background: var(--bg-secondary); border-color: var(--border);">
              <span class="font-display text-[28px] block mb-3" style="color: var(--accent-violet);">01</span>
              <h3 class="text-[17px] font-semibold mb-2">Bingung mau posting apa.</h3>
              <p class="text-[14px] leading-[1.6]" style="color: var(--text-secondary);">Ide habis padahal harus konsisten.</p>
            </div>
            <div class="rounded-2xl p-7 border" style="background: var(--bg-secondary); border-color: var(--border);">
              <span class="font-display text-[28px] block mb-3" style="color: var(--accent-violet);">02</span>
              <h3 class="text-[17px] font-semibold mb-2">Komentar numpuk.</h3>
              <p class="text-[14px] leading-[1.6]" style="color: var(--text-secondary);">Telat balas, interaksi dan momentum hilang.</p>
            </div>
            <div class="rounded-2xl p-7 border" style="background: var(--bg-secondary); border-color: var(--border);">
              <span class="font-display text-[28px] block mb-3" style="color: var(--accent-violet);">03</span>
              <h3 class="text-[17px] font-semibold mb-2">Nggak tahu apa yang jalan.</h3>
              <p class="text-[14px] leading-[1.6]" style="color: var(--text-secondary);">Post mana, jam berapa, hook seperti apa, semua cuma feeling.</p>
            </div>
          </div>
        </div>
      </section>

      <!-- FITUR -->
      <section id="fitur" class="py-16 md:py-24 border-t" style="border-color: var(--border);">
        <div class="max-w-[1000px] mx-auto px-6">
          <h2 class="font-display text-[32px] md:text-[48px] leading-[1.1] mb-3 text-center">
            Bukan sekadar scheduler.
          </h2>
          <p class="text-center mb-14 text-[15px]" style="color: var(--text-secondary);">Lima menu, satu alur: rencanakan, posting, balas, pelajari.</p>

          <div class="space-y-14">
            <!-- Fitur 1: Content -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
              <div>
                <span class="text-[12px] font-bold tracking-widest uppercase block mb-2" style="color: var(--accent-violet);">01 · Content</span>
                <h3 class="text-[22px] md:text-[26px] font-semibold mb-3 leading-tight">Dari satu topik jadi rencana 3 hari.</h3>
                <p class="text-[14px] leading-[1.7]" style="color: var(--text-secondary);">Tulis topik dan pilih gaya, Ixiera menyusun rencana post. Cek Quick Score gratis sebelum menjadwalkan, dan ubah post lama yang ramai jadi Listicle, Opini, atau Cerita.</p>
              </div>
              <div class="rounded-xl p-5 border" style="background: var(--bg-secondary); border-color: var(--border);">
                <div class="text-[10px] font-bold uppercase tracking-widest mb-3" style="color: var(--text-muted);">AI Content Planner</div>
                <div class="rounded-md p-2.5 mb-2 text-xs border" style="background: var(--bg-primary); border-color: var(--border);">Topik / Short Idea</div>
                <div class="rounded-md p-2.5 mb-2 text-xs border flex justify-between" style="background: var(--bg-primary); border-color: var(--border);">
                  <span>Tone / Style</span><span style="color: var(--text-muted);">Storytelling</span>
                </div>
                <div class="rounded-md p-2.5 mb-3 text-xs font-bold text-center" style="background: var(--accent); color: var(--accent-text);">Generate 3-Day Plan</div>
                <div class="rounded-md p-3 border space-y-1" style="background: var(--bg-primary); border-color: var(--border);">
                  <div class="text-[10px] font-bold" style="color: var(--accent-violet);">DAY 1: KOMPLEKSITAS MODEL VS KEBUTUHAN NYATA</div>
                  <p class="text-[11px] leading-relaxed" style="color: var(--text-secondary);">Awal-awal ngulik AI, bawaannya pengen bikin arsitektur yang keliatan paling rumit...</p>
                </div>
              </div>
            </div>

            <!-- Fitur 2: Komentar -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
              <div class="order-2 md:order-1 rounded-xl p-5 border" style="background: var(--bg-secondary); border-color: var(--border);">
                <div class="flex gap-2 mb-4">
                  <div class="px-3 py-1 text-xs font-bold rounded-md" style="background: var(--accent); color: var(--accent-text);">Review Manual</div>
                  <div class="px-3 py-1 text-xs font-bold rounded-md border" style="color: var(--text-secondary); border-color: var(--border);">Full Auto</div>
                </div>
                <div class="space-y-2 text-xs">
                  <div class="flex justify-between items-center p-3 rounded-md border" style="background: var(--bg-primary); border-color: var(--border);">
                    <span>Pertanyaan</span><span class="font-bold" style="color: var(--accent-violet);">Balasan AI</span>
                  </div>
                  <div class="flex justify-between items-center p-3 rounded-md border" style="background: var(--bg-primary); border-color: var(--border);">
                    <span>Pujian</span><span class="font-bold" style="color: var(--accent-mint);">Template</span>
                  </div>
                  <div class="flex justify-between items-center p-3 rounded-md border" style="background: var(--bg-primary); border-color: var(--border);">
                    <span>Spam / Toxic</span><span class="font-bold" style="color: var(--text-muted);">Template</span>
                  </div>
                </div>
              </div>
              <div class="order-1 md:order-2">
                <span class="text-[12px] font-bold tracking-widest uppercase block mb-2" style="color: var(--accent-violet);">02 · Komentar</span>
                <h3 class="text-[22px] md:text-[26px] font-semibold mb-3 leading-tight">Komentar masuk, sudah terpilah.</h3>
                <p class="text-[14px] leading-[1.7]" style="color: var(--text-secondary);">Setiap komentar dikategorikan: pertanyaan, pujian, netral, spam, toxic. Atur tiap kategori: dijawab AI atau pakai template. Pilih Review Manual atau Full Auto, dengan batas balasan per jam.</p>
              </div>
            </div>

            <!-- Fitur 3: Analytics -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
              <div>
                <span class="text-[12px] font-bold tracking-widest uppercase block mb-2" style="color: var(--accent-violet);">03 · Analytics</span>
                <h3 class="text-[22px] md:text-[26px] font-semibold mb-3 leading-tight">Tahu apa yang jalan, bukan cuma feeling.</h3>
                <p class="text-[14px] leading-[1.7]" style="color: var(--text-secondary);">Jam dengan engagement tertinggi, tipe hook, panjang post, dan topik, semuanya dihitung dari data akunmu sendiri.</p>
              </div>
              <div class="rounded-xl p-5 border" style="background: var(--bg-secondary); border-color: var(--border);">
                <div class="flex gap-4 mb-4 text-xs font-bold border-b pb-2" style="color: var(--text-muted); border-color: var(--border);">
                  <span style="color: var(--text-primary); border-bottom: 2px solid var(--accent-violet); padding-bottom: 8px; margin-bottom: -10px;">Best Time</span>
                  <span>Hook</span><span>Length</span>
                </div>
                <div class="grid grid-cols-7 gap-1">
                  <div v-for="i in 21" :key="i" class="h-5 rounded-sm border"
                       :style="{ background: [3,7,11,15,18].includes(i) ? 'color-mix(in srgb, var(--accent-violet) 40%, var(--bg-primary))' : 'var(--bg-primary)', borderColor: 'var(--border)' }"></div>
                </div>
              </div>
            </div>

            <!-- Fitur 4: Pengetahuan -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
              <div class="order-2 md:order-1 rounded-xl p-5 border" style="background: var(--bg-secondary); border-color: var(--border);">
                <div class="rounded-md p-4 border space-y-2" style="background: var(--bg-primary); border-color: var(--border);">
                  <div class="flex justify-between items-center">
                    <span class="text-xs font-bold">Gaya Bahasa</span>
                    <span class="text-[10px] font-bold px-2 py-0.5 rounded-full" style="color: var(--accent-mint); background: color-mix(in srgb, var(--accent-mint) 15%, transparent);">Dipakai AI</span>
                  </div>
                  <p class="text-[11px] leading-relaxed" style="color: var(--text-secondary);">Santai, singkat, hindari jargon. Selalu sapa dengan "kak".</p>
                </div>
              </div>
              <div class="order-1 md:order-2">
                <span class="text-[12px] font-bold tracking-widest uppercase block mb-2" style="color: var(--accent-violet);">04 · Pengetahuan</span>
                <h3 class="text-[22px] md:text-[26px] font-semibold mb-3 leading-tight">Ajari sekali, dipakai di semua balasan.</h3>
                <p class="text-[14px] leading-[1.7]" style="color: var(--text-secondary);">Tulis fakta, aturan, dan gaya bahasamu di Knowledge Base. AI memakainya setiap kali menyusun draf atau membalas komentar, jadi hasilnya nggak pernah generic.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- CONTOH DATA -->
      <section id="contoh" class="py-16 md:py-24 border-t" style="border-color: var(--border); background: var(--bg-secondary);">
        <div class="max-w-[1000px] mx-auto px-6">
          <h2 class="font-display text-[32px] md:text-[48px] leading-[1.1] mb-3 text-center">
            Contoh dari data nyata.
          </h2>
          <p class="text-center mb-12 text-[15px]" style="color: var(--text-secondary);">Hasil Analytics dari 50 post akun pembuat Ixiera. Sampel kecil, dan hasil tiap akun akan berbeda.</p>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
            <div class="rounded-xl p-6 border" style="background: var(--bg-primary); border-color: var(--border);">
              <h3 class="text-sm font-bold mb-5">Hook Performance</h3>
              <div class="space-y-3">
                <div>
                  <div class="flex justify-between text-xs mb-1"><span class="font-bold">Question</span><span>2.92%</span></div>
                  <div class="w-full h-2 rounded-full overflow-hidden" style="background: var(--bg-hover);"><div class="h-full rounded-full" style="width: 92%; background: var(--accent-violet);"></div></div>
                  <div class="text-[10px] mt-0.5 text-right" style="color: var(--text-muted);">n=6</div>
                </div>
                <div>
                  <div class="flex justify-between text-xs mb-1"><span class="font-bold">Story</span><span>1.36%</span></div>
                  <div class="w-full h-2 rounded-full overflow-hidden" style="background: var(--bg-hover);"><div class="h-full rounded-full" style="width: 43%; background: var(--accent-mint);"></div></div>
                  <div class="text-[10px] mt-0.5 text-right" style="color: var(--text-muted);">n=32</div>
                </div>
              </div>
              <p class="text-[11px] mt-5 leading-relaxed pt-4 border-t" style="color: var(--text-secondary); border-color: var(--border);">Di akun ini, post berpembuka pertanyaan rata-rata mendapat engagement lebih dari dua kali lipat post bergaya cerita.</p>
            </div>

            <div class="rounded-xl p-6 border" style="background: var(--bg-primary); border-color: var(--border);">
              <h3 class="text-sm font-bold mb-5">Post Length</h3>
              <div class="space-y-3">
                <div>
                  <div class="flex justify-between text-xs mb-1"><span class="font-bold">300-500 char</span><span>2.96%</span></div>
                  <div class="w-full h-2 rounded-full overflow-hidden" style="background: var(--bg-hover);"><div class="h-full rounded-full" style="width: 93%; background: var(--accent-violet);"></div></div>
                  <div class="text-[10px] mt-0.5 text-right" style="color: var(--text-muted);">n=10</div>
                </div>
                <div>
                  <div class="flex justify-between text-xs mb-1"><span class="font-bold">100-300 char</span><span>1.12%</span></div>
                  <div class="w-full h-2 rounded-full overflow-hidden" style="background: var(--bg-hover);"><div class="h-full rounded-full" style="width: 35%; background: var(--accent-mint);"></div></div>
                  <div class="text-[10px] mt-0.5 text-right" style="color: var(--text-muted);">n=25</div>
                </div>
              </div>
              <p class="text-[11px] mt-5 leading-relaxed pt-4 border-t" style="color: var(--text-secondary); border-color: var(--border);">Post 300-500 karakter mendapat engagement lebih dari tiga kali lipat post di bawah 100 karakter.</p>
            </div>
          </div>
          <p class="text-[11px] text-center mt-6" style="color: var(--text-muted);">ER = engagement rate. Jumlah post per kategori ditampilkan di tiap bar.</p>
        </div>
      </section>

      <!-- CARA KERJA -->
      <section id="cara-kerja" class="py-16 md:py-24 border-t" style="border-color: var(--border);">
        <div class="max-w-[1000px] mx-auto px-6">
          <h2 class="font-display text-[32px] md:text-[48px] leading-[1.1] mb-12 text-center">Mulai dalam 3 langkah.</h2>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div class="space-y-3">
              <div class="w-10 h-10 rounded-full flex items-center justify-center font-display text-[18px] border" style="background: var(--bg-secondary); border-color: var(--border); color: var(--accent-violet);">1</div>
              <h3 class="text-[17px] font-semibold">Daftar dan minta akses.</h3>
              <p class="text-[14px] leading-[1.6]" style="color: var(--text-secondary);">Buat akun, lalu kirim @username Threads kamu. Akses disetujui manual dan kamu dikabari lewat email.</p>
            </div>
            <div class="space-y-3">
              <div class="w-10 h-10 rounded-full flex items-center justify-center font-display text-[18px] border" style="background: var(--bg-secondary); border-color: var(--border); color: var(--accent-violet);">2</div>
              <h3 class="text-[17px] font-semibold">Hubungkan dan ajari gayamu.</h3>
              <p class="text-[14px] leading-[1.6]" style="color: var(--text-secondary);">Setelah disetujui, terima undangan tester di Threads dan login lewat sistem resmi Meta. Tulis dokumen gaya dan aturanmu di Knowledge Base.</p>
            </div>
            <div class="space-y-3">
              <div class="w-10 h-10 rounded-full flex items-center justify-center font-display text-[18px] border" style="background: var(--bg-secondary); border-color: var(--border); color: var(--accent-violet);">3</div>
              <h3 class="text-[17px] font-semibold">Review dan jalan.</h3>
              <p class="text-[14px] leading-[1.6]" style="color: var(--text-secondary);">Setujui draf, atur mode balasan, dan pantau Analytics tiap minggu.</p>
            </div>
          </div>
        </div>
      </section>

      <!-- KEAMANAN -->
      <section class="py-16 md:py-24 border-t" style="border-color: var(--border); background: var(--bg-secondary);">
        <div class="max-w-[1000px] mx-auto px-6 grid grid-cols-1 md:grid-cols-2 gap-10 items-center">
          <div>
            <h2 class="font-display text-[32px] md:text-[48px] leading-[1.1] mb-6">Kamu yang pegang kendali.</h2>
            <ul class="space-y-4">
              <li class="flex items-start gap-3">
                <svg class="w-5 h-5 shrink-0 mt-0.5" style="color: var(--accent-mint);" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                <span class="text-[14px] leading-[1.6]">Password Threads tidak pernah disimpan. Login hanya lewat OAuth resmi Meta.</span>
              </li>
              <li class="flex items-start gap-3">
                <svg class="w-5 h-5 shrink-0 mt-0.5" style="color: var(--accent-mint);" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                <span class="text-[14px] leading-[1.6]">Data analitik dan dokumen gayamu terpisah dari user lain.</span>
              </li>
              <li class="flex items-start gap-3">
                <svg class="w-5 h-5 shrink-0 mt-0.5" style="color: var(--accent-mint);" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                <span class="text-[14px] leading-[1.6]">Teks yang diproses AI dikirim ke penyedia model (Gemini/Groq). Detailnya ada di Kebijakan Privasi.</span>
              </li>
              <li class="flex items-start gap-3">
                <svg class="w-5 h-5 shrink-0 mt-0.5" style="color: var(--accent-mint);" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                <span class="text-[14px] leading-[1.6]">Matikan otomatisasi atau putus koneksi kapan saja lewat Kill Switch.</span>
              </li>
            </ul>
          </div>
          <div class="rounded-2xl p-8 aspect-square flex items-center justify-center relative overflow-hidden border" style="background: var(--bg-primary); border-color: var(--border);">
             <div class="absolute inset-0" style="background: radial-gradient(circle at center, color-mix(in srgb, var(--accent-violet) 12%, transparent) 0%, transparent 70%);"></div>
             <div class="w-24 h-24 rounded-full border-2 flex items-center justify-center" style="border-color: color-mix(in srgb, var(--accent-violet) 35%, transparent);">
               <div class="w-16 h-16 rounded-full border-2 flex items-center justify-center" style="border-color: color-mix(in srgb, var(--accent-violet) 65%, transparent);">
                 <div class="w-8 h-8 rounded-full" style="background: var(--accent-mint); box-shadow: 0 0 20px var(--accent-mint);"></div>
               </div>
             </div>
          </div>
        </div>
      </section>

      <!-- HARGA -->
      <section id="harga" class="py-16 md:py-24 border-t" style="border-color: var(--border);">
        <div class="max-w-[1000px] mx-auto px-6">
          <div class="text-center mb-12">
            <h2 class="font-display text-[32px] md:text-[48px] leading-[1.1] mb-3">Mulai dari sini.</h2>
            <p class="text-[15px]" style="color: var(--text-secondary);">Pilih paket yang sesuai. Kami terus berbenah dari masukanmu.</p>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
            <div class="rounded-2xl p-7 flex flex-col border" style="background: var(--bg-secondary); border-color: var(--border);">
              <h3 class="text-[17px] font-semibold mb-1">Trial 7 Hari</h3>
              <p class="text-[13px] mb-6" style="color: var(--text-secondary);">7 hari · 20 kredit gratis · semua fitur</p>
              <a href="https://app.ixiera.id/login" class="block text-center w-full py-2.5 rounded-md text-[14px] font-medium border transition mt-auto" style="border-color: var(--border); color: var(--text-primary);">Mulai Gratis</a>
            </div>
            <div class="rounded-2xl p-7 flex flex-col relative border-2" style="background: var(--bg-secondary); border-color: var(--accent-violet);">
              <div class="absolute -top-3 left-1/2 -translate-x-1/2 text-[10px] font-bold uppercase tracking-widest px-3 py-1 rounded-full" style="background: var(--accent-violet); color: white;">Popular</div>
              <h3 class="text-[17px] font-semibold mb-1">Paket 30 hari</h3>
              <p class="text-[13px] mb-6" style="color: var(--text-secondary);">Rp29.000 · 100 kredit per bulan · tanpa auto-renew</p>
              <a href="https://app.ixiera.id/login" class="block text-center w-full py-2.5 rounded-md text-[14px] font-bold transition mt-auto" style="background: var(--accent); color: var(--accent-text);">Pilih Pro</a>
            </div>
            <div class="rounded-2xl p-7 flex flex-col border" style="background: var(--bg-secondary); border-color: var(--border);">
              <h3 class="text-[17px] font-semibold mb-1">Paket 30 hari + API key sendiri</h3>
              <p class="text-[13px] mb-6" style="color: var(--text-secondary);">Rp19.000 · pakai API key milikmu · tanpa kredit</p>
              <a href="https://app.ixiera.id/login" class="block text-center w-full py-2.5 rounded-md text-[14px] font-medium border transition mt-auto" style="border-color: var(--border); color: var(--text-primary);">Pilih BYOK</a>
            </div>
          </div>
          <div class="text-center mt-8 space-y-2">
            <p class="text-[12px]" style="color: var(--text-muted);">1 kredit = 1 aksi AI (generate, balasan AI, repurpose, analisis lanjutan). Template balasan dan Quick Score gratis. API key sendiri hanya tersedia di paket berbayar.</p>
            <p class="text-[12px] font-medium" style="color: var(--text-secondary);">Harga beta, terkunci selama kamu berlangganan.</p>
            <a href="https://app.ixiera.id/login" class="inline-block mt-3 px-6 py-2.5 rounded-md text-[14px] font-bold" style="background: var(--accent); color: var(--accent-text);">Minta Akses</a>
          </div>
        </div>
      </section>

      <!-- FAQ -->
      <section id="faq" class="py-16 md:py-24 border-t" style="border-color: var(--border); background: var(--bg-secondary);">
        <div class="max-w-[800px] mx-auto px-6">
          <h2 class="font-display text-[32px] md:text-[48px] leading-[1.1] mb-10 text-center">Pertanyaan Umum</h2>
          <div class="space-y-0 border-t" style="border-color: var(--border);">
            <details class="group border-b py-4 cursor-pointer" style="border-color: var(--border);">
              <summary class="flex justify-between items-center text-[15px] font-semibold list-none">
                Kenapa harus minta akses?
                <span class="group-open:rotate-180 transition"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <p class="text-[14px] mt-3 leading-relaxed" style="color: var(--text-secondary);">Ixiera masih dalam tahap early access, jadi tiap akun ditambahkan manual dan perlu disetujui dulu. Kabar lewat email.</p>
            </details>
            <details class="group border-b py-4 cursor-pointer" style="border-color: var(--border);">
              <summary class="flex justify-between items-center text-[15px] font-semibold list-none">
                Apakah ini gratis?
                <span class="group-open:rotate-180 transition"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <p class="text-[14px] mt-3 leading-relaxed" style="color: var(--text-secondary);">Trial 7 hari gratis dengan 20 kredit. Setelah itu, paket berbayar mulai dari Rp29.000 per bulan.</p>
            </details>
            <details class="group border-b py-4 cursor-pointer" style="border-color: var(--border);">
              <summary class="flex justify-between items-center text-[15px] font-semibold list-none">
                Apa itu kredit?
                <span class="group-open:rotate-180 transition"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <p class="text-[14px] mt-3 leading-relaxed" style="color: var(--text-secondary);">1 kredit = 1 aksi AI (generate, balas komentar, repurpose, analisis lanjutan). Template balasan dan Quick Score gratis tanpa kredit.</p>
            </details>
            <details class="group border-b py-4 cursor-pointer" style="border-color: var(--border);">
              <summary class="flex justify-between items-center text-[15px] font-semibold list-none">
                Apakah posting tanpa izinku?
                <span class="group-open:rotate-180 transition"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <p class="text-[14px] mt-3 leading-relaxed" style="color: var(--text-secondary);">Tidak. Semua posting dan balasan bisa di-review manual dulu sebelum tayang. Kamu yang pegang kendali penuh.</p>
            </details>
            <details class="group border-b py-4 cursor-pointer" style="border-color: var(--border);">
              <summary class="flex justify-between items-center text-[15px] font-semibold list-none">
                Apakah akunku bisa kena blokir?
                <span class="group-open:rotate-180 transition"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <p class="text-[14px] mt-3 leading-relaxed" style="color: var(--text-secondary);">Ixiera pakai API resmi Meta dan mengikuti batas yang ditetapkan. Kami juga punya batas balasan per jam untuk menghindari perilaku yang terlihat seperti spam.</p>
            </details>
            <details class="group border-b py-4 cursor-pointer" style="border-color: var(--border);">
              <summary class="flex justify-between items-center text-[15px] font-semibold list-none">
                Apakah balasannya bisa kasar?
                <span class="group-open:rotate-180 transition"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <p class="text-[14px] mt-3 leading-relaxed" style="color: var(--text-secondary);">Kamu yang menentukan gaya bahasa di Knowledge Base. Balasan akan mengikuti aturan yang kamu tulis.</p>
            </details>
            <details class="group border-b py-4 cursor-pointer" style="border-color: var(--border);">
              <summary class="flex justify-between items-center text-[15px] font-semibold list-none">
                Apa bedanya dengan scheduler biasa?
                <span class="group-open:rotate-180 transition"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <p class="text-[14px] mt-3 leading-relaxed" style="color: var(--text-secondary);">Scheduler biasa cuma menjadwalkan. Ixiera belajar dari data akunmu (jam, hook, panjang, topik) dan membalas komentar dengan gayamu. Satu platform untuk rencana, posting, balas, dan analisis.</p>
            </details>
            <details class="group border-b py-4 cursor-pointer" style="border-color: var(--border);">
              <summary class="flex justify-between items-center text-[15px] font-semibold list-none">
                Datanya dipakai siapa?
                <span class="group-open:rotate-180 transition"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <p class="text-[14px] mt-3 leading-relaxed" style="color: var(--text-secondary);">Data kamu hanya dipakai untuk akunmu sendiri. Tidak dibagikan ke user lain. Detailnya ada di Kebijakan Privasi.</p>
            </details>
            <details class="group border-b py-4 cursor-pointer" style="border-color: var(--border);">
              <summary class="flex justify-between items-center text-[15px] font-semibold list-none">
                Harus paham teknis?
                <span class="group-open:rotate-180 transition"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <p class="text-[14px] mt-3 leading-relaxed" style="color: var(--text-secondary);">Tidak. Setup butuh 3 langkah dan kurang dari 10 menit. Semua otomatisasi jalan di background.</p>
            </details>
          </div>
        </div>
      </section>

      <!-- FINAL CTA -->
      <section class="py-20 md:py-28 border-t text-center px-6" style="border-color: var(--border);">
        <h2 class="font-display text-[36px] md:text-[52px] leading-[1.1] mb-8 max-w-2xl mx-auto">
          Siap berhenti nebak-nebak?
        </h2>
        <a href="https://app.ixiera.id/login" class="inline-block px-8 py-3.5 rounded-md text-[15px] font-bold transition hover:opacity-90" style="background: var(--accent); color: var(--accent-text);">
          Minta Akses
        </a>
      </section>

      <!-- FOOTER -->
      <footer class="border-t py-8 px-6" style="border-color: var(--border);">
        <div class="max-w-[1000px] mx-auto flex flex-col md:flex-row justify-between items-center gap-5 text-[13px]" style="color: var(--text-muted);">
          <div class="flex items-center gap-2">
            <div class="w-6 h-6 flex items-center justify-center rounded text-[10px] font-bold" style="background: var(--accent); color: var(--accent-text);">IX</div>
            <span>© 2026 Ixiera.</span>
          </div>
          <div class="flex gap-5 flex-wrap justify-center">
            <a href="mailto:contact@ixiera.id" class="hover:text-[var(--text-primary)] transition">Email</a>
            <a href="/privacy" class="hover:text-[var(--text-primary)] transition">Kebijakan Privasi</a>
            <a href="/terms" class="hover:text-[var(--text-primary)] transition">Syarat & Ketentuan</a>
            <a href="/data-deletion" class="hover:text-[var(--text-primary)] transition">Hapus Data</a>
          </div>
        </div>
        <div class="max-w-[1000px] mx-auto text-center mt-5 text-[10px]" style="color: var(--text-muted);">
          Ixiera adalah produk independen dan tidak berafiliasi dengan Meta Platforms. Threads adalah merek dagang Meta.
        </div>
      </footer>

      </main>
    </div>
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
  theme.value = document.documentElement.classList.contains('dark') ? 'dark' : 'light'
})
</script>
