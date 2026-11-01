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

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { supabase } from '../../lib/supabase'
import { useNotify } from '../../composables/useNotify'

const { showToast } = useNotify()
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
