<template>
  <div class="space-y-8 relative">
    <NotifyOverlay />
    <div class="flex flex-wrap justify-between items-center gap-4">
      <div>
        <h1 class="text-2xl font-bold text-slate-900 tracking-tight">Auto Reply Inbox</h1>
        <p class="text-slate-500 text-sm mt-1">Review draf balasan AI sebelum diterbitkan ke Threads.</p>
      </div>
      <div class="flex items-center gap-3">
        <button @click="syncRepliesManual" :disabled="isSyncing" class="bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold py-2.5 px-4 rounded-xl transition disabled:opacity-50 flex items-center gap-2">
          <span v-if="isSyncing" class="w-3 h-3 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
          <span>{{ isSyncing ? 'Menarik Draf AI...' : 'Sync Komentar & Draf' }}</span>
        </button>
      </div>
    </div>

    <div class="flex border-b border-slate-200 text-xs font-bold gap-6">
      <button @click="activeTab = 'pending'" class="pb-3 border-b-2 transition" :class="activeTab === 'pending' ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-slate-400'">Antrean Review ({{ pendingLogs.length }})</button>
      <button @click="activeTab = 'history'" class="pb-3 border-b-2 transition" :class="activeTab === 'history' ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-slate-400'">Riwayat Terkirim ({{ historyLogs.length }})</button>
    </div>

    <div v-if="loading" class="p-12 text-center text-xs text-slate-400 animate-pulse">Memuat antrean draf...</div>

    <div v-else-if="activeTab === 'pending'" class="space-y-4">
      <div v-if="pendingLogs.length === 0" class="bg-white border border-slate-200 rounded-2xl p-12 text-center text-xs text-slate-400">Tidak ada draf AI yang menunggu review.</div>
      
      <div v-for="log in pendingLogs" :key="log.id" class="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-4">
        <div class="bg-slate-50 p-3.5 rounded-xl border border-slate-200">
          <span class="text-[10px] font-bold text-slate-500 uppercase">Komentar dari @{{ log.llm_meta?.username || 'audiens' }}:</span>
          <p class="text-xs font-semibold text-slate-900 mt-1">"{{ log.llm_meta?.incoming_comment }}"</p>
        </div>
        
        <div class="bg-indigo-50/50 p-4 rounded-xl border border-indigo-100">
          <span class="text-[10px] font-bold text-indigo-900 uppercase">Draf Balasan AI (Bisa Diedit)</span>
          <textarea v-model="log.final_text" rows="3" class="w-full mt-2 bg-white border border-indigo-200 rounded-lg p-3 text-xs focus:ring-2 focus:ring-indigo-500 resize-none"></textarea>
        </div>
        
        <div class="flex justify-end items-center gap-3">
          <button @click="updateStatus(log.id, 'skipped')" class="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-lg transition">Abaikan</button>
          <button @click="approveAndPublish(log)" :disabled="approvingId === log.id || !log.final_text" class="px-5 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold rounded-lg disabled:opacity-50 transition">
            {{ approvingId === log.id ? 'Menerbitkan...' : 'Kirim ke Threads' }}
          </button>
        </div>
      </div>
    </div>
    
    <div v-else class="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">
      <div v-if="historyLogs.length === 0" class="p-12 text-center text-xs text-slate-400">Belum ada riwayat balasan terkirim.</div>
      <div v-else class="divide-y divide-slate-100">
        <div v-for="log in historyLogs" :key="log.id" class="p-5 hover:bg-slate-50 transition space-y-2">
          <div class="flex justify-between items-center">
            <span class="px-2.5 py-1 text-[10px] font-bold uppercase tracking-wider rounded-md" :class="log.status === 'sent' || log.status === 'approved' ? 'bg-emerald-50 text-emerald-600 border border-emerald-100' : 'bg-slate-100 text-slate-500 border border-slate-200'">{{ log.status }}</span>
            <span class="text-xs text-slate-400">{{ formatDate(log.created_at) }}</span>
          </div>
          <p class="text-xs text-slate-500 italic">"{{ log.llm_meta?.incoming_comment }}"</p>
          <p class="text-xs text-slate-800 font-medium bg-slate-50 p-3 rounded-lg border border-slate-100">{{ log.final_text }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { supabase } from '../lib/supabase'
import { useNotify } from '../composables/useNotify'
import NotifyOverlay from '../components/NotifyOverlay.vue'

const { showToast } = useNotify()
const loading = ref(true)
const isSyncing = ref(false)
const approvingId = ref<string | null>(null)
const activeTab = ref<'pending' | 'history'>('pending')
const logs = ref<any[]>([])

const pendingLogs = computed(() => logs.value.filter(l => !['sent', 'skipped', 'approved'].includes(l.status)))
const historyLogs = computed(() => logs.value.filter(l => ['sent', 'skipped', 'approved'].includes(l.status)))

function formatDate(isoString: string) {
  if (!isoString) return ''
  return new Date(isoString).toLocaleString('id-ID', { dateStyle: 'medium', timeStyle: 'short' })
}

async function fetchLogs() {
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) return
  const { data: account } = await supabase.schema('threads').from('threads_accounts').select('id').eq('user_id', user.id).maybeSingle()
  if (!account) return

  const { data } = await supabase.schema('threads').from('auto_reply_logs').select('*').eq('account_id', account.id).order('created_at', { ascending: false }).limit(50)
  if (data) logs.value = data
  loading.value = false
}

async function syncRepliesManual() {
  isSyncing.value = true
  try {
    const res = await fetch('https://threads-automation-production-53ad.up.railway.app/api/v1/leads/sync-replies', { method: 'GET' })
    if (!res.ok) throw new Error('Gagal terhubung ke backend Python.')

    showToast('Sinkronisasi selesai. Memuat draf terbaru...', 'success')
    await fetchLogs()
  } catch (err: any) {
    showToast('Gagal sync: ' + err.message, 'error')
  } finally {
    isSyncing.value = false
  }
}

async function approveAndPublish(log: any) {
  approvingId.value = log.id
  try {
    const { error } = await supabase.schema('threads').from('auto_reply_logs').update({ status: 'approved', final_text: log.final_text }).eq('id', log.id)
    if (error) throw error
    showToast('Draf disetujui dan siap diterbitkan!', 'success')
    await fetchLogs()
  } catch (err: any) {
    showToast('Gagal memproses: ' + err.message, 'error')
  } finally {
    approvingId.value = null
  }
}

async function updateStatus(id: string, newStatus: string) {
  await supabase.schema('threads').from('auto_reply_logs').update({ status: newStatus }).eq('id', id)
  await fetchLogs()
}

onMounted(() => fetchLogs())
</script>
