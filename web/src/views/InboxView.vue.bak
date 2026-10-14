<template>
  <div class="space-y-8 relative">
    <NotifyOverlay />
    <div class="flex flex-wrap justify-between items-center gap-4">
      <div>
        <h1 class="text-2xl font-bold text-slate-900 tracking-tight">Auto Reply Inbox</h1>
        <p class="text-slate-500 text-sm mt-1">Buat draf balasan AI on-demand atau balas manual komentar masuk.</p>
      </div>
      <div class="flex items-center gap-3">
        <button @click="syncRepliesManual" :disabled="isSyncing" class="bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold py-2.5 px-4 rounded-xl transition disabled:opacity-50 flex items-center gap-2">
          <span v-if="isSyncing" class="w-3 h-3 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
          <span>{{ isSyncing ? 'Menarik Komentar...' : 'Sync Komentar Baru' }}</span>
        </button>
      </div>
    </div>

    <div class="flex justify-between items-end border-b border-slate-200">
      <div class="flex text-xs font-bold gap-6">
        <button @click="activeTab = 'pending'" class="pb-3 border-b-2 transition" :class="activeTab === 'pending' ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-slate-400'">Antrean Review ({{ pendingReplies.length }})</button>
        <button @click="activeTab = 'history'" class="pb-3 border-b-2 transition" :class="activeTab === 'history' ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-slate-400'">Riwayat Terkirim ({{ historyReplies.length }})</button>
      </div>
      
      <button v-if="activeTab === 'pending' && pendingReplies.length > 0" @click="skipAllPending" :disabled="isSkippingAll" class="pb-3 text-xs font-bold text-rose-500 hover:text-rose-700 transition flex items-center gap-1.5 disabled:opacity-50">
        <span v-if="isSkippingAll" class="w-3 h-3 border-2 border-rose-500 border-t-transparent rounded-full animate-spin"></span>
        <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
        <span>{{ isSkippingAll ? 'Memproses...' : 'Abaikan Semua' }}</span>
      </button>
    </div>

    <div v-if="loading" class="p-12 text-center text-xs text-slate-400 animate-pulse">Memuat komentar...</div>

    <div v-else-if="activeTab === 'pending'" class="space-y-4">
      <div v-if="pendingReplies.length === 0" class="bg-white border border-slate-200 rounded-2xl p-12 text-center text-xs text-slate-400">Semua komentar sudah dibalas.</div>
      
      <div v-for="item in pendingReplies" :key="item.id" class="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-4">
        <div class="flex justify-between items-start">
          <div class="space-y-1">
            <span class="text-[10px] font-bold text-indigo-600 uppercase tracking-wide">@{{ item.author_username }}</span>
            <p class="text-xs text-slate-400">{{ formatDate(item.replied_at) }}</p>
          </div>
          <span v-if="item.is_lead" class="px-2.5 py-1 text-[10px] font-bold uppercase tracking-wider rounded-md bg-rose-50 text-rose-600 border border-rose-100 animate-pulse">🔥 Hot Lead</span>
        </div>

        <div class="bg-slate-50 p-3.5 rounded-xl border border-slate-200">
          <p class="text-xs font-semibold text-slate-900">"{{ item.text }}"</p>
        </div>
        
        <div class="bg-indigo-50/50 p-4 rounded-xl border border-indigo-100">
          <div class="flex justify-between items-center mb-2">
            <span class="text-[10px] font-bold text-indigo-900 uppercase">Draf Balasan AI</span>
            <button @click="generateAIDraft(item)" :disabled="generatingId === item.id" class="text-[10px] font-bold bg-purple-100 text-purple-700 hover:bg-purple-200 px-3 py-1.5 rounded-md transition flex items-center gap-1.5 disabled:opacity-50">
              <span v-if="generatingId === item.id" class="w-3 h-3 border-2 border-purple-700 border-t-transparent rounded-full animate-spin"></span>
              <span>✨ {{ generatingId === item.id ? 'Meracik...' : 'Buat Draf AI' }}</span>
            </button>
          </div>
          <textarea v-model="item.draftText" rows="3" placeholder="Tulis balasan manual atau klik tombol Buat Draf AI di atas..." class="w-full bg-white border border-indigo-200 rounded-lg p-3 text-xs focus:ring-2 focus:ring-indigo-500 resize-none"></textarea>
        </div>
        
        <div class="flex justify-end items-center gap-3">
          <button @click="skipReply(item)" class="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-lg transition">Abaikan</button>
          <button @click="approveAndPublish(item)" :disabled="approvingId === item.id || !item.draftText" class="px-5 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold rounded-lg disabled:opacity-50 transition">
            {{ approvingId === item.id ? 'Menerbitkan...' : 'Kirim ke Threads' }}
          </button>
        </div>
      </div>
    </div>
    
    <div v-else class="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">
      <div v-if="historyReplies.length === 0" class="p-12 text-center text-xs text-slate-400">Belum ada riwayat balasan terkirim.</div>
      <div v-else class="divide-y divide-slate-100">
        <div v-for="item in historyReplies" :key="item.id" class="p-5 hover:bg-slate-50 transition space-y-2">
          <div class="flex justify-between items-center">
            <span class="px-2.5 py-1 text-[10px] font-bold uppercase tracking-wider rounded-md" :class="item.is_own ? 'bg-indigo-50 text-indigo-600 border border-indigo-100' : 'bg-emerald-50 text-emerald-600 border border-emerald-100'">
              {{ item.is_own ? 'own_reply' : item.log_status }}
            </span>
            <span class="text-xs text-slate-400">{{ formatDate(item.replied_at) }}</span>
          </div>
          <p class="text-xs text-slate-500 italic">"{{ item.text }}"</p>
          <p v-if="item.draftText" class="text-xs text-slate-800 font-medium bg-slate-50 p-3 rounded-lg border border-slate-100 mt-2">Balasan: {{ item.draftText }}</p>
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

const { showToast, askConfirm } = useNotify()
const loading = ref(true)
const isSyncing = ref(false)
const isSkippingAll = ref(false)
const approvingId = ref<string | null>(null)
const generatingId = ref<string | null>(null)
const activeTab = ref<'pending' | 'history'>('pending')
const repliesData = ref<any[]>([])

const pendingReplies = computed(() => repliesData.value.filter(r => r.log_status !== 'sent' && r.log_status !== 'skipped' && !r.is_own))
const historyReplies = computed(() => repliesData.value.filter(r => r.log_status === 'sent' || r.log_status === 'skipped' || r.is_own))

function formatDate(isoString: string) {
  if (!isoString) return ''
  return new Date(isoString).toLocaleString('id-ID', { dateStyle: 'medium', timeStyle: 'short' })
}

async function safeSaveLog(payload: any) {
  const { id, ...dataToSave } = payload;
  
  const { data: existing } = await supabase.schema('threads').from('auto_reply_logs')
    .select('id').eq('reply_id', dataToSave.reply_id).maybeSingle();

  if (existing && existing.id) {
    const { data, error } = await supabase.schema('threads').from('auto_reply_logs')
      .update(dataToSave).eq('id', existing.id).select().single();
    if (error) throw error;
    return data;
  } else {
    const { data, error } = await supabase.schema('threads').from('auto_reply_logs')
      .insert(dataToSave).select().single();
    if (error) throw error;
    return data;
  }
}

// FIX TOTAL: Fetch tabel secara terpisah dan gabung pakai JS (Anti buta relasi)
async function fetchReplies() {
  loading.value = true
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) return
  const { data: account } = await supabase.schema('threads').from('threads_accounts').select('id').eq('user_id', user.id).maybeSingle()
  if (!account) return

  // 1. Ambil data replies
  const { data: repliesRaw } = await supabase
    .schema('threads')
    .from('replies')
    .select('*')
    .eq('account_id', account.id)
    .order('replied_at', { ascending: false })
    .limit(50)

  if (repliesRaw && repliesRaw.length > 0) {
    const replyIds = repliesRaw.map(r => r.id)
    
    // 2. Ambil data logs secara terpisah berdasarkan ID replies
    const { data: logsRaw } = await supabase
      .schema('threads')
      .from('auto_reply_logs')
      .select('*')
      .in('reply_id', replyIds)

    const logsArray = logsRaw || []

    // 3. Gabungkan murni menggunakan Javascript
    repliesData.value = repliesRaw.map(r => {
      const log = logsArray.find(l => l.reply_id === r.id)
      return {
        ...r,
        log_id: log ? log.id : null,
        draftText: log ? log.final_text : '',
        log_status: log ? log.status : 'unprocessed'
      }
    })
  } else {
    repliesData.value = []
  }
  
  loading.value = false
}

async function syncRepliesManual() {
  isSyncing.value = true
  try {
    const res = await fetch('https://threads-automation-production-53ad.up.railway.app/api/v1/leads/sync-replies', { method: 'GET' })
    if (!res.ok) throw new Error('Gagal terhubung ke backend Python.')
    showToast('Sinkronisasi selesai. Memuat data terbaru...', 'success')
    await fetchReplies()
  } catch (err: any) {
    showToast('Gagal sync: ' + err.message, 'error')
  } finally {
    isSyncing.value = false
  }
}

async function generateAIDraft(item: any) {
  generatingId.value = item.id
  try {
    const res = await fetch('https://threads-automation-production-53ad.up.railway.app/api/v1/rag/generate-reply', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        account_id: item.account_id,
        user_comment: item.text,
        author_username: item.author_username
      })
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.detail || 'Gagal generate respon AI')
    
    item.draftText = data.reply
    
    const savedData = await safeSaveLog({
      account_id: item.account_id,
      reply_id: item.id,
      status: 'pending_review',
      final_text: data.reply,
      llm_meta: { incoming_comment: item.text, username: item.author_username }
    });
    
    if (savedData) {
      item.log_id = savedData.id
      item.log_status = savedData.status
    }
    showToast('Draf AI diracik dan disimpan permanen!', 'success')
  } catch (err: any) {
    showToast('Gagal AI: ' + err.message, 'error')
  } finally {
    generatingId.value = null
  }
}

async function skipReply(item: any) {
  // Update UI instan
  item.log_status = 'skipped'
  try {
    const savedData = await safeSaveLog({
      account_id: item.account_id,
      reply_id: item.id,
      status: 'skipped',
      final_text: item.draftText || 'Diabaikan manual'
    });
    if (savedData) item.log_id = savedData.id
    showToast('Komentar berhasil diabaikan.', 'info')
  } catch (err: any) {
    showToast('Gagal mengabaikan: ' + err.message, 'error')
    await fetchReplies() 
  }
}

async function skipAllPending() {
  if (pendingReplies.value.length === 0) return
  
  askConfirm({
    title: 'Abaikan Semua Komentar',
    message: `Kamu yakin ingin memindahkan ${pendingReplies.value.length} komentar ke riwayat?`,
    confirmText: 'Ya, Abaikan Semua',
    onConfirm: async () => {
      isSkippingAll.value = true
      try {
        // Hapus langsung dari UI detik itu juga
        const itemsToProcess = [...pendingReplies.value]
        itemsToProcess.forEach(i => i.log_status = 'skipped')

        // Eksekusi update database di background
        for (const item of itemsToProcess) {
          await safeSaveLog({
            account_id: item.account_id,
            reply_id: item.id,
            status: 'skipped',
            final_text: item.draftText || 'Diabaikan manual (massal)'
          });
        }
        showToast('Semua komentar berhasil dibersihkan dari antrean.', 'success')
      } catch (err: any) {
        showToast('Gagal memproses masal: ' + err.message, 'error')
        await fetchReplies()
      } finally {
        isSkippingAll.value = false
      }
    }
  })
}

async function approveAndPublish(item: any) {
  approvingId.value = item.id
  try {
    const res = await fetch('https://threads-automation-production-53ad.up.railway.app/api/v1/leads/publish-reply', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        account_id: item.account_id,
        threads_reply_id: item.threads_reply_id,
        text: item.draftText,
        log_id: item.log_id
      })
    })
    
    const data = await res.json()
    if (!res.ok) throw new Error(data.detail || 'Gagal API Threads')

    const savedData = await safeSaveLog({
      account_id: item.account_id,
      reply_id: item.id,
      status: 'sent',
      final_text: item.draftText
    });
    
    if (savedData) item.log_id = savedData.id
    item.log_status = 'sent'
    showToast('Berhasil diterbitkan ke Threads!', 'success')
  } catch (err: any) {
    showToast('Gagal memproses: ' + err.message, 'error')
  } finally {
    approvingId.value = null
  }
}

onMounted(() => fetchReplies())
</script>
