<template>
  <div class="space-y-6 relative pb-24 w-full overflow-x-hidden">
    <div class="flex flex-wrap justify-between items-center gap-4">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">{{ $t('comments.title') }}</h1>
        <p class="text-sm theme-text-muted mt-1">{{ $t('comments.subtitle') }}</p>
      </div>
      <div class="flex items-center gap-3">
        <button @click="syncRepliesManual" :disabled="isSyncing || isBulkProcessing" class="btn btn-primary btn-sm whitespace-nowrap">
          <span v-if="isSyncing" class="w-3 h-3 border-2 border-current border-t-transparent rounded-full animate-spin"></span>
          <span>{{ isSyncing ? $t('common.syncing') : $t('comments.sync') }}</span>
        </button>
      </div>
    </div>

    <!-- AI SETTINGS BAR (Dibuat numpuk ke bawah di HP) -->
    <div class="p-4 rounded-xl border theme-border flex flex-col md:flex-row md:items-center justify-between gap-4" style="background: var(--bg-sec);">
      <div class="flex items-center gap-3">
        <div class="flex items-center gap-2 px-3 py-1.5 rounded-lg border text-xs font-bold transition-colors w-full md:w-auto justify-center"
          :style="isUsingOwnKey ? 'border-color: var(--success); color: var(--success);' : (aiCredits > 0 ? 'border-color: var(--accent); color: var(--accent);' : 'border-color: var(--danger); color: var(--danger);')">
          <span class="w-2 h-2 rounded-full shrink-0" :style="isUsingOwnKey ? 'background: var(--success);' : (aiCredits > 0 ? 'background: var(--accent);' : 'background: var(--danger);')"></span>
          <span v-if="isUsingOwnKey">Unlimited (Own Key)</span>
          <span v-else-if="aiCredits > 0">{{ aiCredits }} Credits Left</span>
          <span v-else>Out of Credits</span>
        </div>
      </div>
      <div class="grid grid-cols-2 md:flex items-center gap-2 w-full md:w-auto">
        <Select v-model="aiProvider" :options="[{label: 'Groq', value: 'groq'}, {label: 'Gemini', value: 'gemini'}]" @update:model-value="fetchModels" class="w-full" />
        <Select v-model="aiModel" :options="availableModels" :disabled="isLoadingModels" class="w-full md:min-w-[150px]" />
      </div>
    </div>

    <!-- SEARCH & FILTER -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
      <div class="md:col-span-2">
        <input v-model="searchQuery" type="text" :placeholder="$t('comments.search_ph')" class="input w-full" />
      </div>
      <div class="w-full">
        <Select 
          v-model="filterCategory" 
          :options="[
            { label: $t('comments.filter_all'), value: 'all' },
            { label: $t('comments.filter_priority'), value: 'priority' },
            { label: $t('comments.filter_question'), value: 'question' },
            { label: $t('comments.filter_praise'), value: 'praise' },
            { label: $t('comments.filter_neutral'), value: 'neutral' },
            { label: $t('comments.filter_spam'), value: 'spam' },
            { label: $t('comments.filter_toxic'), value: 'toxic' }
          ]" 
        />
      </div>
    </div>

    <!-- TABS (Dibuat scrollable horizontal biar gak jebol) -->
    <div class="w-full border-b theme-border pb-0 overflow-x-auto">
      <div class="flex items-center gap-5 w-max pb-3">
        <button @click="activeTab = 'review'" class="text-xs font-bold transition whitespace-nowrap pb-1 border-b-2 -mb-[13px]" :class="tabClass('review')">
          {{ $t('comments.tab_review') }} ({{ reviewCount }})
        </button>
        <button @click="activeTab = 'priority'" class="text-xs font-bold transition whitespace-nowrap pb-1 border-b-2 -mb-[13px]" :class="tabClass('priority')">
          {{ $t('comments.tab_priority') }} ({{ priorityCount }})
        </button>
        <button @click="activeTab = 'conversation'" class="text-xs font-bold transition whitespace-nowrap pb-1 border-b-2 -mb-[13px]" :class="tabClass('conversation')">
          {{ $t('comments.tab_conversation') }} ({{ conversationCount }})
        </button>
        <button @click="activeTab = 'history'" class="text-xs font-bold transition whitespace-nowrap pb-1 border-b-2 -mb-[13px]" :class="tabClass('history')">
          {{ $t('comments.tab_history') }} ({{ historyCount }})
        </button>
      </div>
    </div>

    <!-- SELECT ALL (Dipisah biar gak nabrak tab) -->
    <div v-if="activeTab !== 'history' && currentReplies.length > 0" class="flex justify-end pt-2">
      <label class="flex items-center gap-2 cursor-pointer text-xs font-bold theme-text-muted hover:theme-text">
        <input type="checkbox" :checked="isAllSelected" @change="toggleSelectAll" class="w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500" />
        {{ $t('comments.select_all') }}
      </label>
    </div>

    <div v-if="loading" class="p-12 text-center text-xs theme-text-muted animate-pulse">{{ $t('common.loading') }}</div>

    <div v-else-if="activeTab !== 'history'" class="space-y-4">
      <div v-if="currentReplies.length === 0" class="card p-8 text-center text-xs theme-text-muted">
        {{ emptyMessage }}
      </div>

      <div v-for="item in currentReplies" :key="item.id" class="card p-4 md:p-6 space-y-3 md:space-y-4" :class="{'border-current shadow-sm': selectedIds.has(item.id)}">
        <div class="flex items-start gap-3">
          <input type="checkbox" :checked="selectedIds.has(item.id)" @change="toggleSelection(item.id)" class="w-4 h-4 mt-1 rounded border-gray-300 text-blue-600 focus:ring-blue-500 shrink-0" />
          
          <div class="flex-1 space-y-1 min-w-0">
            <div class="flex items-center gap-2 flex-wrap">
              <span class="text-[10px] font-bold uppercase tracking-wide theme-text">@{{ item.author_username }}</span>
              <Badge>{{ item.classification || 'unclassified' }}</Badge>
              <span v-if="item.is_lead" class="badge badge-accent text-[9px]">
                <span class="w-1.5 h-1.5 rounded-full animate-pulse" style="background: currentColor;"></span>
                Lead
              </span>
            </div>
            <p class="text-[10px] md:text-xs theme-text-muted">{{ formatDate(item.replied_at) }}</p>
          </div>
        </div>
        
        <div class="p-3 md:p-3.5 rounded-xl theme-bg-sec border theme-border space-y-3 ml-0 md:ml-7">
          <div v-if="item.media_url" class="rounded-lg overflow-hidden border theme-border max-w-full md:max-w-sm">
            <img :src="item.media_url" alt="Comment media" class="w-full h-auto object-cover" />
          </div>
          <p v-if="item.text" class="text-xs font-semibold whitespace-pre-wrap break-words">{{ item.text }}</p>
          <p v-else-if="!item.media_url" class="text-xs italic theme-text-muted">(No text content)</p>
        </div>

        <div v-if="item.auto_reply_eligible" class="p-3 md:p-4 rounded-xl theme-bg-sec border theme-border ml-0 md:ml-7">
          <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-2 mb-2">
            <div class="flex items-center gap-2">
              <span class="text-[10px] font-bold uppercase theme-text-sec">{{ $t('comments.draft_reply') }}</span>
              <Badge v-if="item.draft_mode === 'template'" variant="default">{{ $t('comments.from_template') }}</Badge>
              <Badge v-else-if="item.draft_mode === 'llm'" variant="accent">{{ $t('comments.ai_generated') }}</Badge>
            </div>
            
            <button @click="generateAIDraft(item)" :disabled="generatingId === item.id || !item.text || isBulkProcessing" class="btn btn-secondary btn-sm w-full sm:w-auto" :class="{'opacity-50 cursor-not-allowed': !item.text || isBulkProcessing}">
              <span v-if="generatingId === item.id" class="w-3 h-3 border-2 border-current border-t-transparent rounded-full animate-spin"></span>
              <span>{{ generatingId === item.id ? $t('comments.generating') : $t('comments.regenerate_ai') }}</span>
            </button>
          </div>
          <textarea v-model="item.draftText" rows="3" :placeholder="$t('comments.draft_ph')" class="textarea w-full text-xs"></textarea>
        </div>

        <div class="flex justify-end items-center gap-2 md:gap-3 ml-0 md:ml-7">
          <button @click="skipReply(item)" :disabled="isBulkProcessing" class="btn btn-ghost btn-sm">{{ $t('comments.ignore') }}</button>
          <button @click="approveAndPublish(item)" :disabled="approvingId === item.id || !item.draftText || isBulkProcessing" class="btn btn-primary btn-sm">
            <span v-if="approvingId === item.id" class="w-3 h-3 border-2 border-current border-t-transparent rounded-full animate-spin"></span>
            <span>{{ approvingId === item.id ? $t('comments.publishing') : $t('comments.publish') }}</span>
          </button>
        </div>
      </div>
    </div>

    <div v-else class="card overflow-hidden">
      <div v-if="historyReplies.length === 0" class="p-12 text-center text-xs theme-text-muted">{{ $t('comments.no_history') }}</div>
      <div v-else class="list-divided">
        <div v-for="item in historyReplies" :key="item.id" class="p-4 md:p-5 space-y-2">
          <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-2">
            <div class="flex items-center gap-2 flex-wrap">
              <span class="text-[10px] font-bold uppercase tracking-wide theme-text">@{{ item.author_username }}</span>
              <Badge :variant="historyBadgeVariant(item)">{{ historyBadgeLabel(item) }}</Badge>
            </div>
            <span class="text-[10px] md:text-xs theme-text-muted shrink-0">{{ formatDate(item.replied_at) }}</span>
          </div>
          <p class="text-xs theme-text-muted italic whitespace-pre-wrap break-words">{{ item.text }}</p>
          <p v-if="item.draftText" class="text-xs font-medium p-3 rounded-lg theme-bg-sec border theme-border mt-2 whitespace-pre-wrap break-words">{{ item.draftText }}</p>
        </div>
      </div>
    </div>

    <Transition name="fade">
      <div v-if="selectedIds.size > 0" class="fixed bottom-6 left-4 right-4 md:left-1/2 md:-translate-x-1/2 md:right-auto z-50 flex flex-col md:flex-row items-center gap-3 md:gap-4 px-4 md:px-6 py-3 rounded-2xl md:rounded-full shadow-2xl border theme-border theme-bg-sec md:min-w-[300px] justify-between">
        <div class="flex items-center justify-between w-full md:w-auto gap-3">
          <span class="text-xs md:text-sm font-bold theme-text whitespace-nowrap">{{ $t('comments.bulk_selected', { n: selectedIds.size }) }}</span>
          <div class="hidden md:block w-px h-4 bg-current opacity-20"></div>
        </div>
        <div class="flex items-center justify-between w-full md:w-auto gap-3">
          <button @click="handleBulkGenerate" :disabled="isBulkProcessing" class="text-[11px] md:text-xs font-bold text-blue-500 hover:text-blue-600 transition flex items-center gap-1.5">
            <span v-if="isBulkProcessing" class="w-3 h-3 border-2 border-current border-t-transparent rounded-full animate-spin"></span>
            {{ $t('comments.bulk_generate') }}
          </button>
          <button @click="handleBulkIgnore" :disabled="isBulkProcessing" class="text-[11px] md:text-xs font-bold text-gray-500 hover:text-gray-700 transition">{{ $t('comments.bulk_ignore') }}</button>
          <button @click="handleBulkPublish" :disabled="isBulkProcessing" class="text-[11px] md:text-xs font-bold text-green-500 hover:text-green-600 transition">{{ $t('comments.bulk_publish') }}</button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { supabase } from '../lib/supabase'
import { useNotify } from '../composables/useNotify'
import { useI18n } from 'vue-i18n'
import { Badge, Select } from '../components/ui'

const { showToast, askConfirm } = useNotify()
const { t } = useI18n()
const loading = ref(true)
const isSyncing = ref(false)
const approvingId = ref<string | null>(null)
const generatingId = ref<string | null>(null)
const activeTab = ref<'review' | 'priority' | 'conversation' | 'history'>('review')
const repliesData = ref<any[]>([])

const searchQuery = ref('')
const filterCategory = ref('all')
const selectedIds = ref<Set<string>>(new Set())
const isBulkProcessing = ref(false)

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

const reviewReplies = computed(() => repliesData.value.filter(r => !r.is_own && (r.log_status === 'pending_review' || r.log_status === 'approved')))
const priorityReplies = computed(() => repliesData.value.filter(r => !r.is_own && (r.is_lead || r.classification === 'question') && !isProcessed(r)).sort((a, b) => new Date(b.replied_at).getTime() - new Date(a.replied_at).getTime()))
const conversationReplies = computed(() => repliesData.value.filter(r => !r.is_own && !isProcessed(r)))
const historyReplies = computed(() => repliesData.value.filter(r => r.is_own || r.log_status === 'sent' || r.log_status === 'skipped'))

const reviewCount = computed(() => reviewReplies.value.length)
const priorityCount = computed(() => priorityReplies.value.length)
const conversationCount = computed(() => conversationReplies.value.length)
const historyCount = computed(() => historyReplies.value.length)

const currentReplies = computed(() => {
  let base = []
  if (activeTab.value === 'review') base = reviewReplies.value
  else if (activeTab.value === 'priority') base = priorityReplies.value
  else if (activeTab.value === 'conversation') base = conversationReplies.value

  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase()
    base = base.filter(r => (r.text && r.text.toLowerCase().includes(q)) || (r.author_username && r.author_username.toLowerCase().includes(q)))
  }

  if (filterCategory.value !== 'all') {
    if (filterCategory.value === 'priority') base = base.filter(r => r.is_lead || r.classification === 'question')
    else base = base.filter(r => r.classification === filterCategory.value)
  }

  return base
})

const emptyMessage = computed(() => {
  if (searchQuery.value || filterCategory.value !== 'all') return t('comments.no_data')
  if (activeTab.value === 'review') return t('comments.no_review')
  if (activeTab.value === 'priority') return t('comments.no_priority')
  if (activeTab.value === 'conversation') return t('comments.no_conversation')
  return t('comments.no_history')
})

const isAllSelected = computed(() => currentReplies.value.length > 0 && currentReplies.value.every(r => selectedIds.value.has(r.id)))

function toggleSelectAll() {
  if (isAllSelected.value) currentReplies.value.forEach(r => selectedIds.value.delete(r.id))
  else currentReplies.value.forEach(r => selectedIds.value.add(r.id))
}

function toggleSelection(id: string) {
  if (selectedIds.value.has(id)) selectedIds.value.delete(id)
  else selectedIds.value.add(id)
}

function tabClass(tab: string) {
  return activeTab.value === tab ? 'border-current theme-text' : 'border-transparent theme-text-muted hover:theme-text'
}

function formatDate(isoString: string) {
  if (!isoString) return ''
  return new Date(isoString).toLocaleString(undefined, { dateStyle: 'medium', timeStyle: 'short' })
}

function historyBadgeVariant(item: any) { if (item.is_own) return 'default'; if (item.log_status === 'sent') return 'accent'; return 'default' }
function historyBadgeLabel(item: any) { if (item.is_own) return 'own reply'; if (item.log_status === 'sent') return 'sent'; if (item.log_status === 'skipped') return 'skipped'; return item.log_status || 'unknown' }

async function fetchModels() {
  if (!currentAccountId.value) return
  isLoadingModels.value = true
  try {
    const res = await fetch(`https://threads-automation-production-53ad.up.railway.app/api/v1/rag/models/${aiProvider.value}?account_id=${currentAccountId.value}`)
    const data = await res.json()
    if (data.models && data.models.length > 0) {
      availableModels.value = data.models.map((m: any) => ({ label: m.name, value: m.id }))
      aiModel.value = data.models[0].id
    } else { availableModels.value = []; aiModel.value = '' }
  } catch (err) { console.error(err) } finally { isLoadingModels.value = false }
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
  const { data: account } = await supabase.schema('threads').from('threads_accounts').select('id, credit_balance, custom_gemini_key, custom_groq_key, ai_provider').eq('user_id', user.id).maybeSingle()
  if (!account) return

  currentAccountId.value = account.id
  aiCredits.value = account.credit_balance ?? 20
  customGeminiKey.value = account.custom_gemini_key || ''
  customGroqKey.value = account.custom_groq_key || ''
  if (account.ai_provider) aiProvider.value = account.ai_provider
  await fetchModels()

  const { data: repliesRaw } = await supabase.schema('threads').from('replies').select('*').eq('account_id', account.id).order('replied_at', { ascending: false }).limit(100)

  if (repliesRaw && repliesRaw.length > 0) {
    const replyIds = repliesRaw.map(r => r.id)
    const { data: logsRaw } = await supabase.schema('threads').from('auto_reply_logs').select('*').in('reply_id', replyIds)
    const logsArray = logsRaw || []

    repliesData.value = repliesRaw.map(r => {
      const log = logsArray.find(l => l.reply_id === r.id)
      let draft_mode = null;
      if (log && log.llm_meta) draft_mode = log.llm_meta.mode || (log.llm_meta.category ? 'template' : 'llm');
      return { ...r, log_id: log ? log.id : null, draftText: log ? log.final_text : '', log_status: log ? log.status : 'unprocessed', auto_reply_eligible: AUTO_REPLY_CATEGORIES.includes(r.classification), draft_mode }
    })
  } else { repliesData.value = [] }
  
  selectedIds.value.clear()
  loading.value = false
}

async function syncRepliesManual() {
  isSyncing.value = true
  try {
    const res = await fetch('https://threads-automation-production-53ad.up.railway.app/api/v1/leads/sync-replies', { method: 'GET' })
    if (!res.ok) throw new Error('Sync failed')
    showToast('Sync complete!', 'success')
    await fetchReplies()
  } catch (err: any) { showToast('Sync failed: ' + err.message, 'error') } finally { isSyncing.value = false }
}

async function generateAIDraft(item: any) {
  generatingId.value = item.id
  try {
    const res = await fetch('https://threads-automation-production-53ad.up.railway.app/api/v1/rag/generate-reply', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ account_id: item.account_id, user_comment: item.text, author_username: item.author_username, provider: aiProvider.value, model_name: aiModel.value })
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.detail || 'Failed to generate')

    item.draftText = data.reply
    item.draft_mode = 'llm'
    if (!isUsingOwnKey.value) aiCredits.value = Math.max(0, aiCredits.value - 1)

    const savedData = await safeSaveLog({ account_id: item.account_id, reply_id: item.id, status: 'pending_review', final_text: data.reply, llm_meta: { incoming_comment: item.text, username: item.author_username, model: aiModel.value, mode: 'llm' } })
    if (savedData) { item.log_id = savedData.id; item.log_status = savedData.status }
    return true
  } catch (err: any) { showToast('AI Failed: ' + err.message, 'error'); return false } finally { generatingId.value = null }
}

async function skipReply(item: any) {
  item.log_status = 'skipped'
  try {
    const savedData = await safeSaveLog({ account_id: item.account_id, reply_id: item.id, status: 'skipped', final_text: item.draftText || 'Ignored' })
    if (savedData) item.log_id = savedData.id
    return true
  } catch (err: any) { return false }
}

async function approveAndPublish(item: any) {
  approvingId.value = item.id
  try {
    const res = await fetch('https://threads-automation-production-53ad.up.railway.app/api/v1/leads/publish-reply', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ account_id: item.account_id, threads_reply_id: item.threads_reply_id, text: item.draftText, log_id: item.log_id })
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.detail || 'Failed to publish')

    const savedData = await safeSaveLog({ account_id: item.account_id, reply_id: item.id, status: 'sent', final_text: item.draftText })
    if (savedData) item.log_id = savedData.id
    item.log_status = 'sent'
    return true
  } catch (err: any) { showToast('Publish failed: ' + err.message, 'error'); return false } finally { approvingId.value = null }
}

async function handleBulkGenerate() {
  const items = currentReplies.value.filter(r => selectedIds.value.has(r.id) && r.auto_reply_eligible && r.text)
  if (items.length === 0) { showToast('No valid comments selected.', 'error'); return }
  isBulkProcessing.value = true
  let count = 0
  try {
    for (const item of items) { if (await generateAIDraft(item)) count++; await new Promise(r => setTimeout(r, 1000)) }
    showToast(`Generated drafts for ${count} comments.`, 'success')
    selectedIds.value.clear()
  } finally { isBulkProcessing.value = false }
}

async function handleBulkIgnore() {
  const items = currentReplies.value.filter(r => selectedIds.value.has(r.id))
  if (items.length === 0) return
  askConfirm({
    title: t('comments.confirm_ignore_title'), message: t('comments.confirm_ignore_msg', { n: items.length }), confirmText: t('comments.ignore'),
    onConfirm: async () => {
      isBulkProcessing.value = true
      try {
        for (const item of items) await skipReply(item)
        showToast(`Ignored comments.`, 'info')
        selectedIds.value.clear(); await fetchReplies()
      } finally { isBulkProcessing.value = false }
    }
  })
}

async function handleBulkPublish() {
  const items = currentReplies.value.filter(r => selectedIds.value.has(r.id) && r.draftText)
  if (items.length === 0) { showToast('No comments with draft text selected.', 'error'); return }
  askConfirm({
    title: t('comments.confirm_publish_title'), message: t('comments.confirm_publish_msg', { n: items.length }), confirmText: t('comments.publish'),
    onConfirm: async () => {
      isBulkProcessing.value = true
      try {
        for (const item of items) { await approveAndPublish(item); await new Promise(r => setTimeout(r, 2000)) }
        showToast(`Published replies!`, 'success')
        selectedIds.value.clear(); await fetchReplies()
      } finally { isBulkProcessing.value = false }
    }
  })
}

onMounted(() => fetchReplies())
</script>
