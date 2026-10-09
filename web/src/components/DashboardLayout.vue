<template>
  <div class="min-h-screen flex bg-slate-950 text-slate-100">
    <!-- Sidebar -->
    <aside class="w-64 border-r border-slate-800 bg-slate-900/50 p-4 flex flex-col justify-between">
      <div>
        <div class="text-xl font-bold text-indigo-400 mb-8 px-2">Ixiera Threads</div>
        <nav class="space-y-1">
          <router-link to="/" class="flex items-center gap-3 px-3 py-2 rounded-lg text-slate-300 hover:bg-slate-800 hover:text-white transition">
            Dashboard
          </router-link>
          <router-link to="/composer" class="flex items-center gap-3 px-3 py-2 rounded-lg text-slate-300 hover:bg-slate-800 hover:text-white transition">
            Composer
          </router-link>
          <router-link to="/inbox" class="flex items-center gap-3 px-3 py-2 rounded-lg text-slate-300 hover:bg-slate-800 hover:text-white transition">
            Inbox & Auto-Reply
          </router-link>
          <router-link to="/settings" class="flex items-center gap-3 px-3 py-2 rounded-lg text-slate-300 hover:bg-slate-800 hover:text-white transition">
            Settings
          </router-link>
        </nav>
      </div>
      <div class="text-xs text-slate-500 px-2">
        Ixiera.id &copy; 2026
      </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 p-8 overflow-y-auto">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
</script>
