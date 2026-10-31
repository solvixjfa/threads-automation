<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Overview</h1>
      <p class="text-sm theme-text-muted mt-1">Ringkasan performa bisnis Ixiera.</p>
    </div>

    <div v-if="loading" class="animate-pulse grid grid-cols-2 md:grid-cols-4 gap-4">
      <div v-for="i in 4" :key="i" class="h-28 skeleton"></div>
    </div>

    <div v-else-if="stats" class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <!-- MRR -->
      <div class="card p-5 space-y-1 border-l-4" style="border-left-color: var(--success);">
        <span class="text-[10px] font-bold uppercase theme-text-muted">Est. MRR</span>
        <p class="text-2xl font-black">Rp {{ stats.mrr_estimate.toLocaleString('id-ID') }}</p>
      </div>
      <!-- Total Users -->
      <div class="card p-5 space-y-1">
        <span class="text-[10px] font-bold uppercase theme-text-muted">Total Users</span>
        <p class="text-2xl font-black">{{ stats.total_users }}</p>
      </div>
      <!-- Pro Users -->
      <div class="card p-5 space-y-1">
        <span class="text-[10px] font-bold uppercase theme-text-muted">Pro Users</span>
        <p class="text-2xl font-black">{{ stats.pro_credit + stats.pro_byok }}</p>
        <div class="text-[10px] theme-text-muted">{{ stats.pro_credit }} Credit / {{ stats.pro_byok }} BYOK</div>
      </div>
      <!-- Pending Requests -->
      <div class="card p-5 space-y-1 border-l-4" style="border-left-color: var(--warning);">
        <span class="text-[10px] font-bold uppercase theme-text-muted">Pending Requests</span>
        <p class="text-2xl font-black">{{ stats.pending_requests }}</p>
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
const stats = ref<any>(null)
const API_BASE = 'https://threads-automation-production-53ad.up.railway.app/api/v1/admin'

async function getAuthHeader() {
  const { data: { session } } = await supabase.auth.getSession()
  return session ? { 'Authorization': `Bearer ${session.access_token}` } : {}
}

async function load() {
  try {
    const headers = await getAuthHeader()
    const res = await fetch(`${API_BASE}/stats`, { headers })
    const data = await res.json()
    if (data.success) stats.value = data.stats
  } catch (err: any) {
    showToast('Failed load stats: ' + err.message, 'error')
  } finally {
    loading.value = false
  }
}
onMounted(load)
</script>
