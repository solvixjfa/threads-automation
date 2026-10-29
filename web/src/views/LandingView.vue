<template>
  <div class="min-h-screen theme-bg theme-text overflow-x-hidden">
    
    <!-- NAVBAR -->
    <nav class="fixed top-0 w-full z-50 backdrop-blur-lg border-b theme-border" style="background: color-mix(in srgb, var(--bg) 80%, transparent);">
      <div class="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 flex items-center justify-center rounded text-sm font-black theme-accent">IX</div>
          <span class="font-bold tracking-tight text-lg">Ixiera</span>
        </div>
        <div class="flex items-center gap-4">
          <RouterLink to="/login" class="text-sm font-medium theme-text-muted hover:theme-text transition">Masuk</RouterLink>
          <RouterLink to="/login" class="btn btn-primary btn-sm rounded-full px-5">Mulai Gratis</RouterLink>
        </div>
      </div>
    </nav>

    <!-- HERO SECTION -->
    <section class="pt-32 pb-20 px-6 relative overflow-hidden">
      <!-- Background Glow -->
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] rounded-full opacity-20 blur-[100px] pointer-events-none" style="background: var(--accent);"></div>
      
      <div class="max-w-4xl mx-auto text-center relative z-10 space-y-6">
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full border theme-border text-xs font-medium theme-text-muted bg-[var(--bg-sec)]">
          <span class="w-2 h-2 rounded-full animate-pulse" style="background: var(--success);"></span>
          Sedang dalam tahap Beta (Gratis)
        </div>
        
        <h1 class="text-4xl md:text-6xl font-black tracking-tight leading-tight">
          Fokus Berkarya,<br/>
          <span style="color: var(--accent);">Biarkan Ixiera Urus Sisanya.</span>
        </h1>
        
        <p class="text-lg md:text-xl theme-text-muted max-w-2xl mx-auto leading-relaxed">
          Teman setia untuk kreator Threads. Rencanakan konten, balas interaksi dengan hangat, dan pahami audiens Anda—tanpa harus kehabisan energi.
        </p>

        <div class="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
          <RouterLink to="/login" class="btn btn-primary w-full sm:w-auto px-8 py-3 rounded-xl text-base shadow-lg hover:shadow-xl transition-all">
            Mulai Berkarya Sekarang
          </RouterLink>
          <a href="#fitur" class="btn btn-secondary w-full sm:w-auto px-8 py-3 rounded-xl text-base">
            Pelajari Fitur
          </a>
        </div>
      </div>
    </section>

    <!-- MOCKUP UI (PREVIEW APLIKASI) -->
    <section class="px-6 pb-24 relative">
      <div class="max-w-5xl mx-auto rounded-2xl border theme-border shadow-2xl overflow-hidden relative" style="background: var(--bg-sec);">
        <!-- Window Bar -->
        <div class="h-10 border-b theme-border flex items-center px-4 gap-2" style="background: var(--bg);">
          <div class="w-3 h-3 rounded-full bg-red-500/80"></div>
          <div class="w-3 h-3 rounded-full bg-yellow-500/80"></div>
          <div class="w-3 h-3 rounded-full bg-green-500/80"></div>
        </div>
        
        <!-- Mockup Content -->
        <div class="flex h-[400px] md:h-[500px]">
          <!-- Fake Sidebar -->
          <div class="w-16 md:w-48 border-r theme-border p-4 hidden sm:flex flex-col gap-4" style="background: var(--bg);">
            <div class="h-8 w-8 rounded bg-[var(--accent)] opacity-20"></div>
            <div class="h-8 w-full rounded bg-[var(--bg-sec)]"></div>
            <div class="h-8 w-full rounded bg-[var(--bg-sec)]"></div>
            <div class="h-8 w-3/4 rounded bg-[var(--bg-sec)]"></div>
          </div>
          <!-- Fake Main Content -->
          <div class="flex-1 p-6 space-y-6">
            <div class="flex justify-between items-center">
              <div class="space-y-2">
                <div class="h-6 w-32 rounded bg-[var(--bg-sec)]"></div>
                <div class="h-3 w-48 rounded bg-[var(--bg-sec)] opacity-50"></div>
              </div>
              <div class="h-8 w-24 rounded-lg bg-[var(--accent)] opacity-80"></div>
            </div>
            
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div v-for="i in 4" :key="i" class="p-4 rounded-xl border theme-border" style="background: var(--bg);">
                <div class="h-3 w-16 rounded bg-[var(--bg-sec)] mb-2"></div>
                <div class="h-6 w-12 rounded bg-[var(--bg-sec)]"></div>
              </div>
            </div>

            <div class="p-6 rounded-xl border theme-border h-48 flex items-end gap-2" style="background: var(--bg);">
               <div v-for="i in 12" :key="i" class="flex-1 rounded-t bg-[var(--accent)] opacity-60" :style="{ height: (20 + Math.random() * 80) + '%' }"></div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- FITUR SECTION -->
    <section id="fitur" class="py-24 px-6" style="background: var(--bg-sec);">
      <div class="max-w-6xl mx-auto space-y-16">
        <div class="text-center space-y-4 max-w-2xl mx-auto">
          <h2 class="text-3xl font-bold tracking-tight">Dirancang untuk Ketenangan Pikiran Anda</h2>
          <p class="theme-text-muted text-lg">Semua yang Anda butuhkan untuk mengelola Threads, tanpa harus pusing dengan hal teknis.</p>
        </div>

        <div class="grid md:grid-cols-3 gap-8">
          <!-- Fitur 1 -->
          <div class="card p-8 space-y-4 hover:border-current transition-colors group">
            <div class="w-12 h-12 rounded-xl flex items-center justify-center text-2xl mb-2" style="background: color-mix(in srgb, var(--accent) 15%, transparent); color: var(--accent);">✨</div>
            <h3 class="text-xl font-bold">Ide Tak Pernah Habis</h3>
            <p class="theme-text-muted text-sm leading-relaxed">
              AI kami membantu merancang rencana konten 3 hari ke depan. Anda hanya perlu meninjau, memilih, dan memposting.
            </p>
          </div>

          <!-- Fitur 2 -->
          <div class="card p-8 space-y-4 hover:border-current transition-colors group">
            <div class="w-12 h-12 rounded-xl flex items-center justify-center text-2xl mb-2" style="background: color-mix(in srgb, var(--success) 15%, transparent); color: var(--success);">💬</div>
            <h3 class="text-xl font-bold">Interaksi Tetap Hangat</h3>
            <p class="theme-text-muted text-sm leading-relaxed">
              Balas komentar secara otomatis dengan gaya bahasa Anda sendiri. Hemat waktu, tanpa mengorbankan kedekatan dengan audiens.
            </p>
          </div>

          <!-- Fitur 3 -->
          <div class="card p-8 space-y-4 hover:border-current transition-colors group">
            <div class="w-12 h-12 rounded-xl flex items-center justify-center text-2xl mb-2" style="background: color-mix(in srgb, var(--warning) 15%, transparent); color: var(--warning);">📊</div>
            <h3 class="text-xl font-bold">Pahami Waktu Emas Anda</h3>
            <p class="theme-text-muted text-sm leading-relaxed">
              Ketahui jam dan topik terbaik berdasarkan data Anda sendiri. Posting di waktu yang tepat untuk hasil maksimal.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA SECTION -->
    <section class="py-24 px-6 text-center space-y-8">
      <div class="max-w-2xl mx-auto space-y-4">
        <h2 class="text-3xl md:text-4xl font-bold tracking-tight">Siap Menghemat Waktu Anda?</h2>
        <p class="theme-text-muted text-lg">Bergabunglah dengan kreator lain yang sudah mulai tenang dalam berkarya.</p>
      </div>
      <RouterLink to="/login" class="btn btn-primary inline-flex px-10 py-4 rounded-xl text-lg font-bold shadow-lg hover:-translate-y-1 transition-transform">
        Mulai Gunakan Ixiera (Gratis)
      </RouterLink>
    </section>

    <!-- FOOTER -->
    <footer class="py-8 text-center border-t theme-border text-xs theme-text-muted">
      <p>&copy; {{ new Date().getFullYear() }} Ixiera. Dibuat dengan tenang untuk para kreator.</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
// Gak butuh logic berat, ini murni UI
</script>
