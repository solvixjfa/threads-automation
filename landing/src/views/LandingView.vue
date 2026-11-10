<template>
  <div class="min-h-screen font-sans selection:bg-black selection:text-white dark:selection:bg-white dark:selection:text-black bg-[var(--bg)] text-[var(--text)]">

    <!-- SIDEBAR DESKTOP (KIRI) -->
    <aside class="hidden md:flex fixed left-0 top-0 h-screen w-60 border-r border-[var(--line)] bg-[var(--bg)] flex-col z-50">
      <div class="h-16 px-5 flex items-center border-b border-[var(--line)]">
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 flex items-center justify-center rounded-md text-sm font-bold bg-[var(--text)] text-[var(--bg)]">IX</div>
          <span class="font-bold text-xl tracking-tight">Ixiera</span>
        </div>
      </div>

      <nav class="flex-1 p-3 space-y-1 overflow-y-auto">
        <a href="#fitur" class="block px-3 py-2.5 rounded-md text-sm font-medium text-[var(--muted)] hover:text-[var(--text)] hover:bg-[var(--surface-2)] transition">{{ $t('landing.nav.features') }}</a>
        <a href="#cara-kerja" class="block px-3 py-2.5 rounded-md text-sm font-medium text-[var(--muted)] hover:text-[var(--text)] hover:bg-[var(--surface-2)] transition">{{ $t('landing.nav.how_it_works') }}</a>
        <a href="#faq" class="block px-3 py-2.5 rounded-md text-sm font-medium text-[var(--muted)] hover:text-[var(--text)] hover:bg-[var(--surface-2)] transition">{{ $t('landing.nav.faq') }}</a>
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
        <a href="https://app.ixiera.id/login" class="block text-center text-sm font-bold bg-[var(--text)] text-[var(--bg)] py-2.5 rounded-md hover:opacity-90 transition">{{ $t('landing.nav.start_free') }}</a>
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

    <!-- MOBILE DRAWER SIDEBAR (KIRI) -->
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
            <a href="#fitur" @click="mobileMenuOpen=false" class="block px-4 py-3 rounded-lg text-sm font-medium text-[var(--muted)] hover:text-[var(--text)] hover:bg-[var(--surface-2)] transition">{{ $t('landing.nav.features') }}</a>
            <a href="#cara-kerja" @click="mobileMenuOpen=false" class="block px-4 py-3 rounded-lg text-sm font-medium text-[var(--muted)] hover:text-[var(--text)] hover:bg-[var(--surface-2)] transition">{{ $t('landing.nav.how_it_works') }}</a>
            <a href="#faq" @click="mobileMenuOpen=false" class="block px-4 py-3 rounded-lg text-sm font-medium text-[var(--muted)] hover:text-[var(--text)] hover:bg-[var(--surface-2)] transition">{{ $t('landing.nav.faq') }}</a>
          </nav>

          <div class="p-4 border-t border-[var(--line)] space-y-3">
            <div class="flex gap-2">
              <button @click="toggleTheme" class="flex-1 flex items-center justify-center gap-2 px-3 py-3 rounded-lg text-xs font-bold text-[var(--muted)] border border-[var(--line)] hover:bg-[var(--surface-2)] transition">
                <Sun v-if="theme === 'dark'" class="w-4 h-4" />
                <Moon v-else class="w-4 h-4" />
                <span>{{ theme === 'dark' ? 'Light' : 'Dark' }}</span>
              </button>
              <button @click="toggleLang" class="flex-1 px-3 py-3 rounded-lg text-xs font-bold text-[var(--muted)] border border-[var(--line)] hover:bg-[var(--surface-2)] transition">
                {{ locale === 'id' ? 'EN' : 'ID' }}
              </button>
            </div>
            <a href="https://app.ixiera.id/login" class="block text-center text-sm font-bold bg-[var(--text)] text-[var(--bg)] py-3 rounded-lg hover:opacity-90 transition">
              {{ $t('landing.nav.start_free') }}
            </a>
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

    <!-- MAIN CONTENT WRAPPER -->
    <main class="md:ml-60 pt-16 md:pt-0">
      
      <!-- HERO (Basedash Style) -->
      <section class="max-w-[1200px] mx-auto px-6 pb-20 md:pb-32 flex flex-col items-center text-center pt-10 md:pt-24">
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-[var(--line)] mb-8">
          <span class="w-1.5 h-1.5 rounded-full bg-[#3fcb7f]"></span>
          <span class="text-[13px] font-medium tracking-[-0.03em] text-[var(--muted)]">{{ $t('landing.hero.badge') }}</span>
        </div>

        <h1 class="font-serif-display text-[44px] md:text-[56px] leading-[1.1] md:leading-[1.05] tracking-normal mb-6 max-w-4xl mx-auto text-[var(--text)]">
          {{ $t('landing.hero.title_1') }} <br class="hidden md:block"/>
          <span class="italic text-[#9984d8]">{{ $t('landing.hero.title_2') }}</span>
        </h1>

        <p class="text-[16px] md:text-[18px] text-[var(--muted)] tracking-[-0.03em] leading-[1.6] max-w-2xl mx-auto mb-10">
          {{ $t('landing.hero.subtitle') }}
        </p>

        <div class="flex flex-col sm:flex-row items-center gap-4 mb-16 w-full sm:w-auto">
          <a href="https://app.ixiera.id/login" class="w-full sm:w-auto px-8 py-3.5 rounded-md text-[15px] font-medium tracking-[-0.03em] bg-[var(--text)] text-[var(--bg)] hover:opacity-90 transition">{{ $t('landing.hero.cta_primary') }}</a>
          <a href="#contoh" class="w-full sm:w-auto px-8 py-3.5 rounded-md text-[15px] font-medium tracking-[-0.03em] text-[var(--text)] border border-[var(--line)] hover:bg-[var(--surface-2)] transition">{{ $t('landing.hero.cta_secondary') }}</a>
        </div>

        <p class="text-[13px] text-[var(--muted)] tracking-[-0.03em] mb-12">{{ $t('landing.hero.microcopy') }}</p>
      </section>

      <!-- Hero Mockup Image -->
      <section class="max-w-[1000px] mx-auto px-4 md:px-0">
        <div class="relative w-full rounded-xl overflow-hidden border border-[var(--line)] bg-[var(--surface)]">
          <div class="flex items-center gap-1.5 px-4 py-3 border-b border-[var(--line)]">
            <div class="w-2.5 h-2.5 rounded-full bg-[var(--line)]"></div>
            <div class="w-2.5 h-2.5 rounded-full bg-[var(--line)]"></div>
            <div class="w-2.5 h-2.5 rounded-full bg-[var(--line)]"></div>
            <span class="ml-2 text-[10px] text-[var(--muted)] uppercase tracking-widest font-bold">Dashboard</span>
          </div>
          <div class="p-6 md:p-8 grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="bg-[var(--bg)] border border-[var(--line)] rounded-lg p-5">
              <p class="text-[12px] text-[var(--muted)] mb-1">Total Views</p>
              <p class="text-[32px] font-semibold text-[var(--text)] tracking-[-0.03em] mb-2">311,781</p>
              <p class="text-[12px] text-[#3fcb7f] tracking-[-0.03em]">up 126 percent</p>
            </div>
            <div class="bg-[var(--bg)] border border-[var(--line)] rounded-lg p-5">
              <p class="text-[12px] text-[var(--muted)] mb-1">Followers</p>
              <p class="text-[32px] font-semibold text-[var(--text)] tracking-[-0.03em] mb-2">2,592</p>
              <p class="text-[12px] text-[#3fcb7f] tracking-[-0.03em]">up 15 this week</p>
            </div>
            <div class="bg-[var(--bg)] border border-[var(--line)] rounded-lg p-5">
              <p class="text-[12px] text-[var(--muted)] mb-1">Engagement Rate</p>
              <p class="text-[32px] font-semibold text-[var(--text)] tracking-[-0.03em] mb-2">4.8 percent</p>
              <p class="text-[12px] text-[#3fcb7f] tracking-[-0.03em]">up 0.3 percent</p>
            </div>
          </div>
          <div class="absolute inset-0 pointer-events-none" style="background: radial-gradient(circle at 50% 0%, rgba(153,132,216,0.15) 0%, transparent 60%);"></div>
        </div>
      </section>

      <!-- SECTION: MASALAH -->
      <section class="py-20 md:py-32 bg-[var(--bg)] border-t border-[var(--line)]">
        <div class="max-w-[1200px] mx-auto px-6">
          <div class="text-center mb-16">
            <h2 class="font-serif-display text-[36px] md:text-[48px] leading-[1.1] mb-4 text-[var(--text)]">
              {{ $t('landing.problems.title') }}
            </h2>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="bg-[var(--surface)] border border-[var(--line)] rounded-2xl p-8">
              <span class="font-serif-display text-[32px] text-[#9984d8] block mb-4">01</span>
              <h3 class="text-[18px] font-semibold tracking-[-0.03em] text-[var(--text)] mb-2">{{ $t('landing.problems.p1_title') }}</h3>
              <p class="text-[15px] text-[var(--muted)] leading-[1.6] tracking-[-0.03em]">{{ $t('landing.problems.p1_desc') }}</p>
            </div>
            <div class="bg-[var(--surface)] border border-[var(--line)] rounded-2xl p-8">
              <span class="font-serif-display text-[32px] text-[#9984d8] block mb-4">02</span>
              <h3 class="text-[18px] font-semibold tracking-[-0.03em] text-[var(--text)] mb-2">{{ $t('landing.problems.p2_title') }}</h3>
              <p class="text-[15px] text-[var(--muted)] leading-[1.6] tracking-[-0.03em]">{{ $t('landing.problems.p2_desc') }}</p>
            </div>
            <div class="bg-[var(--surface)] border border-[var(--line)] rounded-2xl p-8">
              <span class="font-serif-display text-[32px] text-[#9984d8] block mb-4">03</span>
              <h3 class="text-[18px] font-semibold tracking-[-0.03em] text-[var(--text)] mb-2">{{ $t('landing.problems.p3_title') }}</h3>
              <p class="text-[15px] text-[var(--muted)] leading-[1.6] tracking-[-0.03em]">{{ $t('landing.problems.p3_desc') }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- SECTION: FITUR -->
      <section id="fitur" class="py-20 md:py-32 bg-[var(--bg)] border-t border-[var(--line)]">
        <div class="max-w-[1200px] mx-auto px-6">
          <div class="text-center mb-16">
            <h2 class="font-serif-display text-[36px] md:text-[48px] leading-[1.1] mb-4 text-[var(--text)]">
              {{ $t('landing.features.title') }}
            </h2>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div class="bg-[var(--surface)] border border-[var(--line)] rounded-2xl p-8 hover:border-[#333] transition-colors">
              <div class="w-10 h-10 rounded-lg bg-[#111] border border-[var(--line)] flex items-center justify-center mb-6">
                <span class="text-[#3fcb7f] text-lg font-bold">01</span>
              </div>
              <h3 class="text-[18px] font-semibold text-[var(--text)] mb-2 tracking-[-0.03em]">{{ $t('landing.features.f1_title') }}</h3>
              <p class="text-[14px] text-[var(--muted)] leading-[1.6] tracking-[-0.03em]">{{ $t('landing.features.f1_desc') }}</p>
            </div>
            <div class="bg-[var(--surface)] border border-[var(--line)] rounded-2xl p-8 hover:border-[#333] transition-colors">
              <div class="w-10 h-10 rounded-lg bg-[#111] border border-[var(--line)] flex items-center justify-center mb-6">
                <span class="text-[#3fcb7f] text-lg font-bold">02</span>
              </div>
              <h3 class="text-[18px] font-semibold text-[var(--text)] mb-2 tracking-[-0.03em]">{{ $t('landing.features.f2_title') }}</h3>
              <p class="text-[14px] text-[var(--muted)] leading-[1.6] tracking-[-0.03em]">{{ $t('landing.features.f2_desc') }}</p>
            </div>
            <div class="bg-[var(--surface)] border border-[var(--line)] rounded-2xl p-8 hover:border-[#333] transition-colors">
              <div class="w-10 h-10 rounded-lg bg-[#111] border border-[var(--line)] flex items-center justify-center mb-6">
                <span class="text-[#3fcb7f] text-lg font-bold">03</span>
              </div>
              <h3 class="text-[18px] font-semibold text-[var(--text)] mb-2 tracking-[-0.03em]">{{ $t('landing.features.f3_title') }}</h3>
              <p class="text-[14px] text-[var(--muted)] leading-[1.6] tracking-[-0.03em]">{{ $t('landing.features.f3_desc') }}</p>
            </div>
            <div class="bg-[var(--surface)] border border-[var(--line)] rounded-2xl p-8 hover:border-[#333] transition-colors">
              <div class="w-10 h-10 rounded-lg bg-[#111] border border-[var(--line)] flex items-center justify-center mb-6">
                <span class="text-[#3fcb7f] text-lg font-bold">04</span>
              </div>
              <h3 class="text-[18px] font-semibold text-[var(--text)] mb-2 tracking-[-0.03em]">{{ $t('landing.features.f4_title') }}</h3>
              <p class="text-[14px] text-[var(--muted)] leading-[1.6] tracking-[-0.03em]">{{ $t('landing.features.f4_desc') }}</p>
            </div>
            <div class="bg-[var(--surface)] border border-[var(--line)] rounded-2xl p-8 hover:border-[#333] transition-colors">
              <div class="w-10 h-10 rounded-lg bg-[#111] border border-[var(--line)] flex items-center justify-center mb-6">
                <span class="text-[#3fcb7f] text-lg font-bold">05</span>
              </div>
              <h3 class="text-[18px] font-semibold text-[var(--text)] mb-2 tracking-[-0.03em]">{{ $t('landing.features.f5_title') }}</h3>
              <p class="text-[14px] text-[var(--muted)] leading-[1.6] tracking-[-0.03em]">{{ $t('landing.features.f5_desc') }}</p>
            </div>
            <div class="bg-[var(--surface)] border border-[var(--line)] rounded-2xl p-8 hover:border-[#333] transition-colors">
              <div class="w-10 h-10 rounded-lg bg-[#111] border border-[var(--line)] flex items-center justify-center mb-6">
                <span class="text-[#3fcb7f] text-lg font-bold">06</span>
              </div>
              <h3 class="text-[18px] font-semibold text-[var(--text)] mb-2 tracking-[-0.03em]">{{ $t('landing.features.f6_title') }}</h3>
              <p class="text-[14px] text-[var(--muted)] leading-[1.6] tracking-[-0.03em]">{{ $t('landing.features.f6_desc') }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- SECTION: CARA KERJA -->
      <section id="cara-kerja" class="py-20 md:py-32 bg-[var(--bg)] border-t border-[var(--line)]">
        <div class="max-w-[1200px] mx-auto px-6">
          <div class="text-center mb-16">
            <h2 class="font-serif-display text-[36px] md:text-[48px] leading-[1.1] mb-4 text-[var(--text)]">
              {{ $t('landing.how.title') }}
            </h2>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-8 relative">
            <div class="text-center space-y-4">
              <div class="w-12 h-12 mx-auto rounded-full bg-[#111] border border-[var(--line)] flex items-center justify-center font-bold text-[#9984d8] text-xl">1</div>
              <h3 class="text-[18px] font-semibold">{{ $t('landing.how.s1_title') }}</h3>
              <p class="text-[14px] text-[var(--muted)] px-4">{{ $t('landing.how.s1_desc') }}</p>
            </div>
            <div class="text-center space-y-4">
              <div class="w-12 h-12 mx-auto rounded-full bg-[#111] border border-[var(--line)] flex items-center justify-center font-bold text-[#9984d8] text-xl">2</div>
              <h3 class="text-[18px] font-semibold">{{ $t('landing.how.s2_title') }}</h3>
              <p class="text-[14px] text-[var(--muted)] px-4">{{ $t('landing.how.s2_desc') }}</p>
            </div>
            <div class="text-center space-y-4">
              <div class="w-12 h-12 mx-auto rounded-full bg-[#111] border border-[var(--line)] flex items-center justify-center font-bold text-[#9984d8] text-xl">3</div>
              <h3 class="text-[18px] font-semibold">{{ $t('landing.how.s3_title') }}</h3>
              <p class="text-[14px] text-[var(--muted)] px-4">{{ $t('landing.how.s3_desc') }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- SECTION: KEAMANAN -->
      <section class="py-20 md:py-32 bg-[var(--surface)] border-t border-[var(--line)]">
        <div class="max-w-[1200px] mx-auto px-6 grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
          <div>
            <h2 class="font-serif-display text-[36px] md:text-[48px] leading-[1.1] mb-6 text-[var(--text)]">
              {{ $t('landing.security.title') }}
            </h2>
            <ul class="space-y-3">
              <li class="flex items-center gap-3 text-[14px] text-[var(--text)] tracking-[-0.03em]">
                <svg class="w-5 h-5 text-[#3fcb7f]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                Official Meta API integration
              </li>
              <li class="flex items-center gap-3 text-[14px] text-[var(--text)] tracking-[-0.03em]">
                <svg class="w-5 h-5 text-[#3fcb7f]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                Data isolated per user
              </li>
              <li class="flex items-center gap-3 text-[14px] text-[var(--text)] tracking-[-0.03em]">
                <svg class="w-5 h-5 text-[#3fcb7f]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                Kill switch anytime
              </li>
            </ul>
          </div>
          <div class="bg-[#050607] border border-[var(--line)] rounded-2xl p-8 aspect-square flex items-center justify-center relative overflow-hidden">
             <div class="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(153,132,216,0.1)_0,transparent_70%)]"></div>
             <div class="w-24 h-24 rounded-full border-2 border-[#9984d8]/30 flex items-center justify-center">
               <div class="w-16 h-16 rounded-full border-2 border-[#9984d8]/60 flex items-center justify-center">
                 <div class="w-8 h-8 rounded-full bg-[#3fcb7f] shadow-[0_0_20px_#3fcb7f]"></div>
               </div>
             </div>
          </div>
        </div>
      </section>

      <!-- SECTION: HARGA -->
      <section id="harga" class="py-20 md:py-32 bg-[var(--bg)] border-t border-[var(--line)]">
        <div class="max-w-[1200px] mx-auto px-6">
          <div class="text-center mb-16">
            <h2 class="font-serif-display text-[36px] md:text-[48px] leading-[1.1] mb-4 text-[var(--text)]">
              {{ $t('landing.pricing.title') }}
            </h2>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="bg-[var(--surface)] border border-[var(--line)] rounded-2xl p-8 flex flex-col">
              <h3 class="text-[20px] font-semibold text-[var(--text)] mb-2">Trial</h3>
              <div class="text-[40px] font-bold text-[var(--text)] mb-6">Rp 0<span class="text-[14px] font-normal text-[var(--muted)]">/mo</span></div>
              <ul class="space-y-3 mb-8 flex-1">
                <li class="text-[14px] text-[var(--muted)] flex items-center gap-2"><div class="w-1 h-1 rounded-full bg-white"></div> 7-day trial</li>
                <li class="text-[14px] text-[var(--muted)] flex items-center gap-2"><div class="w-1 h-1 rounded-full bg-white"></div> 20 AI credits</li>
              </ul>
              <a href="https://app.ixiera.id/login" class="block text-center w-full py-3 rounded-md border border-[var(--line)] text-[14px] font-medium hover:bg-[#111] transition">Start free</a>
            </div>
            <div class="bg-[#050607] border border-[#9984d8] rounded-2xl p-8 flex flex-col relative shadow-[0_0_30px_rgba(153,132,216,0.15)]">
              <div class="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-[#9984d8] text-black text-[11px] font-bold uppercase tracking-widest py-1 px-3 rounded-full">Popular</div>
              <h3 class="text-[20px] font-semibold text-white mb-2">Pro</h3>
              <div class="text-[40px] font-bold text-white mb-6">Rp 29k<span class="text-[14px] font-normal text-[#b3b3b3]">/mo</span></div>
              <ul class="space-y-3 mb-8 flex-1">
                <li class="text-[14px] text-[#b3b3b3] flex items-center gap-2"><div class="w-1 h-1 rounded-full bg-white"></div> 100 AI credits</li>
                <li class="text-[14px] text-[#b3b3b3] flex items-center gap-2"><div class="w-1 h-1 rounded-full bg-white"></div> Auto-reply engine</li>
                <li class="text-[14px] text-[#b3b3b3] flex items-center gap-2"><div class="w-1 h-1 rounded-full bg-white"></div> Advanced analytics</li>
              </ul>
              <a href="https://app.ixiera.id/login" class="block text-center w-full py-3 rounded-md bg-white text-black text-[14px] font-medium hover:bg-gray-200 transition">Upgrade Pro</a>
            </div>
            <div class="bg-[var(--surface)] border border-[var(--line)] rounded-2xl p-8 flex flex-col">
              <h3 class="text-[20px] font-semibold text-[var(--text)] mb-2">Enterprise</h3>
              <div class="text-[40px] font-bold text-[var(--text)] mb-6">Custom</div>
              <ul class="space-y-3 mb-8 flex-1">
                <li class="text-[14px] text-[var(--muted)] flex items-center gap-2"><div class="w-1 h-1 rounded-full bg-white"></div> Unlimited accounts</li>
                <li class="text-[14px] text-[var(--muted)] flex items-center gap-2"><div class="w-1 h-1 rounded-full bg-white"></div> Dedicated support</li>
              </ul>
              <a href="mailto:contact@ixiera.id" class="block text-center w-full py-3 rounded-md border border-[var(--line)] text-[14px] font-medium hover:bg-[#111] transition">Contact sales</a>
            </div>
          </div>
        </div>
      </section>

      <!-- SECTION: FAQ -->
      <section id="faq" class="py-20 md:py-32 bg-[var(--bg)] border-t border-[var(--line)]">
        <div class="max-w-[800px] mx-auto px-6">
          <div class="text-center mb-16">
            <h2 class="font-serif-display text-[36px] md:text-[48px] leading-[1.1] mb-4 text-[var(--text)]">
              {{ $t('landing.faq.title') }}
            </h2>
          </div>
          <div class="space-y-0 border-t border-[var(--line)]">
            <details class="group border-b border-[var(--line)] py-5 cursor-pointer">
              <summary class="flex items-center justify-between text-[16px] font-semibold text-[var(--text)] list-none">
                {{ $t('landing.faq.q1') || 'Is this official?' }}
                <span class="transition group-open:rotate-180">
                  <svg class="w-5 h-5 text-[var(--muted)]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                </span>
              </summary>
              <p class="text-[15px] text-[var(--muted)] mt-3 leading-relaxed">{{ $t('landing.faq.a1') }}</p>
            </details>
            <details class="group border-b border-[var(--line)] py-5 cursor-pointer">
              <summary class="flex items-center justify-between text-[16px] font-semibold text-[var(--text)] list-none">
                {{ $t('landing.faq.q2') || 'Is my data safe?' }}
                <span class="transition group-open:rotate-180">
                  <svg class="w-5 h-5 text-[var(--muted)]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                </span>
              </summary>
              <p class="text-[15px] text-[var(--muted)] mt-3 leading-relaxed">{{ $t('landing.faq.a2') }}</p>
            </details>
          </div>
        </div>
      </section>

      <!-- FINAL CTA -->
      <section class="py-24 md:py-32 border-t border-[var(--line)] text-center px-6 bg-[var(--surface)]">
        <h2 class="font-serif-display text-[40px] md:text-[56px] leading-[1.1] text-[var(--text)] mb-8 max-w-3xl mx-auto">
          {{ $t('landing.cta_end.title') }}
        </h2>
        <a href="https://app.ixiera.id/login" class="inline-block px-8 py-4 rounded-md bg-white text-black text-[16px] font-bold hover:bg-gray-200 transition">
          Request Access
        </a>
        <p class="text-[13px] text-[var(--muted)] mt-4 tracking-[-0.03em]">7-day trial - 20 free credits - No upfront payment</p>
      </section>

    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
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
