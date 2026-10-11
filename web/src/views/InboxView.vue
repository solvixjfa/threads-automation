<template>
  <div class="space-y-8 relative">
    <NotifyOverlay />
    <div class="flex flex-wrap justify-between items-center gap-4">
      <div>
        <h1 class="text-2xl font-bold text-slate-900 tracking-tight">Auto Reply Inbox & Leads</h1>
        <p class="text-slate-500 text-sm mt-1">Kelola komentar masuk dan pantau prospek panas (Hot Leads).</p>
      </div>
      <div class="flex items-center gap-3">
        <button @click="syncRepliesManual" :disabled="isSyncing" class="bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold py-2.5 px-4 rounded-xl transition disabled:opacity-50 flex items-center gap-2">
          <span v-if="isSyncing" class="w-3 h-3 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
          <span>{{ isSyncing ? 'Menyinkronkan...' : 'Sync Komentar Threads' }}</span>
        </button>
      </div>
    </div>

    <!-- Tab Filter: Semua Pesan vs Hot Leads -->
    <div class="flex border-b border-slate-200 text-xs font-bold gap-6">
      <button @click="activeTab = 'all'" class="pb-3 border-b-2 transition" :class="activeTab === 'all' ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-slate-400'">Semua Pesan ({{ replies.length }})</button>
      <button @click="activeTab = 'leads'" class="pb-3 border-b-2 transition" :class="activeTab === 'leads' ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-slate-400'">🔥 Hot Leads ({{ hotLeadsCount }})</button>
    </div>

    <div v-if="loading" class="p-12 text-center text-xs text-slate-400 animate-pulse">Memuat pesan inbox...</div>

    <!-- List Pesan / Komentar -->
    <div v-else class="space-y-4">
      <div v-if="filteredReplies.length === 0" class="bg-white border border-slate-200 rounded-2xl p-12 text-center text-xs text-slate-400">
        Belum ada komentar di kategori ini.
      </div>

      <div v-for="item in filteredReplies" :key="item.id" class="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-4">
        <div class="flex justify-between items-start">
          <div class="space-y-1">
            <span class="text-[10px] font-bold text-indigo-600 uppercase tracking-wide">@{{ item.author_username }}</span>
            <p class="text-xs text-slate-400">{{ formatDate(item.replied_at || item.created_at) }}</p>
          </div>
          <span v-if="item.is_lead" class="px-2.5 py-1 text-[10px] font-bold uppercase tracking-wider rounded-md bg-rose-50 text-rose-600 border border-rose-100 animate-pulse">
            🔥 Hot Lead
          </span>
        </div>

        <div class="bg-slate-50 p-3.5 rounded-xl border border-slate-200">
          <p class="text-xs font-semibold text-slate-900">"{{ item.text }}"</p>
        </div>

        <div class="bg-indigo-50/50 p-4 rounded-xl border border-indigo-100 space-y-2">
          <span class="text-[10px] font-bold text-indigo-900 uppercase">Tulis Balasan Manual</span>
          <textarea v-model="item.replyInput" rows="2" placeholder="Tulis balasan untuk audiens ini..." class="w-full bg-white border border-indigo-200 rounded-lg p-3 text-xs focus:ring-2 focus:ring-indigo-500 resize-none"></textarea>
          <div class="flex justify-end">
            <button @click="sendManualReply(item)" :disabled="sendingId === item.id || !item.replyInput" class="px-5 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold rounded-lg disabled:opacity-50 transition">
              {{ sendingId === item.id ? 'Mengirim...' : 'Kirim Balasan' }}
            </button>
          </div>
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
const sendingId = ref<string | null>(null)
const activeTab = ref<'all' | 'leads'>('all')
const replies = ref<any[]>([])

const hotLeadsCount = computed(() => replies.value.filter(r => r.is_lead).length)
const filteredReplies = computed(() => {
  if (activeTab.value === 'leads') {
    return replies.value.filter(r => r.is_lead)
  }
  return replies.value
})

function formatDate(isoString: string) {
  if (!isoString) return ''
  return new Date(isoString).toLocaleString('id-ID', { dateStyle: 'medium', timeStyle: 'short' })
}

async function fetchReplies() {
  loading.value = true
  try {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) return
    const { data: account } = await supabase.schema('threads').from('threads_accounts').select('id').eq('user_id', user.id).maybeSingle()
    if (!account) return

    const { data, error } = await supabase
      .schema('threads')
      .from('replies')
      .select('*')
      .eq('account_id', account.id)
      .order('replied_at', { ascending: false })
      .limit(50)

    if (error) throw error
    
    // Tambah state input lokal untuk balasan
    replies.value = (data || []).map(r => ({ ...r, replyInput: '' }))
  } catch (err: any) {
    showToast('Gagal memuat inbox: ' + err.message, 'error')
  } finally {
    loading.value = false
  }
}

async function syncRepliesManual() {
  isSyncing.value = true
  try {
    const res = await fetch('https://threads-automation-production-53ad.up.railway.app/api/v1/leads/sync-replies')
    const json = await res.json()
    if (!res.ok) throw new Error(json.detail || 'Gagal sinkronisasi')

    showToast('Inbox berhasil disinkronkan dari Meta!', 'success')
    await fetchReplies()
  } catch (err: any) {
    showToast('Gagal sync: ' + err.message, 'error')
  } finally {
    isSyncing.value = false
  }
}

async function sendManualReply(item: any) {
  sendingId.value = item.id
  try {
    // Fitur kirim balasan langsung via Graph API bisa di-mapping ke backend jika diperlukan
    showToast('Fitur kirim balasan langsung segera aktif.', 'info')
  } catch (err: any) {
    showToast('Gagal mengirim: ' + err.message, 'error')
  } finally {
    sendingId.value = null
  }
}

onMounted(() => fetchReplies())
</script>
