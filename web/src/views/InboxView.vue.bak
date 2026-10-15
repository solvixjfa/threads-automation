<template>
  <div class="space-y-8 relative">
    <NotifyOverlay />

    <div class="flex flex-wrap justify-between items-center gap-4">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Auto Reply Inbox</h1>
        <p class="text-sm theme-text-muted mt-1">Kelola komentar masuk dengan draf AI atau balasan template.</p>
      </div>
      <div class="flex items-center gap-3">
        <button @click="syncRepliesManual" :disabled="isSyncing" class="btn btn-primary btn-sm">
          <span v-if="isSyncing" class="w-3 h-3 border-2 border-current border-t-transparent rounded-full animate-spin"></span>
          <span>{{ isSyncing ? 'Menarik Komentar...' : 'Sync Komentar Baru' }}</span>
        </button>
      </div>
    </div>

    <div class="flex justify-between items-end divider">
      <div class="flex text-xs font-bold gap-5 overflow-x-auto">
        <button
          @click="activeTab = 'review'"
          class="pb-3 border-b-2 transition -mb-px whitespace-nowrap"
          :class="tabClass('review')"
        >
          Review ({{ reviewCount }})
        </button>
        <button
          @click="activeTab = 'lead'"
          class="pb-3 border-b-2 transition -mb-px whitespace-nowrap"
          :class="tabClass('lead')"
        >
          Hot Lead ({{ leadCount }})
        </button>
        <button
          @click="activeTab = 'all'"
          class="pb-3 border-b-2 transition -mb-px whitespace-nowrap"
          :class="tabClass('all')"
        >
          Semua ({{ allCount }})
        </button>
        <button
          @click="activeTab = 'history'"
          class="pb-3 border-b-2 transition -mb-px whitespace-nowrap"
          :class="tabClass('history')"
        >
          Riwayat ({{ historyCount }})
        </button>
      </div>

      <button
        v-if="activeTab === 'review' && reviewReplies.length > 0"
        @click="skipAllPending"
        :disabled="isSkippingAll"
        class="pb-3 text-xs font-bold theme-text-muted hover:theme-text transition flex items-center gap-1.5 disabled:opacity-50 shrink-0"
      >
        <span v-if="isSkippingAll" class="w-3 h-3 border-2 border-current border-t-transparent rounded-full animate-spin"></span>
        <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
        </svg>
        <span>{{ isSkippingAll ? 'Memproses...' : 'Abaikan Semua' }}</span>
      </button>
    </div>

    <div v-if="loading" class="p-12 text-center text-xs theme-text-muted animate-pulse">Memuat komentar...</div>

    <div v-else-if="activeTab !== 'history'" class="space-y-4">
      <div v-if="currentReplies.length === 0" class="card p-12 text-center text-xs theme-text-muted">
        {{ emptyMessage }}
      </div>

      <div v-for="item in currentReplies" :key="item.id" class="card p-6 space-y-4">
        <div class="flex justify-between items-start gap-3">
          <div class="space-y-1 min-w-0">
            <div class="flex items-center gap-2 flex-wrap">
              <span class="text-[10px] font-bold uppercase tracking-wide theme-text">@{{ item.author_username }}</span>
              <Badge>{{ categoryLabel(item.classification) }}</Badge>
              <span v-if="item.is_lead" class="badge badge-accent">
                <span class="w-1.5 h-1.5 rounded-full animate-pulse" style="background: currentColor;"></span>
                Hot Lead
              </span>
            </div>
            <p class="text-xs theme-text-muted">{{ formatDate(item.replied_at) }}</p>
          </div>
        </div>

        <div class="p-3.5 rounded-xl theme-bg-sec border theme-border">
          <p class="text-xs font-semibold whitespace-pre-wrap">{{ item.text }}</p>
        </div>

        <div v-if="item.auto_reply_eligible" class="p-4 rounded-xl theme-bg-sec border theme-border">
          <div class="flex justify-between items-center mb-2">
            <span class="text-[10px] font-bold uppercase theme-text-sec">
              {{ item.log_status === 'pending_review' || item.log_status === 'approved' ? 'Draf Balasan' : 'Draf Balasan AI' }}
            </span>
            <button
              @click="generateAIDraft(item)"
              :disabled="generatingId === item.id"
              class="btn btn-secondary btn-sm"
            >
              <span v-if="generatingId === item.id" class="w-3 h-3 border-2 border-current border-t-transparent rounded-full animate-spin"></span>
              <span>{{ generatingId === item.id ? 'Meracik...' : (item.draftText ? 'Regenerate' : 'Buat Draf AI') }}</span>
            </button>
          </div>
          <textarea
            v-model="item.draftText"
            rows="3"
            placeholder="Tulis balasan manual atau klik tombol Buat Draf AI di atas..."
            class="textarea"
          ></textarea>
        </div>

        <div v-else class="p-3 rounded-xl theme-bg-sec border theme-border">
          <p class="text-[11px] theme-text-muted">
            <span v-if="item.classification === 'spam'">Komentar dikategorikan sebagai spam. Tidak dibuatkan draf.</span>
            <span v-else-if="item.classification === 'toxic'">Komentar dikategorikan toxic. Tidak dibuatkan draf.</span>
            <span v-else-if="item.classification === 'unclassified'">Belum diklasifikasi otomatis. Kamu bisa buat draf manual.</span>
            <span v-else>Komentar ini belum masuk antrean balasan otomatis.</span>
          </p>
        </div>

        <div class="flex justify-end items-center gap-3">
          <button @click="skipReply(item)" class="btn btn-ghost btn-sm">Abaikan</button>
          <button
            @click="approveAndPublish(item)"
            :disabled="approvingId === item.id || !item.draftText"
            class="btn btn-primary btn-sm"
          >
            <span v-if="approvingId === item.id" class="w-3 h-3 border-2 border-current border-t-transparent rounded-full animate-spin"></span>
            <span>{{ approvingId === item.id ? 'Menerbitkan...' : 'Kirim ke Threads' }}</span>
          </button>
        </div>
      </div>
    </div>

    <div v-else class="card overflow-hidden">
      <div v-if="historyReplies.length === 0" class="p-12 text-center text-xs theme-text-muted">
        Belum ada riwayat balasan terkirim.
      </div>
      <div v-else class="list-divided">
        <div v-for="item in historyReplies" :key="item.id" class="p-5 space-y-2">
          <div class="flex justify-between items-center gap-3">
            <div class="flex items-center gap-2 flex-wrap">
              <span class="text-[10px] font-bold uppercase tracking-wide theme-text">@{{ item.author_username }}</span>
              <Badge :variant="historyBadgeVariant(item)">{{ historyBadgeLabel(item) }}</Badge>
              <Badge>{{ categoryLabel(item.classification) }}</Badge>
            </div>
            <span class="text-xs theme-text-muted shrink-0">{{ formatDate(item.replied_at) }}</span>
          </div>
          <p class="text-xs theme-text-muted italic whitespace-pre-wrap">{{ item.text }}</p>
          <p v-if="item.draftText" class="text-xs font-medium p-3 rounded-lg theme-bg-sec border theme-border mt-2 whitespace-pre-wrap">
            {{ item.draftText }}
          </p>
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
import { Badge } from '../components/ui'

const { showToast, askConfirm } = useNotify()
const loading = ref(true)
const isSyncing = ref(false)
const isSkippingAll = ref(false)
const approvingId = ref<string | null>(null)
const generatingId = ref<string | null>(null)
const activeTab = ref<'review' | 'lead' | 'all' | 'history'>('review')
const repliesData = ref<any[]>([])

const AUTO_REPLY_CATEGORIES = ['praise', 'neutral', 'question']

const allReplies = computed(() =>
  repliesData.value.filter(r => !r.is_own)
)

const reviewReplies = computed(() =>
  allReplies.value.filter(r =>
    r.log_status === 'pending_review' || r.log_status === 'approved'
  )
)

const leadReplies = computed(() =>
  allReplies.value
    .filter(r => r.is_lead && r.log_status !== 'sent' && r.log_status !== 'skipped')
    .sort((a, b) => new Date(b.replied_at).getTime() - new Date(a.replied_at).getTime())
)

const historyReplies = computed(() =>
  repliesData.value.filter(r =>
    r.log_status === 'sent' || r.log_status === 'skipped' || r.is_own
  )
)

const reviewCount = computed(() => reviewReplies.value.length)
const leadCount = computed(() => leadReplies.value.length)
const allCount = computed(() => allReplies.value.length)
const historyCount = computed(() => historyReplies.value.length)

const currentReplies = computed(() => {
  if (activeTab.value === 'review') return reviewReplies.value
  if (activeTab.value === 'lead') return leadReplies.value
  if (activeTab.value === 'all') return allReplies.value
  return []
})

const emptyMessage = computed(() => {
  if (activeTab.value === 'review') return 'Tidak ada draf yang menunggu review.'
  if (activeTab.value === 'lead') return 'Belum ada hot lead terdeteksi.'
  if (activeTab.value === 'all') return 'Belum ada komentar tersinkron.'
  return 'Tidak ada data.'
})

function tabClass(tab: string) {
  return activeTab.value === tab
    ? 'border-current theme-text'
    : 'border-transparent theme-text-muted hover:theme-text'
}

function formatDate(isoString: string) {
  if (!isoString) return ''
  return new Date(isoString).toLocaleString('id-ID', { dateStyle: 'medium', timeStyle: 'short' })
}

function categoryLabel(cat: string | null | undefined) {
  if (!cat) return 'unclassified'
  return cat
}

function historyBadgeVariant(item: any) {
  if (item.is_own) return 'default'
  if (item.log_status === 'sent') return 'accent'
  return 'default'
}

function historyBadgeLabel(item: any) {
  if (item.is_own) return 'own reply'
  if (item.log_status === 'sent') return 'sent'
  if (item.log_status === 'skipped') return 'skipped'
  return item.log_status || 'unknown'
}

async function safeSaveLog(payload: any) {
  const { id, ...dataToSave } = payload

  const { data: existing } = await supabase
    .schema('threads')
    .from('auto_reply_logs')
    .select('id')
    .eq('reply_id', dataToSave.reply_id)
    .maybeSingle()

  if (existing && existing.id) {
    const { data, error } = await supabase
      .schema('threads')
      .from('auto_reply_logs')
      .update(dataToSave)
      .eq('id', existing.id)
      .select()
      .single()
    if (error) throw error
    return data
  } else {
    const { data, error } = await supabase
      .schema('threads')
      .from('auto_reply_logs')
      .insert(dataToSave)
      .select()
      .single()
    if (error) throw error
    return data
  }
}

async function fetchReplies() {
  loading.value = true
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) return

  const { data: account } = await supabase
    .schema('threads')
    .from('threads_accounts')
    .select('id')
    .eq('user_id', user.id)
    .maybeSingle()

  if (!account) return

  const { data: repliesRaw } = await supabase
    .schema('threads')
    .from('replies')
    .select('*')
    .eq('account_id', account.id)
    .order('replied_at', { ascending: false })
    .limit(100)

  if (repliesRaw && repliesRaw.length > 0) {
    const replyIds = repliesRaw.map(r => r.id)

    const { data: logsRaw } = await supabase
      .schema('threads')
      .from('auto_reply_logs')
      .select('*')
      .in('reply_id', replyIds)

    const logsArray = logsRaw || []

    repliesData.value = repliesRaw.map(r => {
      const log = logsArray.find(l => l.reply_id === r.id)
      const eligible = AUTO_REPLY_CATEGORIES.includes(r.classification)
      return {
        ...r,
        log_id: log ? log.id : null,
        draftText: log ? log.final_text : '',
        log_status: log ? log.status : 'unprocessed',
        auto_reply_eligible: eligible,
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
    })

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
  item.log_status = 'skipped'
  try {
    const savedData = await safeSaveLog({
      account_id: item.account_id,
      reply_id: item.id,
      status: 'skipped',
      final_text: item.draftText || 'Diabaikan manual'
    })
    if (savedData) item.log_id = savedData.id
    showToast('Komentar berhasil diabaikan.', 'info')
  } catch (err: any) {
    showToast('Gagal mengabaikan: ' + err.message, 'error')
    await fetchReplies()
  }
}

async function skipAllPending() {
  if (reviewReplies.value.length === 0) return

  askConfirm({
    title: 'Abaikan Semua Komentar',
    message: 'Kamu yakin ingin memindahkan ' + reviewReplies.value.length + ' komentar ke riwayat?',
    confirmText: 'Ya, Abaikan Semua',
    onConfirm: async () => {
      isSkippingAll.value = true
      try {
        const itemsToProcess = [...reviewReplies.value]
        itemsToProcess.forEach(i => i.log_status = 'skipped')

        for (const item of itemsToProcess) {
          await safeSaveLog({
            account_id: item.account_id,
            reply_id: item.id,
            status: 'skipped',
            final_text: item.draftText || 'Diabaikan manual (massal)'
          })
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
    })

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
