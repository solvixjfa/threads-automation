<template>
  <div class="space-y-8 relative">
    <NotifyOverlay />

    <div class="flex flex-wrap justify-between items-center gap-4">
      <div>
        <h1 class="text-2xl font-bold text-slate-900 tracking-tight">Auto Reply Inbox</h1>
        <p class="text-slate-500 text-sm mt-1">Review dan kelola balasan komentar otomatis buatan AI sebelum terbit ke Threads.</p>
      </div>
      <div class="flex items-center gap-3">
        <button 
          @click="pollRealComments" 
          :disabled="isPolling || isSimulating"
          class="bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold py-2.5 px-4 rounded-xl transition shadow-sm disabled:opacity-50 flex items-center gap-2"
        >
          <span v-if="isPolling" class="w-3 h-3 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
          <span>{{ isPolling ? 'Menyinkronkan...' : 'Sync Komentar Threads' }}</span>
        </button>
        <button 
          @click="simulateComment" 
          :disabled="isSimulating || isPolling"
          class="bg-indigo-50 text-indigo-700 hover:bg-indigo-100 text-xs font-bold py-2.5 px-4 rounded-xl border border-indigo-100 transition disabled:opacity-50 flex items-center gap-2"
        >
          <span v-if="isSimulating" class="w-3 h-3 border-2 border-indigo-600 border-t-transparent rounded-full animate-spin"></span>
          <span>{{ isSimulating ? 'Memproses...' : '+ Tes Simulasi' }}</span>
        </button>
      </div>
    </div>

    <!-- Status Processing Indicator -->
    <div v-if="unprocessedCount > 0" class="bg-indigo-50 border border-indigo-100 rounded-xl p-3.5 flex items-center justify-between text-xs">
      <div class="flex items-center gap-2.5 text-indigo-900 font-bold">
        <span class="w-2 h-2 rounded-full bg-indigo-600 animate-ping"></span>
        <span>AI sedang memproses {{ unprocessedCount }} komentar di background (Vector RAG + Gemini)...</span>
      </div>
      <button @click="fetchLogs" class="text-indigo-700 font-bold underline hover:text-indigo-900">Refresh Status</button>
    </div>

    <!-- Filter Tab -->
    <div class="flex border-b border-slate-200 text-xs font-bold gap-6">
      <button 
        @click="activeTab = 'pending'"
        class="pb-3 border-b-2 transition flex items-center gap-2"
        :class="activeTab === 'pending' ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-slate-400 hover:text-slate-600'"
      >
        <span>Antrean Review</span>
        <span class="bg-amber-100 text-amber-800 px-2 py-0.5 rounded-full text-[10px]">{{ pendingLogs.length }}</span>
      </button>
      <button 
        @click="activeTab = 'history'"
        class="pb-3 border-b-2 transition flex items-center gap-2"
        :class="activeTab === 'history' ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-slate-400 hover:text-slate-600'"
      >
        <span>Riwayat Terkirim / Skipped</span>
        <span class="bg-slate-100 text-slate-600 px-2 py-0.5 rounded-full text-[10px]">{{ historyLogs.length }}</span>
      </button>
    </div>

    <div v-if="loading" class="p-12 text-center text-xs text-slate-400 animate-pulse font-medium">
      Memuat pesan dan balasan AI...
    </div>

    <!-- Tab 1: Pending Review -->
    <div v-else-if="activeTab === 'pending'" class="space-y-4">
      <div v-if="pendingLogs.length === 0" class="bg-white border border-slate-200 rounded-2xl p-12 text-center text-xs text-slate-400 font-medium space-y-3">
        <p>Belum ada balasan komentar yang menunggu review.</p>
        <div class="flex justify-center gap-3">
          <button 
            @click="pollRealComments" 
            class="bg-indigo-600 text-white font-bold px-4 py-2 rounded-lg text-xs hover:bg-indigo-700 transition"
          >
            Sync Komentar Asli
          </button>
          <button 
            @click="simulateComment" 
            class="bg-indigo-50 text-indigo-700 font-bold px-4 py-2 rounded-lg text-xs hover:bg-indigo-100 transition"
          >
            Uji Coba Simulasi
          </button>
        </div>
      </div>

      <div v-for="log in pendingLogs" :key="log.id" class="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-4">
        <div class="flex justify-between items-start">
          <span class="text-[10px] font-bold uppercase tracking-wider bg-amber-50 text-amber-600 border border-amber-100 px-2.5 py-1 rounded-md">
            Menunggu Review
          </span>
          <span class="text-xs text-slate-400">{{ formatDate(log.created_at) }}</span>
        </div>

        <!-- Komentar Audiens -->
        <div v-if="log.llm_meta?.incoming_comment" class="bg-slate-50 p-3.5 rounded-xl border border-slate-200 space-y-1">
          <span class="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Komentar Audiens:</span>
          <p class="text-xs font-semibold text-slate-900">"{{ log.llm_meta.incoming_comment }}"</p>
        </div>

        <!-- Draf AI -->
        <div class="space-y-1.5 bg-indigo-50/50 p-4 rounded-xl border border-indigo-100">
          <div class="flex justify-between items-center">
            <span class="text-[10px] font-bold text-indigo-900 uppercase tracking-wider">Draf Balasan AI (Gemini + Vector RAG)</span>
            <span v-if="log.llm_meta?.model" class="text-[9px] font-bold text-indigo-600 bg-white px-2 py-0.5 rounded border border-indigo-100">
              Model: {{ log.llm_meta.model }}
            </span>
          </div>
          <textarea
            v-model="log.final_text"
            rows="3"
            class="w-full bg-white border border-indigo-200 rounded-lg p-3 text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition resize-none"
          ></textarea>
        </div>

        <div class="flex justify-end items-center gap-3 pt-1">
          <button
            @click="updateStatus(log.id, 'skipped', log.final_text)"
            class="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-lg transition"
          >
            Abaikan / Skip
          </button>
          <button
            @click="approveAndPublish(log)"
            :disabled="approvingId === log.id"
            class="px-5 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold rounded-lg transition shadow-sm disabled:opacity-50 flex items-center gap-2"
          >
            <span v-if="approvingId === log.id" class="w-3 h-3 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
            <span>{{ approvingId === log.id ? 'Menerbitkan...' : 'Approve & Kirim ke Threads' }}</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Tab 2: History -->
    <div v-else class="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">
      <div v-if="historyLogs.length === 0" class="p-12 text-center text-xs text-slate-400 font-medium">
        Belum ada riwayat balasan terkirim atau diabaikan.
      </div>
      <div v-else class="divide-y divide-slate-100">
        <div v-for="log in historyLogs" :key="log.id" class="p-5 hover:bg-slate-50 transition space-y-2">
          <div class="flex justify-between items-center">
            <span
              class="px-2.5 py-1 text-[10px] font-bold uppercase tracking-wider rounded-md"
              :class="{
                'bg-emerald-50 text-emerald-600 border border-emerald-100': ['sent', 'approved'].includes(log.status),
                'bg-slate-100 text-slate-600 border border-slate-200': log.status === 'skipped'
              }"
            >
              {{ log.status }}
            </span>
            <span class="text-xs text-slate-400">{{ formatDate(log.created_at) }}</span>
          </div>

          <p v-if="log.llm_meta?.incoming_comment" class="text-xs text-slate-500 italic">
            Komentar: "{{ log.llm_meta.incoming_comment }}"
          </p>

          <p class="text-xs text-slate-800 font-medium bg-slate-50 p-3 rounded-lg border border-slate-100 whitespace-pre-wrap">
            Balasan: {{ log.final_text || log.generated_text || 'Tidak ada isi balasan.' }}
          </p>
        </div>
      </div>
    </div>
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
const approvingId = ref<string | null>(null)
const activeTab = ref<'pending' | 'history'>('pending')
const logs = ref<any[]>([])
let pollTimer: any = null

const pendingLogs = computed(() => logs.value.filter(l => l.status === 'pending' || l.status === 'generated'))
const historyLogs = computed(() => logs.value.filter(l => l.status !== 'pending' && l.status !== 'generated'))
const unprocessedCount = computed(() => logs.value.filter(l => l.status === 'unprocessed').length)

function formatDate(isoString: string) {
  if (!isoString) return ''
  return new Date(isoString).toLocaleString('id-ID', { dateStyle: 'medium', timeStyle: 'short' })
}

async function fetchLogs() {
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) {
    loading.value = false
    return
  }

  const { data: account } = await supabase
    .schema('threads')
    .from('threads_accounts')
    .select('id')
    .eq('user_id', user.id)
    .maybeSingle()

  if (!account) {
    loading.value = false
    return
  }

  const { data } = await supabase
    .schema('threads')
    .from('auto_reply_logs')
    .select('*')
    .eq('account_id', account.id)
    .order('created_at', { ascending: false })
    .limit(30)

  if (data) logs.value = data
  loading.value = false
}

async function pollRealComments() {
  isPolling.value = true
  try {
    const { data, error } = await supabase.functions.invoke('worker-replies', {
      body: { action: 'sync' }
    })
    if (error) throw error
    if (data?.error) throw new Error(data.error)

    showToast(`Sync selesai dalam < 1s! ${data?.newItems || 0} komentar baru sedang diproses AI.`, 'success')
    await fetchLogs()
  } catch (err: any) {
    showToast('Gagal sync komentar: ' + err.message, 'error')
  } finally {
    isPolling.value = false
  }
}

async function simulateComment() {
  const sampleComments = [
    "Project machine learning XGBoost churn ini akurasinya berapa persen bro?",
    "Bro, Zora AI WhatsApp Agent ini pakai stack opo aja backend-nya?",
    "Teknologi Metal Defect Inspection yang presisi 98.2% itu pake MobileNetV2 ya?",
    "Minimalist banget desain app-nya, bikin pake Tailwind v3 opo Bootstrap 5?"
  ]
  const randomComment = sampleComments[Math.floor(Math.random() * sampleComments.length)]

  isSimulating.value = true
  try {
    const { data, error } = await supabase.functions.invoke('worker-replies', {
      body: { action: 'sync', comment: randomComment }
    })

    if (error) throw error
    if (data?.error) throw new Error(data.error)

    showToast('Komentar simulasi ditambahkan, AI sedang memproses di background!', 'info')
    await fetchLogs()
  } catch (err: any) {
    showToast('Gagal simulasi komentar: ' + err.message, 'error')
  } finally {
    isSimulating.value = false
  }
}

async function approveAndPublish(log: any) {
  approvingId.value = log.id
  try {
    if (log.llm_meta?.media_id === 'simulated_media') {
      await updateStatus(log.id, 'approved', log.final_text)
      showToast('Balasan simulasi disetujui.', 'info')
    } else {
      const { data, error } = await supabase.functions.invoke('worker-replies', {
        body: { action: 'publish_reply', log_id: log.id, final_text: log.final_text }
      })
      if (error) throw error
      if (data?.error) throw new Error(data.error)

      showToast('Balasan berhasil diterbitkan ke Threads!', 'success')
      await fetchLogs()
    }
  } catch (err: any) {
    showToast('Gagal menerbitkan balasan: ' + err.message, 'error')
  } finally {
    approvingId.value = null
  }
}

async function updateStatus(id: string, newStatus: string, finalText: string) {
  try {
    const { error } = await supabase
      .schema('threads')
      .from('auto_reply_logs')
      .update({
        status: newStatus,
        final_text: finalText
      })
      .eq('id', id)

    if (error) throw error
    await fetchLogs()
  } catch (err: any) {
    showToast('Gagal perbarui status: ' + err.message, 'error')
  }
}

onMounted(() => {
  fetchLogs()
  // Auto refresh tiap 4 detik jika ada item unprocessed
  pollTimer = setInterval(() => {
    if (unprocessedCount.value > 0) fetchLogs()
  }, 4000)
})

onUnmounted(() => {
  if (pollTimer) clearInterval(pollTimer)
})
</script>
