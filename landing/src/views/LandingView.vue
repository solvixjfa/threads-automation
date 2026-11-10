<template>
  <div class="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)] font-sans selection:bg-[#9984d8] selection:text-white">
    
    <!-- TOP NAVBAR (FIXED) -->
    <nav class="fixed top-0 left-0 right-0 z-50 h-16 bg-[var(--bg-primary)]/80 backdrop-blur-md border-b border-[var(--border)] flex items-center">
      <div class="w-full max-w-[1200px] mx-auto px-6 flex items-center justify-between">
        
        <!-- Logo -->
        <a href="/" class="flex items-center gap-2">
          <div class="w-7 h-7 flex items-center justify-center rounded text-xs font-bold bg-[var(--accent)] text-[var(--accent-text)]">IX</div>
          <span class="font-bold text-lg tracking-tight">Ixiera</span>
        </a>

        <!-- Desktop Nav Links -->
        <div class="hidden md:flex items-center gap-8 text-sm font-medium text-[var(--text-secondary)]">
          <a href="#fitur" class="hover:text-[var(--text-primary)] transition">Fitur</a>
          <a href="#contoh" class="hover:text-[var(--text-primary)] transition">Contoh Data</a>
          <a href="#cara-kerja" class="hover:text-[var(--text-primary)] transition">Cara Kerja</a>
          <a href="/pricing" class="hover:text-[var(--text-primary)] transition">Harga</a>
          <a href="#faq" class="hover:text-[var(--text-primary)] transition">FAQ</a>
        </div>

        <!-- Desktop Actions (Theme, Lang, CTA) -->
        <div class="hidden md:flex items-center gap-4">
          <!-- Theme Toggle -->
          <button @click="toggleTheme" class="p-2 text-[var(--text-muted)] hover:text-[var(--text-primary)] transition">
            <Sun v-if="theme === 'dark'" class="w-4 h-4" />
            <Moon v-else class="w-4 h-4" />
          </button>
          <!-- Lang Toggle -->
          <button @click="toggleLang" class="text-xs font-bold text-[var(--text-muted)] hover:text-[var(--text-primary)] transition px-2 py-1 rounded border border-[var(--border)]">
            {{ locale.toUpperCase() }}
          </button>
          
          <div class="w-px h-4 bg-[var(--border)] mx-1"></div>

          <a href="https://app.ixiera.id/login" class="text-sm font-medium text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition">Log in</a>
          <a href="https://app.ixiera.id/login" class="btn-bd-primary" style="padding: 8px 16px;">Sign up</a>
        </div>

        <!-- Mobile Hamburger -->
        <button @click="mobileMenuOpen = true" class="md:hidden p-2 text-[var(--text-primary)]">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
        </button>
      </div>
    </nav>

    <!-- MOBILE DRAWER (FULL FIX) -->
    <div v-if="mobileMenuOpen" class="md:hidden fixed inset-0 z-[100] bg-[var(--bg-primary)]/95 backdrop-blur-lg flex flex-col p-6">
      <div class="flex justify-between items-center mb-10">
        <div class="flex items-center gap-2">
          <div class="w-7 h-7 flex items-center justify-center rounded text-xs font-bold bg-[var(--accent)] text-[var(--accent-text)]">IX</div>
          <span class="font-bold text-lg">Ixiera</span>
        </div>
        <button @click="mobileMenuOpen = false" class="p-2 text-[var(--text-primary)]">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
        </button>
      </div>
      
      <nav class="flex flex-col gap-6 text-[16px] font-medium text-[var(--text-secondary)]">
        <a href="#fitur" @click="mobileMenuOpen = false" class="hover:text-[var(--text-primary)] transition">Fitur</a>
        <a href="#contoh" @click="mobileMenuOpen = false" class="hover:text-[var(--text-primary)] transition">Contoh Data</a>
        <a href="#cara-kerja" @click="mobileMenuOpen = false" class="hover:text-[var(--text-primary)] transition">Cara Kerja</a>
        <a href="/pricing" @click="mobileMenuOpen = false" class="hover:text-[var(--text-primary)] transition">Harga</a>
        <a href="#faq" @click="mobileMenuOpen = false" class="hover:text-[var(--text-primary)] transition">FAQ</a>
      </nav>
      
      <div class="mt-auto pt-6 border-t border-[var(--border)] space-y-4">
        <!-- Theme & Lang di Mobile -->
        <div class="flex gap-2">
          <button @click="toggleTheme" class="flex-1 flex items-center justify-center py-2.5 rounded-md border border-[var(--border)] text-[var(--text-muted)]">
            <Sun v-if="theme === 'dark'" class="w-4 h-4" />
            <Moon v-else class="w-4 h-4" />
          </button>
          <button @click="toggleLang" class="flex-1 py-2.5 rounded-md border border-[var(--border)] text-[var(--text-muted)] text-xs font-bold">
            {{ locale.toUpperCase() }}
          </button>
        </div>
        <a href="https://app.ixiera.id/login" class="btn-bd-primary w-full text-center block">Sign up</a>
        <a href="https://app.ixiera.id/login" class="text-center block text-sm text-[var(--text-secondary)] py-1">Log in</a>
      </div>
    </div>

    <!-- MAIN CONTENT -->
    <main class="pt-16">
      
      <!-- HERO -->
      <section class="relative pt-24 pb-20">
        <div class="max-w-[1200px] mx-auto px-6 text-center relative z-10">
          <div class="pill-bd mb-6 mx-auto" style="width: fit-content;">
            <span class="w-1.5 h-1.5 rounded-full" style="background: var(--accent-mint);"></span>
            PUBLIC BETA
          </div>
          
          <h1 class="font-display text-[48px] md:text-[64px] leading-[1.0] mb-6 max-w-[800px] mx-auto text-[var(--text-primary)]">
            Posting yang belajar dari <br class="hidden md:block">
            <span class="italic text-[var(--accent-violet)]">akun kamu sendiri.</span>
          </h1>
          
          <p class="text-[16px] md:text-[18px] leading-[1.56] max-w-[640px] mx-auto mb-10 text-[var(--text-secondary)]">
            Ixiera membaca post kamu yang paling jalan (jam, hook, panjang, topik), lalu membantu bikin rencana konten dan membalas komentar dengan gayamu.
          </p>
          
          <div class="flex flex-col sm:flex-row items-center justify-center gap-3 mb-8">
            <a href="https://app.ixiera.id/login" class="btn-bd-primary w-full sm:w-auto text-center">Minta Akses</a>
            <a href="#contoh" class="btn-bd-ghost w-full sm:w-auto text-center">Lihat contohnya</a>
          </div>
          
          <p class="text-[13px] text-[var(--text-muted)] mb-6">Trial 7 hari &middot; 20 kredit gratis &middot; Tanpa bayar di awal</p>
          
          <div class="flex flex-wrap justify-center gap-x-5 gap-y-2 text-xs text-[var(--text-muted)]">
            <span>Login resmi Meta, tanpa simpan password</span>
            <span>Kill Switch kapan saja</span>
            <span>Data terpisah per user</span>
          </div>
        </div>

        <!-- HERO MOCKUP with GLOW -->
        <div class="max-w-[1000px] mx-auto px-6 pb-16 md:pb-24 relative mt-10">
          <div class="absolute inset-0 pointer-events-none" style="background: radial-gradient(ellipse 70% 60% at 50% 0%, rgba(153,132,216,0.35) 0%, transparent 70%);"></div>
          
          <div class="relative rounded-2xl border border-[var(--border)] overflow-hidden bg-[#050607]">
            <div class="flex items-center gap-1.5 px-4 py-3 border-b border-[#1a1a1a]">
              <div class="w-2.5 h-2.5 rounded-full bg-[#1a1a1a]"></div>
              <div class="w-2.5 h-2.5 rounded-full bg-[#1a1a1a]"></div>
              <div class="w-2.5 h-2.5 rounded-full bg-[#1a1a1a]"></div>
              <span class="ml-2 text-[10px] text-[#666] uppercase tracking-widest font-bold">Dashboard</span>
            </div>
            
            <div class="p-5 md:p-7 space-y-5">
              <div class="grid grid-cols-3 gap-3">
                <div class="bg-black border border-[#1a1a1a] rounded-xl p-3 md:p-4">
                  <p class="text-[10px] text-[#666] mb-1">Views</p>
                  <p class="text-lg md:text-2xl font-bold text-white tracking-tight">311k</p>
                  <p class="text-[10px] text-[#3fcb7f] font-medium">+126%</p>
                </div>
                <div class="bg-black border border-[#1a1a1a] rounded-xl p-3 md:p-4">
                  <p class="text-[10px] text-[#666] mb-1">Followers</p>
                  <p class="text-lg md:text-2xl font-bold text-white tracking-tight">2.5k</p>
                  <p class="text-[10px] text-[#3fcb7f] font-medium">+15</p>
                </div>
                <div class="bg-black border border-[#1a1a1a] rounded-xl p-3 md:p-4">
                  <p class="text-[10px] text-[#666] mb-1">ER</p>
                  <p class="text-lg md:text-2xl font-bold text-white tracking-tight">4.8%</p>
                  <p class="text-[10px] text-[#3fcb7f] font-medium">+0.3</p>
                </div>
              </div>
              
              <div class="bg-black border border-[#1a1a1a] rounded-xl p-4">
                <div class="flex justify-between items-center mb-3">
                  <span class="text-[10px] text-[#666] uppercase tracking-widest font-bold">Growth</span>
                  <span class="text-[10px] text-[#3fcb7f] font-bold">Last 30 days</span>
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
      </section>

      <!-- MASALAH -->
      <section class="py-20 border-t border-[var(--border)]">
        <div class="max-w-[1000px] mx-auto px-6">
          <h2 class="h2-bd">Jadi admin akun sendiri itu melelahkan.</h2>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-5 mt-10">
            <div class="card-bd p-7 feature-card">
              <span class="font-display text-[32px] block mb-3 text-[var(--accent-violet)]">01</span>
              <h3 class="text-[17px] font-semibold mb-2">Bingung mau posting apa.</h3>
              <p class="text-[14px] leading-relaxed text-[var(--text-secondary)]">Ide habis padahal harus konsisten.</p>
            </div>
            <div class="card-bd p-7 feature-card">
              <span class="font-display text-[32px] block mb-3 text-[var(--accent-violet)]">02</span>
              <h3 class="text-[17px] font-semibold mb-2">Komentar numpuk.</h3>
              <p class="text-[14px] leading-relaxed text-[var(--text-secondary)]">Telat balas, interaksi dan momentum hilang.</p>
            </div>
            <div class="card-bd p-7 feature-card">
              <span class="font-display text-[32px] block mb-3 text-[var(--accent-violet)]">03</span>
              <h3 class="text-[17px] font-semibold mb-2">Nggak tahu apa yang jalan.</h3>
              <p class="text-[14px] leading-relaxed text-[var(--text-secondary)]">Post mana, jam berapa, hook seperti apa, semua cuma feeling.</p>
            </div>
          </div>
        </div>
      </section>

      <!-- FITUR -->
      <section id="fitur" class="py-20 border-t border-[var(--border)]">
        <div class="max-w-[1000px] mx-auto px-6">
          <h2 class="h2-bd">Bukan sekadar scheduler.</h2>
          <p class="text-center mb-14 text-[15px] text-[var(--text-secondary)]">Lima menu, satu alur: rencanakan, posting, balas, pelajari.</p>
          
          <div class="space-y-14">
            <!-- Fitur 1 -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
              <div>
                <span class="text-[12px] font-bold tracking-widest uppercase block mb-2 text-[var(--accent-violet)]">01 &middot; Content</span>
                <h3 class="font-display text-[26px] md:text-[30px] leading-tight mb-3">Dari satu topik jadi rencana 3 hari.</h3>
                <p class="text-[14px] leading-relaxed text-[var(--text-secondary)]">Tulis topik dan pilih gaya, Ixiera menyusun rencana post. Cek Quick Score gratis sebelum menjadwalkan, dan ubah post lama yang ramai jadi Listicle, Opini, atau Cerita.</p>
              </div>
              <div class="card-bd p-5">
                <div class="text-[10px] font-bold uppercase tracking-widest mb-3 text-[var(--text-muted)]">AI Content Planner</div>
                <div class="rounded-md p-2.5 mb-2 text-xs border border-[var(--border)] bg-[var(--bg-primary)]">Topik / Short Idea</div>
                <div class="rounded-md p-2.5 mb-2 text-xs border border-[var(--border)] bg-[var(--bg-primary)] flex justify-between"><span>Tone / Style</span><span class="text-[var(--text-muted)]">Storytelling</span></div>
                <div class="rounded-md p-2.5 mb-3 text-xs font-bold text-center bg-[var(--accent)] text-[var(--accent-text)]">Generate 3-Day Plan</div>
                <div class="rounded-md p-3 border border-[var(--border)] bg-[var(--bg-primary)]">
                  <div class="text-[10px] font-bold mb-1 text-[var(--accent-violet)]">DAY 1: KOMPLEKSITAS MODEL VS KEBUTUHAN NYATA</div>
                  <p class="text-[11px] leading-relaxed text-[var(--text-secondary)]">Awal-awal ngulik AI, bawaannya pengen bikin arsitektur yang keliatan paling rumit...</p>
                </div>
              </div>
            </div>

            <!-- Fitur 2 -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
              <div class="order-2 md:order-1 card-bd p-5">
                <div class="flex gap-2 mb-4">
                  <div class="px-3 py-1 text-xs font-bold rounded-md bg-[var(--accent)] text-[var(--accent-text)]">Review Manual</div>
                  <div class="px-3 py-1 text-xs font-bold rounded-md border border-[var(--border)] text-[var(--text-secondary)]">Full Auto</div>
                </div>
                <div class="space-y-2 text-xs">
                  <div class="flex justify-between p-3 rounded-md border border-[var(--border)] bg-[var(--bg-primary)]"><span>Pertanyaan</span><span class="font-bold text-[var(--accent-violet)]">Balasan AI</span></div>
                  <div class="flex justify-between p-3 rounded-md border border-[var(--border)] bg-[var(--bg-primary)]"><span>Pujian</span><span class="font-bold text-[var(--accent-mint)]">Template</span></div>
                  <div class="flex justify-between p-3 rounded-md border border-[var(--border)] bg-[var(--bg-primary)]"><span>Spam / Toxic</span><span class="font-bold text-[var(--text-muted)]">Template</span></div>
                </div>
              </div>
              <div class="order-1 md:order-2">
                <span class="text-[12px] font-bold tracking-widest uppercase block mb-2 text-[var(--accent-violet)]">02 &middot; Komentar</span>
                <h3 class="font-display text-[26px] md:text-[30px] leading-tight mb-3">Komentar masuk, sudah terpilah.</h3>
                <p class="text-[14px] leading-relaxed text-[var(--text-secondary)]">Setiap komentar dikategorikan: pertanyaan, pujian, netral, spam, toxic. Atur tiap kategori: dijawab AI atau pakai template. Pilih Review Manual atau Full Auto, dengan batas balasan per jam.</p>
              </div>
            </div>

            <!-- Fitur 3 -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
              <div>
                <span class="text-[12px] font-bold tracking-widest uppercase block mb-2 text-[var(--accent-violet)]">03 &middot; Analytics</span>
                <h3 class="font-display text-[26px] md:text-[30px] leading-tight mb-3">Tahu apa yang jalan, bukan cuma feeling.</h3>
                <p class="text-[14px] leading-relaxed text-[var(--text-secondary)]">Jam dengan engagement tertinggi, tipe hook, panjang post, dan topik, semuanya dihitung dari data akunmu sendiri.</p>
              </div>
              <div class="card-bd p-5">
                <div class="flex gap-4 mb-4 text-xs font-bold border-b border-[var(--border)] pb-2 text-[var(--text-muted)]">
                  <span class="text-[var(--text-primary)] border-b-2 border-[var(--accent-violet)] pb-2 -mb-[10px]">Best Time</span>
                  <span>Hook</span>
                  <span>Length</span>
                </div>
                <div class="grid grid-cols-7 gap-1">
                  <div v-for="i in 21" :key="i" class="h-5 rounded-sm border border-[var(--border)]" :style="{ background: [3,7,11,15,18].includes(i) ? 'rgba(153,132,216,0.5)' : 'var(--bg-primary)' }"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- CONTOH DATA -->
      <section id="contoh" class="py-20 border-t border-[var(--border)] bg-[var(--bg-secondary)]">
        <div class="max-w-[1000px] mx-auto px-6">
          <h2 class="h2-bd">Contoh dari data nyata.</h2>
          <p class="text-center mb-12 text-[15px] text-[var(--text-secondary)]">Hasil Analytics dari 50 post akun pembuat Ixiera. Sampel kecil, dan hasil tiap akun akan berbeda.</p>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
            <div class="card-bd p-6 bg-[var(--bg-primary)]">
              <h3 class="text-sm font-bold mb-5">Hook Performance</h3>
              <div class="space-y-3">
                <div>
                  <div class="flex justify-between text-xs mb-1"><span class="font-bold">Question</span><span>2.92%</span></div>
                  <div class="w-full h-2 rounded-full overflow-hidden bg-[var(--bg-hover)]"><div class="h-full rounded-full bg-[var(--accent-violet)]" style="width: 92%;"></div></div>
                  <div class="text-[10px] mt-0.5 text-right text-[var(--text-muted)]">n=6</div>
                </div>
                <div>
                  <div class="flex justify-between text-xs mb-1"><span class="font-bold">Story</span><span>1.36%</span></div>
                  <div class="w-full h-2 rounded-full overflow-hidden bg-[var(--bg-hover)]"><div class="h-full rounded-full bg-[var(--accent-mint)]" style="width: 43%;"></div></div>
                  <div class="text-[10px] mt-0.5 text-right text-[var(--text-muted)]">n=32</div>
                </div>
              </div>
              <p class="text-[11px] mt-5 leading-relaxed pt-4 border-t border-[var(--border)] text-[var(--text-secondary)]">Di akun ini, post berpembuka pertanyaan rata-rata mendapat engagement lebih dari dua kali lipat post bergaya cerita.</p>
            </div>
            
            <div class="card-bd p-6 bg-[var(--bg-primary)]">
              <h3 class="text-sm font-bold mb-5">Post Length</h3>
              <div class="space-y-3">
                <div>
                  <div class="flex justify-between text-xs mb-1"><span class="font-bold">300-500 char</span><span>2.96%</span></div>
                  <div class="w-full h-2 rounded-full overflow-hidden bg-[var(--bg-hover)]"><div class="h-full rounded-full bg-[var(--accent-violet)]" style="width: 93%;"></div></div>
                  <div class="text-[10px] mt-0.5 text-right text-[var(--text-muted)]">n=10</div>
                </div>
                <div>
                  <div class="flex justify-between text-xs mb-1"><span class="font-bold">100-300 char</span><span>1.12%</span></div>
                  <div class="w-full h-2 rounded-full overflow-hidden bg-[var(--bg-hover)]"><div class="h-full rounded-full bg-[var(--accent-mint)]" style="width: 35%;"></div></div>
                  <div class="text-[10px] mt-0.5 text-right text-[var(--text-muted)]">n=25</div>
                </div>
              </div>
              <p class="text-[11px] mt-5 leading-relaxed pt-4 border-t border-[var(--border)] text-[var(--text-secondary)]">Post 300-500 karakter mendapat engagement lebih dari tiga kali lipat post di bawah 100 karakter.</p>
            </div>
          </div>
        </div>
      </section>

      <!-- HARGA -->
      <section id="harga" class="py-20 border-t border-[var(--border)]">
        <div class="max-w-[1000px] mx-auto px-6">
          <h2 class="h2-bd">Mulai dari sini.</h2>
          <p class="text-center mb-12 text-[15px] text-[var(--text-secondary)]">Pilih paket yang sesuai. Kami terus berbenah dari masukanmu.</p>
          
          <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
            <div class="card-bd p-7 flex flex-col">
              <h3 class="text-[17px] font-semibold mb-1">Trial 7 Hari</h3>
              <p class="text-[13px] mb-6 text-[var(--text-secondary)]">7 hari &middot; 20 kredit gratis &middot; semua fitur</p>
              <a href="https://app.ixiera.id/login" class="btn-bd-ghost text-center mt-auto">Mulai Gratis</a>
            </div>
            
            <div class="card-bd p-7 flex flex-col relative border-2 border-[var(--accent-violet)]">
              <div class="absolute -top-3 left-1/2 -translate-x-1/2 text-[10px] font-bold uppercase tracking-widest px-3 py-1 rounded-full text-white bg-[var(--accent-violet)]">Popular</div>
              <h3 class="text-[17px] font-semibold mb-1">Paket 30 hari</h3>
              <p class="text-[13px] mb-6 text-[var(--text-secondary)]">Rp29.000 &middot; 100 kredit per bulan &middot; tanpa auto-renew</p>
              <a href="https://app.ixiera.id/login" class="btn-bd-primary text-center mt-auto">Pilih Pro</a>
            </div>
            
            <div class="card-bd p-7 flex flex-col">
              <h3 class="text-[17px] font-semibold mb-1">Paket + API Key Sendiri</h3>
              <p class="text-[13px] mb-6 text-[var(--text-secondary)]">Rp19.000 &middot; pakai API key milikmu &middot; tanpa kredit</p>
              <a href="https://app.ixiera.id/login" class="btn-bd-ghost text-center mt-auto">Pilih BYOK</a>
            </div>
          </div>
          
          <div class="text-center mt-8 space-y-2">
            <p class="text-[12px] text-[var(--text-muted)]">1 kredit = 1 aksi AI (generate, balasan AI, repurpose, analisis lanjutan). Template balasan dan Quick Score gratis.</p>
            <p class="text-[12px] font-medium text-[var(--text-secondary)]">Harga beta, terkunci selama kamu berlangganan.</p>
            <a href="https://app.ixiera.id/login" class="btn-bd-primary inline-block mt-3">Minta Akses</a>
          </div>
        </div>
      </section>

      <!-- FAQ -->
      <section id="faq" class="py-20 border-t border-[var(--border)] bg-[var(--bg-secondary)]">
        <div class="max-w-[800px] mx-auto px-6">
          <h2 class="h2-bd">Pertanyaan Umum</h2>
          <div class="border-t border-[var(--border)] mt-8">
            <details class="group border-b border-[var(--border)] py-4 cursor-pointer">
              <summary class="flex justify-between items-center text-[15px] font-semibold list-none text-[var(--text-primary)]">
                Kenapa harus minta akses?
                <span class="group-open:rotate-180 transition"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <p class="text-[14px] mt-3 leading-relaxed text-[var(--text-secondary)]">Ixiera masih dalam tahap early access, jadi tiap akun ditambahkan manual dan perlu disetujui dulu. Kabar lewat email.</p>
            </details>
            <details class="group border-b border-[var(--border)] py-4 cursor-pointer">
              <summary class="flex justify-between items-center text-[15px] font-semibold list-none text-[var(--text-primary)]">
                Apakah ini gratis?
                <span class="group-open:rotate-180 transition"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <p class="text-[14px] mt-3 leading-relaxed text-[var(--text-secondary)]">Trial 7 hari gratis dengan 20 kredit. Setelah itu, paket berbayar mulai dari Rp29.000 per bulan.</p>
            </details>
            <details class="group border-b border-[var(--border)] py-4 cursor-pointer">
              <summary class="flex justify-between items-center text-[15px] font-semibold list-none text-[var(--text-primary)]">
                Apa itu kredit?
                <span class="group-open:rotate-180 transition"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <p class="text-[14px] mt-3 leading-relaxed text-[var(--text-secondary)]">1 kredit = 1 aksi AI (generate, balas komentar, repurpose, analisis lanjutan). Template balasan dan Quick Score gratis tanpa kredit.</p>
            </details>
            <details class="group border-b border-[var(--border)] py-4 cursor-pointer">
              <summary class="flex justify-between items-center text-[15px] font-semibold list-none text-[var(--text-primary)]">
                Apakah posting tanpa izinku?
                <span class="group-open:rotate-180 transition"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></span>
              </summary>
              <p class="text-[14px] mt-3 leading-relaxed text-[var(--text-secondary)]">Tidak. Semua posting dan balasan bisa di-review manual dulu sebelum tayang. Kamu yang pegang kendali penuh.</p>
            </details>
          </div>
        </div>
      </section>

      <!-- FINAL CTA -->
      <section class="py-24 text-center border-t border-[var(--border)]">
        <div class="max-w-[800px] mx-auto px-6">
          <h2 class="font-display text-[40px] md:text-[56px] leading-[1.0] mb-8">Siap berhenti nebak-nebak?</h2>
          <a href="https://app.ixiera.id/login" class="btn-bd-primary inline-block">Minta Akses</a>
        </div>
      </section>

      <!-- FOOTER -->
      <footer class="border-t border-[var(--border)] py-8">
        <div class="max-w-[1000px] mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-5 text-[13px] text-[var(--text-muted)]">
          <div class="flex items-center gap-2">
            <div class="w-6 h-6 flex items-center justify-center rounded text-[10px] font-bold bg-[var(--accent)] text-[var(--accent-text)]">IX</div>
            <span>2026 Ixiera.</span>
          </div>
          <div class="flex gap-5 flex-wrap justify-center">
            <a href="mailto:contact@ixiera.id" class="hover:text-[var(--text-primary)] transition">Email</a>
            <a href="/privacy" class="hover:text-[var(--text-primary)] transition">Kebijakan Privasi</a>
            <a href="/terms" class="hover:text-[var(--text-primary)] transition">Syarat & Ketentuan</a>
          </div>
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
