<template>
  <div class="space-y-6 w-full max-w-full overflow-hidden">
    <!-- CARD: CONNECTED THREADS ACCOUNTS -->
    <div class="card p-5 md:p-6 w-full space-y-5">
      <div class="flex flex-wrap items-start justify-between gap-3 pb-4 border-b theme-border">
        <div>
          <h2 class="text-lg font-bold">{{ $t('settings.account.title') }}</h2>
          <p class="text-xs theme-text-muted mt-1">{{ $t('settings.account.subtitle') }}</p>
        </div>
        <div class="flex items-center gap-2">
          <span class="px-3 py-1 rounded-full border theme-border bg-[var(--surface-2)] text-xs font-bold">
            {{ accountStore.accounts.length }} / {{ accountStore.maxAccounts }} Akun
          </span>
          <span class="px-2.5 py-1 rounded-full border theme-border text-xs font-bold uppercase">
            {{ planLabel }}
          </span>
        </div>
      </div>

      <div v-if="accountStore.loading && accountStore.accounts.length === 0" class="animate-pulse h-24 bg-[var(--surface-2)] rounded-lg"></div>

      <div v-else-if="accountStore.accounts.length > 0" class="space-y-3">
        <div
          v-for="acc in accountStore.accounts"
          :key="acc.id"
          class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 rounded-xl border transition"
          :class="acc.id === accountStore.activeAccountId ? 'border-[var(--border-strong)] bg-[var(--surface-2)]' : 'theme-border'"
        >
          <div class="flex items-center gap-3.5 min-w-0">
            <div v-if="acc.profile_picture_url" class="w-12 h-12 rounded-full overflow-hidden shrink-0 border theme-border">
              <img :src="acc.profile_picture_url" alt="Profile" class="w-full h-full object-cover" />
            </div>
            <div v-else class="w-12 h-12 rounded-full flex items-center justify-center bg-[var(--text)] text-[var(--bg)] text-base font-black shrink-0">
              {{ acc.username ? acc.username.charAt(0).toUpperCase() : 'IX' }}
            </div>

            <div class="min-w-0">
              <div class="flex items-center gap-2 flex-wrap">
                <h3 class="font-bold text-base truncate">@{{ acc.username || 'unknown' }}</h3>
                <span
                  v-if="acc.id === accountStore.activeAccountId"
                  class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-green-500/15 text-green-500"
                >
                  AKTIF
                </span>
                <span
                  v-else
                  class="px-2 py-0.5 rounded-full text-[10px] font-medium border theme-border theme-text-muted"
                >
                  {{ acc.connection_status }}
                </span>
              </div>
              <p class="text-xs theme-text-muted mt-0.5">
                Token berlaku s/d {{ acc.token_expires_at ? formatDate(acc.token_expires_at) : '-' }}
              </p>
            </div>
          </div>

          <div class="flex items-center gap-2 shrink-0 justify-end">
            <button
              v-if="acc.id !== accountStore.activeAccountId"
              @click="handleSwitch(acc.id, acc.username)"
              class="btn btn-primary text-xs"
            >
              Gunakan Akun
            </button>
            <button @click="handleConnect" class="btn btn-secondary text-xs">
              Reconnect
            </button>
          </div>
        </div>

        <!-- TOMBOL TAMBAH AKUN BARU ATAU UPGRADE -->
        <div class="pt-3 border-t theme-border flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <p class="text-xs theme-text-muted">
            <template v-if="accountStore.canAddAccount">
              Semua akun berbagi paket <b>{{ planLabel }}</b>, saldo kredit, dan API key yang sama.
            </template>
            <template v-else>
              Batas maksimal paket <b>{{ planLabel }}</b> ({{ accountStore.maxAccounts }} akun) sudah tercapai.
            </template>
          </p>

          <button
            v-if="accountStore.canAddAccount"
            @click="handleConnect"
            class="btn btn-primary text-xs shrink-0"
          >
            + Tambah Akun Threads
          </button>
          <RouterLink
            v-else
            to="/pricing"
            class="btn btn-primary text-xs shrink-0"
          >
            Upgrade Kuota Akun
          </RouterLink>
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
import { computed, onMounted } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import { supabase } from '../../lib/supabase'
import { useNotify } from '../../composables/useNotify'
import { useTheme } from '../../composables/useTheme'
import { useAccountStore } from '../../stores/accounts'
import LanguageSwitcher from '../../components/LanguageSwitcher.vue'

const route = useRoute()
const router = useRouter()
const { showToast } = useNotify()
const { theme, toggle: toggleTheme } = useTheme()
const accountStore = useAccountStore()

const planLabel = computed(() => {
  const p = accountStore.effectivePlan
  if (p === 'paid_credit') return 'Pro Credit (Maks 10 Akun)'
  if (p === 'paid_byok') return 'Pro BYOK (Maks 3 Akun)'
  if (p === 'trial') return 'Trial (Maks 1 Akun)'
  return 'Free (Maks 1 Akun)'
})

function formatDate(iso: string) {
  if (!iso) return ''
  return new Date(iso).toLocaleDateString('id-ID', { dateStyle: 'medium' })
}

function handleSwitch(id: string, username: string | null) {
  accountStore.setActiveAccount(id)
  showToast(`Beralih ke akun @${username || 'Threads'}`, 'success')
}

async function handleLogout() {
  await supabase.auth.signOut()
  accountStore.reset()
  window.location.href = '/login'
}

async function handleConnect() {
  try {
    showToast('Mengarahkan ke Threads...', 'info')
    const { data, error } = await supabase.functions.invoke('threads-oauth-start', {
      body: {}
    })
    if (error) throw new Error(error.message || 'Gagal memulai OAuth')
    if (!data?.url) throw new Error('URL OAuth tidak diterima dari server')
    window.location.href = data.url
  } catch (err: any) {
    console.error('[oauth]', err)
    showToast('Gagal koneksi Threads: ' + (err.message || 'Unknown error'), 'error')
  }
}

onMounted(async () => {
  await accountStore.fetchAccounts(true)

  if (route.query.connected === 'true') {
    const connectedUser = String(route.query.username || '')
    const matched = accountStore.accounts.find(a => a.username === connectedUser)
    if (matched) {
      accountStore.setActiveAccount(matched.id)
    }
    showToast(`Akun @${connectedUser} berhasil terhubung!`, 'success')
    router.replace({ path: '/profile/account', query: {} })
  } else if (route.query.error) {
    showToast(decodeURIComponent(String(route.query.error)), 'error')
    router.replace({ path: '/profile/account', query: {} })
  }
})
</script>
