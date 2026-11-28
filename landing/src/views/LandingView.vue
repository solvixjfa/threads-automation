<template>
  <div class="min-h-screen font-sans selection:bg-[var(--text)] selection:text-[var(--bg)] bg-[var(--bg)] text-[var(--text)] overflow-x-hidden">
    <!-- NAVBAR -->
    <AppNavbar />

    <main class="pt-24 md:pt-32">
      <!-- HERO -->
      <section class="max-w-[1120px] mx-auto px-6 pb-20 md:pb-28 flex flex-col md:flex-row items-center gap-12">
        <div class="flex-1 space-y-6 text-center md:text-left fade-in">
          <div class="inline-flex items-center px-3 py-1 rounded-full border border-[var(--line)] text-xs font-bold tracking-widest text-[var(--muted)] uppercase">
            {{ $t('landing.hero.badge') }}
          </div>

          <h1 class="font-display text-5xl md:text-7xl leading-[1.05]">
            {{ locale === 'id' ? 'Ubah akun Threads' : 'Turn your Threads' }} <br class="hidden md:block"/>
            <span class="italic text-[var(--text)]">
              {{ locale === 'id' ? 'jadi mesin closing.' : 'into a growth engine.' }}
            </span>
          </h1>

          <p class="text-lg text-[var(--muted)] leading-relaxed max-w-xl mx-auto md:mx-0">
            {{ locale === 'id'
              ? 'Cari topik yang lagi ramai, bikin rencana konten 3 hari sesuai gaya bahasamu, posting sekalian ke Instagram, sampai balas ratusan komentar & mention otomatis.'
              : 'Spot trending topics, build 3-day content plans in your own voice, cross-post to Instagram, and reply to comments & mentions automatically.' }}
          </p>

          <div class="flex flex-col sm:flex-row items-center justify-center md:justify-start gap-4 pt-3">
            <a href="https://app.ixiera.online/login" class="w-full sm:w-auto px-8 py-3.5 rounded-full text-base font-bold bg-[var(--text)] text-[var(--bg)] hover:opacity-90 transition">
              {{ locale === 'id' ? 'Mulai Trial Gratis 7 Hari' : 'Start 7-Day Free Trial' }}
            </a>
            <a href="#contoh" class="w-full sm:w-auto px-8 py-3.5 rounded-full text-base font-bold border border-[var(--line)] hover:bg-[var(--surface-2)] transition">
              {{ locale === 'id' ? 'Lihat Cara Kerja' : 'See How It Works' }}
            </a>
          </div>

          <p class="text-xs text-[var(--muted)] pt-1">
            {{ locale === 'id'
              ? 'Gratis 7 hari + 15.000 Token AI • Tanpa kartu kredit • Langsung aktif'
              : 'Free 7-day trial + 15,000 AI Tokens • No credit card • Instant access' }}
          </p>

          <div class="flex flex-col sm:flex-row gap-4 pt-6 text-xs text-[var(--muted)] justify-center md:justify-start">
            <span class="flex items-center gap-2">
              <svg class="w-4 h-4 text-[var(--text)]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
              {{ $t('landing.hero.trust_1') }}
            </span>
            <span class="flex items-center gap-2">
              <svg class="w-4 h-4 text-[var(--text)]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
              {{ $t('landing.hero.trust_2') }}
            </span>
            <span class="flex items-center gap-2">
              <svg class="w-4 h-4 text-[var(--text)]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
              {{ $t('landing.hero.trust_3') }}
            </span>
          </div>
        </div>

        <!-- MOCKUP HERO: DASHBOARD (PIXEL PERFECT) -->
        <div class="flex-1 w-full max-w-md mx-auto fade-in">
          <div class="border border-[#222] rounded-2xl overflow-hidden bg-[#050607] shadow-2xl">
            <div class="flex items-center gap-1.5 px-4 py-3 border-b border-[#1a1a1a] bg-[#0a0a0a]">
              <div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div>
              <div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div>
              <div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div>
              <div class="ml-auto text-[10px] font-mono text-[#666]">app.ixiera.online/dashboard</div>
            </div>
            <div class="p-5 space-y-4">
              <div class="grid grid-cols-2 gap-3">
                <div class="bg-[#000] border border-[#1a1a1a] rounded-xl p-3">
                  <p class="text-[10px] text-[#666] mb-1">TOTAL VIEWS</p>
                  <p class="text-xl font-bold text-white tracking-tight">324.158</p>
                </div>
                <div class="bg-[#000] border border-[#1a1a1a] rounded-xl p-3">
                  <p class="text-[10px] text-[#666] mb-1">AVG ENGAGEMENT</p>
                  <p class="text-xl font-bold text-white tracking-tight">3.42%</p>
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
                    <linearGradient id="chartGradientHero" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.2" />
                      <stop offset="100%" stop-color="#ffffff" stop-opacity="0" />
                    </linearGradient>
                  </defs>
                  <path d="M0,60 Q50,55 80,45 T160,35 T240,20 T320,15 L400,10 L400,80 L0,80 Z" fill="url(#chartGradientHero)" />
                  <path d="M0,60 Q50,55 80,45 T160,35 T240,20 T320,15 L400,10" stroke="#ffffff" stroke-width="1.5" fill="none" />
                </svg>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- SPONSOR-STYLE MOVING MARQUEE: GEMINI & GROQ -->
      <section class="border-y border-[var(--line)] bg-[var(--surface)] py-7 overflow-hidden">
        <div class="max-w-[1120px] mx-auto px-6 mb-4 text-center">
          <p class="text-[11px] font-bold uppercase tracking-[0.2em] text-[var(--muted)]">
            {{ locale === 'id' ? 'Ditenagai Teknologi AI Terbaik' : 'Powered by Leading AI Models' }}
          </p>
        </div>

        <div class="ix-marquee-wrap select-none">
          <div class="ix-marquee-track">
            <!-- Group A -->
            <div class="ix-marquee-group">
              <div class="flex items-center gap-3">
                <svg class="w-6 h-6 shrink-0" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                  <defs>
                    <linearGradient id="geminiColorA" x1="2" y1="2" x2="22" y2="22" gradientUnits="userSpaceOnUse">
                      <stop offset="0%" stop-color="#4285F4"/>
                      <stop offset="45%" stop-color="#9B72CB"/>
                      <stop offset="80%" stop-color="#D96570"/>
                      <stop offset="100%" stop-color="#F49C46"/>
                    </linearGradient>
                  </defs>
                  <path d="M12 2C12.35 7.25 16.75 11.65 22 12C16.75 12.35 12.35 16.75 12 22C11.65 16.75 7.25 12.35 2 12C7.25 11.65 11.65 7.25 12 2Z" fill="url(#geminiColorA)"/>
                </svg>
                <span class="text-base font-bold tracking-tight text-[var(--text)]">Google Gemini</span>
                <span class="text-xs text-[var(--muted)]">• {{ locale === 'id' ? 'Ide & Rencana Konten' : 'Content & Idea Planning' }}</span>
              </div>

              <div class="flex items-center gap-3">
                <span class="w-6 h-6 rounded-md bg-[#F55036] text-white inline-flex items-center justify-center shrink-0">
                  <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                    <path d="M13 2L4 14h7l-1 8 10-12h-7l0-8z"/>
                  </svg>
                </span>
                <span class="text-base font-bold tracking-tight text-[var(--text)]">Groq</span>
                <span class="text-xs text-[var(--muted)]">• {{ locale === 'id' ? 'Balas Komentar Kilat' : 'Instant Comment Replies' }}</span>
              </div>

              <div class="flex items-center gap-3">
                <svg class="w-6 h-6 shrink-0" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                  <path d="M12 2C12.35 7.25 16.75 11.65 22 12C16.75 12.35 12.35 16.75 12 22C11.65 16.75 7.25 12.35 2 12C7.25 11.65 11.65 7.25 12 2Z" fill="url(#geminiColorA)"/>
                </svg>
                <span class="text-base font-bold tracking-tight text-[var(--text)]">Google Gemini</span>
                <span class="text-xs text-[var(--muted)]">• {{ locale === 'id' ? 'Belajar Gaya Bahasamu' : 'Learns Your Writing Style' }}</span>
              </div>

              <div class="flex items-center gap-3">
                <span class="w-6 h-6 rounded-md bg-[#F55036] text-white inline-flex items-center justify-center shrink-0">
                  <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                    <path d="M13 2L4 14h7l-1 8 10-12h-7l0-8z"/>
                  </svg>
                </span>
                <span class="text-base font-bold tracking-tight text-[var(--text)]">Groq</span>
                <span class="text-xs text-[var(--muted)]">• {{ locale === 'id' ? 'Respon Otomatis 24/7' : '24/7 Auto Responses' }}</span>
              </div>
            </div>

            <!-- Group B (Exact clone for seamless loop) -->
            <div class="ix-marquee-group" aria-hidden="true">
              <div class="flex items-center gap-3">
                <svg class="w-6 h-6 shrink-0" viewBox="0 0 24 24" fill="none">
                  <path d="M12 2C12.35 7.25 16.75 11.65 22 12C16.75 12.35 12.35 16.75 12 22C11.65 16.75 7.25 12.35 2 12C7.25 11.65 11.65 7.25 12 2Z" fill="url(#geminiColorA)"/>
                </svg>
                <span class="text-base font-bold tracking-tight text-[var(--text)]">Google Gemini</span>
                <span class="text-xs text-[var(--muted)]">• {{ locale === 'id' ? 'Ide & Rencana Konten' : 'Content & Idea Planning' }}</span>
              </div>

              <div class="flex items-center gap-3">
                <span class="w-6 h-6 rounded-md bg-[#F55036] text-white inline-flex items-center justify-center shrink-0">
                  <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M13 2L4 14h7l-1 8 10-12h-7l0-8z"/>
                  </svg>
                </span>
                <span class="text-base font-bold tracking-tight text-[var(--text)]">Groq</span>
                <span class="text-xs text-[var(--muted)]">• {{ locale === 'id' ? 'Balas Komentar Kilat' : 'Instant Comment Replies' }}</span>
              </div>

              <div class="flex items-center gap-3">
                <svg class="w-6 h-6 shrink-0" viewBox="0 0 24 24" fill="none">
                  <path d="M12 2C12.35 7.25 16.75 11.65 22 12C16.75 12.35 12.35 16.75 12 22C11.65 16.75 7.25 12.35 2 12C7.25 11.65 11.65 7.25 12 2Z" fill="url(#geminiColorA)"/>
                </svg>
                <span class="text-base font-bold tracking-tight text-[var(--text)]">Google Gemini</span>
                <span class="text-xs text-[var(--muted)]">• {{ locale === 'id' ? 'Belajar Gaya Bahasamu' : 'Learns Your Writing Style' }}</span>
              </div>

              <div class="flex items-center gap-3">
                <span class="w-6 h-6 rounded-md bg-[#F55036] text-white inline-flex items-center justify-center shrink-0">
                  <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M13 2L4 14h7l-1 8 10-12h-7l0-8z"/>
                  </svg>
                </span>
                <span class="text-base font-bold tracking-tight text-[var(--text)]">Groq</span>
                <span class="text-xs text-[var(--muted)]">• {{ locale === 'id' ? 'Respon Otomatis 24/7' : '24/7 Auto Responses' }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>
      <!-- FITUR UTAMA -->
      <section id="contoh" class="scroll-mt-16 py-20 md:py-32">
        <span id="fitur"></span>
        <div class="max-w-[1120px] mx-auto px-6">
          <div class="text-center mb-20 fade-in">
            <h2 class="font-display text-4xl md:text-5xl">
              {{ locale === 'id' ? 'Bukan sekadar scheduler biasa.' : 'Far more than a basic scheduler.' }}
            </h2>
            <p class="text-lg text-[var(--muted)] mt-4 max-w-2xl mx-auto">
              {{ locale === 'id'
                ? 'Riset topik yang lagi ramai, tulis draf pakai gayamu sendiri, tayang sekalian ke Instagram, sampai balas komentar & mention dari satu layar.'
                : 'Spot trending topics, draft in your own voice, cross-post to Instagram, and reply to comments & mentions in one flow.' }}
            </p>
          </div>

          <div class="space-y-32">
            <!-- Fitur 1: Composer + Location Tagging + Cross-Post IG -->
            <div class="flex flex-col md:flex-row items-center gap-12">
              <div class="flex-1 space-y-4 fade-in">
                <span class="text-xs font-bold uppercase tracking-widest text-[var(--muted)]">01 · AI Composer & Instagram</span>
                <h3 class="font-display text-3xl md:text-4xl">
                  {{ locale === 'id'
                    ? 'Dari satu ide jadi rencana 3 hari, tayang di Threads & Instagram.'
                    : 'Turn one topic into a 3-day plan, live on Threads & Instagram.' }}
                </h3>
                <p class="text-[var(--muted)] leading-relaxed">
                  {{ locale === 'id'
                    ? 'Gemini menyusun rencana konten 3 hari sesuai karakter tulisanmu. Cek Quick Score gratis sebelum tayang, tambah tag lokasi, dan aktifkan Share to Instagram biar sekali tulis langsung tayang di dua platform.'
                    : 'Gemini drafts a 3-day plan matched to your voice. Check free Quick Score, add location tags, and toggle Share to Instagram to publish on both platforms at once.' }}
                </p>
                <div class="flex flex-wrap gap-2 pt-2">
                  <span class="text-xs font-mono px-2.5 py-1 rounded border border-[var(--line)] bg-[var(--surface)]">3-Day AI Planner</span>
                  <span class="text-xs font-mono px-2.5 py-1 rounded border border-[var(--line)] bg-[var(--surface)]">Location Tagging</span>
                  <span class="text-xs font-mono px-2.5 py-1 rounded border border-[var(--line)] bg-[var(--surface)]">Share to Instagram</span>
                </div>
              </div>

              <div class="flex-1 w-full">
                <div class="border border-[#222] rounded-xl overflow-hidden bg-[#050607] shadow-2xl">
                  <div class="flex items-center gap-1.5 px-4 py-3 border-b border-[#1a1a1a] bg-[#0a0a0a]">
                    <div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div><div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div><div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div>
                    <span class="ml-2 text-[10px] text-[#666] font-mono">app.ixiera.online/content/create</span>
                  </div>
                  <div class="p-5">
                    <div class="border border-[#222] rounded-xl p-4 bg-[#0a0a0a] mb-4">
                      <div class="text-[10px] font-bold text-white mb-3 flex items-center justify-between">
                        <span class="flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-white"></span> AI CONTENT PLANNER</span>
                        <span class="text-[9px] font-mono text-[#888]">GEMINI</span>
                      </div>
                      <div class="grid grid-cols-2 gap-3 mb-3">
                        <div>
                          <label class="text-[9px] text-[#666] block mb-1">Topik / Ide Singkat</label>
                          <div class="w-full bg-[#000] border border-[#222] rounded-md px-2 py-1.5 text-[10px] text-white">Strategi jualan organik</div>
                        </div>
                        <div>
                          <label class="text-[9px] text-[#666] block mb-1">Tag Lokasi</label>
                          <div class="w-full bg-[#000] border border-[#222] rounded-md px-2 py-1.5 text-[10px] text-white flex justify-between items-center">
                            <span>Jakarta, Indonesia</span>
                            <span class="text-[8px] text-[#888]">LOKASI</span>
                          </div>
                        </div>
                      </div>
                      <div class="flex items-center justify-between pt-2 border-t border-[#1a1a1a]">
                        <span class="text-[10px] text-[#999] flex items-center gap-1.5">
                          <span class="w-6 h-3.5 rounded-full bg-white inline-flex items-center justify-end p-0.5"><span class="w-2.5 h-2.5 rounded-full bg-black"></span></span>
                          Share to Instagram
                        </span>
                        <button class="bg-white text-black text-[10px] font-bold px-3 py-1.5 rounded-md">Bikin Rencana 3 Hari</button>
                      </div>
                    </div>

                    <div class="border border-[#222] rounded-xl p-4 bg-[#0a0a0a]">
                      <div class="text-[10px] font-bold text-white mb-2 flex justify-between">
                        <span>TEKS POSTINGAN UTAMA</span>
                        <span class="text-[#666] font-normal">312 / 500 Karakter</span>
                      </div>
                      <div class="w-full bg-[#000] border border-[#222] rounded-md p-2.5 text-[10px] text-[#ccc] leading-relaxed mb-3">
                        3 kesalahan yang bikin akun Threads sepi interaksi padahal posting tiap hari...
                      </div>
                      <div class="flex justify-between items-center pt-2 border-t border-[#222]">
                        <span class="bg-[#1a1a1a] text-[9px] text-[#aaa] px-2 py-1 rounded">Quick Score: 92/100</span>
                        <button class="bg-white text-black text-[10px] font-bold px-3 py-1.5 rounded-md">Jadwalkan</button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Fitur 2: Smart Inbox (Comments + Public Mentions) -->
            <div class="flex flex-col md:flex-row-reverse items-center gap-12">
              <div class="flex-1 space-y-4 fade-in">
                <span class="text-xs font-bold uppercase tracking-widest text-[var(--muted)]">02 · Smart Inbox & Mentions</span>
                <h3 class="font-display text-3xl md:text-4xl">
                  {{ locale === 'id'
                    ? 'Komentar & @mentions terjawab cepat sebelum momentum hilang.'
                    : 'Comments & @mentions answered before momentum fades.' }}
                </h3>
                <p class="text-[var(--muted)] leading-relaxed">
                  {{ locale === 'id'
                    ? 'Semua komentar post dan mention publik masuk ke satu inbox rapi. AI langsung memilah pertanyaan calon pembeli, pujian, hingga spam—kamu tinggal klik kirim atau aktifkan balas otomatis dengan batas aman per jam.'
                    : 'All post comments and public mentions land in one clean inbox. AI sorts buyer questions, praise, and spam—approve in one click or turn on auto-reply with safe hourly caps.' }}
                </p>
                <div class="flex flex-wrap gap-2 pt-2">
                  <span class="text-xs font-mono px-2.5 py-1 rounded border border-[var(--line)] bg-[var(--surface)]">Filter Komentar Otomatis</span>
                  <span class="text-xs font-mono px-2.5 py-1 rounded border border-[var(--line)] bg-[var(--surface)]">Tab Public Mentions</span>
                  <span class="text-xs font-mono px-2.5 py-1 rounded border border-[var(--line)] bg-[var(--surface)]">Kill Switch Aman</span>
                </div>
              </div>

              <div class="flex-1 w-full">
                <div class="border border-[#222] rounded-xl overflow-hidden bg-[#050607] shadow-2xl">
                  <div class="flex items-center gap-1.5 px-4 py-3 border-b border-[#1a1a1a] bg-[#0a0a0a]">
                    <div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div><div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div><div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div>
                    <span class="ml-2 text-[10px] text-[#666] font-mono">app.ixiera.online/inbox</span>
                  </div>
                  <div class="p-5">
                    <div class="flex gap-4 border-b border-[#222] pb-2 mb-4 text-[10px] font-bold">
                      <span class="text-white border-b-2 border-white pb-2 -mb-[10px]">Comments (4)</span>
                      <span class="text-[#aaa]">Mentions (2)</span>
                      <span class="text-[#666]">Priority (1)</span>
                      <span class="text-[#666]">History (48)</span>
                    </div>

                    <div class="border border-[#222] rounded-xl p-4 bg-[#0a0a0a]">
                      <div class="flex items-center justify-between mb-3">
                        <div class="flex items-center gap-2">
                          <div class="w-5 h-5 rounded-full bg-[#222]"></div>
                          <span class="text-[10px] font-bold text-white">@founder_lokal</span>
                        </div>
                        <span class="text-[9px] font-mono font-bold text-white bg-[#1a1a1a] px-2 py-0.5 rounded border border-[#333]">PERTANYAAN • GROQ</span>
                      </div>

                      <div class="bg-[#000] border border-[#222] rounded-lg p-2.5 text-[10px] text-white mb-3">
                        Ini bisa dipakai buat jadwalin utasan panjang sekaligus cross-post IG?
                      </div>

                      <div class="border border-[#222] rounded-lg bg-[#000] p-3">
                        <div class="flex justify-between items-center mb-2">
                          <span class="text-[9px] font-bold text-[#666]">DRAF BALASAN • SESUAI GAYA KAMU</span>
                          <span class="text-[9px] font-mono text-[#888]">INSTAN</span>
                        </div>
                        <div class="text-[10px] text-[#ccc] bg-[#111] border border-[#222] rounded p-2 mb-3">
                          Bisa banget! Tinggal pecah utasan di Composer dan aktifkan toggle Share to Instagram. Bisa coba gratis 7 hari di ixiera.online.
                        </div>
                        <div class="flex justify-end gap-2">
                          <button class="text-[9px] font-bold text-[#666] px-2 py-1">Abaikan</button>
                          <button class="bg-white text-black text-[9px] font-bold px-3 py-1.5 rounded-md">Kirim ke Threads</button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Fitur 3: Trending Topics Radar, Keyword Search & Analytics -->
            <div class="flex flex-col md:flex-row items-center gap-12">
              <div class="flex-1 space-y-4 fade-in">
                <span class="text-xs font-bold uppercase tracking-widest text-[var(--muted)]">03 · Trending & Analytics</span>
                <h3 class="font-display text-3xl md:text-4xl">
                  {{ locale === 'id'
                    ? 'Ikuti topik yang lagi naik & baca performa pakai data nyata.'
                    : 'Ride live trending topics & measure what converts with real data.' }}
                </h3>
                <p class="text-[var(--muted)] leading-relaxed">
                  {{ locale === 'id'
                    ? 'Pantau daftar topik yang lagi ramai di Threads, cari postingan lewat kata kunci, intip profil kreator di niche kamu, dan temukan jam terbaik untuk posting dari data akunmu sendiri.'
                    : 'Track live trending topics on Threads, search posts by keyword, inspect creator profiles in your niche, and find your best posting hours from your own account data.' }}
                </p>
                <div class="flex flex-wrap gap-2 pt-2">
                  <span class="text-xs font-mono px-2.5 py-1 rounded border border-[var(--line)] bg-[var(--surface)]">Trending Topics</span>
                  <span class="text-xs font-mono px-2.5 py-1 rounded border border-[var(--line)] bg-[var(--surface)]">Profile Discovery</span>
                  <span class="text-xs font-mono px-2.5 py-1 rounded border border-[var(--line)] bg-[var(--surface)]">Best Time Heatmap</span>
                </div>
              </div>

              <div class="flex-1 w-full">
                <div class="border border-[#222] rounded-xl overflow-hidden bg-[#050607] shadow-2xl">
                  <div class="flex items-center gap-1.5 px-4 py-3 border-b border-[#1a1a1a] bg-[#0a0a0a]">
                    <div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div><div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div><div class="w-2.5 h-2.5 rounded-full bg-[#333]"></div>
                    <span class="ml-2 text-[10px] text-[#666] font-mono">app.ixiera.online/content/trending</span>
                  </div>
                  <div class="p-5 space-y-4">
                    <div class="border border-[#222] rounded-xl p-4 bg-[#0a0a0a]">
                      <div class="text-[9px] text-[#888] font-mono uppercase tracking-wider mb-2">TRENDING TOPICS HARI INI</div>
                      <div class="flex flex-wrap gap-1.5">
                        <span class="text-[10px] font-bold bg-white text-black px-2.5 py-1 rounded-full">#SaaSIndonesia</span>
                        <span class="text-[10px] bg-[#141414] text-[#ccc] border border-[#222] px-2.5 py-1 rounded-full">#CreatorEconomy</span>
                        <span class="text-[10px] bg-[#141414] text-[#ccc] border border-[#222] px-2.5 py-1 rounded-full">#AIWorkflow</span>
                        <span class="text-[10px] bg-[#141414] text-[#ccc] border border-[#222] px-2.5 py-1 rounded-full">#DigitalMarketing</span>
                      </div>
                    </div>

                    <div class="border border-[#222] rounded-xl p-4 bg-[#0a0a0a]">
                      <div class="flex justify-between items-center mb-2">
                        <span class="text-[10px] font-bold text-white">Waktu Terbaik Posting (WIB)</span>
                        <span class="text-[9px] font-mono text-[#888]">3.20% AVG ER</span>
                      </div>
                      <div class="text-sm font-bold text-white mb-3">Selasa & Kamis, 08:00–12:00 WIB</div>
                      <div class="space-y-2">
                        <div class="flex items-center justify-between bg-[#111] p-2 rounded border border-[#222]">
                          <span class="text-[10px] text-white">Hook Pertanyaan (2.92% ER)</span>
                          <span class="text-[9px] font-mono text-white bg-[#222] px-2 py-0.5 rounded">2.1x Lebih Tinggi</span>
                        </div>
                        <div class="flex items-center justify-between bg-[#111] p-2 rounded border border-[#222]">
                          <span class="text-[10px] text-white">Panjang 300–500 Karakter (2.96% ER)</span>
                          <span class="text-[9px] font-mono text-white bg-[#222] px-2 py-0.5 rounded">Optimal</span>
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

      <!-- PRICING SECTION -->
      <section id="pricing" class="py-20 md:py-32 border-t border-[var(--line)] bg-[var(--surface)]">
        <div class="max-w-[1160px] mx-auto px-6">
          <div class="text-center mb-14 fade-in">
            <span class="text-xs font-mono font-bold uppercase tracking-widest text-[var(--muted)]">
              {{ locale === 'id' ? 'HARGA TRANSPARAN • TANPA AUTO-RENEW' : 'TRANSPARENT PRICING • NO AUTO-RENEW' }}
            </span>
            <h2 class="font-display text-4xl md:text-5xl mt-2">
              {{ locale === 'id' ? 'Mulai gratis, upgrade kapan siap.' : 'Start free, upgrade when ready.' }}
            </h2>
            <p class="text-base text-[var(--muted)] mt-3 max-w-xl mx-auto">
              {{ locale === 'id'
                ? 'Coba semua fitur selama 7 hari tanpa kartu kredit. Setelah itu pilih paket 30 hari sekali bayar tanpa langganan otomatis.'
                : 'Try every feature for 7 days with no credit card. Afterward, pick a one-time 30-day pass with zero auto-renewal.' }}
            </p>
          </div>

          <!-- Free Trial Banner -->
          <div class="border border-[var(--line)] rounded-2xl p-6 bg-[var(--bg)] mb-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
            <div>
              <div class="flex items-center gap-2.5 mb-1">
                <span class="text-xs font-mono font-bold uppercase tracking-wider px-2.5 py-0.5 rounded bg-[var(--surface-2)] text-[var(--text)]">7-Day Free Trial</span>
                <span class="text-lg font-bold">Rp 0</span>
              </div>
              <p class="text-sm text-[var(--muted)]">
                {{ locale === 'id'
                  ? '15.000 Token AI (Gemini & Groq) • 1 Akun Threads • Akses penuh Composer, Inbox & Analytics tanpa kartu kredit.'
                  : '15,000 AI Tokens (Gemini & Groq) • 1 Threads Account • Full access to Composer, Inbox & Analytics with no credit card.' }}
              </p>
            </div>
            <a href="https://app.ixiera.online/login" class="w-full md:w-auto shrink-0 text-center px-6 py-3 rounded-full text-sm font-bold border border-[var(--line)] hover:bg-[var(--surface-2)] transition">
              {{ locale === 'id' ? 'Mulai Trial Gratis' : 'Start Free Trial' }}
            </a>
          </div>

          <!-- 4 Paid Tiers -->
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
            <!-- Starter -->
            <div class="border border-[var(--line)] rounded-2xl p-7 bg-[var(--bg)] flex flex-col">
              <div class="text-xs font-mono uppercase text-[var(--muted)] mb-1">{{ locale === 'id' ? 'Starter (30 Hari)' : 'Starter (30 Days)' }}</div>
              <div class="text-3xl font-bold mb-2">Rp 59.000<span class="text-xs font-normal text-[var(--muted)]"> / {{ locale === 'id' ? '30 hari' : '30 days' }}</span></div>
              <p class="text-xs text-[var(--muted)] mb-5">
                {{ locale === 'id' ? 'Untuk kreator solo & personal branding rutin.' : 'For solo creators & consistent personal branding.' }}
              </p>
              <ul class="space-y-2.5 text-sm text-[var(--muted)] mb-7 border-t border-[var(--line)] pt-5">
                <li>✓ <strong class="text-[var(--text)]">{{ locale === 'id' ? '100.000 Token AI' : '100,000 AI Tokens' }}</strong> {{ locale === 'id' ? '/ bulan' : '/ month' }}</li>
                <li>✓ <strong class="text-[var(--text)]">{{ locale === 'id' ? 'Maksimal 2 Akun' : 'Up to 2' }}</strong> {{ locale === 'id' ? 'Threads' : 'Threads Accounts' }}</li>
                <li>✓ AI Planner, Repurpose & Auto Reply</li>
                <li>✓ Location Tag & IG Cross-Post</li>
              </ul>
              <a href="https://app.ixiera.online/login" class="mt-auto block text-center py-3 rounded-full text-sm font-bold border border-[var(--line)] hover:bg-[var(--surface-2)] transition">
                {{ locale === 'id' ? 'Pilih Starter' : 'Choose Starter' }}
              </a>
            </div>

            <!-- Pro -->
            <div class="border-2 border-[var(--text)] rounded-2xl p-7 bg-[var(--bg)] relative shadow-xl flex flex-col">
              <div class="absolute -top-3 left-1/2 -translate-x-1/2 bg-[var(--text)] text-[var(--bg)] text-[10px] font-bold px-3 py-1 rounded-full uppercase">
                {{ locale === 'id' ? 'Paling Laris' : 'Most Popular' }}
              </div>
              <div class="text-xs font-mono uppercase text-[var(--muted)] mb-1">{{ locale === 'id' ? 'Pro (30 Hari)' : 'Pro (30 Days)' }}</div>
              <div class="text-3xl font-bold mb-2">Rp 99.000<span class="text-xs font-normal text-[var(--muted)]"> / {{ locale === 'id' ? '30 hari' : '30 days' }}</span></div>
              <p class="text-xs text-[var(--muted)] mb-5">
                {{ locale === 'id' ? 'Kuota besar untuk kreator aktif & multi-akun.' : 'High token quota for active creators & multi-account.' }}
              </p>
              <ul class="space-y-2.5 text-sm text-[var(--muted)] mb-7 border-t border-[var(--line)] pt-5">
                <li>✓ <strong class="text-[var(--text)]">{{ locale === 'id' ? '300.000 Token AI' : '300,000 AI Tokens' }}</strong> {{ locale === 'id' ? '/ bulan' : '/ month' }}</li>
                <li>✓ <strong class="text-[var(--text)]">{{ locale === 'id' ? 'Maksimal 5 Akun' : 'Up to 5' }}</strong> {{ locale === 'id' ? 'Threads' : 'Threads Accounts' }}</li>
                <li>✓ Full Auto Reply + Knowledge Base</li>
                <li>✓ Trending Radar, Discovery & Analytics</li>
              </ul>
              <a href="https://app.ixiera.online/login" class="mt-auto block text-center py-3 rounded-full text-sm font-bold bg-[var(--text)] text-[var(--bg)] hover:opacity-90 transition">
                {{ locale === 'id' ? 'Pilih Pro' : 'Choose Pro' }}
              </a>
            </div>

            <!-- Business -->
            <div class="border border-[var(--line)] rounded-2xl p-7 bg-[var(--bg)] flex flex-col">
              <div class="text-xs font-mono uppercase text-[var(--muted)] mb-1">{{ locale === 'id' ? 'Business (30 Hari)' : 'Business (30 Days)' }}</div>
              <div class="text-3xl font-bold mb-2">Rp 179.000<span class="text-xs font-normal text-[var(--muted)]"> / {{ locale === 'id' ? '30 hari' : '30 days' }}</span></div>
              <p class="text-xs text-[var(--muted)] mb-5">
                {{ locale === 'id' ? 'Untuk tim bisnis, brand & social media manager.' : 'For business teams, brands & social managers.' }}
              </p>
              <ul class="space-y-2.5 text-sm text-[var(--muted)] mb-7 border-t border-[var(--line)] pt-5">
                <li>✓ <strong class="text-[var(--text)]">{{ locale === 'id' ? '750.000 Token AI' : '750,000 AI Tokens' }}</strong> {{ locale === 'id' ? '/ bulan' : '/ month' }}</li>
                <li>✓ <strong class="text-[var(--text)]">{{ locale === 'id' ? 'Maksimal 20 Akun' : 'Up to 20' }}</strong> {{ locale === 'id' ? 'Threads' : 'Threads Accounts' }}</li>
                <li>✓ {{ locale === 'id' ? 'Semua Fitur Otomatisasi Penuh' : 'All Full Automation Features' }}</li>
                <li>✓ Smart Inbox, Mentions & Knowledge Base</li>
              </ul>
              <a href="https://app.ixiera.online/login" class="mt-auto block text-center py-3 rounded-full text-sm font-bold border border-[var(--line)] hover:bg-[var(--surface-2)] transition">
                {{ locale === 'id' ? 'Pilih Business' : 'Choose Business' }}
              </a>
            </div>

            <!-- Agency BYOK -->
            <div class="border border-[var(--line)] rounded-2xl p-7 bg-[var(--bg)] flex flex-col">
              <div class="text-xs font-mono uppercase text-[var(--muted)] mb-1">{{ locale === 'id' ? 'Agency BYOK (30 Hari)' : 'Agency BYOK (30 Days)' }}</div>
              <div class="text-3xl font-bold mb-2">Rp 249.000<span class="text-xs font-normal text-[var(--muted)]"> / {{ locale === 'id' ? '30 hari' : '30 days' }}</span></div>
              <p class="text-xs text-[var(--muted)] mb-5">
                {{ locale === 'id' ? 'Pakai API key Gemini / Groq milikmu sendiri.' : 'Use your own Gemini / Groq API keys.' }}
              </p>
              <ul class="space-y-2.5 text-sm text-[var(--muted)] mb-7 border-t border-[var(--line)] pt-5">
                <li>✓ <strong class="text-[var(--text)]">{{ locale === 'id' ? 'Unlimited Token' : 'Unlimited Tokens' }}</strong> ({{ locale === 'id' ? 'API Key Sendiri' : 'Own API Keys' }})</li>
                <li>✓ <strong class="text-[var(--text)]">{{ locale === 'id' ? 'Maksimal 50 Akun' : 'Up to 50' }}</strong> {{ locale === 'id' ? 'Threads' : 'Threads Accounts' }}</li>
                <li>✓ {{ locale === 'id' ? 'Tanpa Batas Pemakaian AI' : 'No AI Usage Limits' }}</li>
                <li>✓ {{ locale === 'id' ? 'Cocok untuk Agensi & High-Volume' : 'Ideal for Agencies & High-Volume' }}</li>
              </ul>
              <a href="https://app.ixiera.online/login" class="mt-auto block text-center py-3 rounded-full text-sm font-bold border border-[var(--line)] hover:bg-[var(--surface-2)] transition">
                {{ locale === 'id' ? 'Pilih Agency BYOK' : 'Choose Agency BYOK' }}
              </a>
            </div>
          </div>

          <div class="text-center mt-8">
            <RouterLink to="/pricing" class="text-xs font-bold underline underline-offset-4 text-[var(--muted)] hover:text-[var(--text)] transition">
              {{ locale === 'id' ? 'Lihat tabel perbandingan fitur lengkap & aturan token →' : 'View full feature comparison table & token rules →' }}
            </RouterLink>
          </div>
        </div>
      </section>

      <!-- BLOG & FREE RESOURCES SECTION -->
      <section id="resources" class="py-20 md:py-32 border-t border-[var(--line)] bg-[var(--bg)]">
        <div class="max-w-[1120px] mx-auto px-6">
          <div class="flex flex-col md:flex-row md:items-end justify-between mb-12 gap-4 fade-in">
            <div>
              <span class="text-xs font-mono font-bold uppercase tracking-widest text-[var(--muted)]">
                PLAYBOOK & FREE RESOURCES
              </span>
              <h2 class="font-display text-4xl md:text-5xl mt-2">
                {{ locale === 'id' ? 'Panduan & template siap pakai.' : 'Guides & ready-to-use templates.' }}
              </h2>
            </div>
            <RouterLink to="/blog" class="text-sm font-bold underline underline-offset-4 hover:opacity-80 transition">
              {{ locale === 'id' ? 'Lihat Semua Artikel & Resource →' : 'Browse All Articles & Resources →' }}
            </RouterLink>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <RouterLink
              v-for="post in featuredPosts"
              :key="post.slug"
              :to="`/blog/${post.slug}`"
              class="border rounded-2xl p-6 bg-[var(--surface)] hover:border-[var(--text)] transition flex flex-col justify-between group"
              :class="post.isResource ? 'border-[var(--text)]' : 'border-[var(--line)]'"
            >
              <div>
                <div class="flex items-center justify-between text-xs mb-4">
                  <span
                    class="font-mono font-bold uppercase px-2 py-0.5 rounded"
                    :class="post.isResource ? 'bg-[var(--text)] text-[var(--bg)]' : 'bg-[var(--surface-2)] text-[var(--muted)]'"
                  >
                    {{ locale === 'id' ? post.category.id : post.category.en }}
                  </span>
                  <span class="text-[var(--muted)]">{{ locale === 'id' ? post.readTime.id : post.readTime.en }}</span>
                </div>
                <h3 class="text-lg font-bold leading-snug mb-2 group-hover:underline underline-offset-4">
                  {{ locale === 'id' ? post.title.id : post.title.en }}
                </h3>
                <p class="text-sm text-[var(--muted)] leading-relaxed">
                  {{ locale === 'id' ? post.excerpt.id : post.excerpt.en }}
                </p>
              </div>
              <div class="mt-6 pt-4 border-t border-[var(--line)] text-xs font-bold flex items-center justify-between">
                <span>{{ post.isResource ? (locale === 'id' ? 'Ambil Template Gratis' : 'Get Free Templates') : (locale === 'id' ? 'Baca Panduan' : 'Read Guide') }}</span>
                <span>&rarr;</span>
              </div>
            </RouterLink>
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
                <svg class="w-5 h-5 transition-transform duration-300 shrink-0 ml-4" :class="{'rotate-180': faqOpen === i}" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
              </button>
              <div v-if="faqOpen === i" class="px-6 pb-4 text-sm text-[var(--muted)] leading-relaxed">{{ $t('landing.faq.a' + i) }}</div>
            </div>
          </div>
        </div>
      </section>

      <!-- FINAL CTA -->
      <section class="py-20 md:py-28 border-t border-[var(--line)] bg-[var(--bg)] text-center px-6">
        <div class="max-w-2xl mx-auto space-y-6 fade-in">
          <h2 class="font-display text-4xl md:text-6xl">
            {{ locale === 'id' ? 'Siap bikin akun Threads ' : 'Ready to put your Threads ' }}
            <span class="italic">{{ locale === 'id' ? 'kerja otomatis?' : 'on autopilot?' }}</span>
          </h2>
          <p class="text-base text-[var(--muted)]">
            {{ locale === 'id'
              ? 'Daftar dalam 30 detik, hubungkan akun lewat login resmi Meta, dan klaim 15.000 Token AI gratis sekarang.'
              : 'Sign up in 30 seconds, connect via official Meta login, and claim 15,000 free AI Tokens today.' }}
          </p>
          <div class="pt-2">
            <a href="https://app.ixiera.online/login" class="inline-block px-10 py-4 rounded-full text-base font-bold bg-[var(--text)] text-[var(--bg)] hover:opacity-90 transition">
              {{ locale === 'id' ? 'Mulai Trial Gratis 7 Hari' : 'Start 7-Day Free Trial' }}
            </a>
          </div>
        </div>
      </section>
    </main>

    <!-- FOOTER -->
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useI18n } from 'vue-i18n'
import AppNavbar from '../components/layouts/AppNavbar.vue'
import AppFooter from '../components/layouts/AppFooter.vue'
import { blogPosts } from '../data/blogPosts'

const { locale } = useI18n({ useScope: 'global' })
const faqOpen = ref<number | null>(1)
const featuredPosts = computed(() => blogPosts.slice(0, 3))

onMounted(() => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible')
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

/* Sponsor-style smooth infinite marquee */
.ix-marquee-wrap {
  width: 100%;
  overflow: hidden;
  -webkit-mask-image: linear-gradient(to right, transparent, black 8%, black 92%, transparent);
  mask-image: linear-gradient(to right, transparent, black 8%, black 92%, transparent);
}
.ix-marquee-track {
  display: flex;
  width: max-content;
  will-change: transform;
  animation: ixMarqueeMove 24s linear infinite;
}
.ix-marquee-wrap:hover .ix-marquee-track {
  animation-play-state: paused;
}
.ix-marquee-group {
  display: flex;
  align-items: center;
  gap: 3rem;
  padding-right: 3rem;
  flex-shrink: 0;
}
@keyframes ixMarqueeMove {
  0% { transform: translate3d(0, 0, 0); }
  100% { transform: translate3d(-50%, 0, 0); }
}

@media (prefers-reduced-motion: reduce) {
  .fade-in {
    transition: none !important;
    animation: none !important;
    opacity: 1 !important;
    transform: none !important;
  }
}
</style>
