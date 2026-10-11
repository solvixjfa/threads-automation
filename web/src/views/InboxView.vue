<template>
  <div class="space-y-8 relative">
    <NotifyOverlay />
    <div class="flex flex-wrap justify-between items-center gap-4">
      <div>
        <h1 class="text-2xl font-bold text-slate-900 tracking-tight">Auto Reply Inbox</h1>
        <p class="text-slate-500 text-sm mt-1">Review dan kelola balasan komentar otomatis buatan AI.</p>
      </div>
      <div class="flex items-center gap-3">
        <button @click="pollRealComments" :disabled="isPolling || isSimulating" class="bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold py-2.5 px-4 rounded-xl transition disabled:opacity-50 flex items-center gap-2">
          <span v-if="isPolling" class="w-3 h-3 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
          <span>{{ isPolling ? 'Menyinkronkan...' : 'Sync Komentar Threads' }}</span>
        </button>
        <button @click="simulateComment" :disabled="isSimulating || isPolling" class="bg-indigo-50 text-indigo-700 hover:bg-indigo-100 text-xs font-bold py-2.5 px-4 rounded-xl border border-indigo-100 transition disabled:opacity-50">
          + Tes Simulasi
        </button>
      </div>
    </div>

    <!-- AI Processing Indicator -->
    <div v-if="unprocessedCount > 0" class="bg-indigo-50 border border-indigo-100 rounded-xl p-3.5 flex items-center justify-between text-xs">
      <div class="flex items-center gap-2.5 text-indigo-900 font-bold">
        <span class="w-3 h-3 border-2 border-indigo-600 border-t-transparent rounded-full animate-spin"></span>
        <span>AI sedang memproses {{ unprocessedCount }} komentar... Harap tunggu.</span>
      </div>
    </div>

    <div class="flex border-b border-slate-200 text-xs font-bold gap-6">
      <button @click="activeTab = 'pending'" class="pb-3 border-b-2 transition" :class="activeTab === 'pending' ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-slate-400'">Antrean Review</button>
      <button @click="activeTab = 'history'" class="pb-3 border-b-2 transition" :class="activeTab === 'history' ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-slate-400'">Riwayat Terkirim</button>
    </div>

    <div v-if="loading" class="p-12 text-center text-xs text-slate-400 animate-pulse">Memuat pesan...</div>

    <!-- List Pending -->
    <div v-else-if="activeTab === 'pending'" class="space-y-4">
      <div v-if="pendingLogs.length === 0" class="bg-white border border-slate-200 rounded-2xl p-12 text-center text-xs text-slate-400">Belum ada balasan menunggu review.</div>
      <div v-for="log in pendingLogs" :key="log.id" class="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-4">
        <div class="bg-slate-50 p-3.5 rounded-xl border border-slate-200">
          <span class="text-[10px] font-bold text-slate-500 uppercase">Komentar:</span>
          <p class="text-xs font-semibold text-slate-900">"{{ log.llm_meta?.incoming_comment }}"</p>
        </div>
        <div class="bg-indigo-50/50 p-4 rounded-xl border border-indigo-100">
          <span class="text-[10px] font-bold text-indigo-900 uppercase">Draf Balasan AI</span>
          <textarea v-model="log.final_text" rows="3" class="w-full mt-2 bg-white border border-indigo-200 rounded-lg p-3 text-xs focus:ring-2 focus:ring-indigo-500 resize-none"></textarea>
        </div>
        <div class="flex justify-end items-center gap-3">
          <button @click="updateStatus(log.id, 'skipped', log.final_text)" class="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-lg">Abaikan</button>
          <button @click="approveAndPublish(log)" :disabled="approvingId === log.id" class="px-5 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold rounded-lg disabled:opacity-50">
            {{ approvingId === log.id ? 'Menerbitkan...' : 'Kirim ke Threads' }}
          </button>
        </div>
      </div>
    </div>
    
    <!-- List History Sama Seperti Sebelumnya -->
    <div v-else class="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm"><p class="text-center text-xs text-slate-500">Fitur riwayat.</p></div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { supabase } from '../lib/supabase'
import { useNotify } from '../composables/useNotify'
import NotifyOverlay from '../components/NotifyOverlay.vue'

const { showToast } = useNotify()
const loading = ref(true)
const isPolling = ref(false)
const isSimulating = ref(false)
const isAiProcessing = ref(false)
const approvingId = ref<string | null>(null)
const activeTab = ref<'pending' | 'history'>('pending')
const logs = ref<any[]>([])
let aiWorkerTimer: any = null

const pendingLogs = computed(() => logs.value.filter(l => l.status === 'pending'))
const unprocessedCount = computed(() => logs.value.filter(l => l.status === 'unprocessed').length)

async function fetchLogs() {
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) return
  const { data: account } = await supabase.schema('threads').from('threads_accounts').select('id').eq('user_id', user.id).maybeSingle()
  if (!account) return

  const { data } = await supabase.schema('threads').from('auto_reply_logs').select('*').eq('account_id', account.id).order('created_at', { ascending: false }).limit(30)
  if (data) logs.value = data
  loading.value = false
}

// 1. Fungsi Mandor: Memerintahkan Backend Proses AI
async function triggerAiQueue() {
  if (isAiProcessing.value || unprocessedCount.value === 0) return
  isAiProcessing.value = true
  try {
    const { data: { user } } = await supabase.auth.getUser()
    await supabase.functions.invoke('worker-replies', { body: { action: 'process_queue', user_id: user?.id } })
    await fetchLogs()
  } catch (err) {
    console.error(err)
  } finally {
    isAiProcessing.value = false
  }
}

async function pollRealComments() {
  isPolling.value = true
  try {
    const { data: { user } } = await supabase.auth.getUser()
    const { data, error } = await supabase.functions.invoke('worker-replies', { body: { action: 'sync', user_id: user?.id } })
    if (error || data?.error) throw new Error(error?.message || data?.error)

    showToast(`Sync selesai! ${data?.newItems || 0} data baru ditarik.`, 'success')
    await fetchLogs()
    
    // Langsung perintah AI jalan
    if (unprocessedCount.value > 0) triggerAiQueue()
  } catch (err: any) {
    showToast('Gagal sync: ' + err.message, 'error')
  } finally {
    isPolling.value = false
  }
}

async function simulateComment() {
  isSimulating.value = true
  try {
    const { data: { user } } = await supabase.auth.getUser()
    const sample = "Project XGBoost churn ini akurasinya berapa persen bro?"
    await supabase.functions.invoke('worker-replies', { body: { action: 'sync', comment: sample, user_id: user?.id } })
    showToast('Komentar simulasi masuk antrean.', 'info')
    await fetchLogs()
    if (unprocessedCount.value > 0) triggerAiQueue()
  } catch (err: any) {
    showToast('Gagal simulasi: ' + err.message, 'error')
  } finally {
    isSimulating.value = false
  }
}

async function approveAndPublish(log: any) {
  approvingId.value = log.id
  try {
    if (log.llm_meta?.media_id === 'simulated_media') {
      await updateStatus(log.id, 'approved', log.final_text)
      showToast('Simulasi disetujui.', 'info')
    } else {
      const { data: { user } } = await supabase.auth.getUser()
      const { data, error } = await supabase.functions.invoke('worker-replies', { body: { action: 'publish_reply', log_id: log.id, final_text: log.final_text, user_id: user?.id } })
      if (error || data?.error) throw new Error(error?.message || data?.error)
      showToast('Berhasil diterbitkan!', 'success')
      await fetchLogs()
    }
  } catch (err: any) {
    showToast('Gagal terbit: ' + err.message, 'error')
  } finally {
    approvingId.value = null
  }
}

async function updateStatus(id: string, newStatus: string, finalText: string) {
  await supabase.schema('threads').from('auto_reply_logs').update({ status: newStatus, final_text: finalText }).eq('id', id)
  await fetchLogs()
}

onMounted(() => {
  fetchLogs()
  // Loop cerdas: Hanya akan trigger AI jika ada antrean yang belum diproses
  aiWorkerTimer = setInterval(() => {
    if (unprocessedCount.value > 0) triggerAiQueue()
  }, 5000)
})

onUnmounted(() => {
  if (aiWorkerTimer) clearInterval(aiWorkerTimer)
})
</script>
