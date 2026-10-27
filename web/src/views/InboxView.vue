<template>
  <div class="space-y-8 relative">
    <div class="flex flex-wrap justify-between items-center gap-4">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Comments</h1>
        <p class="text-sm theme-text-muted mt-1">Reply to comments on your posts with AI drafts or templates.</p>
      </div>
      <div class="flex items-center gap-3">
        <button @click="syncRepliesManual" :disabled="isSyncing" class="btn btn-primary btn-sm">
          <span v-if="isSyncing" class="w-3 h-3 border-2 border-current border-t-transparent rounded-full animate-spin"></span>
          <span>{{ isSyncing ? 'Syncing...' : 'Sync Comments' }}</span>
        </button>
      </div>
    </div>

    <!-- AI SETTINGS BAR -->
    <div class="p-4 rounded-xl border theme-border flex flex-wrap items-center justify-between gap-4" style="background: var(--bg-sec);">
      <div class="flex items-center gap-3">
        <div class="flex items-center gap-2 px-3 py-1.5 rounded-lg border text-xs font-bold transition-colors"
          :style="isUsingOwnKey ? 'border-color: var(--success); color: var(--success);' : (aiCredits > 0 ? 'border-color: var(--accent); color: var(--accent);' : 'border-color: var(--danger); color: var(--danger);')">
          <span class="w-2 h-2 rounded-full" :style="isUsingOwnKey ? 'background: var(--success);' : (aiCredits > 0 ? 'background: var(--accent);' : 'background: var(--danger);')"></span>
          <span v-if="isUsingOwnKey">Unlimited (Own Key)</span>
          <span v-else-if="aiCredits > 0">{{ aiCredits }} Credits Left</span>
          <span v-else>Out of Credits</span>
        </div>
      </div>
      <div class="flex items-center gap-3">
        <Select v-model="aiProvider" :options="[{label: 'Groq (Fast)', value: 'groq'}, {label: 'Gemini (Smart)', value: 'gemini'}]" @update:model-value="fetchModels" />
        <Select v-model="aiModel" :options="availableModels" :disabled="isLoadingModels" class="min-w-[150px]" />
      </div>
    </div>

    <div class="flex justify-between items-end divider">
      <div class="flex text-xs font-bold gap-5 overflow-x-auto">
        <button @click="activeTab = 'review'" class="pb-3 border-b-2 transition -mb-px whitespace-nowrap" :class="tabClass('review')">
          Review ({{ reviewCount }})
        </button>
        <button @click="activeTab = 'priority'" class="pb-3 border-b-2 transition -mb-px whitespace-nowrap" :class="tabClass('priority')">
          Priority ({{ priorityCount }})
        </button>
        <button @click="activeTab = 'conversation'" class="pb-3 border-b-2 transition -mb-px whitespace-nowrap" :class="tabClass('conversation')">
          Conversation ({{ conversationCount }})
        </button>
        <button @click="activeTab = 'history'" class="pb-3 border-b-2 transition -mb-px whitespace-nowrap" :class="tabClass('history')">
          History ({{ historyCount }})
        </button>
      </div>

      <button v-if="activeTab === 'review' && reviewReplies.length > 0" @click="skipAllPending" :disabled="isSkippingAll" class="pb-3 text-xs font-bold theme-text-muted hover:theme-text transition flex items-center gap-1.5 disabled:opacity-50 shrink-0">
        <span v-if="isSkippingAll" class="w-3 h-3 border-2 border-current border-t-transparent rounded-full animate-spin"></span>
        <span>{{ isSkippingAll ? 'Processing...' : 'Ignore All' }}</span>
      </button>
    </div>

    <div v-if="loading" class="p-12 text-center text-xs theme-text-muted animate-pulse">Loading comments...</div>

    <div v-else-if="activeTab !== 'history'" class="space-y-4">
      <div v-if="currentReplies.length === 0" class="card p-12 text-center text-xs theme-text-muted">
        {{ emptyMessage }}
      </div>

      <div v-for="item in currentReplies" :key="item.id" class="card p-6 space-y-4">
        <div class="flex justify-between items-start gap-3">
          <div class="space-y-1 min-w-0">
            <div class="flex items-center gap-2 flex-wrap">
              <span class="text-[10px] font-bold uppercase tracking-wide theme-text">@{{ item.author_username }}</span>
              <Badge>{{ item.classification || 'unclassified' }}</Badge>
              <span v-if="item.is_lead" class="badge badge-accent">
                <span class="w-1.5 h-1.5 rounded-full animate-pulse" style="background: currentColor;"></span>
                Lead
              </span>
            </div>
            <p class="text-xs theme-text-muted">{{ formatDate(item.replied_at) }}</p>
          </div>
        </div>
        
        <!-- HANDLE MEDIA / GAMBAR -->
        <div class="p-3.5 rounded-xl theme-bg-sec border theme-border space-y-3">
          <!-- Nampilin gambar kalau ada -->
          <div v-if="item.media_url" class="rounded-lg overflow-hidden border theme-border max-w-sm">
            <img :src="item.media_url" alt="Comment media" class="w-full h-auto object-cover" />
          </div>
          <p v-if="item.text" class="text-xs font-semibold whitespace-pre-wrap">{{ item.text }}</p>
          <p v-else-if="!item.media_url" class="text-xs italic theme-text-muted">(No text content)</p>
        </div>

        <!-- AI DRAFTING LOGIC -->
        <div v-if="item.auto_reply_eligible" class="p-4 rounded-xl theme-bg-sec border theme-border">
          <div class="flex justify-between items-center mb-2">
            <span class="text-[10px] font-bold uppercase theme-text-sec">Draft Reply</span>
            <!-- Tombol AI Dimatiin kalau gak ada teks -->
            <button @click="generateAIDraft(item)" :disabled="generatingId === item.id || !item.text" class="btn btn-secondary btn-sm" :class="{'opacity-50 cursor-not-allowed': !item.text}">
              <span v-if="generatingId === item.id" class="w-3 h-3 border-2 border-current border-t-transparent rounded-full animate-spin"></span>
              <span>{{ generatingId === item.id ? 'Generating...' : (item.draftText ? 'Regenerate' : 'Generate AI Draft') }}</span>
            </button>
          </div>
          <textarea v-model="item.draftText" rows="3" placeholder="Type a manual reply or click Generate AI Draft above..." class="textarea"></textarea>
        </div>

        <div v-else class="p-3 rounded-xl theme-bg-sec border theme-border">
          <p class="text-[11px] theme-text-muted">
            <span v-if="item.classification === 'spam'">Comment marked as spam. No draft generated.</span>
            <span v-else-if="item.classification === 'toxic'">Comment marked as toxic. No draft generated.</span>
            <span v-else>This comment is not in the auto-reply queue.</span>
          </p>
        </div>

        <div class="flex justify-end items-center gap-3">
          <button @click="skipReply(item)" class="btn btn-ghost btn-sm">Ignore</button>
          <button @click="approveAndPublish(item)" :disabled="approvingId === item.id || !item.draftText" class="btn btn-primary btn-sm">
            <span v-if="approvingId === item.id" class="w-3 h-3 border-2 border-current border-t-transparent rounded-full animate-spin"></span>
            <span>{{ approvingId === item.id ? 'Publishing...' : 'Send to Threads' }}</span>
          </button>
        </div>
      </div>
    </div>

    <div v-else class="card overflow-hidden">
      <div v-if="historyReplies.length === 0" class="p-12 text-center text-xs theme-text-muted">No reply history yet.</div>
      <div v-else class="list-divided">
        <div v-for="item in historyReplies" :key="item.id" class="p-5 space-y-2">
          <div class="flex justify-between items-center gap-3">
            <div class="flex items-center gap-2 flex-wrap">
              <span class="text-[10px] font-bold uppercase tracking-wide theme-text">@{{ item.author_username }}</span>
              <Badge :variant="historyBadgeVariant(item)">{{ historyBadgeLabel(item) }}</Badge>
            </div>
            <span class="text-xs theme-text-muted shrink-0">{{ formatDate(item.replied_at) }}</span>
          </div>
          <p class="text-xs theme-text-muted italic whitespace-pre-wrap">{{ item.text }}</p>
          <p v-if="item.draftText" class="text-xs font-medium p-3 rounded-lg theme-bg-sec border theme-border mt-2 whitespace-pre-wrap">{{ item.draftText }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { supabase } from '../lib/supabase'
import { useNotify } from '../composables/useNotify'
import { Badge, Select } from '../components/ui'

const { showToast, askConfirm } = useNotify()
const loading = ref(true)
const isSyncing = ref(false)
const isSkippingAll = ref(false)
const approvingId = ref<string | null>(null)
const generatingId = ref<string | null>(null)
const activeTab = ref<'review' | 'priority' | 'conversation' | 'history'>('review')
const repliesData = ref<any[]>([])

const aiProvider = ref('groq')
const aiModel = ref('')
const availableModels = ref<{id: string, name: string}[]>([])
const isLoadingModels = ref(false)
const aiCredits = ref(20)
const customGeminiKey = ref('')
const customGroqKey = ref('')
const currentAccountId = ref<string | null>(null)

const isUsingOwnKey = computed(() => {
  if (aiProvider.value === 'groq') return !!customGroqKey.value
  return !!customGeminiKey.value
})

const AUTO_REPLY_CATEGORIES = ['praise', 'neutral', 'question']

function isProcessed(r: any) { return r.log_status === 'sent' || r.log_status === 'skipped' }

// REVIEW: Yang bener-bener butuh di-approve
const reviewReplies = computed(() => repliesData.value.filter(r => !r.is_own && (r.log_status === 'pending_review' || r.log_status === 'approved')))

// PRIORITY: Leads + Question yang belum diproses (Bukan cuma leads sempit)
const priorityReplies = computed(() => repliesData.value.filter(r => !r.is_own && (r.is_lead || r.classification === 'question') && !isProcessed(r)).sort((a, b) => new Date(b.replied_at).getTime() - new Date(a.replied_at).getTime()))

// CONVERSATION: Semua reply (kecuali history)
const conversationReplies = computed(() => repliesData.value.filter(r => !r.is_own && !isProcessed(r)))

const historyReplies = computed(() => repliesData.value.filter(r => r.is_own || r.log_status === 'sent' || r.log_status === 'skipped'))

const reviewCount = computed(() => reviewReplies.value.length)
const priorityCount = computed(() => priorityReplies.value.length)
const conversationCount = computed(() => conversationReplies.value.length)
const historyCount = computed(() => historyReplies.value.length)

const currentReplies = computed(() => {
  if (activeTab.value === 'review') return reviewReplies.value
  if (activeTab.value === 'priority') return priorityReplies.value
  if (activeTab.value === 'conversation') return conversationReplies.value
  return []
})

const emptyMessage = computed(() => {
  if (activeTab.value === 'review') return 'No drafts waiting for review.'
  if (activeTab.value === 'priority') return 'No priority comments right now.'
  if (activeTab.value === 'conversation') return 'All conversations are clear.'
  return 'No data.'
})

function tabClass(tab: string) {
  return activeTab.value === tab ? 'border-current theme-text' : 'border-transparent theme-text-muted hover:theme-text'
}

function formatDate(isoString: string) {
  if (!isoString) return ''
  return new Date(isoString).toLocaleString('en-US', { dateStyle: 'medium', timeStyle: 'short' })
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

async function fetchModels() {
  if (!currentAccountId.value) return
  isLoadingModels.value = true
  try {
    const res = await fetch(`https://threads-automation-production-53ad.up.railway.app/api/v1/rag/models/${aiProvider.value}?account_id=${currentAccountId.value}`)
    const data = await res.json()
    if (data.models && data.models.length > 0) {
      availableModels.value = data.models.map((m: any) => ({ label: m.name, value: m.id }))
      aiModel.value = data.models[0].id
    } else {
      availableModels.value = []
      aiModel.value = ''
    }
  } catch (err) {
    console.error('Failed to load models', err)
  } finally {
    isLoadingModels.value = false
  }
}

async function safeSaveLog(payload: any) {
  const { id, ...dataToSave } = payload
  const { data: existing } = await supabase.schema('threads').from('auto_reply_logs').select('id').eq('reply_id', dataToSave.reply_id).maybeSingle()
  
  if (existing && existing.id) {
    const { data, error } = await supabase.schema('threads').from('auto_reply_logs').update(dataToSave).eq('id', existing.id).select().single()
    if (error) throw error
    return data
  } else {
    const { data, error } = await supabase.schema('threads').from('auto_reply_logs').insert(dataToSave).select().single()
    if (error) throw error
    return data
  }
}

async function fetchReplies() {
  loading.value = true
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) return

  const { data: account } = await supabase.schema('threads').from('threads_accounts').select('id, ai_credits, custom_gemini_key, custom_groq_key, ai_provider').eq('user_id', user.id).maybeSingle()
  if (!account) return

  currentAccountId.value = account.id
  aiCredits.value = account.ai_credits ?? 20
  customGeminiKey.value = account.custom_gemini_key || ''
  customGroqKey.value = account.custom_groq_key || ''
  if (account.ai_provider) aiProvider.value = account.ai_provider
  await fetchModels()

  // NOTE: Pastikan tabel 'replies' lu punya kolom 'media_url'
  const { data: repliesRaw } = await supabase.schema('threads').from('replies').select('*').eq('account_id', account.id).order('replied_at', { ascending: false }).limit(100)

  if (repliesRaw && repliesRaw.length > 0) {
    const replyIds = repliesRaw.map(r => r.id)
    const { data: logsRaw } = await supabase.schema('threads').from('auto_reply_logs').select('*').in('reply_id', replyIds)
    const logsArray = logsRaw || []

    repliesData.value = repliesRaw.map(r => {
      const log = logsArray.find(l => l.reply_id === r.id)
      const eligible = AUTO_REPLY_CATEGORIES.includes(r.classification)
      return { ...r, log_id: log ? log.id : null, draftText: log ? log.final_text : '', log_status: log ? log.status : 'unprocessed', auto_reply_eligible: eligible }
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
    if (!res.ok) throw new Error('Failed to sync with backend.')
    showToast('Sync complete. Loading new data...', 'success')
    await fetchReplies()
  } catch (err: any) {
    showToast('Sync failed: ' + err.message, 'error')
  } finally { isSyncing.value = false }
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
        author_username: item.author_username,
        provider: aiProvider.value,
        model_name: aiModel.value
      })
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.detail || 'Failed to generate AI reply')

    item.draftText = data.reply
    if (!isUsingOwnKey.value) aiCredits.value = Math.max(0, aiCredits.value - 1)

    const savedData = await safeSaveLog({
      account_id: item.account_id, reply_id: item.id, status: 'pending_review',
      final_text: data.reply, llm_meta: { incoming_comment: item.text, username: item.author_username, model: aiModel.value }
    })
    
    if (savedData) { item.log_id = savedData.id; item.log_status = savedData.status }
    showToast('AI Draft generated and saved!', 'success')
  } catch (err: any) {
    showToast('AI Failed: ' + err.message, 'error')
  } finally { generatingId.value = null }
}

async function skipReply(item: any) {
  item.log_status = 'skipped'
  try {
    const savedData = await safeSaveLog({ account_id: item.account_id, reply_id: item.id, status: 'skipped', final_text: item.draftText || 'Ignored manually' })
    if (savedData) item.log_id = savedData.id
    showToast('Comment moved to History.', 'info')
  } catch (err: any) {
    showToast('Failed to ignore: ' + err.message, 'error')
    await fetchReplies()
  }
}

async function skipAllPending() {
  if (reviewReplies.value.length === 0) return
  askConfirm({
    title: 'Ignore All Comments',
    message: `Are you sure you want to move ${reviewReplies.value.length} comments to history?`,
    confirmText: 'Yes, Ignore All',
    onConfirm: async () => {
      isSkippingAll.value = true
      try {
        const itemsToProcess = [...reviewReplies.value]
        itemsToProcess.forEach(i => i.log_status = 'skipped')
        for (const item of itemsToProcess) {
          await safeSaveLog({ account_id: item.account_id, reply_id: item.id, status: 'skipped', final_text: item.draftText || 'Ignored (bulk)' })
        }
        showToast('All comments moved to History.', 'success')
      } catch (err: any) {
        showToast('Bulk action failed: ' + err.message, 'error')
        await fetchReplies()
      } finally { isSkippingAll.value = false }
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
    if (!res.ok) throw new Error(data.detail || 'Failed to publish to Threads')

    const savedData = await safeSaveLog({ account_id: item.account_id, reply_id: item.id, status: 'sent', final_text: item.draftText })
    if (savedData) item.log_id = savedData.id
    item.log_status = 'sent'
    showToast('Successfully published to Threads!', 'success')
  } catch (err: any) {
    showToast('Publish failed: ' + err.message, 'error')
  } finally { approvingId.value = null }
}

onMounted(() => fetchReplies())
</script>
