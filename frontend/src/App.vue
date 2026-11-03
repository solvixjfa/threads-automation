<template>
  <div v-if="loading" class="h-screen w-screen flex items-center justify-center theme-bg">
    <p class="text-xs font-medium tracking-widest animate-pulse theme-text-muted">LOADING...</p>
  </div>

  <div v-else-if="!session" class="min-h-screen w-full overflow-x-hidden theme-bg">
    <RouterView />
  </div>

  <div v-else-if="isAdminPage" class="min-h-screen w-full overflow-x-hidden theme-bg theme-text">
    <RouterView />
  </div>

  <!-- LAYOUT UTAMA -->
  <div v-else class="flex min-h-screen w-full theme-bg theme-text">
    <AppSidebar
      :open="sidebarOpen"
      :email="session.user.email"
      :isAdmin="session.user.email === 'jepri097@gmail.com'"
      @close="sidebarOpen = false"
      @logout="handleLogout"
    />

    <!-- min-w-0 wajib biar sidebar gak narik layar -->
    <div class="flex-1 flex flex-col min-w-0 w-full">
      <header class="md:hidden flex items-center justify-between h-16 px-4 border-b theme-border theme-bg shrink-0 z-30 sticky top-0">
        <div class="flex items-center gap-2">
          <div v-if="userAvatar" class="w-7 h-7 rounded-full overflow-hidden shrink-0 border border-[var(--border)]">
            <img :src="userAvatar" class="w-full h-full object-cover" />
          </div>
          <div v-else class="w-7 h-7 flex items-center justify-center rounded text-xs font-black theme-accent shrink-0">IX</div>
          <span v-if="threadsUsername" class="font-bold tracking-tight text-sm">@{{ threadsUsername }}</span>
        </div>
        <button @click="sidebarOpen = true" class="p-2 rounded-md theme-bg-hover">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
      </header>

      <!-- p-4 disini biar ada jarak, flex-1 biar narik ke bawah -->
      <main class="flex-1 p-4 md:p-8 w-full pb-20 md:pb-8">
        <div class="max-w-5xl mx-auto h-full flex flex-col w-full">
          <RouterView />
        </div>
      </main>
    </div>
    <BottomNav />
  </div>
  <NotifyOverlay />
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { RouterView, useRouter, useRoute } from 'vue-router'
import { supabase } from './lib/supabase'
import AppSidebar from './components/AppSidebar.vue'
import NotifyOverlay from './components/NotifyOverlay.vue'
import BottomNav from './components/BottomNav.vue'
import { useTheme } from './composables/useTheme'

const router = useRouter()
const route = useRoute()
const session = ref<any>(null)
const userAvatar = ref('')
const threadsUsername = ref('')
const loading = ref(true)
const sidebarOpen = ref(false)

const isAdminPage = computed(() => route.path.startsWith('/admin'))

const { initTheme } = useTheme()
initTheme()

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
