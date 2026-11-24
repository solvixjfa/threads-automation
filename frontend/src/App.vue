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
      :isAdmin="isUserAdmin"
      @close="sidebarOpen = false"
      @logout="handleLogout"
      class="hidden md:flex"
    />

    <div class="flex-1 flex flex-col min-w-0 w-full">
      <!-- TOP BAR MOBILE UNTUK SWITCH AKUN -->
      <header class="md:hidden sticky top-0 z-30 flex items-center justify-between gap-2 px-4 py-2.5 border-b theme-border theme-bg/95 backdrop-blur-sm">
        <div class="flex-1 min-w-0 max-w-[230px]">
          <AccountSwitcher />
        </div>
        <RouterLink
          v-if="isUserAdmin"
          to="/admin"
          class="px-2.5 py-1.5 rounded-lg text-xs font-bold text-white bg-black dark:bg-white dark:text-black shrink-0"
        >
          Admin
        </RouterLink>
      </header>

      <main class="flex-1 p-4 md:p-8 w-full pb-20 md:pb-8">
        <div class="max-w-5xl mx-auto h-full flex flex-col w-full">
          <RouterView :key="accountStore.activeAccountId || 'no-account'" />
        </div>
      </main>
    </div>
    <BottomNav />
  </div>
  <NotifyOverlay />
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { RouterView, RouterLink, useRouter, useRoute } from 'vue-router'
import { supabase } from './lib/supabase'
import AppSidebar from './components/AppSidebar.vue'
import AccountSwitcher from './components/AccountSwitcher.vue'
import NotifyOverlay from './components/NotifyOverlay.vue'
import BottomNav from './components/BottomNav.vue'
import { useTheme } from './composables/useTheme'
import { useAccountStore } from './stores/accounts'

const router = useRouter()
const route = useRoute()
const accountStore = useAccountStore()

const session = ref<any>(null)
const loading = ref(true)
const sidebarOpen = ref(false)

const isAdminPage = computed(() => route.path.startsWith('/admin'))
const isUserAdmin = computed(() => {
  return session.value?.user?.email === 'jepri097@gmail.com' || accountStore.effectiveRole === 'admin'
})

const { initTheme } = useTheme()
initTheme()

async function handleLogout() {
  await supabase.auth.signOut()
  accountStore.reset()
  session.value = null
  router.push('/login')
}

onMounted(async () => {
  const { data } = await supabase.auth.getSession()
  session.value = data.session
  if (data.session) {
    await accountStore.fetchAccounts(true)
  }
  loading.value = false

  supabase.auth.onAuthStateChange(async (_event, _session) => {
    session.value = _session
    if (_session) {
      await accountStore.fetchAccounts(true)
    } else {
      accountStore.reset()
    }
  })
})
</script>
