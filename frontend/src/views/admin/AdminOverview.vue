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

      <!-- TOKEN USAGE CARD -->
      <div v-if="tokenStats" class="col-span-full grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
        <div class="card p-5 space-y-1 border-l-4 border-blue-500">
          <span class="text-[10px] font-bold uppercase theme-text-muted">Total Generates</span>
          <p class="text-2xl font-black">{{ tokenStats.total_generates }}</p>
        </div>
        <div class="card p-5 space-y-1 border-l-4 border-purple-500">
          <span class="text-[10px] font-bold uppercase theme-text-muted">Prompt Tokens (30d)</span>
          <p class="text-2xl font-black">{{ tokenStats.total_prompt.toLocaleString('id-ID') }}</p>
        </div>
        <div class="card p-5 space-y-1 border-l-4 border-green-500">
          <span class="text-[10px] font-bold uppercase theme-text-muted">Completion Tokens (30d)</span>
          <p class="text-2xl font-black">{{ tokenStats.total_completion.toLocaleString('id-ID') }}</p>
        </div>
      </div>
      <!-- PER USER TOKEN TABLE -->
      <div v-if="tokenStats" class="col-span-full mt-4">
        <button @click="showPerUser = !showPerUser" class="btn btn-secondary btn-sm mb-4">
          {{ showPerUser ? 'Sembunyikan Per User' : 'Lihat Detail Per User' }}
        </button>
        
        <div v-if="showPerUser" class="card p-5 space-y-4">
          <input v-model="searchQuery" type="text" placeholder="Cari username..." class="input w-full text-sm" />
          <div class="overflow-x-auto">
            <table class="w-full text-left text-sm whitespace-nowrap">
              <thead>
                <tr class="border-b border-gray-700">
                  <th class="pb-2 pr-4">Username</th>
                  <th class="pb-2 px-4 text-center">Generates</th>
                  <th class="pb-2 px-4 text-right">Prompt Tokens</th>
                  <th class="pb-2 pl-4 text-right">Completion Tokens</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="u in filteredUsers" :key="u.account_id" class="border-b border-gray-800 hover:bg-gray-800/50">
                  <td class="py-2 pr-4">{{ u.username || u.account_id.slice(0, 8) }}</td>
                  <td class="py-2 px-4 text-center">{{ u.generates }}</td>
                  <td class="py-2 px-4 text-right">{{ u.prompt.toLocaleString('id-ID') }}</td>
                  <td class="py-2 pl-4 text-right">{{ u.completion.toLocaleString('id-ID') }}</td>
                </tr>
                <tr v-if="filteredUsers.length === 0">
                  <td colspan="4" class="py-4 text-center text-gray-500">User tidak ditemukan.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { supabase } from '../../lib/supabase'

const loading = ref(true)
const stats = ref<any>(null)
const tokenStats = ref<any>(null)
const perUserStats = ref<any[]>([])
const showPerUser = ref(false)
const searchQuery = ref('')
const errorMessage = ref('')

const filteredUsers = computed(() => {
  if (!searchQuery.value) return perUserStats.value
  const q = searchQuery.value.toLowerCase()
  return perUserStats.value.filter(u => (u.username || '').toLowerCase().includes(q))
})

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

    
    // Fetch Token Stats
    try {
      const tokenRes = await fetch(`${API_BASE}/token-stats`, { headers })
      const tokenData = await tokenRes.json()
      if (tokenData.success) { tokenStats.value = tokenData.stats; perUserStats.value = tokenData.per_user || [] }
    } catch (e) { console.error('Failed to fetch token stats', e) }

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
