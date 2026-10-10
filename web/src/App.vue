<template>
  <div class="min-h-screen bg-white text-zinc-900 font-sans antialiased selection:bg-zinc-900 selection:text-white">
    <!-- Header Navbar (Tampil jika sudah login) -->
    <header v-if="session" class="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-zinc-200">
      <div class="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
        <div class="flex items-center space-x-8">
          <router-link to="/dashboard" class="flex items-center space-x-2">
            <span class="bg-black text-white px-2 py-1 rounded text-xs font-black tracking-widest uppercase">IX</span>
            <span class="font-bold text-base tracking-tight text-black">ixiera.id</span>
          </router-link>

          <nav class="hidden md:flex items-center space-x-1 text-xs font-semibold">
            <router-link to="/dashboard" active-class="bg-zinc-100 text-black" class="px-3 py-2 rounded-lg text-zinc-600 hover:text-black transition">Dashboard</router-link>
            <router-link to="/composer" active-class="bg-zinc-100 text-black" class="px-3 py-2 rounded-lg text-zinc-600 hover:text-black transition">Composer</router-link>
            <router-link to="/inbox" active-class="bg-zinc-100 text-black" class="px-3 py-2 rounded-lg text-zinc-600 hover:text-black transition">Inbox</router-link>
            <router-link to="/settings" active-class="bg-zinc-100 text-black" class="px-3 py-2 rounded-lg text-zinc-600 hover:text-black transition">Settings</router-link>
          </nav>
        </div>

        <div class="flex items-center space-x-3">
          <span class="text-xs font-medium text-zinc-500 hidden sm:inline">{{ session.user.email }}</span>
          <button @click="handleLogout" class="bg-zinc-100 hover:bg-zinc-200 text-black text-xs font-bold px-3.5 py-2 rounded-lg border border-zinc-300 transition">
            Logout
          </button>
        </div>
      </div>

      <!-- Mobile Navigation Bar -->
      <div class="md:hidden border-t border-zinc-100 flex items-center justify-around py-2 px-2 text-xs font-medium bg-white">
        <router-link to="/dashboard" active-class="font-bold text-black border-b-2 border-black" class="py-1 text-zinc-500">Dashboard</router-link>
        <router-link to="/composer" active-class="font-bold text-black border-b-2 border-black" class="py-1 text-zinc-500">Composer</router-link>
        <router-link to="/inbox" active-class="font-bold text-black border-b-2 border-black" class="py-1 text-zinc-500">Inbox</router-link>
        <router-link to="/settings" active-class="font-bold text-black border-b-2 border-black" class="py-1 text-zinc-500">Settings</router-link>
      </div>
    </header>

    <!-- Main Content Area -->
    <main class="max-w-6xl mx-auto px-4 py-8">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { supabase } from './lib/supabase'

const router = useRouter()
const session = ref<any>(null)

async function handleLogout() {
  await supabase.auth.signOut()
  router.push('/login')
}

onMounted(async () => {
  const { data } = await supabase.auth.getSession()
  session.value = data.session

  supabase.auth.onAuthStateChange((_event, _session) => {
    session.value = _session
  })
})
</script>
