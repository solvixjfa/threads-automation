<template>
  <div class="min-h-screen font-sans selection:bg-black selection:text-white dark:selection:bg-white dark:selection:text-black bg-[var(--bg)] text-[var(--text)] overflow-x-hidden">
    
    <!-- NAVBAR -->
    <nav class="fixed top-0 w-full z-50 border-b border-[var(--line)] bg-[var(--bg)]/80 backdrop-blur-md">
      <div class="max-w-[1120px] mx-auto px-6 h-16 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 flex items-center justify-center rounded-md text-sm font-bold bg-[var(--text)] text-[var(--bg)]">IX</div>
          <span class="font-bold text-xl tracking-tight">Ixiera</span>
        </div>
        
        <div class="hidden md:flex items-center gap-8">
          <a href="#fitur" class="text-sm font-medium text-[var(--muted)] hover:text-[var(--text)] transition-colors">{{ $t('landing.nav.features') }}</a>
          <a href="#cara-kerja" class="text-sm font-medium text-[var(--muted)] hover:text-[var(--text)] transition-colors">{{ $t('landing.nav.how_it_works') }}</a>
          <a href="#faq" class="text-sm font-medium text-[var(--muted)] hover:text-[var(--text)] transition-colors">{{ $t('landing.nav.faq') }}</a>
        </div>

        <div class="hidden md:flex items-center gap-4">
          <button @click="toggleTheme" class="p-2 rounded-full hover:bg-[var(--surface-2)] transition-colors">
            <Sun v-if="theme === 'dark'" class="w-5 h-5 text-[var(--text)]" />
            <Moon v-else class="w-5 h-5 text-[var(--text)]" />
          </button>
          
          <button @click="toggleLang" class="text-sm font-bold border border-[var(--line)] px-3 py-1.5 rounded-full hover:bg-[var(--surface-2)] transition">{{ locale.toUpperCase() }}</button>
          
          <a href="https://app.ixiera.id/login" class="text-sm font-bold bg-[var(--text)] text-[var(--bg)] px-6 py-2 rounded-full hover:opacity-90 transition">{{ $t('landing.nav.start_free') }}</a>
        </div>

        <button @click="mobileMenuOpen = !mobileMenuOpen" class="md:hidden p-2">
          <svg v-if="!mobileMenuOpen" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
          <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
        </button>
      </div>

      <div v-if="mobileMenuOpen" class="md:hidden border-t border-[var(--line)] bg-[var(--bg)] px-6 py-4 space-y-4 shadow-xl">
        <a href="#fitur" @click="mobileMenuOpen=false" class="block text-sm font-medium">{{ $t('landing.nav.features') }}</a>
        <a href="#cara-kerja" @click="mobileMenuOpen=false" class="block text-sm font-medium">{{ $t('landing.nav.how_it_works') }}</a>
        <a href="#faq" @click="mobileMenuOpen=false" class="block text-sm font-medium">{{ $t('landing.nav.faq') }}</a>
        <div class="pt-4 border-t border-[var(--line)] flex flex-col gap-4">
          <div class="flex items-center justify-between">
            <button @click="toggleTheme" class="flex items-center gap-2 text-sm font-medium text-[var(--muted)]">
              <Sun v-if="theme === 'dark'" class="w-5 h-5" />
              <Moon v-else class="w-5 h-5" />
              <span>{{ theme === 'dark' ? 'Light Mode' : 'Dark Mode' }}</span>
            </button>
            <button @click="toggleLang" class="text-sm font-bold border border-[var(--line)] px-3 py-1.5 rounded-md">{{ locale === 'id' ? 'EN' : 'ID' }}</button>
          </div>
          <a href="https://app.ixiera.id/login" class="block text-center text-sm font-bold bg-[var(--text)] text-[var(--bg)] py-3 rounded-md">{{ $t('landing.nav.start_free') }}</a>
        </div>
      </div>
    </nav>

    <main class="pt-24 md:pt-32">
      <!-- HERO -->
      <section class="max-w-[1120px] mx-auto px-6 pb-20 md:pb-32 flex flex-col md:flex-row items-center gap-12">
        <div class="flex-1 space-y-6 text-center md:text-left fade-in">
          <div class="inline-flex items-center px-3 py-1 rounded-full border border-[var(--line)] text-xs font-bold tracking-widest text-[var(--muted)] uppercase">{{ $t('landing.hero.badge') }}</div>
          <h1 class="text-4xl md:text-6xl font-bold tracking-tight leading-[1.05]">
            {{ $t('landing.hero.title_1') }} <br class="hidden md:block"/>
            <span class="underline decoration-4 underline-offset-8 decoration-[var(--text)]">{{ $t('landing.hero.title_2') }}</span>
          </h1>
          <p class="text-lg text-[var(--muted)] leading-relaxed max-w-xl mx-auto md:mx-0">{{ $t('landing.hero.subtitle') }}</p>
          <div class="flex flex-col sm:flex-row items-center justify-center md:justify-start gap-4 pt-4">
            <a href="https://app.ixiera.id/login" class="w-full sm:w-auto px-8 py-3.5 rounded-full text-base font-bold bg-[var(--text)] text-[var(--bg)] hover:opacity-90 transition">{{ $t('landing.hero.cta_primary') }}</a>
            <a href="#contoh" class="w-full sm:w-auto px-8 py-3.5 rounded-full text-base font-bold border border-[var(--line)] hover:bg-[var(--surface-2)] transition">{{ $t('landing.hero.cta_secondary') }}</a>
          </div>
          <p class="text-xs text-[var(--muted)] pt-2">{{ $t('landing.hero.microcopy') }}</p>
          <div class="flex flex-col sm:flex-row gap-4 pt-8 text-xs text-[var(--muted)] justify-center md:justify-start">
            <span class="flex items-center gap-2"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg> {{ $t('landing.hero.trust_1') }}</span>
            <span class="flex items-center gap-2"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg> {{ $t('landing.hero.trust_2') }}</span>
            <span class="flex items-center gap-2"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg> {{ $t('landing.hero.trust_3') }}</span>
          </div>
        </div>
        
        <!-- MOCKUP: Hook Chart (Hero) -->
        <div class="flex-1 w-full max-w-md mx-auto fade-in">
          <div class="border border-dashed border-[var(--line)] rounded-xl overflow-hidden bg-[var(--surface)]">
            <div class="flex items-center gap-1.5 px-4 py-3 border-b border-[var(--line)]">
              <div class="w-2.5 h-2.5 rounded-full bg-[var(--line)]"></div><div class="w-2.5 h-2.5 rounded-full bg-[var(--line)]"></div><div class="w-2.5 h-2.5 rounded-full bg-[var(--line)]"></div>
              <span class="ml-2 text-[10px] text-[var(--muted)] uppercase tracking-widest font-bold">Hook Performance</span>
            </div>
            <div class="p-6 space-y-4">
              <div v-for="(item, index) in hookData" :key="item.label" class="space-y-1">
                <div class="flex justify-between text-xs font-bold"><span>{{ item.label }}</span><span>{{ item.er }}%</span></div>
                <div class="w-full bg-[var(--surface-2)] h-2 rounded-full">
                  <div class="h-full rounded-full bar-grow" :class="index === 0 ? 'bg-[var(--text)]' : 'bg-[var(--bar-dim)]'" :style="{ width: getBarWidth(item.er) }"></div>
                </div>
                <div class="text-[10px] text-[var(--muted)] text-right">n={{ item.n }}</div>
              </div>
            </div>
            <div class="bg-[var(--surface-2)] text-center py-2 text-[10px] text-[var(--muted)] uppercase tracking-widest font-bold">
              Data nyata
            </div>
          </div>
        </div>
      </section>

      <!-- MASALAH -->
      <section class="border-t border-[var(--line)] bg-[var(--surface)] py-20 md:py-32">
        <div class="max-w-[1120px] mx-auto px-6">
          <h2 class="text-3xl md:text-5xl font-bold tracking-tight text-center mb-16 fade-in">{{ $t('landing.problems.title') }}</h2>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-12">
            <div class="space-y-4 fade-in">
              <span class="text-5xl font-bold text-[var(--faint)]">01</span>
              <h3 class="text-xl font-bold">{{ $t('landing.problems.p1_title') }}</h3>
              <p class="text-[var(--muted)]">{{ $t('landing.problems.p1_desc') }}</p>
            </div>
            <div class="space-y-4 fade-in" style="transition-delay: 100ms">
              <span class="text-5xl font-bold text-[var(--faint)]">02</span>
              <h3 class="text-xl font-bold">{{ $t('landing.problems.p2_title') }}</h3>
              <p class="text-[var(--muted)]">{{ $t('landing.problems.p2_desc') }}</p>
            </div>
            <div class="space-y-4 fade-in" style="transition-delay: 200ms">
              <span class="text-5xl font-bold text-[var(--faint)]">03</span>
              <h3 class="text-xl font-bold">{{ $t('landing.problems.p3_title') }}</h3>
              <p class="text-[var(--muted)]">{{ $t('landing.problems.p3_desc') }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- FITUR -->
      <section id="fitur" class="py-20 md:py-32 border-t border-[var(--line)]">
        <div class="max-w-[1120px] mx-auto px-6">
          <div class="text-center mb-20 fade-in">
            <h2 class="text-3xl md:text-5xl font-bold tracking-tight">{{ $t('landing.features.title') }}</h2>
            <p class="text-lg text-[var(--muted)] mt-4">{{ $t('landing.features.subtitle') }}</p>
          </div>

          <div class="space-y-24">
            <!-- Fitur 1: Content (INTERAKTIF) -->
            <div class="flex flex-col md:flex-row items-center gap-12">
              <div class="flex-1 space-y-4 fade-in">
                <span class="text-xs font-bold uppercase tracking-widest text-[var(--muted)]">01 · Content</span>
                <h3 class="text-2xl font-bold">{{ $t('landing.features.f1_title') }}</h3>
                <p class="text-[var(--muted)] leading-relaxed">{{ $t('landing.features.f1_desc') }}</p>
              </div>
              <div class="flex-1 w-full">
                <div class="border border-dashed border-[var(--line)] rounded-xl overflow-hidden bg-[var(--surface)]">
                  <div class="flex items-center gap-1.5 px-4 py-3 border-b border-[var(--line)]"><div class="w-2.5 h-2.5 rounded-full bg-[var(--line)]"></div><div class="w-2.5 h-2.5 rounded-full bg-[var(--line)]"></div><div class="w-2.5 h-2.5 rounded-full bg-[var(--line)]"></div></div>
                  <div class="p-6 space-y-4">
                    <div class="space-y-2"><label class="text-xs font-bold text-[var(--muted)]">Topik</label><div class="border border-[var(--line)] rounded-md p-3 text-sm bg-[var(--bg)]">Kenapa RAG sederhana sering sudah cukup</div></div>
                    <div class="space-y-2"><label class="text-xs font-bold text-[var(--muted)]">Gaya</label><div class="border border-[var(--line)] rounded-md p-3 text-sm bg-[var(--bg)]">Educational & Insight</div></div>
                    <button @click="simulateGenerate" :disabled="isGenerating" class="w-full py-3 bg-[var(--text)] text-[var(--bg)] rounded-md font-bold text-sm flex items-center justify-center gap-2 transition-opacity hover:opacity-90">
                      <span v-if="isGenerating" class="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin"></span>
                      <span>{{ isGenerating ? 'Menyusun rencana...' : 'Generate Rencana 3 Hari' }}</span>
                      <span v-if="!isGenerating" class="text-[10px] opacity-70 border border-[var(--bg)]/20 px-2 py-0.5 rounded-full">1 kredit</span>
                    </button>
                    <div v-if="generatedPlan" class="pt-4 space-y-2 animate-[fade-in_0.5s_ease-out]">
                      <div class="flex items-center gap-2 text-sm"><span class="font-bold text-[var(--muted)]">Hari 1:</span> <span>Rahasia dibalik RAG yang efisien</span></div>
                      <div class="flex items-center gap-2 text-sm"><span class="font-bold text-[var(--muted)]">Hari 2:</span> <span>Kapan harus pakai Fine-tuning?</span></div>
                      <div class="flex items-center gap-2 text-sm"><span class="font-bold text-[var(--muted)]">Hari 3:</span> <span>Studi kasus implementasi sederhana</span></div>
                    </div>
                  </div>
                  <div class="bg-[var(--surface-2)] text-center py-2 text-[10px] text-[var(--muted)] uppercase tracking-widest font-bold">Contoh tampilan</div>
                </div>
              </div>
            </div>

            <!-- Fitur 2: Komentar (INTERAKTIF) -->
            <div class="flex flex-col md:flex-row-reverse items-center gap-12">
              <div class="flex-1 space-y-4 fade-in">
                <span class="text-xs font-bold uppercase tracking-widest text-[var(--muted)]">02 · Komentar</span>
                <h3 class="text-2xl font-bold">{{ $t('landing.features.f2_title') }}</h3>
                <p class="text-[var(--muted)] leading-relaxed">{{ $t('landing.features.f2_desc') }}</p>
              </div>
              <div class="flex-1 w-full">
                <div class="border border-dashed border-[var(--line)] rounded-xl overflow-hidden bg-[var(--surface)]">
                  <div class="flex items-center gap-1.5 px-4 py-3 border-b border-[var(--line)]"><div class="w-2.5 h-2.5 rounded-full bg-[var(--line)]"></div><div class="w-2.5 h-2.5 rounded-full bg-[var(--line)]"></div><div class="w-2.5 h-2.5 rounded-full bg-[var(--line)]"></div></div>
                  <div class="p-6 space-y-4">
                    <div class="flex rounded-md border border-[var(--line)] p-1 bg-[var(--bg)]">
                      <button @click="mockReplyMode = 'manual'" :class="mockReplyMode === 'manual' ? 'bg-[var(--text)] text-[var(--bg)] shadow-sm' : 'text-[var(--muted)] hover:text-[var(--text)]'" class="flex-1 py-1.5 text-xs font-bold rounded transition-colors">Review Manual</button>
                      <button @click="mockReplyMode = 'auto'" :class="mockReplyMode === 'auto' ? 'bg-[var(--text)] text-[var(--bg)] shadow-sm' : 'text-[var(--muted)] hover:text-[var(--text)]'" class="flex-1 py-1.5 text-xs font-bold rounded transition-colors">Full Auto</button>
                    </div>
                    <div class="text-xs text-[var(--muted)] flex justify-between"><span>Maks balasan per jam:</span><span class="font-bold text-[var(--text)]">5</span></div>
                    <div class="space-y-2 text-xs">
                      <div class="flex justify-between p-2 bg-[var(--bg)] border border-[var(--line)] rounded"><span>Pertanyaan</span><span class="font-bold">{{ mockReplyMode === 'auto' ? 'Langsung Balas' : 'Balasan AI' }}</span></div>
                      <div class="flex justify-between p-2 bg-[var(--bg)] border border-[var(--line)] rounded"><span>Pujian</span><span class="font-bold">{{ mockReplyMode === 'auto' ? 'Langsung Balas' : 'Template' }}</span></div>
                      <div class="flex justify-between p-2 bg-[var(--bg)] border border-[var(--line)] rounded"><span>Spam / Toxic</span><span class="font-bold">{{ mockReplyMode === 'auto' ? 'Langsung Balas' : 'Template' }}</span></div>
                    </div>
                  </div>
                  <div class="bg-[var(--surface-2)] text-center py-2 text-[10px] text-[var(--muted)] uppercase tracking-widest font-bold">Contoh tampilan</div>
                </div>
              </div>
            </div>

            <!-- Fitur 3: Analytics (INTERAKTIF & GRAFIK JELAS) -->
            <div class="flex flex-col md:flex-row items-center gap-12">
              <div class="flex-1 space-y-4 fade-in">
                <span class="text-xs font-bold uppercase tracking-widest text-[var(--muted)]">03 · Analytics</span>
                <h3 class="text-2xl font-bold">{{ $t('landing.features.f3_title') }}</h3>
                <p class="text-[var(--muted)] leading-relaxed">{{ $t('landing.features.f3_desc') }}</p>
              </div>
              <div class="flex-1 w-full">
                <div class="border border-dashed border-[var(--line)] rounded-xl overflow-hidden bg-[var(--surface)]">
                  <div class="flex items-center gap-1.5 px-4 py-3 border-b border-[var(--line)]"><div class="w-2.5 h-2.5 rounded-full bg-[var(--line)]"></div><div class="w-2.5 h-2.5 rounded-full bg-[var(--line)]"></div><div class="w-2.5 h-2.5 rounded-full bg-[var(--line)]"></div></div>
                  <div class="p-6 space-y-4">
                    <div class="flex gap-4 border-b border-[var(--line)] pb-2 text-xs font-bold">
                      <button @click="activeMockTab = 'best'" :class="activeMockTab === 'best' ? 'border-b-2 border-[var(--text)] pb-2 text-[var(--text)]' : 'text-[var(--muted)] pb-2 hover:text-[var(--text)] transition-colors'">Best Time</button>
                      <button @click="activeMockTab = 'hook'" :class="activeMockTab === 'hook' ? 'border-b-2 border-[var(--text)] pb-2 text-[var(--text)]' : 'text-[var(--muted)] pb-2 hover:text-[var(--text)] transition-colors'">Hook</button>
                      <button @click="activeMockTab = 'length'" :class="activeMockTab === 'length' ? 'border-b-2 border-[var(--text)] pb-2 text-[var(--text)]' : 'text-[var(--muted)] pb-2 hover:text-[var(--text)] transition-colors'">Length</button>
                    </div>
                    
                    <!-- Best Time Heatmap -->
                    <div v-if="activeMockTab === 'best'" class="flex gap-2">
                      <div class="flex flex-col justify-between text-[9px] text-[var(--muted)] py-1">
                        <span>Sen</span><span>Sel</span><span>Rab</span><span>Kam</span><span>Jum</span><span>Sab</span><span>Min</span>
                      </div>
                      <div class="flex-1 grid grid-cols-12 gap-1">
                        <div v-for="i in 84" :key="i" class="h-4 rounded-sm bg-[var(--line)]"
                             :class="{
                               'opacity-20': i % 5 === 0,
                               'bg-[var(--text)] opacity-100': i === 12 || i === 25 || i === 38 || i === 51, /* Highlighted cells (dark) */
                               'bg-[var(--bar-dim)] opacity-60': i % 3 === 0
                             }">
                        </div>
                      </div>
                    </div>

                    <!-- Hook Bars -->
                    <div v-if="activeMockTab === 'hook'" class="space-y-3 py-2">
                       <div class="space-y-1"><div class="flex justify-between text-[10px] font-bold"><span>Question</span><span>2.92%</span></div><div class="w-full bg-[var(--surface-2)] h-1.5 rounded-full"><div class="h-full bg-[var(--text)] w-[80%] rounded-full"></div></div></div>
                       <div class="space-y-1"><div class="flex justify-between text-[10px] font-bold"><span>Story</span><span>1.36%</span></div><div class="w-full bg-[var(--surface-2)] h-1.5 rounded-full"><div class="h-full bg-[var(--bar-dim)] w-[40%] rounded-full"></div></div></div>
                    </div>

                    <!-- Length Bars -->
                    <div v-if="activeMockTab === 'length'" class="space-y-3 py-2">
                       <div class="space-y-1"><div class="flex justify-between text-[10px] font-bold"><span>300-500 char</span><span>2.96%</span></div><div class="w-full bg-[var(--surface-2)] h-1.5 rounded-full"><div class="h-full bg-[var(--text)] w-[90%] rounded-full"></div></div></div>
                       <div class="space-y-1"><div class="flex justify-between text-[10px] font-bold"><span>100-300 char</span><span>1.12%</span></div><div class="w-full bg-[var(--surface-2)] h-1.5 rounded-full"><div class="h-full bg-[var(--bar-dim)] w-[35%] rounded-full"></div></div></div>
                    </div>

                  </div>
                  <div class="bg-[var(--surface-2)] text-center py-2 text-[10px] text-[var(--muted)] uppercase tracking-widest font-bold">Contoh tampilan</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- DATA NYATA -->
      <section id="contoh" class="py-20 md:py-32 bg-[var(--surface)] border-t border-[var(--line)]">
        <div class="max-w-[1120px] mx-auto px-6">
          <div class="text-center mb-16 fade-in">
            <h2 class="text-3xl md:text-5xl font-bold tracking-tight">{{ $t('landing.realData.title') }}</h2>
            <p class="text-lg text-[var(--muted)] mt-4 max-w-2xl mx-auto">{{ $t('landing.realData.subtitle') }}</p>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <!-- Hook Card -->
            <div class="border border-solid border-[var(--line)] rounded-xl overflow-hidden bg-[var(--bg)] fade-in">
              <div class="flex justify-between items-center px-4 py-3 border-b border-[var(--line)]">
                <span class="text-xs font-bold uppercase tracking-widest">Hook Performance</span>
                <span class="text-[10px] font-bold bg-[var(--text)] text-[var(--bg)] px-2 py-1 rounded-full">{{ $t('landing.realData.hook_label') }}</span>
              </div>
              <div class="p-6 space-y-4">
                <div v-for="(item, index) in hookData.slice(0, 2)" :key="item.label" class="space-y-1">
                  <div class="flex justify-between text-xs font-bold"><span>{{ item.label }}</span><span>{{ item.er }}%</span></div>
                  <div class="w-full bg-[var(--surface-2)] h-2 rounded-full">
                    <div class="h-full rounded-full bar-grow" :class="index === 0 ? 'bg-[var(--text)]' : 'bg-[var(--bar-dim)]'" :style="{ width: getBarWidth(item.er) }"></div>
                  </div>
                  <div class="text-[10px] text-[var(--muted)] text-right">n={{ item.n }}</div>
                </div>
              </div>
              <div class="px-6 pb-6 text-sm text-[var(--muted)] border-t border-[var(--line)] pt-4">{{ $t('landing.realData.hook_desc') }}</div>
            </div>
            <!-- Length Card -->
            <div class="border border-solid border-[var(--line)] rounded-xl overflow-hidden bg-[var(--bg)] fade-in" style="transition-delay: 100ms">
              <div class="flex justify-between items-center px-4 py-3 border-b border-[var(--line)]">
                <span class="text-xs font-bold uppercase tracking-widest">Post Length</span>
                <span class="text-[10px] font-bold bg-[var(--text)] text-[var(--bg)] px-2 py-1 rounded-full">{{ $t('landing.realData.len_label') }}</span>
              </div>
              <div class="p-6 space-y-4">
                <div v-for="(item, index) in lengthData.slice(0, 2)" :key="item.label" class="space-y-1">
                  <div class="flex justify-between text-xs font-bold"><span>{{ item.label }}</span><span>{{ item.er }}%</span></div>
                  <div class="w-full bg-[var(--surface-2)] h-2 rounded-full">
                    <div class="h-full rounded-full bar-grow" :class="index === 0 ? 'bg-[var(--text)]' : 'bg-[var(--bar-dim)]'" :style="{ width: getBarWidth(item.er) }"></div>
                  </div>
                  <div class="text-[10px] text-[var(--muted)] text-right">n={{ item.n }}</div>
                </div>
              </div>
              <div class="px-6 pb-6 text-sm text-[var(--muted)] border-t border-[var(--line)] pt-4">{{ $t('landing.realData.len_desc') }}</div>
            </div>
          </div>
          <p class="text-center text-xs text-[var(--muted)] mt-8">{{ $t('landing.realData.note') }}</p>
        </div>
      </section>

      <!-- CARA KERJA -->
      <section id="cara-kerja" class="py-20 md:py-32 border-t border-[var(--line)]">
        <div class="max-w-[1120px] mx-auto px-6">
          <h2 class="text-3xl md:text-5xl font-bold tracking-tight text-center mb-16 fade-in">{{ $t('landing.how.title') }}</h2>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-8 relative">
            <div class="hidden md:block absolute top-8 left-[15%] right-[15%] h-px bg-[var(--line)] z-0"></div>
            <div class="relative z-10 text-center space-y-4 fade-in">
              <div class="w-16 h-16 mx-auto rounded-full border border-[var(--line)] bg-[var(--bg)] flex items-center justify-center text-2xl font-bold">1</div>
              <h3 class="font-bold text-lg">{{ $t('landing.how.s1_title') }}</h3>
              <p class="text-sm text-[var(--muted)] px-4">{{ $t('landing.how.s1_desc') }}</p>
            </div>
            <div class="relative z-10 text-center space-y-4 fade-in" style="transition-delay: 100ms">
              <div class="w-16 h-16 mx-auto rounded-full border border-[var(--line)] bg-[var(--bg)] flex items-center justify-center text-2xl font-bold">2</div>
              <h3 class="font-bold text-lg">{{ $t('landing.how.s2_title') }}</h3>
              <p class="text-sm text-[var(--muted)] px-4">{{ $t('landing.how.s2_desc') }}</p>
            </div>
            <div class="relative z-10 text-center space-y-4 fade-in" style="transition-delay: 200ms">
              <div class="w-16 h-16 mx-auto rounded-full border border-[var(--line)] bg-[var(--bg)] flex items-center justify-center text-2xl font-bold">3</div>
              <h3 class="font-bold text-lg">{{ $t('landing.how.s3_title') }}</h3>
              <p class="text-sm text-[var(--muted)] px-4">{{ $t('landing.how.s3_desc') }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- KEAMANAN -->
      <section class="py-20 md:py-32 bg-[var(--surface)] border-t border-[var(--line)]">
        <div class="max-w-[1120px] mx-auto px-6 text-center fade-in">
          <h2 class="text-3xl md:text-4xl font-bold tracking-tight mb-12">{{ $t('landing.security.title') }}</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 text-sm text-left">
            <div class="flex gap-3"><svg class="w-6 h-6 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg><p class="text-[var(--muted)]">{{ $t('landing.security.s1') }}</p></div>
            <div class="flex gap-3"><svg class="w-6 h-6 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path></svg><p class="text-[var(--muted)]">{{ $t('landing.security.s2') }}</p></div>
            <div class="flex gap-3"><svg class="w-6 h-6 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg><p class="text-[var(--muted)]">{{ $t('landing.security.s3') }}</p></div>
            <div class="flex gap-3"><svg class="w-6 h-6 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636"></path></svg><p class="text-[var(--muted)]">{{ $t('landing.security.s4') }}</p></div>
          </div>
        </div>
      </section>

      <!-- HARGA -->
      <section id="harga" class="py-20 md:py-32 border-t border-[var(--line)]">
        <div class="max-w-[1120px] mx-auto px-6 text-center fade-in">
          <h2 class="text-3xl md:text-5xl font-bold tracking-tight mb-4">{{ $t('landing.pricing.title') }}</h2>
          <p class="text-[var(--muted)] max-w-2xl mx-auto mb-16">{{ $t('landing.pricing.desc') }}</p>
          
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6 text-left max-w-5xl mx-auto">
            <div class="border-2 border-[var(--text)] rounded-xl p-8 space-y-4 bg-[var(--bg)] relative">
              <!-- Badge dihapus, diganti border tebal aja -->
              <h3 class="text-lg font-bold">{{ $t('landing.pricing.p1_title') }}</h3>
              <p class="text-sm text-[var(--muted)]">{{ $t('landing.pricing.p1_desc') }}</p>
            </div>
            <div class="border border-[var(--line)] rounded-xl p-8 space-y-4 bg-[var(--surface)]">
              <h3 class="text-lg font-bold">{{ $t('landing.pricing.p2_title') }}</h3>
              <p class="text-sm text-[var(--muted)]">{{ $t('landing.pricing.p2_desc') }}</p>
            </div>
            <div class="border border-[var(--line)] rounded-xl p-8 space-y-4 bg-[var(--surface)]">
              <h3 class="text-lg font-bold">{{ $t('landing.pricing.p3_title') }}</h3>
              <p class="text-sm text-[var(--muted)]">{{ $t('landing.pricing.p3_desc') }}</p>
            </div>
          </div>
          <p class="text-xs text-[var(--muted)] mt-8 max-w-3xl mx-auto">{{ $t('landing.pricing.note') }}</p>
          <a href="https://app.ixiera.id/login" class="inline-block mt-8 px-10 py-4 rounded-full text-lg font-bold bg-[var(--text)] text-[var(--bg)] hover:opacity-90 transition">{{ $t('landing.pricing.cta') }}</a>
        </div>
      </section>

      <!-- FAQ -->
      <section id="faq" class="py-20 md:py-32 bg-[var(--surface)] border-t border-[var(--line)]">
        <div class="max-w-3xl mx-auto px-6 fade-in">
          <h2 class="text-3xl font-bold tracking-tight text-center mb-12">{{ $t('landing.faq.title') }}</h2>
          <div class="space-y-2">
            <div v-for="i in 9" :key="i" class="border border-[var(--line)] rounded-lg bg-[var(--bg)] overflow-hidden">
              <button @click="faqOpen = faqOpen === i ? null : i" class="w-full px-6 py-4 text-left flex justify-between items-center font-bold hover:bg-[var(--surface-2)] transition">
                <span>{{ $t('landing.faq.q' + i) }}</span>
                <svg class="w-5 h-5 transition-transform duration-300" :class="{'rotate-180': faqOpen === i}" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
              </button>
              <div v-if="faqOpen === i" class="px-6 pb-4 text-sm text-[var(--muted)] leading-relaxed">{{ $t('landing.faq.a' + i) }}</div>
            </div>
          </div>
        </div>
      </section>

      <!-- CTA PENUTUP -->
      <section class="py-24 text-center px-6 border-t border-[var(--line)]">
        <div class="max-w-3xl mx-auto space-y-8 fade-in">
          <h2 class="text-3xl md:text-5xl font-bold tracking-tight">{{ $t('landing.cta_end.title') }}</h2>
          <a href="https://app.ixiera.id/login" class="inline-flex items-center gap-2 px-10 py-4 rounded-full text-lg font-bold bg-[var(--text)] text-[var(--bg)] hover:opacity-90 transition">{{ $t('landing.cta_end.btn') }}</a>
        </div>
      </section>

    </main>

    <!-- FOOTER -->
    <footer class="py-12 border-t border-[var(--line)] text-center text-sm text-[var(--muted)]">
      <div class="flex flex-wrap justify-center items-center gap-4 mb-4">
        <a href="mailto:contact@ixiera.id" class="hover:text-[var(--text)] transition-colors">{{ $t('landing.footer.email') }}</a>
        <span class="hidden sm:inline text-[var(--line)]">·</span>
        <RouterLink to="/privacy" class="hover:text-[var(--text)] transition-colors">{{ $t('landing.footer.privacy') }}</RouterLink>
        <span class="hidden sm:inline text-[var(--line)]">·</span>
        <RouterLink to="/terms" class="hover:text-[var(--text)] transition-colors">{{ $t('landing.footer.terms') }}</RouterLink>
        <span class="hidden sm:inline text-[var(--line)]">·</span>
        <RouterLink to="/data-deletion" class="hover:text-[var(--text)] transition-colors">{{ $t('landing.footer.delete') }}</RouterLink>
      </div>
      <p class="text-xs text-[var(--muted)]">&copy; 2026 Ixiera.</p>
      <p class="text-[10px] max-w-2xl mx-auto px-4 mt-2">{{ $t('landing.footer.disclaimer') }}</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { RouterLink } from 'vue-router'
import { useTheme } from '../composables/useTheme'
import { Sun, Moon } from 'lucide-vue-next'

const { locale } = useI18n()
const { theme, toggle: toggleTheme } = useTheme()
const mobileMenuOpen = ref(false)
const faqOpen = ref<number | null>(1)

// STATE BUAT MOCKUP INTERAKTIF
const mockReplyMode = ref('manual') 
const activeMockTab = ref('best')
const isGenerating = ref(false)
const generatedPlan = ref(false)

// Fungsi simulasi loading generate content
function simulateGenerate() {
  isGenerating.value = true
  generatedPlan.value = false
  setTimeout(() => {
    isGenerating.value = false
    generatedPlan.value = true
  }, 1000)
}

// STATE DATA HARDCODE
const hookData = ref([
  { label: 'Question', er: 2.92, n: 6 },
  { label: 'Story', er: 1.36, n: 32 },
  { label: 'Statement', er: 0.90, n: 10 },
  { label: 'List', er: 0.00, n: 2 }
])
const lengthData = ref([
  { label: '300–500 char', er: 2.96, n: 10 },
  { label: '100–300 char', er: 1.12, n: 25 },
])

// Fungsi hitung lebar bar (max 3.5%)
function getBarWidth(er: number) {
  const maxER = 3.5
  const pct = (er / maxER) * 100
  return `${Math.min(pct, 100)}%`
}

function toggleLang() {
  locale.value = locale.value === 'id' ? 'en' : 'id'
  localStorage.setItem('app_lang', locale.value)
}

onMounted(() => {
  // Fade-in Animation
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible')
        entry.target.querySelectorAll('.bar-grow').forEach(bar => {
          const width = (bar as HTMLElement).style.width;
          (bar as HTMLElement).style.width = '0%';
          setTimeout(() => {
            (bar as HTMLElement).style.width = width;
          }, 50);
        })
        observer.unobserve(entry.target)
      }
    })
  }, { threshold: 0.1 })

  document.querySelectorAll('.fade-in').forEach(el => observer.observe(el))
})
</script>

<style>
:root {
  --bg: #000000; --surface: #0A0A0A; --surface-2: #141414;
  --line: #262626; --text: #FFFFFF; --muted: #A3A3A3;
  --faint: #8A8A8A; --bar-dim: #404040;
}
html:not(.dark) {
  --bg: #FFFFFF; --surface: #FAFAFA; --surface-2: #F2F2F2;
  --line: #E5E5E5; --text: #0A0A0A; --muted: #525252;
  --faint: #737373; --bar-dim: #C4C4C4;
}
body {
  background-color: var(--bg);
  color: var(--text);
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  font-variant-numeric: tabular-nums;
  -webkit-font-smoothing: antialiased;
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
.bar-grow {
  transition: width 800ms cubic-bezier(0.4, 0, 0.2, 1);
}
@media (prefers-reduced-motion: reduce) {
  .fade-in, .bar-grow {
    transition: none !important;
    animation: none !important;
    opacity: 1 !important;
    transform: none !important;
  }
}
</style>
