<template>
  <div class="min-h-screen bg-[var(--bg)] text-[var(--text)] font-sans">
    <AppNavbar />
    <main class="pt-32 pb-24 px-6 max-w-[1120px] mx-auto text-center">
      <h1 class="font-display text-5xl md:text-6xl mb-6">Harga yang <br><span class="italic">transparan.</span></h1>
      <p class="text-lg text-[var(--muted)] mb-16 max-w-2xl mx-auto">Mulai dengan trial 7 hari. Tanpa kartu kredit. Harga terkunci selama kamu berlangganan.</p>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto text-left">
        <!-- Card 1 -->
        <div class="border border-[var(--line)] rounded-2xl p-8 bg-[var(--surface)] flex flex-col">
          <h3 class="text-xl font-bold mb-2">Trial</h3>
          <p class="text-sm text-[var(--muted)] mb-6">Coba semua fitur.</p>
          <div class="text-4xl font-bold mb-6">Rp 0<span class="text-sm text-[var(--muted)] font-normal">/7 hari</span></div>
          <a href="https://app.ixiera.id/login" class="mt-auto block text-center py-3 rounded-full font-bold border border-[var(--line)] hover:bg-[var(--surface-2)] transition">Mulai Trial</a>
        </div>
        <!-- Card 2 -->
        <div class="border-2 border-[var(--text)] rounded-2xl p-8 bg-[var(--bg)] relative shadow-xl flex flex-col">
          <div class="absolute -top-3 left-1/2 -translate-x-1/2 bg-[var(--text)] text-[var(--bg)] text-[10px] font-bold px-3 py-1 rounded-full uppercase">Populer</div>
          <h3 class="text-xl font-bold mb-2">Pro</h3>
          <p class="text-sm text-[var(--muted)] mb-6">Untuk yang serius otomatisasi.</p>
          <div class="text-4xl font-bold mb-6">Rp 29rb<span class="text-sm text-[var(--muted)] font-normal">/bulan</span></div>
          <a href="https://app.ixiera.id/login" class="mt-auto block text-center py-3 rounded-full font-bold bg-[var(--text)] text-[var(--bg)] hover:opacity-90 transition">Pilih Pro</a>
        </div>
        <!-- Card 3 -->
        <div class="border border-[var(--line)] rounded-2xl p-8 bg-[var(--surface)] flex flex-col">
          <h3 class="text-xl font-bold mb-2">BYOK</h3>
          <p class="text-sm text-[var(--muted)] mb-6">Bawa API Key sendiri.</p>
          <div class="text-4xl font-bold mb-6">Rp 19rb<span class="text-sm text-[var(--muted)] font-normal">/bulan</span></div>
          <a href="https://app.ixiera.id/login" class="mt-auto block text-center py-3 rounded-full font-bold border border-[var(--line)] hover:bg-[var(--surface-2)] transition">Pilih BYOK</a>
        </div>
      </div>
    </main>
    <AppFooter />
  </div>
</template>
<script setup lang="ts">
import AppNavbar from '../components/layouts/AppNavbar.vue'
import AppFooter from '../components/layouts/AppFooter.vue'
</script>
