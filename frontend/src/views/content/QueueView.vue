<template>
  <div class="space-y-4 relative pb-24 w-full">
    <Card padding="false">
      <div class="p-5 divider flex justify-between items-center theme-bg-sec">
        <div class="flex items-center gap-2">
          <span class="text-xs font-bold uppercase tracking-wide">{{ $t('content.queue.title') }}</span>
          <Badge>{{ groupedPosts.length }} groups</Badge>
        </div>
        <button @click="refreshAll" class="text-xs font-bold hover:underline">{{ $t('common.refresh') }}</button>
      </div>

      <div class="flex gap-2 px-5 pt-4 pb-3 overflow-x-auto hide-scrollbar w-full">
        <button
          v-for="tab in tabs"
          :key="tab.value"
          @click="switchTab(tab.value)"
          class="px-3 py-1.5 text-xs font-bold rounded-lg transition whitespace-nowrap flex-shrink-0"
          :class="activeFilter === tab.value ? 'theme-accent' : 'theme-bg-sec theme-text-muted hover:theme-text'"
        >
          {{ $t(tab.labelKey) }} ({{ counts[tab.value] }})
        </button>
      </div>

      <div v-if="loading" class="p-8 text-center text-xs theme-text-muted font-medium animate-pulse">
        {{ $t('common.loading') }}
      </div>

      <div v-else-if="groupedPosts.length === 0" class="p-12 text-center text-xs theme-text-muted">
        {{ emptyMessage }}
      </div>

      <div v-else class="list-divided">
        <div v-for="dateGroup in groupedByDate" :key="dateGroup.key" class="border-b theme-border last:border-0">
          <div class="px-5 py-3 theme-bg-sec text-xs font-bold uppercase tracking-wide theme-text-muted sticky top-0 z-10">
            {{ $t('content.queue.' + dateGroup.key) }}
          </div>

          <div class="divide-y theme-border">
            <div v-for="group in dateGroup.items" :key="group.id" class="p-5 space-y-3">
              <div v-if="group.isThread" class="flex items-center justify-between pb-2 border-b theme-border">
                <div class="flex items-center gap-3">
                  <input
                    type="checkbox"
                    :checked="isGroupSelected(group)"
                    @change="toggleGroupSelection(group)"
                    class="w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500 flex-shrink-0"
                  />
                  <Badge variant="accent">Thread</Badge>
                  <span class="text-xs font-bold theme-text-muted">{{ $t('content.queue.thread_parts', { n: group.parts.length }) }}</span>
                </div>
                <button @click="toggleExpand(group.id)" class="text-xs font-bold hover:underline flex-shrink-0">
                  {{ expandedThreads.has(group.id) ? $t('content.queue.hide_parts') : $t('content.queue.show_parts') }}
                </button>
              </div>

              <div v-for="post in (group.isThread && !expandedThreads.has(group.id) ? [group.parts[0]] : group.parts)"
                   :key="post.id"
                   class="space-y-3 pt-2 w-full"
                   :class="{ 'opacity-50 pointer-events-none': group.isThread && !expandedThreads.has(group.id) && post.sequence_number > 1 }">

                <div class="flex items-start gap-3 w-full">
                  <input
                    v-if="!group.isThread"
                    type="checkbox"
                    :checked="selectedPosts.has(post.id)"
                    @change="togglePostSelection(post.id)"
                    class="w-4 h-4 mt-1 rounded border-gray-300 text-blue-600 focus:ring-blue-500 flex-shrink-0"
                  />
                  <div class="flex-1 space-y-1 min-w-0">
                    <div class="flex items-center gap-2 flex-wrap">
                      <Badge :variant="statusVariant(post.status)">{{ post.status }}</Badge>
                      <span v-if="post.sequence_number > 1" class="text-[10px] font-bold theme-text-muted">Part {{ post.sequence_number }}</span>
                    </div>
                    <p class="text-sm font-medium whitespace-pre-wrap break-words">{{ post.text }}</p>
                    <p v-if="post.last_error && post.status !== 'published' && post.status !== 'scheduled'" class="text-xs text-red-400 bg-red-950/30 border border-red-900/50 rounded-md px-2.5 py-1.5 mt-1 break-words">{{ post.last_error }}</p>
                    <img
                      v-if="post.media && post.media.url"
                      :src="post.media.url"
                      class="w-full max-w-[200px] rounded-lg border theme-border object-cover mt-2"
                      alt="Post media"
                    />
                  </div>
                </div>

                <div class="flex items-center justify-between pt-1 text-xs gap-3 flex-wrap w-full">
                  <span class="theme-text-muted font-medium">{{ formatTime(post.scheduled_for) }}</span>

                  <div v-if="post.status === 'scheduled'" class="flex items-center gap-2 flex-wrap">
                    <Button variant="secondary" size="sm" @click="openEditModal(post)">{{ $t('content.queue.edit') }}</Button>
                    <Button variant="danger" size="sm" @click="confirmDeletePost(post.id)">{{ $t('content.queue.delete') }}</Button>
                  </div>
                  <div v-else-if="post.status !== 'published'" class="flex items-center gap-2 flex-wrap">
                    <Button size="sm" @click="handleRetryPost(post.id)" :loading="retryingId === post.id">{{ $t('content.queue.retry') }}</Button>
                    <Button variant="danger" size="sm" @click="confirmDeletePost(post.id)">{{ $t('content.queue.delete') }}</Button>
                  </div>
                  <div v-else-if="post.published_media_id" class="flex items-center gap-3 flex-wrap">
                    <a :href="post.permalink && post.permalink.includes('/@') ? post.permalink.replace('threads.net', 'threads.com') : (currentAccount?.username ? 'https://www.threads.com/@' + currentAccount.username : 'https://www.threads.com')" target="_blank" class="text-xs font-bold hover:underline">
                      {{ $t('content.queue.view_threads') }}
                    </a>
                    <Button variant="danger" size="sm" @click="confirmDeleteFromThreads(post.id)" :loading="deletingThreadsId === post.id">
                      {{ $t('content.queue.delete_threads') }}
                    </Button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="hasMore" class="p-4 text-center border-t theme-border">
          <Button variant="secondary" size="sm" @click="loadMore" :loading="loadingMore">
            Load More
          </Button>
        </div>
      </div>
    </Card>

    <!-- FLOATING BULK ACTION BAR -->
    <Transition name="fade">
      <div v-if="totalSelected > 0" class="fixed bottom-6 left-1/2 -translate-x-1/2 z-50 flex items-center gap-4 px-6 py-3 rounded-full shadow-2xl border theme-border theme-bg-sec">
        <span class="text-sm font-bold theme-text">{{ $t('content.queue.bulk_selected', { n: totalSelected }) }}</span>
        <div class="w-px h-4 theme-border bg-current opacity-20"></div>
        <button @click="handleBulkDelete" :disabled="isBulkDeleting" class="text-sm font-bold text-red-500 hover:text-red-600 transition flex items-center gap-2">
          <span v-if="isBulkDeleting" class="w-3 h-3 border-2 border-current border-t-transparent rounded-full animate-spin"></span>
          {{ $t('content.queue.bulk_delete') }}
        </button>
      </div>
    </Transition>

    <!-- EDIT MODAL -->
    <Teleport to="body">
      <div v-if="editingPost" class="fixed inset-0 backdrop-blur-sm z-[100] flex items-center justify-center p-4" style="background: rgba(0,0,0,0.6);">
        <div class="card max-w-lg w-full p-6 space-y-4 shadow-2xl flex flex-col max-h-[90vh]" style="background: var(--bg);">
          <div class="flex justify-between items-center pb-2 border-b theme-border shrink-0">
            <div class="flex gap-4">
              <button @click="modalTab = 'edit'" class="text-base font-bold transition" :class="modalTab === 'edit' ? 'theme-text border-b-2 border-current' : 'theme-text-muted hover:theme-text'">{{ $t('content.queue.edit_tab_edit') }}</button>
              <button @click="modalTab = 'preview'" class="text-base font-bold transition" :class="modalTab === 'preview' ? 'theme-text border-b-2 border-current' : 'theme-text-muted hover:theme-text'">{{ $t('content.queue.edit_tab_preview') }}</button>
            </div>
            <button @click="magicRewrite" :disabled="isRewriting || !editForm.text" class="text-xs font-bold flex items-center gap-1.5 px-3 py-1.5 rounded-lg border theme-border hover:theme-bg-sec transition-colors">
              <span v-if="isRewriting" class="w-3 h-3 border-2 border-current border-t-transparent rounded-full animate-spin"></span>
              <span v-else>✨</span>
              <span>{{ isRewriting ? $t('content.queue.magic_rewriting') : $t('content.queue.magic_rewrite') }}</span>
            </button>
          </div>

          <div class="overflow-y-auto pr-2 flex-1">
            <div v-if="modalTab === 'edit'" class="space-y-4">
              <Textarea v-model="editForm.text" :rows="6" :max-length="500" />
              <div class="space-y-1">
                <label class="label theme-text">{{ $t('content.queue.new_time') }}</label>
                <input v-model="editForm.scheduled_for" type="datetime-local" class="input" />
              </div>
            </div>

            <div v-else class="py-4">
              <div class="flex gap-3">
                <div class="w-10 h-10 rounded-full theme-bg-sec border theme-border shrink-0 flex items-center justify-center font-bold text-xs">IX</div>
                <div class="flex-1 min-w-0">
                  <div class="flex items-center gap-1">
                    <span class="font-bold text-sm theme-text">ixiera.online</span>
                    <span class="text-xs theme-text-muted">· now</span>
                  </div>
                  <p class="text-sm whitespace-pre-wrap break-words mt-1 leading-relaxed theme-text">{{ editForm.text }}</p>
                </div>
              </div>
            </div>
          </div>

          <div class="flex justify-end gap-3 pt-4 border-t theme-border shrink-0">
            <Button variant="secondary" @click="editingPost = null">{{ $t('content.queue.cancel') }}</Button>
            <Button @click="saveEdit" :disabled="isUpdating || modalTab === 'preview'" :loading="isUpdating">
              {{ isUpdating ? $t('common.processing') : $t('content.queue.save_changes') }}
            </Button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { supabase } from '../../lib/supabase'
import { useNotify } from '../../composables/useNotify'
import { useI18n } from 'vue-i18n'
import { Card, Button, Textarea, Badge } from '../../components/ui'
import { useAccountStore } from '../../stores/accounts'

const accountStore = useAccountStore()

const { showToast, askConfirm } = useNotify()
const { t } = useI18n()

const PAGE_SIZE = 30
const FAILED_STATUSES = ['error', 'failed', 'quota_exceeded']

const loading = ref(true)
const loadingMore = ref(false)
const hasMore = ref(false)
const isUpdating = ref(false)
const isRewriting = ref(false)
const isBulkDeleting = ref(false)

const posts = ref<any[]>([])
const counts = ref({ scheduled: 0, published: 0, failed: 0, all: 0 })
const retryingId = ref<string | null>(null)
const deletingThreadsId = ref<string | null>(null)
const activeFilter = ref<'all' | 'scheduled' | 'published' | 'failed'>('scheduled')
const editingPost = ref<any>(null)
const editForm = ref({ text: '', scheduled_for: '' })
const modalTab = ref<'edit' | 'preview'>('edit')
const expandedThreads = ref<Set<string>>(new Set())

const currentAccountId = ref<string | null>(null)
const aiProvider = ref('groq')

const selectedPosts = ref<Set<string>>(new Set())
const selectedThreads = ref<Set<string>>(new Set())

const tabs = [
  { labelKey: 'content.queue.tab_scheduled', value: 'scheduled' as const },
  { labelKey: 'content.queue.tab_published', value: 'published' as const },
  { labelKey: 'content.queue.tab_failed', value: 'failed' as const },
  { labelKey: 'content.queue.tab_all', value: 'all' as const },
]

const groupedPosts = computed(() => {
  const groups = new Map()
  posts.value.forEach(post => {
    const groupId = post.parent_id || post.id
    if (!groups.has(groupId)) {
      groups.set(groupId, { id: groupId, parts: [], isThread: false })
    }
    groups.get(groupId).parts.push(post)
  })

  return Array.from(groups.values()).map(g => {
    g.parts.sort((a: any, b: any) => (a.sequence_number || 0) - (b.sequence_number || 0))
    g.isThread = g.parts.length > 1
    return g
  })
})

const groupedByDate = computed(() => {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  const tomorrow = new Date(today)
  tomorrow.setDate(tomorrow.getDate() + 1)

  const groups: Record<string, any[]> = {
    today: [], tomorrow: [], upcoming: [], past: []
  }

  const sorted = [...groupedPosts.value].sort((a, b) => {
    const tA = new Date(a.parts[0].scheduled_for).getTime()
    const tB = new Date(b.parts[0].scheduled_for).getTime()
    return activeFilter.value === 'scheduled' ? tA - tB : tB - tA
  })

  sorted.forEach(group => {
    const postDate = new Date(group.parts[0].scheduled_for)
    postDate.setHours(0, 0, 0, 0)

    if (postDate.getTime() === today.getTime()) groups.today.push(group)
    else if (postDate.getTime() === tomorrow.getTime()) groups.tomorrow.push(group)
    else if (postDate > tomorrow) groups.upcoming.push(group)
    else groups.past.push(group)
  })

  return Object.entries(groups)
    .filter(([_, items]) => items.length > 0)
    .map(([key, items]) => ({ key, items }))
})

const totalSelected = computed(() => selectedPosts.value.size + selectedThreads.value.size)

function togglePostSelection(id: string) {
  if (selectedPosts.value.has(id)) selectedPosts.value.delete(id)
  else selectedPosts.value.add(id)
}

function toggleGroupSelection(group: any) {
  if (selectedThreads.value.has(group.id)) selectedThreads.value.delete(group.id)
  else selectedThreads.value.add(group.id)
}

function isGroupSelected(group: any) {
  return selectedThreads.value.has(group.id)
}

const emptyMessage = computed(() => {
  if (activeFilter.value === 'scheduled') return t('content.queue.empty_scheduled')
  if (activeFilter.value === 'published') return t('content.queue.empty_published')
  if (activeFilter.value === 'failed') return t('content.queue.empty_failed')
  return t('content.queue.empty_all')
})

function toggleExpand(groupId: string) {
  if (expandedThreads.value.has(groupId)) expandedThreads.value.delete(groupId)
  else expandedThreads.value.add(groupId)
}

function formatTime(isoString: string) {
  if (!isoString) return ''
  return new Date(isoString).toLocaleString(undefined, { dateStyle: 'short', timeStyle: 'short' })
}

function statusVariant(status: string) {
  if (status === 'published') return 'accent'
  if (status !== 'scheduled' && status !== 'published') return 'danger'
  return 'default'
}

async function ensureAccount() {
  if (currentAccountId.value) return currentAccountId.value
  const account = await accountStore.ensureActiveAccount()
  if (!account) return null
  currentAccountId.value = account.id
  if (account.ai_provider) aiProvider.value = account.ai_provider
  return account.id
}

async function loadCounts(accountId: string) {
  const base = () => supabase.schema('threads').from('scheduled_posts').select('*', { count: 'exact', head: true }).eq('account_id', accountId)
  const [schedRes, pubRes, failRes, allRes] = await Promise.all([
    base().eq('status', 'scheduled'),
    base().eq('status', 'published'),
    base().not('status', 'in', '("scheduled","published")'),
    base()
  ])
  counts.value = {
    scheduled: schedRes.count || 0,
    published: pubRes.count || 0,
    failed: failRes.count || 0,
    all: allRes.count || 0
  }
}

function buildFilteredQuery(accountId: string, offset: number) {
  const isAscending = activeFilter.value === 'scheduled'
  let q = supabase
    .schema('threads')
    .from('scheduled_posts')
    .select('*')
    .eq('account_id', accountId)
    .order('scheduled_for', { ascending: isAscending })
    .range(offset, offset + PAGE_SIZE - 1)

  if (activeFilter.value === 'scheduled') q = q.eq('status', 'scheduled')
  else if (activeFilter.value === 'published') q = q.eq('status', 'published')
  else if (activeFilter.value === 'failed') q = q.not('status', 'in', '("scheduled","published")')

  return q
}

async function loadPosts(reset = true) {
  if (reset) {
    loading.value = true
    posts.value = []
    selectedPosts.value.clear()
    selectedThreads.value.clear()
  } else {
    loadingMore.value = true
  }

  const accountId = await ensureAccount()
  if (!accountId) {
    loading.value = false
    loadingMore.value = false
    return
  }

  const offset = reset ? 0 : posts.value.length
  const { data } = await buildFilteredQuery(accountId, offset)
  const rows = data || []

  if (reset) posts.value = rows
  else posts.value = [...posts.value, ...rows]

  hasMore.value = rows.length === PAGE_SIZE
  loading.value = false
  loadingMore.value = false
}

async function switchTab(tab: 'all' | 'scheduled' | 'published' | 'failed') {
  if (activeFilter.value === tab) return
  activeFilter.value = tab
  await loadPosts(true)
}

async function loadMore() {
  if (loadingMore.value || !hasMore.value) return
  await loadPosts(false)
}

async function refreshAll() {
  const accountId = await ensureAccount()
  if (!accountId) return
  await Promise.all([loadCounts(accountId), loadPosts(true)])
}

async function handleBulkDelete() {
  const allIds: string[] = []
  groupedPosts.value.forEach(group => {
    if (selectedThreads.value.has(group.id)) {
      group.parts.forEach((p: any) => allIds.push(p.id))
    } else {
      group.parts.forEach((p: any) => {
        if (selectedPosts.value.has(p.id)) allIds.push(p.id)
      })
    }
  })

  if (allIds.length === 0) return

  askConfirm({
    title: 'Delete Selected Posts',
    message: `Are you sure you want to delete ${allIds.length} post(s)?`,
    confirmText: 'Delete',
    onConfirm: async () => {
      isBulkDeleting.value = true
      try {
        const res = await fetch('https://api.ixiera.online/api/v1/queue/bulk-delete', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ post_ids: allIds })
        })
        if (!res.ok) throw new Error('Bulk delete failed')
        showToast(`${allIds.length} posts deleted.`, 'info')
        selectedPosts.value.clear()
        selectedThreads.value.clear()
        await refreshAll()
      } catch (err: any) {
        showToast('Error: ' + err.message, 'error')
      } finally {
        isBulkDeleting.value = false
      }
    }
  })
}

function openEditModal(post: any) {
  editingPost.value = post
  modalTab.value = 'edit'
  editForm.value.text = post.text
  const d = new Date(post.scheduled_for)
  d.setMinutes(d.getMinutes() - d.getTimezoneOffset())
  editForm.value.scheduled_for = d.toISOString().slice(0, 16)
}

async function saveEdit() {
  if (!editingPost.value) return
  isUpdating.value = true
  try {
    const localDate = new Date(editForm.value.scheduled_for)
    const res = await fetch('https://api.ixiera.online/api/v1/queue/edit', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        post_id: editingPost.value.id,
        text: editForm.value.text,
        scheduled_for: localDate.toISOString()
      })
    })
    if (!res.ok) throw new Error('Update failed')
    editingPost.value = null
    showToast('Post updated successfully.', 'success')
    await refreshAll()
  } catch (err: any) {
    showToast('Update failed: ' + err.message, 'error')
  } finally {
    isUpdating.value = false
  }
}

async function magicRewrite() {
  if (!editForm.value.text.trim()) return
  isRewriting.value = true
  try {
    const res = await fetch('https://api.ixiera.online/api/v1/rag/improve', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        account_id: currentAccountId.value,
        text: editForm.value.text,
        provider: aiProvider.value,
        model_name: null
      })
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.detail)
    editForm.value.text = data.improved_text
    showToast('Text magically improved!', 'success')
  } catch (err: any) {
    showToast('Magic Rewrite failed: ' + err.message, 'error')
  } finally {
    isRewriting.value = false
  }
}

function confirmDeletePost(id: string) {
  askConfirm({
    title: 'Delete Scheduled Post',
    message: 'Are you sure you want to delete this post?',
    confirmText: 'Delete Post',
    onConfirm: () => deletePost(id)
  })
}

async function deletePost(id: string) {
  try {
    const res = await fetch(`https://api.ixiera.online/api/v1/queue/${id}`, { method: 'DELETE' })
    if (!res.ok) throw new Error('Failed to delete')
    showToast('Post deleted.', 'info')
    await refreshAll()
  } catch (err: any) {
    showToast('Delete failed: ' + err.message, 'error')
  }
}

async function handleRetryPost(id: string) {
  retryingId.value = id
  try {
    const res = await fetch('https://api.ixiera.online/api/v1/queue/retry', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ post_id: id })
    })
    if (!res.ok) throw new Error('Failed to retry')
    showToast('Post re-queued for publishing.', 'success')
    await refreshAll()
  } catch (err: any) {
    showToast('Retry failed: ' + err.message, 'error')
  } finally {
    retryingId.value = null
  }
}


function confirmDeleteFromThreads(id: string) {
  askConfirm({
    title: 'Delete Post from Threads',
    message: 'This will permanently delete the post from your Threads profile and database. Continue?',
    confirmText: 'Delete on Threads',
    onConfirm: () => deleteFromThreads(id)
  })
}

async function deleteFromThreads(id: string) {
  deletingThreadsId.value = id
  try {
    const res = await fetch(`https://api.ixiera.online/api/v1/queue/${id}/threads`, { method: 'DELETE' })
    const data = await res.json().catch(() => ({}))
    if (!res.ok) throw new Error(data.detail || 'Failed to delete from Threads')
    showToast('Post deleted from Threads.', 'success')
    await refreshAll()
  } catch (err: any) {
    showToast('Threads Delete failed: ' + err.message, 'error')
  } finally {
    deletingThreadsId.value = null
  }
}

onMounted(() => refreshAll())
</script>
