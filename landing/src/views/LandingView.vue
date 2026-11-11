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
          <a href="#fitur" class="hover:text-[var(--text-primary)] transition">{{ $t('nav.features') }}</a>
          <a href="#contoh" class="hover:text-[var(--text-primary)] transition">{{ $t('nav.data') }}</a>
          <a href="#cara-kerja" class="hover:text-[var(--text-primary)] transition">{{ $t('nav.how') }}</a>
          <a href="/pricing" class="hover:text-[var(--text-primary)] transition">{{ $t('nav.pricing') }}</a>
          <a href="#faq" class="hover:text-[var(--text-primary)] transition">{{ $t('nav.faq') }}</a>
        </div>
        <div class="hidden md:flex items-center gap-4">
          <button @click="toggleTheme" class="p-2 text-[var(--text-muted)] hover:text-[var(--text-primary)] transition">
            <Sun v-if="theme === 'dark'" class="w-4 h-4" />
            <Moon v-else class="w-4 h-4" />
          </button>
          <button @click="toggleLang" class="text-xs font-bold text-[var(--text-muted)] hover:text-[var(--text-primary)] transition px-2 py-1 rounded border border-[var(--border)]">
            {{ locale.toUpperCase() }}
          </button>
          <div class="w-px h-4 bg-[var(--border)] mx-1"></div>
          <a href="https://app.ixiera.id/login" class="text-sm font-medium text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition">{{ $t('nav.login') }}</a>
          <a href="https://app.ixiera.id/signup" class="btn-bd-primary" style="padding: 8px 16px;">{{ $t('nav.signup') }}</a>
        </div>
        <button @click="mobileMenuOpen = true" class="md:hidden p-2 text-[var(--text-primary)]">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
        </button>
      </div>
    </nav>

    <!-- MOBILE DRAWER -->
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
        <a href="#fitur" @click="mobileMenuOpen = false" class="hover:text-[var(--text-primary)] transition">{{ $t('nav.features') }}</a>
        <a href="#contoh" @click="mobileMenuOpen = false" class="hover:text-[var(--text-primary)] transition">{{ $t('nav.data') }}</a>
        <a href="#cara-kerja" @click="mobileMenuOpen = false" class="hover:text-[var(--text-primary)] transition">{{ $t('nav.how') }}</a>
        <a href="/pricing" @click="mobileMenuOpen = false" class="hover:text-[var(--text-primary)] transition">{{ $t('nav.pricing') }}</a>
        <a href="#faq" @click="mobileMenuOpen = false" class="hover:text-[var(--text-primary)] transition">{{ $t('nav.faq') }}</a>
      </nav>
      <div class="mt-auto pt-6 border-t border-[var(--border)] space-y-4">
        <div class="flex gap-2">
          <button @click="toggleTheme" class="flex-1 flex items-center justify-center py-2.5 rounded-md border border-[var(--border)] text-[var(--text-muted)]">
            <Sun v-if="theme === 'dark'" class="w-4 h-4" />
            <Moon v-else class="w-4 h-4" />
          </button>
          <button @click="toggleLang" class="flex-1 py-2.5 rounded-md border border-[var(--border)] text-[var(--text-muted)] text-xs font-bold">
            {{ locale.toUpperCase() }}
          </button>
        </div>
        <a href="https://app.ixiera.id/signup" class="btn-bd-primary w-full text-center block">{{ $t('nav.signup') }}</a>
        <a href="https://app.ixiera.id/login" class="text-center block text-sm text-[var(--text-secondary)] py-1">{{ $t('nav.login') }}</a>
      </div>
    </div>

    <main class="pt-16">
      <!-- HERO -->
      <section class="relative pt-24 pb-20">
        <div class="max-w-[1200px] mx-auto px-6 text-center relative z-10">
          <div class="pill-bd mb-6 mx-auto" style="width: fit-content;">
            <span class="w-1.5 h-1.5 rounded-full" style="background: var(--accent-mint);"></span>
            {{ $t('hero.badge') }}
          </div>
          <h1 class="font-display text-[48px] md:text-[64px] leading-[1.0] mb-6 max-w-[800px] mx-auto text-[var(--text-primary)]">
            {{ $t('hero.title1') }} <br class="hidden md:block">
            <span class="italic text-[var(--accent-violet)]">{{ $t('hero.title2') }}</span>
          </h1>
          <p class="text-[16px] md:text-[18px] leading-[1.56] max-w-[640px] mx-auto mb-10 text-[var(--text-secondary)]">
            {{ $t('hero.subtitle') }}
          </p>
          <div class="flex flex-col sm:flex-row items-center justify-center gap-3 mb-8">
            <a href="https://app.ixiera.id/signup" class="btn-bd-primary w-full sm:w-auto text-center">{{ $t('hero.cta1') }}</a>
            <a href="#contoh" class="btn-bd-ghost w-full sm:w-auto text-center">{{ $t('hero.cta2') }}</a>
          </div>
          <p class="text-[13px] text-[var(--text-muted)] mb-6">{{ $t('hero.trust1') }}</p>
          <div class="flex flex-wrap justify-center gap-x-5 gap-y-2 text-xs text-[var(--text-muted)]">
            <span>{{ $t('hero.trust2') }}</span>
            <span>{{ $t('hero.trust3') }}</span>
            <span>{{ $t('hero.trust4') }}</span>
          </div>
        </div>
        <!-- Hero Mockup -->
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
          <h2 class="h2-bd">{{ $t('problem.title') }}</h2>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-5 mt-10">
            <div class="card-bd p-7 feature-card">
              <span class="font-display text-[32px] block mb-3 text-[var(--accent-violet)]">01</span>
              <h3 class="text-[17px] font-semibold mb-2">{{ $t('problem.c1_title') }}</h3>
              <p class="text-[14px] leading-relaxed text-[var(--text-secondary)]">{{ $t('problem.c1_desc') }}</p>
            </div>
            <div class="card-bd p-7 feature-card">
              <span class="font-display text-[32px] block mb-3 text-[var(--accent-violet)]">02</span>
              <h3 class="text-[17px] font-semibold mb-2">{{ $t('problem.c2_title') }}</h3>
              <p class="text-[14px] leading-relaxed text-[var(--text-secondary)]">{{ $t('problem.c2_desc') }}</p>
            </div>
            <div class="card-bd p-7 feature-card">
              <span class="font-display text-[32px] block mb-3 text-[var(--accent-violet)]">03</span>
              <h3 class="text-[17px] font-semibold mb-2">{{ $t('problem.c3_title') }}</h3>
              <p class="text-[14px] leading-relaxed text-[var(--text-secondary)]">{{ $t('problem.c3_desc') }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- FITUR (MOCKUP DIPERBAIKI - BASEDASH STYLE) -->
      <section id="fitur" class="py-20 border-t border-[var(--border)]">
        <div class="max-w-[1000px] mx-auto px-6">
          <h2 class="h2-bd">{{ $t('features.title') }}</h2>
          <p class="text-center mb-16 text-[15px] text-[var(--text-secondary)]">{{ $t('features.subtitle') }}</p>
          
          <div class="space-y-20">
            <!-- Fitur 1 -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-10 items-center">
              <div>
                <span class="text-[12px] font-bold tracking-widest uppercase block mb-2 text-[var(--accent-violet)]">01 &middot; Content</span>
                <h3 class="font-display text-[28px] md:text-[32px] leading-tight mb-4">{{ $t('features.f1_title') }}</h3>
                <p class="text-[15px] leading-relaxed text-[var(--text-secondary)]">{{ $t('features.f1_desc') }}</p>
              </div>
              <!-- Mockup 1 -->
              <div class="card-bd p-6 bg-[#050607] border-[#222] relative overflow-hidden">
                <div class="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-[#9984d8] to-transparent"></div>
                <div class="text-[11px] font-bold uppercase tracking-widest mb-4 text-[#666]">AI Content Planner</div>
                <div class="space-y-3 mb-5">
                  <input type="text" placeholder="Topik / Short Idea" class="w-full px-4 py-3 rounded-lg border border-[#222] bg-[#000] text-sm text-white placeholder-gray-600 focus:outline-none focus:border-[#9984d8] transition">
                  <div class="relative">
                    <input type="text" placeholder="Tone / Style" class="w-full px-4 py-3 rounded-lg border border-[#222] bg-[#000] text-sm text-white placeholder-gray-600 focus:outline-none focus:border-[#9984d8] transition">
                    <span class="absolute right-4 top-1/2 -translate-y-1/2 text-xs text-gray-600 font-medium">Storytelling</span>
                  </div>
                </div>
                <button class="w-full bg-white text-black font-semibold py-3 rounded-lg hover:bg-gray-200 transition text-sm mb-5">
                  Generate 3-Day Plan
                </button>
                <div class="p-4 rounded-xl border border-[#222] bg-[#000]">
                  <h3 class="text-[11px] font-bold text-[#9984d8] uppercase mb-1.5 tracking-wide">DAY 1: KOMPLEKSITAS MODEL</h3>
                  <p class="text-[13px] text-gray-500 leading-relaxed">Awal-awal ngulik AI, bawaannya pengen bikin arsitektur yang keliatan paling rumit...</p>
                </div>
              </div>
            </div>

            <!-- Fitur 2 -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-10 items-center">
              <!-- Mockup 2 -->
              <div class="order-2 md:order-1 card-bd p-6 bg-[#050607] border-[#222] relative overflow-hidden">
                <div class="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-[#3fcb7f] to-transparent"></div>
                <!-- Segmented Control -->
                <div class="flex p-1 bg-[#111] rounded-lg mb-6 border border-[#222]">
                  <button class="flex-1 px-4 py-2.5 text-xs font-semibold bg-[#222] rounded-md text-white transition-all">
                    Review Manual
                  </button>
                  <button class="flex-1 px-4 py-2.5 text-xs font-semibold text-gray-600 hover:text-white transition-all">
                    Full Auto
                  </button>
                </div>
                <!-- Badges -->
                <div class="space-y-3">
                  <div class="flex items-center justify-between p-4 rounded-xl border border-[#222] bg-[#000]">
                    <span class="text-sm font-medium text-white">Pertanyaan</span>
                    <span class="text-[10px] font-bold text-[#9984d8] bg-[#9984d8]/10 px-3 py-1.5 rounded-md border border-[#9984d8]/20">Balasan AI</span>
                  </div>
                  <div class="flex items-center justify-between p-4 rounded-xl border border-[#222] bg-[#000]">
                    <span class="text-sm font-medium text-white">Pujian</span>
                    <span class="text-[10px] font-bold text-[#3fcb7f] bg-[#3fcb7f]/10 px-3 py-1.5 rounded-md border border-[#3fcb7f]/20">Template</span>
                  </div>
                  <div class="flex items-center justify-between p-4 rounded-xl border border-[#222] bg-[#000]">
                    <span class="text-sm font-medium text-white">Spam / Toxic</span>
                    <span class="text-[10px] font-bold text-gray-600 bg-gray-500/10 px-3 py-1.5 rounded-md border border-gray-500/20">Template</span>
                  </div>
                </div>
              </div>
              <div class="order-1 md:order-2">
                <span class="text-[12px] font-bold tracking-widest uppercase block mb-2 text-[var(--accent-violet)]">02 &middot; Komentar</span>
                <h3 class="font-display text-[28px] md:text-[32px] leading-tight mb-4">{{ $t('features.f2_title') }}</h3>
                <p class="text-[15px] leading-relaxed text-[var(--text-secondary)]">{{ $t('features.f2_desc') }}</p>
              </div>
            </div>

            <!-- Fitur 3 -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-10 items-center">
              <div>
                <span class="text-[12px] font-bold tracking-widest uppercase block mb-2 text-[var(--accent-violet)]">03 &middot; Analytics</span>
                <h3 class="font-display text-[28px] md:text-[32px] leading-tight mb-4">{{ $t('features.f3_title') }}</h3>
                <p class="text-[15px] leading-relaxed text-[var(--text-secondary)]">{{ $t('features.f3_desc') }}</p>
              </div>
              <!-- Mockup 3 -->
              <div class="card-bd p-6 bg-[#050607] border-[#222] relative overflow-hidden">
                <div class="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-[#9984d8] to-transparent"></div>
                <div class="flex gap-6 mb-5 text-xs font-semibold border-b border-[#222] pb-3 text-gray-600">
                  <span class="text-white border-b-2 border-[#9984d8] pb-3 -mb-[13px]">Best Time</span>
                  <span class="hover:text-white transition">Hook</span>
                  <span class="hover:text-white transition">Length</span>
                </div>
                <div class="grid grid-cols-7 gap-1.5">
                  <div v-for="i in 21" :key="i" class="aspect-square rounded border border-[#222]" :style="{ background: [3,7,11,15,18].includes(i) ? 'rgba(153,132,216,0.6)' : '#000' }"></div>
                </div>
                <div class="mt-4 flex items-center justify-between text-[10px] text-gray-600">
                  <span>Mon</span>
                  <span>Sun</span>
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
                </div>
                <div>
                  <div class="flex justify-between text-xs mb-1"><span class="font-bold">Story</span><span>1.36%</span></div>
                  <div class="w-full h-2 rounded-full overflow-hidden bg-[var(--bg-hover)]"><div class="h-full rounded-full bg-[var(--accent-mint)]" style="width: 43%;"></div></div>
                </div>
              </div>
            </div>
            <div class="card-bd p-6 bg-[var(--bg-primary)]">
              <h3 class="text-sm font-bold mb-5">Post Length</h3>
              <div class="space-y-3">
                <div>
                  <div class="flex justify-between text-xs mb-1"><span class="font-bold">300-500 char</span><span>2.96%</span></div>
                  <div class="w-full h-2 rounded-full overflow-hidden bg-[var(--bg-hover)]"><div class="h-full rounded-full bg-[var(--accent-violet)]" style="width: 93%;"></div></div>
                </div>
                <div>
                  <div class="flex justify-between text-xs mb-1"><span class="font-bold">100-300 char</span><span>1.12%</span></div>
                  <div class="w-full h-2 rounded-full overflow-hidden bg-[var(--bg-hover)]"><div class="h-full rounded-full bg-[var(--accent-mint)]" style="width: 35%;"></div></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- CARA KERJA -->
      <section id="cara-kerja" class="py-20 border-t border-[var(--border)]">
        <div class="max-w-[1000px] mx-auto px-6">
          <h2 class="h2-bd">Mulai dalam 3 langkah.</h2>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mt-10">
            <div class="space-y-3">
              <div class="w-10 h-10 rounded-full flex items-center justify-center font-display text-[18px] border border-[var(--border)] bg-[var(--bg-secondary)] text-[var(--accent-violet)]">1</div>
              <h3 class="text-[17px] font-semibold">Daftar dan minta akses.</h3>
              <p class="text-[14px] leading-relaxed text-[var(--text-secondary)]">Buat akun, lalu kirim @username Threads kamu. Akses disetujui manual dan kamu dikabari lewat email.</p>
            </div>
            <div class="space-y-3">
              <div class="w-10 h-10 rounded-full flex items-center justify-center font-display text-[18px] border border-[var(--border)] bg-[var(--bg-secondary)] text-[var(--accent-violet)]">2</div>
              <h3 class="text-[17px] font-semibold">Hubungkan dan ajari gayamu.</h3>
              <p class="text-[14px] leading-relaxed text-[var(--text-secondary)]">Setelah disetujui, terima undangan tester di Threads dan login lewat sistem resmi Meta. Tulis dokumen gaya dan aturanmu di Knowledge Base.</p>
            </div>
            <div class="space-y-3">
              <div class="w-10 h-10 rounded-full flex items-center justify-center font-display text-[18px] border border-[var(--border)] bg-[var(--bg-secondary)] text-[var(--accent-violet)]">3</div>
              <h3 class="text-[17px] font-semibold">Review dan jalan.</h3>
              <p class="text-[14px] leading-relaxed text-[var(--text-secondary)]">Setujui draf, atur mode balasan, dan pantau Analytics tiap minggu.</p>
            </div>
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
          <h2 class="font-display text-[40px] md:text-[56px] leading-[1.0] mb-8">{{ $t('cta.title') }}</h2>
          <a href="https://app.ixiera.id/signup" class="btn-bd-primary inline-block">{{ $t('cta.btn') }}</a>
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
