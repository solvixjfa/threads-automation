<template>
  <div v-if="loading" class="h-screen w-screen flex items-center justify-center bg-slate-50">
    <p class="text-xs font-medium text-slate-400 tracking-widest animate-pulse">MEMUAT SISTEM...</p>
  </div>
  
  <div v-else-if="!session" class="min-h-screen bg-slate-50">
    <router-view />
  </div>

  <div v-else class="flex h-screen bg-slate-50 font-sans text-slate-900 selection:bg-indigo-600 selection:text-white overflow-hidden">
    
    <!-- Mobile Header -->
    <header class="md:hidden absolute top-0 left-0 right-0 h-16 bg-white border-b border-slate-200 flex items-center justify-between px-4 z-20">
      <div class="flex items-center gap-3">
        <button @click="sidebarOpen = true" class="text-slate-600 hover:text-indigo-600 focus:outline-none p-1">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
        <div class="flex items-center gap-2">
          <span class="bg-indigo-600 text-white px-2 py-1 rounded text-[10px] font-black tracking-widest uppercase">IX</span>
          <span class="font-bold text-sm tracking-tight text-slate-800">ixiera.id</span>
        </div>
      </div>
    </header>

    <!-- Overlay Mobile Sidebar -->
    <div v-if="sidebarOpen" @click="sidebarOpen = false" class="md:hidden fixed inset-0 bg-slate-900/40 z-30 transition-opacity"></div>

    <!-- Sidebar (Desktop & Mobile) -->
    <aside 
      :class="sidebarOpen ? 'translate-x-0' : '-translate-x-full'"
      class="md:translate-x-0 fixed md:static inset-y-0 left-0 z-40 w-64 bg-white border-r border-slate-200 flex flex-col transition-transform duration-300 ease-in-out shadow-2xl md:shadow-none"
    >
      <div class="p-6 hidden md:flex items-center gap-3 border-b border-slate-100">
        <span class="bg-indigo-600 text-white px-2 py-1 rounded text-xs font-black tracking-widest uppercase shadow-sm">IX</span>
        <span class="font-bold text-lg tracking-tight text-slate-800">ixiera.id</span>
      </div>
      
      <div class="md:hidden p-4 border-b border-slate-100 flex justify-end">
        <button @click="sidebarOpen = false" class="p-2 text-slate-400 hover:text-slate-700 bg-slate-50 rounded-lg">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <nav class="flex-1 px-4 py-6 space-y-1.5 overflow-y-auto">
        <router-link @click="sidebarOpen = false" to="/dashboard" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-slate-500 hover:text-indigo-600 hover:bg-indigo-50 transition" active-class="bg-indigo-50 text-indigo-700 font-bold">Dashboard</router-link>
        <router-link @click="sidebarOpen = false" to="/composer" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-slate-500 hover:text-indigo-600 hover:bg-indigo-50 transition" active-class="bg-indigo-50 text-indigo-700 font-bold">Composer</router-link>
        <router-link @click="sidebarOpen = false" to="/inbox" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-slate-500 hover:text-indigo-600 hover:bg-indigo-50 transition" active-class="bg-indigo-50 text-indigo-700 font-bold">Inbox</router-link>
        <router-link @click="sidebarOpen = false" to="/settings" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-slate-500 hover:text-indigo-600 hover:bg-indigo-50 transition" active-class="bg-indigo-50 text-indigo-700 font-bold">Settings</router-link>
      </nav>
      
      <div class="p-4 border-t border-slate-100 mt-auto">
        <div class="px-3 pb-3 truncate text-xs text-slate-400">{{ session.user.email }}</div>
        <button @click="handleLogout" class="w-full text-left px-3 py-2 text-sm font-bold text-rose-600 hover:bg-rose-50 rounded-lg transition">Keluar</button>
      </div>
    </aside>

    <!-- Main Content Area -->
    <main class="flex-1 overflow-y-auto pt-16 md:pt-0 p-4 md:p-8 bg-slate-50/50 relative">
      <div class="max-w-4xl mx-auto">
        <router-view />
      </div>
    </main>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { supabase } from './lib/supabase'

const router = useRouter()
const session = ref<any>(null)
const loading = ref(true)
const sidebarOpen = ref(false)

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
