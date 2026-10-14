<template>
  <div v-if="loading" class="h-screen w-screen flex items-center justify-center theme-bg">
    <p class="text-xs font-medium tracking-widest animate-pulse theme-text-muted">LOADING...</p>
  </div>

  <div v-else-if="!session" class="min-h-screen theme-bg">
    <RouterView />
  </div>

  <div v-else class="flex h-screen overflow-hidden theme-bg theme-text">
    <AppSidebar
      :open="sidebarOpen"
      :email="session.user.email"
      @close="sidebarOpen = false"
      @logout="handleLogout"
    />

    <div class="flex-1 flex flex-col min-w-0">
      <header class="md:hidden flex items-center justify-between h-16 px-4 border-b theme-border theme-bg">
        <div class="flex items-center gap-2">
          <div class="w-7 h-7 flex items-center justify-center rounded text-xs font-black theme-accent">IX</div>
          <span class="font-bold tracking-tight text-sm">ixiera.id</span>
        </div>
        <button @click="sidebarOpen = true" class="p-2 rounded-md theme-bg-hover">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
      </header>

      <main class="flex-1 overflow-y-auto p-4 md:p-8">
        <div class="max-w-5xl mx-auto">
          <RouterView />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { RouterView, useRouter } from 'vue-router'
import { supabase } from './lib/supabase'
import AppSidebar from './components/AppSidebar.vue'
import { useTheme } from './composables/useTheme'

const router = useRouter()
const session = ref<any>(null)
const loading = ref(true)
const sidebarOpen = ref(false)

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
