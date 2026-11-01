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

const { showToast, askConfirm } = useNotify()
const loadingRag = ref(true)
const isSavingRag = ref(false)
const accountId = ref<string | null>(null)
const ragItems = ref<any[]>([])
const expanded = ref<Record<string, boolean>>({})
const ragForm = ref({ category: 'portfolio', title: '', content: '' })

async function initAccount() {
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) return
  const { data: account } = await supabase.schema('threads').from('threads_accounts').select('id').eq('user_id', user.id).maybeSingle()
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

onMounted(async () => { await initAccount(); fetchKnowledge() })
</script>

<style scoped>
.line-clamp-3 { display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
</style>
