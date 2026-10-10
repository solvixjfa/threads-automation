<template>
  <div v-if="loading" class="h-screen w-screen flex items-center justify-center bg-zinc-50">
    <p class="text-xs font-medium text-zinc-400 tracking-widest animate-pulse">MEMUAT...</p>
  </div>
  
  <div v-else-if="!session" class="min-h-screen bg-zinc-50">
    <router-view />
  </div>

  <div v-else class="flex h-screen bg-zinc-50 font-sans text-zinc-900 selection:bg-zinc-900 selection:text-white">
    <!-- Desktop Sidebar -->
    <aside class="hidden md:flex flex-col w-64 bg-white border-r border-zinc-200 shadow-sm">
      <div class="p-6 flex items-center gap-3 border-b border-zinc-100">
        <span class="bg-black text-white px-2 py-1 rounded text-xs font-black tracking-widest uppercase">IX</span>
        <span class="font-bold text-lg tracking-tight">ixiera.id</span>
      </div>
      <nav class="flex-1 px-4 py-6 space-y-1">
        <router-link to="/dashboard" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-zinc-500 hover:text-black hover:bg-zinc-100 transition" active-class="bg-zinc-100 text-black font-bold">Dashboard</router-link>
        <router-link to="/composer" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-zinc-500 hover:text-black hover:bg-zinc-100 transition" active-class="bg-zinc-100 text-black font-bold">Composer</router-link>
        <router-link to="/inbox" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-zinc-500 hover:text-black hover:bg-zinc-100 transition" active-class="bg-zinc-100 text-black font-bold">Inbox</router-link>
        <router-link to="/settings" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-zinc-500 hover:text-black hover:bg-zinc-100 transition" active-class="bg-zinc-100 text-black font-bold">Settings</router-link>
      </nav>
      <div class="p-4 border-t border-zinc-100">
        <div class="px-3 pb-3 truncate text-xs text-zinc-400">{{ session.user.email }}</div>
        <button @click="handleLogout" class="w-full text-left px-3 py-2 text-sm font-bold text-red-600 hover:bg-red-50 rounded-lg transition">Keluar</button>
      </div>
    </aside>

    <!-- Mobile Layout & Main Content -->
    <div class="flex-1 flex flex-col min-w-0 overflow-hidden relative">
      <!-- Mobile Top Header -->
      <header class="md:hidden bg-white border-b border-zinc-200 p-4 flex justify-between items-center z-10 shadow-sm">
        <div class="flex items-center gap-2">
          <span class="bg-black text-white px-2 py-1 rounded-[4px] text-[10px] font-black tracking-widest uppercase">IX</span>
          <span class="font-bold text-sm tracking-tight">ixiera.id</span>
        </div>
        <button @click="handleLogout" class="text-xs font-bold text-red-500 bg-red-50 px-3 py-1.5 rounded-md">Keluar</button>
      </header>

      <!-- Main Content Area -->
      <main class="flex-1 overflow-y-auto p-4 md:p-8 pb-24 md:pb-8">
        <router-view />
      </main>

      <!-- Mobile Bottom Navigation -->
      <nav class="md:hidden absolute bottom-0 left-0 right-0 bg-white border-t border-zinc-200 flex justify-around pb-safe z-50 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)]">
        <router-link to="/dashboard" class="flex-1 py-3 text-center text-xs font-medium text-zinc-400" active-class="text-black font-bold border-t-2 border-black -mt-[1px]">Dash</router-link>
        <router-link to="/composer" class="flex-1 py-3 text-center text-xs font-medium text-zinc-400" active-class="text-black font-bold border-t-2 border-black -mt-[1px]">Tulis</router-link>
        <router-link to="/inbox" class="flex-1 py-3 text-center text-xs font-medium text-zinc-400" active-class="text-black font-bold border-t-2 border-black -mt-[1px]">Inbox</router-link>
        <router-link to="/settings" class="flex-1 py-3 text-center text-xs font-medium text-zinc-400" active-class="text-black font-bold border-t-2 border-black -mt-[1px]">Seting</router-link>
      </nav>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { supabase } from './lib/supabase'

const router = useRouter()
const session = ref<any>(null)
const loading = ref(true)

async function handleLogout() {
  await supabase.auth.signOut()
  session.value = null
  router.push('/login')
}

onMounted(async () => {
  const { data } = await supabase.auth.getSession()
  session.value = data.session
  loading.value = false

  supabase.auth.onAuthStateChange((_event, _session) => {
    session.value = _session
  })
})
</script>
