<template>
  <div class="min-h-screen bg-[var(--bg)] text-[var(--text)] font-sans">
    <AppNavbar />
    <main class="pt-32 pb-24 px-6 max-w-[800px] mx-auto text-center">
      <h1 class="font-display text-5xl md:text-6xl mb-6">Tiga langkah <br><span class="italic text-[var(--muted)]">untuk mulai.</span></h1>
      <p class="text-lg text-[var(--muted)] mb-16">Dari nol sampai otomatisasi penuh, kurang dari 10 menit.</p>
      
      <div class="space-y-12 text-left">
        <div class="border border-[var(--line)] bg-[var(--surface)] rounded-2xl p-8 flex gap-6">
          <div class="w-12 h-12 shrink-0 rounded-full bg-[var(--text)] text-[var(--bg)] flex items-center justify-center text-xl font-bold">1</div>
          <div>
            <h3 class="text-xl font-bold mb-2">Daftar & Hubungkan Threads</h3>
            <p class="text-[var(--muted)]">Buat akun, lalu login menggunakan OAuth resmi Meta. Kami tidak pernah menyimpan password Threads kamu.</p>
          </div>
        </div>
        <div class="border border-[var(--line)] bg-[var(--surface)] rounded-2xl p-8 flex gap-6">
          <div class="w-12 h-12 shrink-0 rounded-full bg-[var(--text)] text-[var(--bg)] flex items-center justify-center text-xl font-bold">2</div>
          <div>
            <h3 class="text-xl font-bold mb-2">Atur Gaya Bahasa</h3>
            <p class="text-[var(--muted)]">Tulis aturan dan gaya bahasa kamu di Knowledge Base. AI akan meniru gaya tersebut setiap kali membuat draf atau membalas komentar.</p>
          </div>
        </div>
        <div class="border border-[var(--line)] bg-[var(--surface)] rounded-2xl p-8 flex gap-6">
          <div class="w-12 h-12 shrink-0 rounded-full bg-[var(--text)] text-[var(--bg)] flex items-center justify-center text-xl font-bold">3</div>
          <div>
            <h3 class="text-xl font-bold mb-2">Review & Otomatisasi</h3>
            <p class="text-[var(--muted)]">Pilih mode Review Manual (setujui dulu sebelum tayang) atau Full Auto. Pantau performanya di halaman Analytics.</p>
          </div>
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
