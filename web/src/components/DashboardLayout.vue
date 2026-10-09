<template>
  <div class="min-h-screen bg-black text-slate-100 flex flex-col md:flex-row">
    <!-- Desktop Sidebar (Hidden on Mobile) -->
    <aside class="hidden md:flex md:w-64 border-r border-zinc-800 bg-black/50 p-6 flex-col justify-between shrink-0 min-h-screen sticky top-0">
      <div class="space-y-8">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-full bg-white text-black font-black flex items-center justify-center text-sm shadow-md">
            IX
          </div>
          <span class="text-lg font-bold tracking-tight text-white">Ixiera Threads</span>
        </div>

        <nav class="space-y-1.5">
          <router-link
            to="/"
            exact-active-class="bg-zinc-900 text-white font-semibold border-zinc-700"
            class="flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm text-zinc-400 hover:text-white hover:bg-zinc-900/60 border border-transparent transition-all duration-200"
          >
            Dashboard
          </router-link>
          <router-link
            to="/composer"
            exact-active-class="bg-zinc-900 text-white font-semibold border-zinc-700"
            class="flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm text-zinc-400 hover:text-white hover:bg-zinc-900/60 border border-transparent transition-all duration-200"
          >
            Composer
          </router-link>
          <router-link
            to="/inbox"
            exact-active-class="bg-zinc-900 text-white font-semibold border-zinc-700"
            class="flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm text-zinc-400 hover:text-white hover:bg-zinc-900/60 border border-transparent transition-all duration-200"
          >
            Inbox & Auto-Reply
          </router-link>
          <router-link
            to="/settings"
            exact-active-class="bg-zinc-900 text-white font-semibold border-zinc-700"
            class="flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm text-zinc-400 hover:text-white hover:bg-zinc-900/60 border border-transparent transition-all duration-200"
          >
            Settings
          </router-link>
        </nav>
      </div>

      <div class="text-xs text-zinc-500 font-mono">
        Ixiera.id &copy; 2026
      </div>
    </aside>

    <!-- Mobile Top Header -->
    <header class="md:hidden flex items-center justify-between px-5 py-4 border-b border-zinc-800 bg-black sticky top-0 z-40">
      <div class="flex items-center gap-2.5">
        <div class="w-7 h-7 rounded-full bg-white text-black font-black flex items-center justify-center text-xs">
          IX
        </div>
        <span class="font-bold text-sm tracking-tight text-white">Ixiera Threads</span>
      </div>
    </header>

    <!-- Main Content Area -->
    <main class="flex-1 p-4 sm:p-6 md:p-10 max-w-7xl w-full mx-auto pb-24 md:pb-10">
      <router-view />
    </main>

    <!-- Mobile Bottom Navigation Bar -->
    <nav class="md:hidden fixed bottom-0 left-0 right-0 bg-black/90 backdrop-blur-md border-t border-zinc-800 flex items-center justify-around px-2 py-3 z-50">
      <router-link
        to="/"
        exact-active-class="text-white font-bold"
        class="flex flex-col items-center gap-1 text-[11px] text-zinc-500 transition"
      >
        <span>Dashboard</span>
      </router-link>
      <router-link
        to="/composer"
        exact-active-class="text-white font-bold"
        class="flex flex-col items-center gap-1 text-[11px] text-zinc-500 transition"
      >
        <span>Composer</span>
      </router-link>
      <router-link
        to="/inbox"
        exact-active-class="text-white font-bold"
        class="flex flex-col items-center gap-1 text-[11px] text-zinc-500 transition"
      >
        <span>Inbox</span>
      </router-link>
      <router-link
        to="/settings"
        exact-active-class="text-white font-bold"
        class="flex flex-col items-center gap-1 text-[11px] text-zinc-500 transition"
      >
        <span>Settings</span>
      </router-link>
    </nav>
  </div>
</template>

<script setup lang="ts">
</script>
