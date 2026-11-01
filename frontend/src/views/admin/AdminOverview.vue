<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Overview</h1>
      <p class="text-sm theme-text-muted mt-1">Ringkasan performa bisnis Ixiera.</p>
    </div>

    <div v-if="loading" class="animate-pulse grid grid-cols-2 md:grid-cols-4 gap-4">
      <div v-for="i in 4" :key="i" class="h-28 skeleton"></div>
    </div>

    <!-- STATE JIKA DATA GAGAL -->
    <div v-else-if="!stats" class="p-6 text-center border-2 border-dashed border-red-500/50 rounded-xl space-y-4">
      <p class="text-sm font-bold text-red-500">Gagal memuat data statistik.</p>
      <div class="p-4 bg-red-500/10 rounded-lg text-left overflow-x-auto">
        <p class="text-xs font-mono text-red-600 whitespace-pre-wrap">{{ errorMessage }}</p>
      </div>
      <button @click="load" class="btn btn-secondary btn-sm mt-2">Coba Lagi</button>
    </div>

    <!-- STATE DATA BERHASIL -->
    <div v-else class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div class="card p-5 space-y-1 border-l-4" style="border-left-color: var(--success);">
        <span class="text-[10px] font-bold uppercase theme-text-muted">Est. MRR</span>
        <p class="text-2xl font-black">Rp {{ stats.mrr_estimate.toLocaleString('id-ID') }}</p>
      </div>
      <div class="card p-5 space-y-1">
        <span class="text-[10px] font-bold uppercase theme-text-muted">Total Users</span>
        <p class="text-2xl font-black">{{ stats.total_users }}</p>
      </div>
      <div class="card p-5 space-y-1">
        <span class="text-[10px] font-bold uppercase theme-text-muted">Pro Users</span>
        <p class="text-2xl font-black">{{ stats.pro_credit + stats.pro_byok }}</p>
        <div class="text-[10px] theme-text-muted">{{ stats.pro_credit }} Credit / {{ stats.pro_byok }} BYOK</div>
      </div>
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

const loading = ref(true)
const stats = ref<any>(null)
const errorMessage = ref('')
const API_BASE = 'https://threads-automation-r9so.onrender.com/api/v1/admin'

async function getAuthHeader() {
  const { data: { session } } = await supabase.auth.getSession()
  return session ? { 'Authorization': `Bearer ${session.access_token}` } : {}
}

async function load() {
  loading.value = true
  errorMessage.value = ''
  try {
    const headers = await getAuthHeader()
    if (!headers.Authorization) throw new Error("Lu belum login / Session expired.")

    const res = await fetch(`${API_BASE}/stats`, { headers })
    
    // Baca teks respons dulu (bisa JSON atau HTML error)
    const textData = await res.text()
    let jsonData: any = {}
    try { jsonData = JSON.parse(textData) } catch(e) { /* Bukan JSON */ }

    if (!res.ok) {
      if (res.status === 401) throw new Error("401: Unauthorized. Token invalid.")
      if (res.status === 403) throw new Error("403: Forbidden. Lu bukan admin.")
      if (res.status === 404) throw new Error("404: Endpoint /stats belum ada di Railway.")
      throw new Error(`[${res.status}] ${jsonData.detail || textData.slice(0, 100)}`)
    }

    if (jsonData.success) {
      stats.value = jsonData.stats
    } else {
      throw new Error("Respons backend gak ada key 'success'.")
    }
  } catch (err: any) {
    errorMessage.value = err.message
    stats.value = null
  } finally {
    loading.value = false
  }
}
onMounted(load)
</script>
