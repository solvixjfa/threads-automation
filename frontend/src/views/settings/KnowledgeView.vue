<template>
  <div class="space-y-6">
    <Card>
      <template #header>
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-sm font-bold">{{ $t('settings.knowledge.title') }}</h2>
            <p class="text-xs theme-text-muted mt-0.5">{{ $t('settings.knowledge.subtitle') }}</p>
          </div>
          <Badge>pgvector / 768d</Badge>
        </div>
      </template>

      <!-- Upload Section -->
      <div class="space-y-3">
        <div class="flex items-center justify-between">
          <label class="label mb-0">📎 Upload Dokumen (.txt / .md)</label>
          <Badge>PDF/DOCX Coming Soon</Badge>
        </div>
        <div
          @dragover.prevent="dragActive = true"
          @dragleave.prevent="dragActive = false"
          @drop.prevent="handleDrop"
          @click="fileInput?.click()"
          class="border-2 border-dashed rounded-lg p-5 text-center cursor-pointer transition-colors"
          :class="dragActive ? 'border-blue-500 bg-blue-500/10' : 'theme-border hover:theme-bg-sec'"
        >
          <div v-if="!isUploading">
            <p class="text-sm font-medium">Drop file .txt atau .md di sini, atau klik untuk pilih</p>
            <p class="text-xs theme-text-muted mt-1">Max 5MB per file. PDF/DOCX coming soon — convert ke .txt dulu.</p>
          </div>
          <div v-else class="flex items-center justify-center gap-2">
            <div class="animate-spin w-4 h-4 border-2 border-current border-t-transparent rounded-full"></div>
            <span class="text-sm">Mengupload dan embed...</span>
          </div>
          <input ref="fileInput" type="file" accept=".txt,.md" multiple class="hidden" @change="handleFileInput" />
        </div>
        <div v-if="uploadProgress.length > 0" class="space-y-1">
          <div v-for="p in uploadProgress" :key="p.name" class="text-xs flex justify-between">
            <span class="truncate">{{ p.name }}</span>
            <span :class="p.status === 'done' ? 'text-green-500' : p.status === 'error' ? 'text-red-500' : 'theme-text-muted'">
              {{ p.message || p.status }}
            </span>
          </div>
        </div>
      </div>

      <div class="divider my-5"></div>
      <p class="text-xs theme-text-muted mb-2">Atau input manual:</p>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="space-y-1">
          <Select v-model="ragForm.category" :label="$t('settings.knowledge.category')" :options="[
            { label: $t('settings.knowledge.cat_portfolio'), value: 'portfolio' },
            { label: $t('settings.knowledge.cat_persona'), value: 'persona' },
            { label: $t('settings.knowledge.cat_rules'), value: 'rules' },
            { label: $t('settings.knowledge.cat_faq'), value: 'faq' }
          ]" />
        </div>
        <div class="md:col-span-2 space-y-1">
          <label class="label">{{ $t('settings.knowledge.doc_title') }}</label>
          <input v-model="ragForm.title" type="text" :placeholder="$t('settings.knowledge.doc_ph')" class="input" />
        </div>
      </div>

      <div class="space-y-1 mt-4">
        <label class="label">{{ $t('settings.knowledge.doc_content') }}</label>
        <textarea v-model="ragForm.content" rows="5" :placeholder="$t('settings.knowledge.doc_content_ph')" class="textarea"></textarea>
      </div>

      <template #footer>
        <div class="flex justify-end">
          <Button @click="saveKnowledge" :disabled="isSavingRag || !ragForm.title || !ragForm.content" :loading="isSavingRag">
            {{ isSavingRag ? $t('common.processing') : $t('settings.knowledge.add_btn') }}
          </Button>
        </div>
      </template>
    </Card>

    <Card padding="false">
      <div class="p-5 divider flex justify-between items-center theme-bg-sec">
        <div class="flex items-center gap-2">
          <span class="text-xs font-bold uppercase tracking-wide">{{ $t('settings.knowledge.saved_docs') }}</span>
          <Badge>{{ ragItems.length }}</Badge>
        </div>
        <button @click="fetchKnowledge" class="text-xs font-bold hover:underline">{{ $t('settings.knowledge.refresh') }}</button>
      </div>

      <div v-if="loadingRag" class="p-8 text-center text-xs theme-text-muted animate-pulse">{{ $t('common.loading') }}</div>
      <div v-else-if="ragItems.length === 0" class="p-8 text-center text-xs theme-text-muted">{{ $t('settings.knowledge.empty') }}</div>

      <div v-else class="list-divided">
        <div v-for="item in ragItems" :key="item.id" class="p-5 space-y-3">
          <div class="flex items-start justify-between gap-3">
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2 flex-wrap mb-1">
                <Badge>{{ item.category }}</Badge>
                <h3 class="text-sm font-bold truncate">{{ item.title }}</h3>
              </div>
              <p class="text-xs theme-text-sec whitespace-pre-wrap leading-relaxed" :class="{ 'line-clamp-3': !expanded[item.id] }">{{ item.content }}</p>
              <button v-if="item.content && item.content.length > 200" @click="expanded[item.id] = !expanded[item.id]" class="text-xs font-bold mt-2 hover:underline">
                {{ expanded[item.id] ? $t('settings.knowledge.show_less') : $t('settings.knowledge.read_more') }}
              </button>
            </div>
            <button @click="confirmDeleteKnowledge(item.id, item.title)" class="text-xs font-bold theme-text-muted hover:theme-text shrink-0">{{ $t('settings.knowledge.delete_btn') }}</button>
          </div>
        </div>
      </div>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { supabase } from '../../lib/supabase'
import { useNotify } from '../../composables/useNotify'
import { Card, Button, Badge, Select } from '../../components/ui'
import { useAccountStore } from '../../stores/accounts'

const accountStore = useAccountStore()

const { showToast, askConfirm } = useNotify()
const loadingRag = ref(true)
const isSavingRag = ref(false)
const accountId = ref<string | null>(null)
const ragItems = ref<any[]>([])
const expanded = ref<Record<string, boolean>>({})
const ragForm = ref({ category: 'portfolio', title: '', content: '' })

// Upload state
const fileInput = ref<HTMLInputElement | null>(null)
const isUploading = ref(false)
const dragActive = ref(false)
const uploadProgress = ref<Array<{ name: string; status: 'pending' | 'uploading' | 'done' | 'error'; inserted?: number; message?: string }>>([])

async function initAccount() {
  const account = await accountStore.ensureActiveAccount()
  if (account) accountId.value = account.id
}

async function fetchKnowledge() {
  loadingRag.value = true
  if (!accountId.value) await initAccount()
  if (!accountId.value) { loadingRag.value = false; return }
  const { data, error } = await supabase.schema('threads').from('brand_knowledge').select('*').eq('account_id', accountId.value).order('created_at', { ascending: false })
  if (data && !error) ragItems.value = data
  loadingRag.value = false
}

async function saveKnowledge() {
  if (!ragForm.value.title || !ragForm.value.content) return showToast('Fill title and content.', 'error')
  if (!accountId.value) return showToast('Connect a Threads account first.', 'error')

  isSavingRag.value = true
  try {
    const response = await fetch('https://threads-automation-r9so.onrender.com/api/v1/rag/embed', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ account_id: accountId.value, title: ragForm.value.title, content: ragForm.value.content, category: ragForm.value.category })
    })
    if (!response.ok) throw new Error('Failed to process document')
    ragForm.value.title = ''; ragForm.value.content = ''
    showToast('Document added.', 'success')
    await fetchKnowledge()
  } catch (err: any) { showToast('Failed to save: ' + err.message, 'error') } finally { isSavingRag.value = false }
}

function confirmDeleteKnowledge(id: string, title: string) {
  askConfirm({
    title: 'Delete document', message: `Delete "${title}"? This cannot be undone.`, confirmText: 'Delete',
    onConfirm: () => deleteKnowledge(id)
  })
}

async function deleteKnowledge(id: string) {
  try {
    const { error } = await supabase.schema('threads').from('brand_knowledge').delete().eq('id', id)
    if (error) throw error
    showToast('Document deleted.', 'info')
    await fetchKnowledge()
  } catch (err: any) { showToast('Failed to delete: ' + err.message, 'error') }
}

function chunkText(text: string, size = 1000, overlap = 100): string[] {
  const trimmed = (text || '').trim()
  if (!trimmed) return []
  if (trimmed.length <= size) return [trimmed]
  const out: string[] = []
  const step = size - overlap
  for (let i = 0; i < trimmed.length; i += step) out.push(trimmed.slice(i, i + size))
  return out
}

function readFileAsText(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => resolve(String(reader.result || ''))
    reader.onerror = () => reject(new Error('Failed to read file'))
    reader.readAsText(file, 'utf-8')
  })
}

function handleFileInput(e: Event) {
  const input = e.target as HTMLInputElement
  if (input.files) handleFiles(Array.from(input.files))
  input.value = ''
}

function handleDrop(e: DragEvent) {
  dragActive.value = false
  const files = e.dataTransfer?.files
  if (files && files.length > 0) handleFiles(Array.from(files))
}

async function handleFiles(files: File[]) {
  if (!accountId.value) await initAccount()
  if (!accountId.value) return showToast('Connect a Threads account first.', 'error')

  const MAX_SIZE = 5 * 1024 * 1024
  const valid: File[] = []

  for (const f of files) {
    const name = f.name.toLowerCase()
    if (name.endsWith('.pdf') || name.endsWith('.docx') || name.endsWith('.doc')) {
      showToast(`${f.name}: PDF/DOCX coming soon. Convert to .txt first.`, 'error')
      continue
    }
    if (!(name.endsWith('.txt') || name.endsWith('.md'))) {
      showToast(`${f.name}: only .txt and .md supported.`, 'error')
      continue
    }
    if (f.size > MAX_SIZE) {
      showToast(`${f.name}: file too large (max 5MB).`, 'error')
      continue
    }
    valid.push(f)
  }

  if (valid.length === 0) return

  isUploading.value = true
  uploadProgress.value = valid.map(f => ({ name: f.name, status: 'pending' as const }))

  let successCount = 0
  for (const f of valid) {
    const entry = uploadProgress.value.find(x => x.name === f.name)!
    entry.status = 'uploading'
    try {
      const text = await readFileAsText(f)
      const chunks = chunkText(text)
      if (chunks.length === 0) {
        entry.status = 'error'; entry.message = 'Empty file'
        continue
      }
      const res = await fetch('https://threads-automation-r9so.onrender.com/api/v1/rag/embed-batch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          account_id: accountId.value,
          title_prefix: f.name.replace(/\.[^.]+$/, ''),
          category: ragForm.value.category || 'general',
          chunks,
        })
      })
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const data = await res.json()
      const inserted = data?.data?.inserted ?? 0
      const failed = data?.data?.failed ?? 0
      entry.inserted = inserted
      entry.status = failed > 0 ? 'error' : 'done'
      entry.message = failed > 0 ? `${inserted} ok, ${failed} failed` : `${inserted} chunk`
      if (failed === 0) successCount++
    } catch (err: any) {
      entry.status = 'error'
      entry.message = err.message || 'Failed'
    }
  }

  isUploading.value = false
  if (successCount > 0) {
    showToast(`${successCount} file berhasil di-embed.`, 'success')
    await fetchKnowledge()
  }
  setTimeout(() => { uploadProgress.value = [] }, 5000)
}

onMounted(async () => { await initAccount(); fetchKnowledge() })
</script>

<style scoped>
.line-clamp-3 { display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
</style>
