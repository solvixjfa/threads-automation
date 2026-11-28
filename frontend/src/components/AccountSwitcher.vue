<template>
  <div ref="containerRef" class="relative w-full">
    <button
      type="button"
      :disabled="store.isSyncing"
      @click="open = !open"
      class="w-full flex items-center justify-between gap-2 px-2.5 py-2 rounded-xl border theme-border bg-[var(--surface-2)] hover:border-[var(--border-strong)] disabled:opacity-75 transition text-left"
    >
      <div class="flex items-center gap-2.5 min-w-0">
        <div
          v-if="active?.profile_picture_url"
          class="w-7 h-7 rounded-full overflow-hidden shrink-0 border border-[var(--border)]"
        >
          <img :src="active.profile_picture_url" referrerpolicy="no-referrer" class="w-full h-full object-cover" />
        </div>
        <div
          v-else
          class="w-7 h-7 flex items-center justify-center rounded-full text-xs font-black theme-accent shrink-0"
        >
          {{ active?.username ? active.username.charAt(0).toUpperCase() : 'IX' }}
        </div>

        <div class="min-w-0">
          <div class="text-xs font-bold truncate theme-text">
            {{ active?.username ? '@' + active.username : ($i18n.locale === 'id' ? 'Hubungkan Akun' : 'Connect Account') }}
          </div>
          <div class="text-[10px] theme-text-muted truncate">
            {{ store.isSyncing ? ($i18n.locale === 'id' ? 'Menyinkronkan data...' : 'Syncing data...') : ($i18n.locale === 'id' ? `${store.accounts.length}/${store.maxAccounts} akun aktif` : `${store.accounts.length}/${store.maxAccounts} active accounts`) }}
          </div>
        </div>
      </div>

      <RefreshCw v-if="store.isSyncing" class="w-3.5 h-3.5 theme-text-muted shrink-0 animate-spin" />
      <ChevronDown
        v-else
        class="w-4 h-4 theme-text-muted shrink-0 transition-transform duration-150"
        :class="open ? 'rotate-180' : ''"
      />
    </button>

    <!-- Banner indikator jeda sinkronisasi saat berpindah akun -->
    <div
      v-if="store.isSyncing"
      class="fixed top-3 left-1/2 -translate-x-1/2 z-[60] flex items-center gap-2 px-4 py-2 rounded-full border border-zinc-700 bg-zinc-900/95 text-white text-xs font-medium shadow-2xl backdrop-blur"
    >
      <RefreshCw class="w-3.5 h-3.5 animate-spin text-emerald-400 shrink-0" />
      <span>{{ store.syncStatusText || ($i18n.locale === 'id' ? 'Menyinkronkan data akun...' : 'Syncing account data...') }}</span>
    </div>

    <div
      v-if="open"
      class="absolute left-0 right-0 mt-1.5 z-50 rounded-xl border theme-border theme-bg shadow-xl p-1.5 space-y-1"
    >
      <div class="px-2 py-1 flex items-center justify-between text-[10px] font-bold uppercase tracking-wider theme-text-muted">
        <span>{{ $i18n.locale === 'id' ? 'Akun Threads' : 'Threads Accounts' }}</span>
        <span>{{ store.accounts.length }}/{{ store.maxAccounts }}</span>
      </div>

      <div v-if="store.accounts.length === 0" class="px-2.5 py-2 text-xs theme-text-muted">
        {{ $i18n.locale === 'id' ? 'Belum ada akun terhubung.' : 'No accounts connected yet.' }}
      </div>

      <button
        v-for="acc in store.accounts"
        :key="acc.id"
        type="button"
        @click="selectAccount(acc.id)"
        class="w-full flex items-center justify-between gap-2 px-2.5 py-2 rounded-lg text-left transition"
        :class="acc.id === active?.id ? 'theme-bg-hover font-bold' : 'hover:theme-bg-hover'"
      >
        <div class="flex items-center gap-2 min-w-0">
          <div
            v-if="acc.profile_picture_url"
            class="w-6 h-6 rounded-full overflow-hidden shrink-0 border border-[var(--border)]"
          >
            <img :src="acc.profile_picture_url" referrerpolicy="no-referrer" class="w-full h-full object-cover" />
          </div>
          <div
            v-else
            class="w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-black theme-accent shrink-0"
          >
            {{ acc.username ? acc.username.charAt(0).toUpperCase() : 'IX' }}
          </div>
          <div class="min-w-0">
            <div class="text-xs truncate theme-text">@{{ acc.username || 'unknown' }}</div>
            <div class="text-[10px] theme-text-muted truncate">
              {{ acc.connection_status === 'connected' ? 'Connected' : acc.connection_status }}
            </div>
          </div>
        </div>

        <Check v-if="acc.id === active?.id" class="w-3.5 h-3.5 text-green-500 shrink-0" />
      </button>

      <div class="pt-1 border-t theme-border">
        <RouterLink
          to="/profile/account"
          @click="open = false"
          class="w-full flex items-center justify-center gap-1.5 px-2.5 py-2 rounded-lg text-xs font-bold theme-text hover:theme-bg-hover transition"
        >
          <Plus class="w-3.5 h-3.5" />
          <span>{{ store.canAddAccount ? 'Tambah / Kelola Akun' : 'Kelola Akun (Kuota Penuh)' }}</span>
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { RouterLink } from 'vue-router'
import { ChevronDown, Check, Plus, RefreshCw } from 'lucide-vue-next'
import { useAccountStore } from '../stores/accounts'

const store = useAccountStore()
const open = ref(false)
const containerRef = ref<HTMLElement | null>(null)

const active = computed(() => store.activeAccount)

async function selectAccount(id: string) {
  open.value = false
  await store.setActiveAccount(id, false)
}

function handleClickOutside(e: MouseEvent) {
  if (containerRef.value && !containerRef.value.contains(e.target as Node)) {
    open.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
