<template>
  <div class="min-h-screen">

    
    <!-- TOP NAVBAR (BASEDASH STYLE) -->
    <nav class="fixed top-0 left-0 right-0 z-50 h-16 bg-black/80 backdrop-blur-md border-b border-[var(--border)]/50 flex items-center">
      <div class="container-bd w-full flex items-center justify-between">
        <!-- Logo -->
        <div class="flex items-center gap-2">
          <div class="w-7 h-7 flex items-center justify-center rounded text-xs font-bold bg-[var(--accent)] text-[var(--accent-text)]">IX</div>
          <span class="font-bold text-lg text-[var(--text-primary)] tracking-tight">Ixiera</span>
        </div>

        <!-- Center Links -->
        <div class="hidden md:flex items-center gap-8 text-sm font-medium text-[var(--text-secondary)]">
          <a href="#fitur" class="hover:text-[var(--text-primary)] transition">Fitur</a>
          <a href="#contoh" class="hover:text-[var(--text-primary)] transition">Contoh Data</a>
          <a href="#cara-kerja" class="hover:text-[var(--text-primary)] transition">Cara Kerja</a>
          <a href="/pricing" class="hover:text-[var(--text-primary)] transition">Harga</a>
          <a href="#faq" class="hover:text-[var(--text-primary)] transition">FAQ</a>
        </div>

        <!-- Right Actions -->
        <div class="hidden md:flex items-center gap-4">
          <button @click="toggleTheme" class="p-2 text-[var(--text-muted)] hover:text-[var(--text-primary)] transition">
            <Sun v-if="theme === 'dark'" class="w-4 h-4" />
            <Moon v-else class="w-4 h-4" />
          </button>
          <a href="https://app.ixiera.id/login" class="text-sm font-medium text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition">Log in</a>
          <a href="https://app.ixiera.id/login" class="btn-bd-primary" style="padding: 8px 16px;">Sign up</a>
        </div>

        <!-- Mobile Hamburger -->
        <button @click="mobileMenuOpen = true" class="md:hidden p-2 text-[var(--text-primary)]">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
        </button>
      </div>
    </nav>
    <!-- MOBILE DRAWER BARU -->
    <div v-if="mobileMenuOpen" class="md:hidden fixed inset-0 z-[100] bg-black/95 backdrop-blur-md flex flex-col p-6">
      <div class="flex justify-between items-center mb-10">
        <div class="flex items-center gap-2">
          <div class="w-7 h-7 flex items-center justify-center rounded text-xs font-bold bg-white text-black">IX</div>
          <span class="font-bold text-lg text-white">Ixiera</span>
        </div>
        <button @click="mobileMenuOpen = false" class="p-2 text-white">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
        </button>
      </div>
      
      <nav class="flex flex-col gap-6 text-[16px] font-medium text-[#b3b3b3]">
        <a href="#fitur" @click="mobileMenuOpen = false" class="hover:text-white transition">Fitur</a>
        <a href="#contoh" @click="mobileMenuOpen = false" class="hover:text-white transition">Contoh Data</a>
        <a href="#cara-kerja" @click="mobileMenuOpen = false" class="hover:text-white transition">Cara Kerja</a>
        <a href="/pricing" @click="mobileMenuOpen = false" class="hover:text-white transition">Harga</a>
        <a href="#faq" @click="mobileMenuOpen = false" class="hover:text-white transition">FAQ</a>
      </nav>
      
      <div class="mt-auto pt-6 border-t border-[#333]">
        <a href="https://app.ixiera.id/login" class="btn-bd-primary w-full text-center block mb-3">Sign up</a>
        <a href="https://app.ixiera.id/login" class="text-center block text-sm text-[#b3b3b3]">Log in</a>
      </div>
    </div>


    <!-- MAIN CONTENT -->
    <main class="pt-16">
      <!-- HERO -->
      <section class="relative pt-24 pb-20">
        <div class="container-bd text-center relative z-10">
          <div class="pill-bd mb-6 mx-auto" style="width: fit-content;">
            <span class="w-1.5 h-1.5 rounded-full" style="background: #3fcb7f;"></span>
            PUBLIC BETA
          </div>
          
          <h1 class="font-display text-[48px] md:text-[64px] leading-[1.0] mb-6 max-w-3xl mx-auto text-[var(--text-primary)]">
            Posting yang belajar dari <br class="hidden md:block">
            <span class="italic" style="color: #9984d8;">akun kamu sendiri.</span>
          </h1>
          
          <p class="text-[18px] leading-[1.56] max-w-[640px] mx-auto mb-10 text-[var(--text-secondary)]" style="letter-spacing: -0.03em;">
            Ixiera membaca post kamu yang paling jalan (jam, hook, panjang, topik), lalu membantu bikin rencana konten dan membalas komentar dengan gayamu.
          </p>
          
          <div class="flex flex-col sm:flex-row items-center justify-center gap-4 mb-8">
            <a href="https://app.ixiera.id/login" class="btn-bd-primary w-full sm:w-auto text-center">Minta Akses</a>
            <a href="#contoh" class="btn-bd-ghost w-full sm:w-auto text-center">Lihat contohnya</a>
          </div>
          
          <p class="text-[13px] text-[var(--text-muted)] mb-6" style="letter-spacing: -0.03em;">Trial 7 hari &middot; 20 kredit gratis &middot; Tanpa bayar di awal</p>
        </div>
      </section>

      <!-- HERO MOCKUP with GLOW -->
        <div class="container-bd pb-16 md:pb-24 relative">
          <div class="mockup-glow absolute inset-0 pointer-events-none" style="background: radial-gradient(ellipse 70% 60% at 50% 0%, rgba(153,132,216,0.35) 0%, transparent 70%);"></div>
          <div class="relative rounded-2xl border border-[var(--border)] overflow-hidden bg-[#050607]" >
            <div class="flex items-center gap-1.5 px-4 py-3 border-b border-[#1a1a1a]">
              <div class="w-2.5 h-2.5 rounded-full bg-[#1a1a1a]"></div>
              <div class="w-2.5 h-2.5 rounded-full bg-[#1a1a1a]"></div>
              <div class="w-2.5 h-2.5 rounded-full bg-[#1a1a1a]"></div>
              <span class="ml-2 text-[10px] text-[#666] uppercase tracking-widest font-bold">Dashboard</span>
            </div>

            <div class="p-5 md:p-7 space-y-5">
              <div class="grid grid-cols-3 gap-3">
                <div class="bg-black border border-[#1a1a1a] rounded-xl p-3 md:p-4">
                  <p class="text-[10px] text-[#666] mb-1" style="letter-spacing: -0.03em;">Views</p>
                  <p class="text-lg md:text-2xl font-bold text-white" style="letter-spacing: -0.03em;">311k</p>
                  <p class="text-[10px] text-[#3fcb7f] font-medium" style="letter-spacing: -0.03em;">+126%</p>
                </div>
                <div class="bg-black border border-[#1a1a1a] rounded-xl p-3 md:p-4">
                  <p class="text-[10px] text-[#666] mb-1" style="letter-spacing: -0.03em;">Followers</p>
                  <p class="text-lg md:text-2xl font-bold text-white" style="letter-spacing: -0.03em;">2.5k</p>
                  <p class="text-[10px] text-[#3fcb7f] font-medium" style="letter-spacing: -0.03em;">+15</p>
                </div>
                <div class="bg-black border border-[#1a1a1a] rounded-xl p-3 md:p-4">
                  <p class="text-[10px] text-[#666] mb-1" style="letter-spacing: -0.03em;">ER</p>
                  <p class="text-lg md:text-2xl font-bold text-white" style="letter-spacing: -0.03em;">4.8%</p>
                  <p class="text-[10px] text-[#3fcb7f] font-medium" style="letter-spacing: -0.03em;">+0.3</p>
                </div>
              </div>

              <div class="bg-black border border-[#1a1a1a] rounded-xl p-4">
                <div class="flex justify-between items-center mb-3">
                  <span class="text-[10px] text-[#666] uppercase tracking-widest font-bold">Growth</span>
                  <span class="text-[10px] text-[#3fcb7f] font-bold" style="letter-spacing: -0.03em;">Last 30 days</span>
                </div>
                <svg viewBox="0 0 400 80" class="w-full" preserveAspectRatio="none" style="height: 60px;">
                  <defs>
                    <linearGradient id="chartGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stop-color="#9984d8" stop-opacity="0.4" />
                      <stop offset="100%" stop-color="#9984d8" stop-opacity="0" />
                    </linearGradient>
                  </defs>
                  <path d="M0,70 Q50,65 80,55 T160,45 T240,30 T320,20 L400,10 L400,80 L0,80 Z" fill="url(#chartGradient)" />
                  <path d="M0,70 Q50,65 80,55 T160,45 T240,30 T320,20 L400,10" stroke="#9984d8" stroke-width="2" fill="none" />
                </svg>
              </div>
            </div>
          </div>
        </div>
      <!-- MASALAH -->
      <section class="section-bd">
        <div class="container-bd">
          <h2 class="h2-bd">Jadi admin akun sendiri itu melelahkan.</h2>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-5 mt-10">
            <div class="card-bd p-7 feature-card">
              <span class="font-display text-[32px] block mb-3" style="color: #9984d8;">01</span>
              <h3 class="text-[17px] font-semibold mb-2 text-[var(--text-primary)]" style="letter-spacing: -0.03em;">Bingung mau posting apa.</h3>
              <p class="text-[14px] leading-relaxed text-[var(--text-secondary)]" style="letter-spacing: -0.03em;">Ide habis padahal harus konsisten.</p>
            </div>
            <div class="card-bd p-7 feature-card">
              <span class="font-display text-[32px] block mb-3" style="color: #9984d8;">02</span>
              <h3 class="text-[17px] font-semibold mb-2 text-[var(--text-primary)]" style="letter-spacing: -0.03em;">Komentar numpuk.</h3>
              <p class="text-[14px] leading-relaxed text-[var(--text-secondary)]" style="letter-spacing: -0.03em;">Telat balas, interaksi dan momentum hilang.</p>
            </div>
            <div class="card-bd p-7 feature-card">
              <span class="font-display text-[32px] block mb-3" style="color: #9984d8;">03</span>
              <h3 class="text-[17px] font-semibold mb-2 text-[var(--text-primary)]" style="letter-spacing: -0.03em;">Nggak tahu apa yang jalan.</h3>
              <p class="text-[14px] leading-relaxed text-[var(--text-secondary)]" style="letter-spacing: -0.03em;">Post mana, jam berapa, hook seperti apa, semua cuma feeling.</p>
            </div>
          </div>
        </div>
      </section>

      <!-- FITUR -->
      <section id="fitur" class="section-bd">
        <div class="container-bd">
          <h2 class="h2-bd">Bukan sekadar scheduler.</h2>
          <p class="text-center mb-14 text-[15px] text-[var(--text-secondary)]" style="letter-spacing: -0.03em;">Lima menu, satu alur: rencanakan, posting, balas, pelajari.</p>

          <div class="space-y-14">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
              <div>
                <span class="text-[12px] font-bold tracking-widest uppercase block mb-2" style="color: #9984d8;">01 &middot; Content</span>
                <h3 class="font-display text-[26px] md:text-[30px] leading-tight mb-3 text-[var(--text-primary)]">Dari satu topik jadi rencana 3 hari.</h3>
                <p class="text-[14px] leading-relaxed text-[var(--text-secondary)]" style="letter-spacing: -0.03em;">Tulis topik dan pilih gaya, Ixiera menyusun rencana post. Cek Quick Score gratis sebelum menjadwalkan, dan ubah post lama yang ramai jadi Listicle, Opini, atau Cerita.</p>
              </div>
              <div class="card-bd p-5">
                <div class="text-[10px] font-bold uppercase tracking-widest mb-3 text-[var(--text-muted)]">AI Content Planner</div>
                <div class="rounded-md p-2.5 mb-2 text-xs border border-[var(--border)] bg-[var(--bg-primary)] text-[var(--text-primary)]">Topik / Short Idea</div>
                <div class="rounded-md p-2.5 mb-2 text-xs border border-[var(--border)] bg-[var(--bg-primary)] text-[var(--text-primary)] flex justify-between"><span>Tone / Style</span><span class="text-[var(--text-muted)]">Storytelling</span></div>
                <div class="rounded-md p-2.5 mb-3 text-xs font-bold text-center bg-[var(--accent)] text-[var(--accent-text)]">Generate 3-Day Plan</div>
                <div class="rounded-md p-3 border border-[var(--border)] bg-[var(--bg-primary)]">
                  <div class="text-[10px] font-bold mb-1" style="color: #9984d8;">DAY 1: KOMPLEKSITAS MODEL VS KEBUTUHAN NYATA</div>
                  <p class="text-[11px] leading-relaxed text-[var(--text-secondary)]">Awal-awal ngulik AI, bawaannya pengen bikin arsitektur yang keliatan paling rumit...</p>
                </div>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
              <div class="order-2 md:order-1 card-bd p-5">
                <div class="flex gap-2 mb-4">
                  <div class="px-3 py-1 text-xs font-bold rounded-md bg-[var(--accent)] text-[var(--accent-text)]">Review Manual</div>
                  <div class="px-3 py-1 text-xs font-bold rounded-md border border-[var(--border)] text-[var(--text-secondary)]">Full Auto</div>
                </div>
                <div class="space-y-2 text-xs">
                  <div class="flex justify-between p-3 rounded-md border border-[var(--border)] bg-[var(--bg-primary)] text-[var(--text-primary)]"><span>Pertanyaan</span><span class="font-bold" style="color: #9984d8;">Balasan AI</span></div>
                  <div class="flex justify-between p-3 rounded-md border border-[var(--border)] bg-[var(--bg-primary)] text-[var(--text-primary)]"><span>Pujian</span><span class="font-bold" style="color: #3fcb7f;">Template</span></div>
                  <div class="flex justify-between p-3 rounded-md border border-[var(--border)] bg-[var(--bg-primary)] text-[var(--text-primary)]"><span>Spam / Toxic</span><span class="font-bold text-[var(--text-muted)]">Template</span></div>
                </div>
              </div>
              <div class="order-1 md:order-2">
                <span class="text-[12px] font-bold tracking-widest uppercase block mb-2" style="color: #9984d8;">02 &middot; Komentar</span>
                <h3 class="font-display text-[26px] md:text-[30px] leading-tight mb-3 text-[var(--text-primary)]">Komentar masuk, sudah terpilah.</h3>
                <p class="text-[14px] leading-relaxed text-[var(--text-secondary)]" style="letter-spacing: -0.03em;">Setiap komentar dikategorikan: pertanyaan, pujian, netral, spam, toxic. Atur tiap kategori: dijawab AI atau pakai template. Pilih Review Manual atau Full Auto, dengan batas balasan per jam.</p>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
              <div>
                <span class="text-[12px] font-bold tracking-widest uppercase block mb-2" style="color: #9984d8;">03 &middot; Analytics</span>
                <h3 class="font-display text-[26px] md:text-[30px] leading-tight mb-3 text-[var(--text-primary)]">Tahu apa yang jalan, bukan cuma feeling.</h3>
                <p class="text-[14px] leading-relaxed text-[var(--text-secondary)]" style="letter-spacing: -0.03em;">Jam dengan engagement tertinggi, tipe hook, panjang post, dan topik, semuanya dihitung dari data akunmu sendiri.</p>
              </div>
              <div class="card-bd p-5">
                <div class="flex gap-4 mb-4 text-xs font-bold border-b border-[var(--border)] pb-2 text-[var(--text-muted)]">
                  <span class="text-[var(--text-primary)]" style="border-bottom: 2px solid #9984d8; padding-bottom: 8px; margin-bottom: -10px;">Best Time</span>
                  <span>Hook</span>
                  <span>Length</span>
                </div>
                <div class="grid grid-cols-7 gap-1">
                  <div v-for="i in 21" :key="i" class="h-5 rounded-sm border border-[var(--border)]" :style="{ background: [3,7,11,15,18].includes(i) ? 'rgba(153,132,216,0.5)' : 'var(--bg-primary)' }"></div>
                </div>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
              <div class="order-2 md:order-1 card-bd p-5">
                <div class="rounded-md p-4 border border-[var(--border)] bg-[var(--bg-primary)] space-y-2">
                  <div class="flex justify-between items-center">
                    <span class="text-xs font-bold text-[var(--text-primary)]">Gaya Bahasa</span>
                    <span class="text-[10px] font-bold px-2 py-0.5 rounded-full" style="color: #3fcb7f; background: rgba(63,203,127,0.15);">Dipakai AI</span>
                  </div>
                  <p class="text-[11px] leading-relaxed text-[var(--text-secondary)]">Santai, singkat, hindari jargon. Selalu sapa dengan "kak".</p>
                </div>
              </div>
              <div class="order-1 md:order-2">
                <span class="text-[12px] font-bold tracking-widest uppercase block mb-2" style="color: #9984d8;">04 &middot; Pengetahuan</span>
                <h3 class="font-display text-[26px] md:text-[30px] leading-tight mb-3 text-[var(--text-primary)]">Ajari sekali, dipakai di semua balasan.</h3>
                <p class="text-[14px] leading-relaxed text-[var(--text-secondary)]" style="letter-spacing: -0.03em;">Tulis fakta, aturan, dan gaya bahasamu di Knowledge Base. AI memakainya setiap kali menyusun draf atau membalas komentar, jadi hasilnya nggak pernah generic.</p>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
              <div>
                <span class="text-[12px] font-bold tracking-widest uppercase block mb-2" style="color: #9984d8;">05 &middot; Dashboard</span>
                <h3 class="font-display text-[26px] md:text-[30px] leading-tight mb-3 text-[var(--text-primary)]">Semua terpantau di satu layar.</h3>
                <p class="text-[14px] leading-relaxed text-[var(--text-secondary)]" style="letter-spacing: -0.03em;">Views, likes, replies, dan post terbaikmu. Antrean menunjukkan apa yang akan tayang, sudah tayang, atau gagal.</p>
              </div>
              <div class="card-bd p-5">
                <div class="grid grid-cols-3 gap-2 text-center">
                  <div class="p-2 rounded border border-[var(--border)] bg-[var(--bg-primary)]"><div class="text-[9px] text-[var(--text-muted)]">Views</div><div class="text-sm font-bold text-[var(--text-primary)]">311k</div></div>
                  <div class="p-2 rounded border border-[var(--border)] bg-[var(--bg-primary)]"><div class="text-[9px] text-[var(--text-muted)]">Likes</div><div class="text-sm font-bold text-[var(--text-primary)]">2.5k</div></div>
                  <div class="p-2 rounded border border-[var(--border)] bg-[var(--bg-primary)]"><div class="text-[9px] text-[var(--text-muted)]">ER</div><div class="text-sm font-bold text-[var(--text-primary)]">4.8%</div></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- CONTOH DATA -->
      <section id="contoh" class="section-bd" style="background: var(--bg-secondary);">
        <div class="container-bd">
          <h2 class="h2-bd">Contoh dari data nyata.</h2>
          <p class="text-center mb-12 text-[15px] text-[var(--text-secondary)]" style="letter-spacing: -0.03em;">Hasil Analytics dari 50 post akun pembuat Ixiera. Sampel kecil, dan hasil tiap akun akan berbeda.</p>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
            <div class="card-bd p-6" style="background: var(--bg-primary);">
              <h3 class="text-sm font-bold mb-5 text-[var(--text-primary)]" style="letter-spacing: -0.03em;">Hook Performance</h3>
              <div class="space-y-3">
                <div>
                  <div class="flex justify-between text-xs mb-1 text-[var(--text-primary)]"><span class="font-bold">Question</span><span>2.92%</span></div>
                  <div class="w-full h-2 rounded-full overflow-hidden" style="background: var(--bg-hover);"><div class="h-full rounded-full" style="width: 92%; background: #9984d8;"></div></div>
                  <div class="text-[10px] mt-0.5 text-right text-[var(--text-muted)]">n=6</div>
                </div>
                <div>
                  <div class="flex justify-between text-xs mb-1 text-[var(--text-primary)]"><span class="font-bold">Story</span><span>1.36%</span></div>
                  <div class="w-full h-2 rounded-full overflow-hidden" style="background: var(--bg-hover);"><div class="h-full rounded-full" style="width: 43%; background: #3fcb7f;"></div></div>
                  <div class="text-[10px] mt-0.5 text-right text-[var(--text-muted)]">n=32</div>
                </div>
              </div>
              <p class="text-[11px] mt-5 leading-relaxed pt-4 border-t border-[var(--border)] text-[var(--text-secondary)]" style="letter-spacing: -0.03em;">Di akun ini, post berpembuka pertanyaan rata-rata mendapat engagement lebih dari dua kali lipat post bergaya cerita.</p>
            </div>

            <div class="card-bd p-6" style="background: var(--bg-primary);">
              <h3 class="text-sm font-bold mb-5 text-[var(--text-primary)]" style="letter-spacing: -0.03em;">Post Length</h3>
              <div class="space-y-3">
                <div>
                  <div class="flex justify-between text-xs mb-1 text-[var(--text-primary)]"><span class="font-bold">300-500 char</span><span>2.96%</span></div>
                  <div class="w-full h-2 rounded-full overflow-hidden" style="background: var(--bg-hover);"><div class="h-full rounded-full" style="width: 93%; background: #9984d8;"></div></div>
                  <div class="text-[10px] mt-0.5 text-right text-[var(--text-muted)]">n=10</div>
                </div>
                <div>
                  <div class="flex justify-between text-xs mb-1 text-[var(--text-primary)]"><span class="font-bold">100-300 char</span><span>1.12%</span></div>
                  <div class="w-full h-2 rounded-full overflow-hidden" style="background: var(--bg-hover);"><div class="h-full rounded-full" style="width: 35%; background: #3fcb7f;"></div></div>
                  <div class="text-[10px] mt-0.5 text-right text-[var(--text-muted)]">n=25</div>
                </div>
              </div>
              <p class="text-[11px] mt-5 leading-relaxed pt-4 border-t border-[var(--border)] text-[var(--text-secondary)]" style="letter-spacing: -0.03em;">Post 300-500 karakter mendapat engagement lebih dari tiga kali lipat post di bawah 100 karakter.</p>
            </div>
          </div>
          <p class="text-[11px] text-center mt-6 text-[var(--text-muted)]" style="letter-spacing: -0.03em;">ER = engagement rate. Jumlah post per kategori ditampilkan di tiap bar.</p>
        </div>
      </section>

      <!-- CARA KERJA -->
      <section id="cara-kerja" class="section-bd">
        <div class="container-bd">
          <h2 class="h2-bd">Mulai dalam 3 langkah.</h2>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mt-10">
            <div class="space-y-3">
              <div class="w-10 h-10 rounded-full flex items-center justify-center font-display text-[18px] border border-[var(--border)] bg-[var(--bg-secondary)]" style="color: #9984d8;">1</div>
              <h3 class="text-[17px] font-semibold text-[var(--text-primary)]" style="letter-spacing: -0.03em;">Daftar dan minta akses.</h3>
              <p class="text-[14px] leading-relaxed text-[var(--text-secondary)]" style="letter-spacing: -0.03em;">Buat akun, lalu kirim @username Threads kamu. Akses disetujui manual dan kamu dikabari lewat email.</p>
            </div>
            <div class="space-y-3">
              <div class="w-10 h-10 rounded-full flex items-center justify-center font-display text-[18px] border border-[var(--border)] bg-[var(--bg-secondary)]" style="color: #9984d8;">2</div>
              <h3 class="text-[17px] font-semibold text-[var(--text-primary)]" style="letter-spacing: -0.03em;">Hubungkan dan ajari gayamu.</h3>
              <p class="text-[14px] leading-relaxed text-[var(--text-secondary)]" style="letter-spacing: -0.03em;">Setelah disetujui, terima undangan tester di Threads dan login lewat sistem resmi Meta. Tulis dokumen gaya dan aturanmu di Knowledge Base.</p>
            </div>
            <div class="space-y-3">
              <div class="w-10 h-10 rounded-full flex items-center justify-center font-display text-[18px] border border-[var(--border)] bg-[var(--bg-secondary)]" style="color: #9984d8;">3</div>
              <h3 class="text-[17px] font-semibold text-[var(--text-primary)]" style="letter-spacing: -0.03em;">Review dan jalan.</h3>
              <p class="text-[14px] leading-relaxed text-[var(--text-secondary)]" style="letter-spacing: -0.03em;">Setujui draf, atur mode balasan, dan pantau Analytics tiap minggu.</p>
            </div>
          </div>
        </div>
      </section>

      <!-- KEAMANAN -->
      <section class="section-bd" style="background: var(--bg-secondary);">
        <div class="container-bd">
          <h2 class="h2-bd">Kamu yang pegang kendali.</h2>
          <ul class="space-y-4 max-w-2xl mx-auto">
            <li class="flex items-start gap-3">
              <svg class="w-5 h-5 shrink-0 mt-0.5" style="color: #3fcb7f;" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
              <span class="text-[14px] leading-relaxed text-[var(--text-primary)]" style="letter-spacing: -0.03em;">Password Threads tidak pernah disimpan. Login hanya lewat OAuth resmi Meta.</span>
            </li>
            <li class="flex items-start gap-3">
              <svg class="w-5 h-5 shrink-0 mt-0.5" style="color: #3fcb7f;" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
              <span class="text-[14px] leading-relaxed text-[var(--text-primary)]" style="letter-spacing: -0.03em;">Data analitik dan dokumen gayamu terpisah dari user lain.</span>
            </li>
            <li class="flex items-start gap-3">
              <svg class="w-5 h-5 shrink-0 mt-0.5" style="color: #3fcb7f;" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
              <span class="text-[14px] leading-relaxed text-[var(--text-primary)]" style="letter-spacing: -0.03em;">Teks yang diproses AI dikirim ke penyedia model (Gemini/Groq). Detailnya ada di Kebijakan Privasi.</span>
            </li>
            <li class="flex items-start gap-3">
              <svg class="w-5 h-5 shrink-0 mt-0.5" style="color: #3fcb7f;" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
              <span class="text-[14px] leading-relaxed text-[var(--text-primary)]" style="letter-spacing: -0.03em;">Matikan otomatisasi atau putus koneksi kapan saja lewat Kill Switch.</span>
            </li>
          </ul>
        </div>
      </section>

      <!-- HARGA -->
      <section id="harga" class="section-bd">
        <div class="container-bd">
          <h2 class="h2-bd">Mulai dari sini.</h2>
          <p class="text-center mb-12 text-[15px] text-[var(--text-secondary)]" style="letter-spacing: -0.03em;">Pilih paket yang sesuai. Kami terus berbenah dari masukanmu.</p>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
            <div class="card-bd p-7 flex flex-col">
              <h3 class="text-[17px] font-semibold mb-1 text-[var(--text-primary)]" style="letter-spacing: -0.03em;">Trial 7 Hari</h3>
              <p class="text-[13px] mb-6 text-[var(--text-secondary)]" style="letter-spacing: -0.03em;">7 hari &middot; 20 kredit gratis &middot; semua fitur</p>
              <a href="https://app.ixiera.id/login" class="btn-bd-ghost text-center mt-auto">Mulai Gratis</a>
            </div>
            <div class="card-bd p-7 flex flex-col relative" style="border: 2px solid #9984d8;">
              <div class="absolute -top-3 left-1/2 -translate-x-1/2 text-[10px] font-bold uppercase tracking-widest px-3 py-1 rounded-full text-white" style="background: #9984d8;">Popular</div>
              <h3 class="text-[17px] font-semibold mb-1 text-[var(--text-primary)]" style="letter-spacing: -0.03em;">Paket 30 hari</h3>
              <p class="text-[13px] mb-6 text-[var(--text-secondary)]" style="letter-spacing: -0.03em;">Rp29.000 &middot; 100 kredit per bulan &middot; tanpa auto-renew</p>
              <a href="https://app.ixiera.id/login" class="btn-bd-primary text-center mt-auto">Pilih Pro</a>
            </div>
            <div class="card-bd p-7 flex flex-col">
              <h3 class="text-[17px] font-semibold mb-1 text-[var(--text-primary)]" style="letter-spacing: -0.03em;">Paket + API Key Sendiri</h3>
              <p class="text-[13px] mb-6 text-[var(--text-secondary)]" style="letter-spacing: -0.03em;">Rp19.000 &middot; pakai API key milikmu &middot; tanpa kredit</p>
              <a href="https://app.ixiera.id/login" class="btn-bd-ghost text-center mt-auto">Pilih BYOK</a>
            </div>
          </div>
          <div class="text-center mt-8 space-y-2">
            <p class="text-[12px] text-[var(--text-muted)]" style="letter-spacing: -0.03em;">1 kredit = 1 aksi AI (generate, balasan AI, repurpose, analisis lanjutan). Template balasan dan Quick Score gratis. API key sendiri hanya tersedia di paket berbayar.</p>
            <p class="text-[12px] font-medium text-[var(--text-secondary)]" style="letter-spacing: -0.03em;">Harga beta, terkunci selama kamu berlangganan.</p>
            <a href="https://app.ixiera.id/login" class="btn-bd-primary inline-block mt-3">Minta Akses</a>
          </div>
        </div>
      </section>

      <!-- FAQ -->
      <section id="faq" class="section-bd" style="background: var(--bg-secondary);">
        <div class="container-bd" style="max-width: 800px;">
          <h2 class="h2-bd">Pertanyaan Umum</h2>
          <div class="border-t border-[var(--border)] mt-8">
            <details class="group border-b border-[var(--border)] py-4 cursor-pointer">
              <summary class="flex justify-between items-center text-[15px] font-semibold list-none text-[var(--text-primary)]" style="letter-spacing: -0.03em;">
                Kenapa harus minta akses?
                <span class="group-open:rotate-180 transition"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <p class="text-[14px] mt-3 leading-relaxed text-[var(--text-secondary)]" style="letter-spacing: -0.03em;">Ixiera masih dalam tahap early access, jadi tiap akun ditambahkan manual dan perlu disetujui dulu. Kabar lewat email.</p>
            </details>
            <details class="group border-b border-[var(--border)] py-4 cursor-pointer">
              <summary class="flex justify-between items-center text-[15px] font-semibold list-none text-[var(--text-primary)]" style="letter-spacing: -0.03em;">
                Apakah ini gratis?
                <span class="group-open:rotate-180 transition"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <p class="text-[14px] mt-3 leading-relaxed text-[var(--text-secondary)]" style="letter-spacing: -0.03em;">Trial 7 hari gratis dengan 20 kredit. Setelah itu, paket berbayar mulai dari Rp29.000 per bulan.</p>
            </details>
            <details class="group border-b border-[var(--border)] py-4 cursor-pointer">
              <summary class="flex justify-between items-center text-[15px] font-semibold list-none text-[var(--text-primary)]" style="letter-spacing: -0.03em;">
                Apa itu kredit?
                <span class="group-open:rotate-180 transition"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <p class="text-[14px] mt-3 leading-relaxed text-[var(--text-secondary)]" style="letter-spacing: -0.03em;">1 kredit = 1 aksi AI (generate, balas komentar, repurpose, analisis lanjutan). Template balasan dan Quick Score gratis tanpa kredit.</p>
            </details>
            <details class="group border-b border-[var(--border)] py-4 cursor-pointer">
              <summary class="flex justify-between items-center text-[15px] font-semibold list-none text-[var(--text-primary)]" style="letter-spacing: -0.03em;">
                Apakah posting tanpa izinku?
                <span class="group-open:rotate-180 transition"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <p class="text-[14px] mt-3 leading-relaxed text-[var(--text-secondary)]" style="letter-spacing: -0.03em;">Tidak. Semua posting dan balasan bisa di-review manual dulu sebelum tayang. Kamu yang pegang kendali penuh.</p>
            </details>
            <details class="group border-b border-[var(--border)] py-4 cursor-pointer">
              <summary class="flex justify-between items-center text-[15px] font-semibold list-none text-[var(--text-primary)]" style="letter-spacing: -0.03em;">
                Apakah akunku bisa kena blokir?
                <span class="group-open:rotate-180 transition"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <p class="text-[14px] mt-3 leading-relaxed text-[var(--text-secondary)]" style="letter-spacing: -0.03em;">Ixiera pakai API resmi Meta dan mengikuti batas yang ditetapkan. Kami juga punya batas balasan per jam untuk menghindari perilaku yang terlihat seperti spam.</p>
            </details>
            <details class="group border-b border-[var(--border)] py-4 cursor-pointer">
              <summary class="flex justify-between items-center text-[15px] font-semibold list-none text-[var(--text-primary)]" style="letter-spacing: -0.03em;">
                Apakah balasannya bisa kasar?
                <span class="group-open:rotate-180 transition"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <p class="text-[14px] mt-3 leading-relaxed text-[var(--text-secondary)]" style="letter-spacing: -0.03em;">Kamu yang menentukan gaya bahasa di Knowledge Base. Balasan akan mengikuti aturan yang kamu tulis.</p>
            </details>
            <details class="group border-b border-[var(--border)] py-4 cursor-pointer">
              <summary class="flex justify-between items-center text-[15px] font-semibold list-none text-[var(--text-primary)]" style="letter-spacing: -0.03em;">
                Apa bedanya dengan scheduler biasa?
                <span class="group-open:rotate-180 transition"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <p class="text-[14px] mt-3 leading-relaxed text-[var(--text-secondary)]" style="letter-spacing: -0.03em;">Scheduler biasa cuma menjadwalkan. Ixiera belajar dari data akunmu (jam, hook, panjang, topik) dan membalas komentar dengan gayamu. Satu platform untuk rencana, posting, balas, dan analisis.</p>
            </details>
            <details class="group border-b border-[var(--border)] py-4 cursor-pointer">
              <summary class="flex justify-between items-center text-[15px] font-semibold list-none text-[var(--text-primary)]" style="letter-spacing: -0.03em;">
                Datanya dipakai siapa?
                <span class="group-open:rotate-180 transition"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <p class="text-[14px] mt-3 leading-relaxed text-[var(--text-secondary)]" style="letter-spacing: -0.03em;">Data kamu hanya dipakai untuk akunmu sendiri. Tidak dibagikan ke user lain. Detailnya ada di Kebijakan Privasi.</p>
            </details>
            <details class="group border-b border-[var(--border)] py-4 cursor-pointer">
              <summary class="flex justify-between items-center text-[15px] font-semibold list-none text-[var(--text-primary)]" style="letter-spacing: -0.03em;">
                Harus paham teknis?
                <span class="group-open:rotate-180 transition"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <p class="text-[14px] mt-3 leading-relaxed text-[var(--text-secondary)]" style="letter-spacing: -0.03em;">Tidak. Setup butuh 3 langkah dan kurang dari 10 menit. Semua otomatisasi jalan di background.</p>
            </details>
          </div>
        </div>
      </section>

      <!-- FINAL CTA -->
      <section class="section-bd text-center">
        <div class="container-bd">
          <h2 class="font-display text-[48px] md:text-[56px] leading-[1.0] mb-8 text-[var(--text-primary)]">Siap berhenti nebak-nebak?</h2>
          <a href="https://app.ixiera.id/login" class="btn-bd-primary inline-block">Minta Akses</a>
        </div>
      </section>

      <!-- FOOTER -->
      <footer class="border-t border-[var(--border)] py-8">
        <div class="container-bd flex flex-col md:flex-row justify-between items-center gap-5 text-[13px] text-[var(--text-muted)]" style="letter-spacing: -0.03em;">
          <div class="flex items-center gap-2">
            <div class="w-6 h-6 flex items-center justify-center rounded text-[10px] font-bold bg-[var(--accent)] text-[var(--accent-text)]">IX</div>
            <span>2026 Ixiera.</span>
          </div>
          <div class="flex gap-5 flex-wrap justify-center">
            <a href="mailto:contact@ixiera.id" class="hover:text-[var(--text-primary)] transition">Email</a>
            <a href="/privacy" class="hover:text-[var(--text-primary)] transition">Kebijakan Privasi</a>
            <a href="/terms" class="hover:text-[var(--text-primary)] transition">Syarat &amp; Ketentuan</a>
            <a href="/data-deletion" class="hover:text-[var(--text-primary)] transition">Hapus Data</a>
          </div>
        </div>
        <div class="container-bd text-center mt-5 text-[10px] text-[var(--text-muted)]" style="letter-spacing: -0.03em;">
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
  theme.value = document.documentElement.classList.contains('dark') ? 'dark' : 'light'
})
</script>
