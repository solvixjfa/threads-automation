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
            {{ accountStore.accounts.length }} / {{ accountStore.maxAccounts }} {{ $i18n.locale === 'id' ? 'Akun' : 'Accounts' }}
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
              <img :src="acc.profile_picture_url" referrerpolicy="no-referrer" alt="Profile" class="w-full h-full object-cover" />
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
                  {{ $i18n.locale === 'id' ? 'AKTIF' : 'ACTIVE' }}
                </span>
                <span
                  v-else
                  class="px-2 py-0.5 rounded-full text-[10px] font-medium border theme-border theme-text-muted"
                >
                  {{ acc.connection_status }}
                </span>
              </div>
              <p class="text-xs theme-text-muted mt-0.5">
                {{ $i18n.locale === 'id' ? 'Token berlaku s/d' : 'Token valid until' }} {{ acc.token_expires_at ? formatDate(acc.token_expires_at) : '-' }}
              </p>
            </div>
          </div>

          <div class="flex items-center gap-2 shrink-0 justify-end">
            <button
              v-if="acc.id !== accountStore.activeAccountId"
              @click="handleSwitch(acc.id, acc.username)"
              class="btn btn-primary text-xs"
            >
              {{ $i18n.locale === 'id' ? 'Gunakan Akun' : 'Switch Account' }}
            </button>
            <div class="flex items-center gap-2"><button @click="handleConnect" class="btn btn-secondary text-xs">
              Reconnect
            </button><button type="button" :disabled="disconnectingId === acc.id" @click="handleDisconnectAccount(acc)" class="px-3 py-1.5 rounded-lg text-xs font-medium border border-red-500/30 bg-red-500/10 text-red-400 hover:bg-red-500/20 disabled:opacity-50 transition">{{ disconnectingId === acc.id ? ($i18n.locale === 'id' ? 'Memutus...' : 'Disconnecting...') : ($i18n.locale === 'id' ? 'Putus' : 'Disconnect') }}</button></div>
          </div>
        </div>

        <!-- TOMBOL TAMBAH AKUN BARU ATAU UPGRADE -->
        <div class="pt-3 border-t theme-border flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <p class="text-xs theme-text-muted">
            <template v-if="accountStore.canAddAccount">
              <template v-if="$i18n.locale === 'id'">
                Semua akun berbagi paket <b>{{ planLabel }}</b>, saldo token, dan API key yang sama.
              </template>
              <template v-else>
                All accounts share the same <b>{{ planLabel }}</b> plan, token balance, and API keys.
              </template>
            </template>
            <template v-else>
              <template v-if="$i18n.locale === 'id'">
                Batas maksimal paket <b>{{ planLabel }}</b> ({{ accountStore.maxAccounts }} akun) sudah tercapai.
              </template>
              <template v-else>
                Maximum limit for <b>{{ planLabel }}</b> ({{ accountStore.maxAccounts }} accounts) has been reached.
              </template>
            </template>
          </p>

          <button
            v-if="accountStore.canAddAccount"
            @click="handleConnect"
            class="btn btn-primary text-xs shrink-0"
          >
            {{ $i18n.locale === 'id' ? '+ Tambah Akun Threads' : '+ Add Threads Account' }}
          </button>
          <RouterLink
            v-else
            to="/pricing"
            class="btn btn-primary text-xs shrink-0"
          >
            {{ $i18n.locale === 'id' ? 'Upgrade Kuota Akun' : 'Upgrade Account Limit' }}
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
            <p class="text-xs theme-text-muted mt-0.5">{{ $i18n.locale === 'id' ? 'Ubah tema gelap atau terang' : 'Switch between dark and light theme' }}</p>
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
            <p class="text-xs theme-text-muted mt-0.5">{{ $i18n.locale === 'id' ? 'Pilih bahasa aplikasi' : 'Choose application language' }}</p>
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
  
    <!-- Danger Zone: Delete Account & Delete Full Data -->
    <div class="rounded-2xl border border-red-500/25 bg-zinc-900/60 p-5 space-y-4 mt-6">
      <div>
        <h3 class="text-base font-semibold text-red-400">{{ $i18n.locale === 'id' ? 'Zona Bahaya' : 'Danger Zone' }}</h3>
        <p class="text-xs text-zinc-400 mt-1">
          {{ $i18n.locale === 'id' ? 'Kelola penghapusan akun Ixiera dan data yang terhubung. Tindakan ini bersifat permanen.' : 'Manage deletion of your Ixiera account and connected data. This action is permanent.' }}
        </p>
      </div>

      <div class="space-y-3 pt-1">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 p-3.5 rounded-xl border border-zinc-800 bg-zinc-950/60">
          <div>
            <p class="text-sm font-medium text-zinc-100">{{ $i18n.locale === 'id' ? 'Hapus Akun Saja' : 'Delete Account Only' }}</p>
            <p class="text-xs text-zinc-400 mt-0.5">
              {{ $i18n.locale === 'id' ? 'Hapus akun login Ixiera dan putus koneksi Threads. Riwayat analitik sistem tetap disimpan secara anonim.' : 'Delete your Ixiera login account and disconnect Threads. System analytics history is retained anonymously.' }}
            </p>
          </div>
          <button
            type="button"
            @click="openDeleteModal('account_only')"
            class="shrink-0 px-3.5 py-2 rounded-xl text-xs font-semibold border border-red-500/40 bg-red-500/10 text-red-400 hover:bg-red-500/20 transition"
          >
            {{ $i18n.locale === 'id' ? 'Hapus Akun Saja' : 'Delete Account Only' }}
          </button>
        </div>

        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 p-3.5 rounded-xl border border-red-500/30 bg-red-950/20">
          <div>
            <p class="text-sm font-medium text-red-300">{{ $i18n.locale === 'id' ? 'Hapus Full Data' : 'Delete All Data' }}</p>
            <p class="text-xs text-zinc-400 mt-0.5">
              {{ $i18n.locale === 'id' ? 'Hapus permanen akun Ixiera beserta seluruh akun Threads, jadwal konten, auto-reply, knowledge base, dan riwayat token.' : 'Permanently delete your Ixiera account along with all connected Threads accounts, scheduled posts, auto-replies, knowledge base, and token history.' }}
            </p>
          </div>
          <button
            type="button"
            @click="openDeleteModal('full_data')"
            class="shrink-0 px-3.5 py-2 rounded-xl text-xs font-semibold bg-red-600 text-white hover:bg-red-500 transition"
          >
            {{ $i18n.locale === 'id' ? 'Hapus Full Data' : 'Delete All Data' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Modal Confirm Account Deletion -->
    <div
      v-if="deleteModalMode"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4"
    >
      <div class="w-full max-w-md rounded-2xl border border-zinc-800 bg-zinc-900 p-5 space-y-4 shadow-2xl">
        <h4 class="text-base font-semibold text-white">
          {{ deleteModalMode === 'full_data' ? ($i18n.locale === 'id' ? 'Konfirmasi Hapus Full Data' : 'Confirm Delete All Data') : ($i18n.locale === 'id' ? 'Konfirmasi Hapus Akun Saja' : 'Confirm Delete Account Only') }}
        </h4>
        <p class="text-xs text-zinc-300 leading-relaxed">
          {{
            deleteModalMode === 'full_data'
              ? ($i18n.locale === 'id'
                  ? 'Seluruh data akun, koneksi Threads, jadwal post, auto-reply, knowledge base, dan sisa token akan dihapus permanen dan tidak bisa dikembalikan.'
                  : 'All account data, Threads connections, scheduled posts, auto-replies, knowledge base, and remaining tokens will be permanently deleted and cannot be undone.')
              : ($i18n.locale === 'id'
                  ? 'Akun login Ixiera Anda akan dihapus dan koneksi Threads diputus secara permanen.'
                  : 'Your Ixiera login account will be permanently deleted and Threads connections disconnected.')
          }}
        </p>
        <div>
          <label class="block text-xs text-zinc-400 mb-1.5">
            <template v-if="$i18n.locale === 'id'">Ketik <span class="font-bold text-red-400">HAPUS</span> untuk melanjutkan:</template>
            <template v-else>Type <span class="font-bold text-red-400">HAPUS</span> to continue:</template>
          </label>
          <input
            v-model="deleteConfirmInput"
            type="text"
            placeholder="HAPUS"
            class="w-full rounded-xl border border-zinc-700 bg-zinc-950 px-3 py-2 text-sm text-white focus:border-red-500 focus:outline-none"
          />
        </div>
        <p v-if="deleteErrorMsg" class="text-xs text-red-400">{{ deleteErrorMsg }}</p>
        <div class="flex items-center justify-end gap-2 pt-2">
          <button
            type="button"
            :disabled="isDeletingAccount"
            @click="deleteModalMode = null"
            class="px-4 py-2 rounded-xl text-xs font-medium border border-zinc-700 text-zinc-300 hover:bg-zinc-800"
          >
            {{ $i18n.locale === 'id' ? 'Batal' : 'Cancel' }}
          </button>
          <button
            type="button"
            :disabled="deleteConfirmInput !== 'HAPUS' || isDeletingAccount"
            @click="executeAccountDeletion"
            class="px-4 py-2 rounded-xl text-xs font-semibold bg-red-600 text-white hover:bg-red-500 disabled:opacity-40"
          >
            {{ isDeletingAccount ? ($i18n.locale === 'id' ? 'Menghapus...' : 'Deleting...') : ($i18n.locale === 'id' ? 'Konfirmasi Hapus' : 'Confirm Delete') }}
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { supabase } from '../../lib/supabase'
import { useNotify } from '../../composables/useNotify'
import { useTheme } from '../../composables/useTheme'
import { useAccountStore } from '../../stores/accounts'
import LanguageSwitcher from '../../components/LanguageSwitcher.vue'

const route = useRoute()
const router = useRouter()
const { locale } = useI18n()
const { showToast } = useNotify()
const { theme, toggle: toggleTheme } = useTheme()
const accountStore = useAccountStore()

const planLabel = computed(() => {
  const p = accountStore.effectivePlan
  const isId = locale.value === 'id'
  if (p === 'agency') return isId ? 'Agency BYOK (Maks 50 Akun)' : 'Agency BYOK (Max 50 Accounts)'
  if (p === 'business') return isId ? 'Business (Maks 20 Akun)' : 'Business (Max 20 Accounts)'
  if (p === 'pro') return isId ? 'Pro (Maks 5 Akun)' : 'Pro (Max 5 Accounts)'
  if (p === 'starter') return isId ? 'Starter (Maks 2 Akun)' : 'Starter (Max 2 Accounts)'
  if (p === 'paid_credit') return isId ? `Pro Token (Maks ${accountStore.maxAccounts} Akun)` : `Pro Token (Max ${accountStore.maxAccounts} Accounts)`
  if (p === 'paid_byok') return isId ? `Pro BYOK (Maks ${accountStore.maxAccounts} Akun)` : `Pro BYOK (Max ${accountStore.maxAccounts} Accounts)`
  if (p === 'trial') return isId ? 'Trial (Maks 1 Akun)' : 'Trial (Max 1 Account)'
  return isId ? 'Free (Maks 1 Akun)' : 'Free (Max 1 Account)'
})

function formatDate(iso: string) {
  if (!iso) return ''
  return new Date(iso).toLocaleDateString(locale.value === 'id' ? 'id-ID' : 'en-US', { dateStyle: 'medium' })
}

function handleSwitch(id: string, username: string | null) {
  accountStore.setActiveAccount(id)
  showToast(locale.value === 'id' ? `Beralih ke akun @${username || 'Threads'}` : `Switched to @${username || 'Threads'}`, 'success')
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


const disconnectingId = ref<string | null>(null)
const deleteModalMode = ref<'account_only' | 'full_data' | null>(null)
const deleteConfirmInput = ref('')
const isDeletingAccount = ref(false)
const deleteErrorMsg = ref('')

function openDeleteModal(mode: 'account_only' | 'full_data') {
  deleteModalMode.value = mode
  deleteConfirmInput.value = ''
  deleteErrorMsg.value = ''
}

async function handleDisconnectAccount(accItem: { id: string; username?: string }) {
  if (!accItem?.id) return
  const uname = accItem.username ? `@${accItem.username}` : 'akun ini'
  if (!window.confirm(`Putus koneksi ${uname} dari Ixiera?`)) return

  disconnectingId.value = accItem.id
  try {
    const { data, error } = await supabase.functions.invoke('delete-account', {
      body: { mode: 'disconnect_account', account_id: accItem.id },
    })
    if (error || data?.error) {
      throw new Error(data?.error || error?.message || 'Gagal memutus koneksi akun')
    }
    if (localStorage.getItem('ixiera_active_account_id') === accItem.id) {
      localStorage.removeItem('ixiera_active_account_id')
    }
    window.location.reload()
  } catch (err: any) {
    alert(err?.message || 'Gagal memutus koneksi akun Threads')
  } finally {
    disconnectingId.value = null
  }
}

async function executeAccountDeletion() {
  if (!deleteModalMode.value || deleteConfirmInput.value !== 'HAPUS') return
  isDeletingAccount.value = true
  deleteErrorMsg.value = ''
  try {
    const { data, error } = await supabase.functions.invoke('delete-account', {
      body: { mode: deleteModalMode.value },
    })
    if (error || data?.error) {
      throw new Error(data?.error || error?.message || 'Gagal menghapus akun')
    }
    localStorage.clear()
    await supabase.auth.signOut()
    window.location.href = '/login'
  } catch (err: any) {
    deleteErrorMsg.value = err?.message || 'Terjadi kesalahan saat menghapus akun'
  } finally {
    isDeletingAccount.value = false
  }
}

</script>
