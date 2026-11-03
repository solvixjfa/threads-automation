<template>
  <div class="space-y-6 w-full max-w-full overflow-hidden">
    
    <!-- CARD: CONNECTED ACCOUNT (DENGAN AVATAR) -->
    <div class="card p-5 md:p-6 w-full">
      <div class="flex items-center justify-between pb-4 border-b theme-border mb-4">
        <div>
          <h2 class="text-lg font-bold">{{ $t('settings.account.title') }}</h2>
          <p class="text-xs theme-text-muted mt-1">{{ $t('settings.account.subtitle') }}</p>
        </div>
        <div v-if="account" class="flex items-center gap-2 px-3 py-1 rounded-full border theme-border bg-[var(--surface-2)] text-xs font-bold">
          <span class="w-2 h-2 rounded-full bg-green-500"></span>
          CONNECTED
        </div>
      </div>

      <div v-if="loading" class="animate-pulse h-20 bg-[var(--surface-2)] rounded-lg"></div>

      <div v-else-if="account" class="space-y-4">
        <!-- AVATAR & USERNAME SECTION -->
        <div class="flex items-center gap-4 p-4 rounded-xl border theme-border bg-[var(--surface-2)]">
          <div v-if="avatarUrl" class="w-16 h-16 rounded-full overflow-hidden shrink-0 border-2 theme-border">
            <img :src="avatarUrl" alt="Profile" class="w-full h-full object-cover" />
          </div>
          <div v-else class="w-16 h-16 rounded-full flex items-center justify-center bg-[var(--text)] text-[var(--bg)] text-xl font-black shrink-0">
            {{ threadsUsername ? threadsUsername.charAt(0).toUpperCase() : 'IX' }}
          </div>
          <div class="min-w-0">
            <h3 class="font-bold text-lg truncate">@{{ threadsUsername }}</h3>
            <p class="text-xs theme-text-muted">{{ $t('settings.account.ready') }}</p>
          </div>
        </div>

        <div class="flex justify-end pt-2">
          <button @click="handleConnect" class="btn btn-secondary text-sm">
            {{ $t('settings.account.reconnect') }}
          </button>
        </div>
      </div>

      <div v-else class="text-center py-6">
        <p class="text-sm theme-text-muted mb-4">{{ $t('settings.account.start') }}</p>
        <button @click="handleConnect" class="btn btn-primary text-sm">
          {{ $t('settings.account.connect') }}
        </button>
      </div>
    </div>

    <!-- APPEARANCE CARD -->
    <div class="card p-5 md:p-6 w-full">
      <h2 class="text-lg font-bold mb-4">Appearance</h2>
      <div class="space-y-4">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-bold">Dark Mode</p>
            <p class="text-xs theme-text-muted mt-0.5">Ubah tema gelap atau terang</p>
          </div>
          <button
            @click="toggleTheme"
            type="button"
            class="relative w-12 h-6 rounded-full transition-colors"
            :class="theme === 'dark' ? 'bg-white' : 'bg-gray-400'"
            :aria-label="theme === 'dark' ? 'Switch to light' : 'Switch to dark'"
          >
            <span
              class="absolute top-0.5 left-0.5 w-5 h-5 rounded-full shadow transition-transform"
              :class="theme === 'dark' ? 'translate-x-6 bg-black' : 'translate-x-0 bg-white'"
            ></span>
          </button>
        </div>
        <div class="flex items-center justify-between pt-4 border-t theme-border">
          <div>
            <p class="text-sm font-bold">Language</p>
            <p class="text-xs theme-text-muted mt-0.5">Pilih bahasa aplikasi</p>
          </div>
          <LanguageSwitcher />
        </div>
      </div>
    </div>

    <!-- ACCOUNT ACTIONS CARD -->
    <div class="card p-5 md:p-6 w-full">
      <h2 class="text-lg font-bold mb-4">Account Actions</h2>
      <button
        @click="handleLogout"
        type="button"
        class="w-full py-2.5 px-4 rounded-lg border border-red-500/40 text-red-500 hover:bg-red-500/10 transition font-bold text-sm"
      >
        Logout
      </button>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { supabase } from '../../lib/supabase'
import { useNotify } from '../../composables/useNotify'
import { useTheme } from '../../composables/useTheme'
import LanguageSwitcher from '../../components/LanguageSwitcher.vue'

const { showToast } = useNotify()
const { theme, toggle: toggleTheme } = useTheme()

async function handleLogout() {
  await supabase.auth.signOut()
  window.location.href = '/login'
}
const loading = ref(true)
const account = ref<any>(null)
const avatarUrl = ref('')
const threadsUsername = ref('')

async function fetchAccountData() {
  loading.value = true
  try {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) return

    const { data } = await supabase.schema('threads')
      .from('threads_accounts')
      .select('*')
      .eq('user_id', user.id)
      .maybeSingle()

    if (data) {
      account.value = data
      avatarUrl.value = data.profile_picture_url || ''
      threadsUsername.value = data.username || ''
    }
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

async function handleConnect() {
  // Logika connect Threads (OAuth) taruh di sini
  showToast('Mengarahkan ke OAuth Meta...', 'info')
}

onMounted(() => {
  fetchAccountData()
})
</script>
