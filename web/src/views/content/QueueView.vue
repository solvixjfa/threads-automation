<template>
  <div class="space-y-4 relative pb-24">                                                                                                        
    <Card padding="false">
      <div class="p-5 divider flex justify-between items-center theme-bg-sec">                                                                
        <div class="flex items-center gap-2">
          <span class="text-xs font-bold uppercase tracking-wide">Scheduled Queue</span>
          <Badge>{{ filteredPosts.length }} groups</Badge>
        </div>
        <button @click="loadPosts" class="text-xs font-bold hover:underline">Refresh</button>
      </div>

      <div class="flex gap-2 px-5 pt-4 pb-3 overflow-x-auto">
        <button
          v-for="tab in tabs"
          :key="tab.value"                                                   
          @click="activeFilter = tab.value"
          class="px-3 py-1.5 text-xs font-bold rounded-lg transition whitespace-nowrap"
          :class="activeFilter === tab.value ? 'theme-accent' : 'theme-bg-sec theme-text-muted hover:theme-text'"
        >
          {{ tab.label }} ({{ countByStatus(tab.value) }})
        </button>
      </div>

      <div v-if="loading" class="p-8 text-center text-xs theme-text-muted font-medium animate-pulse">
        Loading queue...
      </div>

      <div v-else-if="filteredPosts.length === 0" class="p-12 text-center text-xs theme-text-muted">
        {{ emptyMessage }}
      </div>

      <div v-else class="list-divided">
        <!-- LOOPING PER GROUP TANGGAL -->
        <div v-for="dateGroup in groupedByDate" :key="dateGroup.label" class="border-b theme-border last:border-0">
          
          <!-- DATE SEPARATOR (FITUR 3) -->
          <div class="px-5 py-3 theme-bg-sec text-xs font-bold uppercase tracking-wide theme-text-muted sticky top-0 z-10">
            {{ dateGroup.label }}
          </div>

          <div class="divide-y theme-border">
            <!-- LOOPING POSTS DALAM TANGGAL -->
            <div v-for="group in dateGroup.items" :key="group.id" class="p-5 space-y-3">
              
              <div v-if="group.isThread" class="flex items-center justify-between pb-2 border-b theme-border">
                <div class="flex items-center gap-3">
                  <input 
                    type="checkbox" 
                    :checked="isGroupSelected(group)" 
                    @change="toggleGroupSelection(group)"
                    class="w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                  <Badge variant="accent">Thread</Badge>
                  <span class="text-xs font-bold theme-text-muted">{{ group.parts.length }} Parts</span>
                </div>
                <button @click="toggleExpand(group.id)" class="text-xs font-bold hover:underline">
                  {{ expandedThreads.has(group.id) ? 'Hide Parts' : 'Show Parts' }}
                </button>
              </div>

              <div v-for="post in (group.isThread && !expandedThreads.has(group.id) ? [group.parts[0]] : group.parts)" 
                   :key="post.id" 
                   class="space-y-3 pt-2"
                   :class="{ 'opacity-50 pointer-events-none': group.isThread && !expandedThreads.has(group.id) && post.sequence_number > 1 }">
                
                <div class="flex items-start gap-3">                 
                  <input 
                    v-if="!group.isThread"
                    type="checkbox" 
                    :checked="selectedPosts.has(post.id)" 
                    @change="togglePostSelection(post.id)"
                    class="w-4 h-4 mt-1 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                  <div class="flex-1 space-y-1">
                    <div class="flex items-center gap-2 flex-wrap">
                      <Badge :variant="statusVariant(post.status)">{{ post.status }}</Badge>
                      <span v-if="post.sequence_number > 1" class="text-[10px] font-bold theme-text-muted">Part {{ post.sequence_number }}</span>
                    </div>
                    <p class="text-sm font-medium whitespace-pre-wrap">{{ post.text }}</p>
                  </div>
                </div>

                <div class="flex items-center justify-between pt-1 text-xs gap-3 flex-wrap">
                  <span class="theme-text-muted font-medium">{{ formatTime(post.scheduled_for) }}</span>
                  
                  <div v-if="post.status === 'scheduled'" class="flex items-center gap-2">                                                                
                    <Button variant="secondary" size="sm" @click="openEditModal(post)">Edit</Button>                                                      
                    <Button variant="danger" size="sm" @click="confirmDeletePost(post.id)">Delete</Button>                                               
                  </div>                                                             
                  <div v-else-if="['error', 'failed', 'quota_exceeded'].includes(post.status)" class="flex items-center gap-2">
                    <Button size="sm" @click="handleRetryPost(post.id)" :loading="retryingId === post.id">Retry</Button>
                  </div>
                  <a v-else-if="post.published_media_id" :href="'https://www.threads.net/post/' + post.published_media_id" target="_blank" class="text-xs font-bold hover:underline">
                    View on Threads
                  </a>                                                             
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>                                                           
    </Card>

    <!-- FLOATING BULK ACTION BAR (FITUR 4) -->
    <Transition name="fade">
      <div v-if="totalSelected > 0" class="fixed bottom-6 left-1/2 -translate-x-1/2 z-50 flex items-center gap-4 px-6 py-3 rounded-full shadow-2xl border theme-border theme-bg-sec">
        <span class="text-sm font-bold theme-text">{{ totalSelected }} selected</span>
        <div class="w-px h-4 theme-border bg-current opacity-20"></div>
        <button @click="handleBulkDelete" :disabled="isBulkDeleting" class="text-sm font-bold text-red-500 hover:text-red-600 transition flex items-center gap-2">
          <span v-if="isBulkDeleting" class="w-3 h-3 border-2 border-current border-t-transparent rounded-full animate-spin"></span>
          Delete Selected
        </button>
      </div>
    </Transition>

    <!-- EDIT MODAL DENGAN FITUR 5 (PREVIEW) -->
    <Teleport to="body">                                                 
      <div v-if="editingPost" class="fixed inset-0 backdrop-blur-sm z-[100] flex items-center justify-center p-4" style="background: rgba(0,0,0,0.6);">
        <div class="card max-w-lg w-full p-6 space-y-4 shadow-2xl flex flex-col max-h-[90vh]" style="background: var(--bg);">
          
          <div class="flex justify-between items-center pb-2 border-b theme-border shrink-0">
            <div class="flex gap-4">
              <button @click="modalTab = 'edit'" class="text-base font-bold transition" :class="modalTab === 'edit' ? 'theme-text border-b-2 border-current' : 'theme-text-muted hover:theme-text'">Edit Post</button>
              <button @click="modalTab = 'preview'" class="text-base font-bold transition" :class="modalTab === 'preview' ? 'theme-text border-b-2 border-current' : 'theme-text-muted hover:theme-text'">Preview</button>
            </div>
            <button @click="magicRewrite" :disabled="isRewriting || !editForm.text" class="text-xs font-bold flex items-center gap-1.5 px-3 py-1.5 rounded-lg border theme-border hover:theme-bg-sec transition-colors">
              <span v-if="isRewriting" class="w-3 h-3 border-2 border-current border-t-transparent rounded-full animate-spin"></span>
              <span v-else>✨</span>
              <span>{{ isRewriting ? 'Improving...' : 'Magic Rewrite' }}</span>
            </button>
          </div>
          
          <div class="overflow-y-auto pr-2 flex-1">
            <!-- TAB EDIT -->
            <div v-if="modalTab === 'edit'" class="space-y-4">
              <Textarea v-model="editForm.text" :rows="6" :max-length="500" />
              <div class="space-y-1">
                <label class="label theme-text">New Schedule Time</label>
                <input v-model="editForm.scheduled_for" type="datetime-local" class="input" />
              </div>  
            </div>

            <!-- TAB PREVIEW (MOCKUP THREADS) -->
            <div v-else class="py-4">
              <div class="flex gap-3">
                <div class="w-10 h-10 rounded-full theme-bg-sec border theme-border shrink-0 flex items-center justify-center font-bold text-xs">IX</div>
                <div class="flex-1">
                  <div class="flex items-center gap-1">
                    <span class="font-bold text-sm theme-text">ixiera.id</span>
                    <span class="text-xs theme-text-muted">· now</span>
                  </div>
                  <p class="text-sm whitespace-pre-wrap mt-1 leading-relaxed theme-text">{{ editForm.text }}</p>
                  
                  <div class="flex items-center gap-4 mt-4 text-gray-500">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path></svg>
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path></svg>
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path></svg>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="flex justify-end gap-3 pt-4 border-t theme-border shrink-0">
            <Button variant="secondary" @click="editingPost = null">Cancel</Button>
            <Button @click="saveEdit" :disabled="isUpdating || modalTab === 'preview'" :loading="isUpdating">
              {{ isUpdating ? 'Saving...' : 'Save Changes' }}
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
import { Card, Button, Textarea, Badge } from '../../components/ui'

const { showToast, askConfirm } = useNotify()

const loading = ref(true)
const isUpdating = ref(false)  
const isRewriting = ref(false)
const isBulkDeleting = ref(false)                                    
const posts = ref<any[]>([])
const retryingId = ref<string | null>(null)
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
  { label: 'Scheduled', value: 'scheduled' as const },                 
  { label: 'Published', value: 'published' as const },
  { label: 'Failed', value: 'failed' as const },
  { label: 'All', value: 'all' as const },
]

const filteredPosts = computed(() => {
  let filtered = posts.value
  if (activeFilter.value === 'failed') {
    filtered = posts.value.filter(p => ['error', 'failed', 'quota_exceeded'].includes(p.status))
  } else if (activeFilter.value !== 'all') {
    filtered = posts.value.filter(p => p.status === activeFilter.value)
  }

  const groups = new Map()
  filtered.forEach(post => {
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

// FITUR 3: GROUPING BY DATE
const groupedByDate = computed(() => {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  const tomorrow = new Date(today)
  tomorrow.setDate(tomorrow.getDate() + 1)

  const groups: Record<string, any[]> = {
    'Today': [], 'Tomorrow': [], 'Upcoming': [], 'Past': []
  }

  // Sort by date first
  const sorted = [...filteredPosts.value].sort((a, b) => {
    return new Date(a.parts[0].scheduled_for).getTime() - new Date(b.parts[0].scheduled_for).getTime()
  })

  sorted.forEach(group => {
    const postDate = new Date(group.parts[0].scheduled_for)
    postDate.setHours(0, 0, 0, 0)

    if (postDate.getTime() === today.getTime()) groups['Today'].push(group)
    else if (postDate.getTime() === tomorrow.getTime()) groups['Tomorrow'].push(group)
    else if (postDate > tomorrow) groups['Upcoming'].push(group)
    else groups['Past'].push(group)
  })

  return Object.entries(groups)
    .filter(([_, items]) => items.length > 0)
    .map(([label, items]) => ({ label, items }))
})

// FITUR 4: BULK SELECT LOGIC
const totalSelected = computed(() => selectedPosts.value.size + selectedThreads.value.size)

function togglePostSelection(id: string) {
  if (selectedPosts.value.has(id)) selectedPosts.value.delete(id)
  else selectedPosts.value.add(id)
}

function toggleGroupSelection(group: any) {
  if (selectedThreads.value.has(group.id)) {
    selectedThreads.value.delete(group.id)
  } else {
    selectedThreads.value.add(group.id)
  }
}

function isGroupSelected(group: any) {
  return selectedThreads.value.has(group.id)
}

async function handleBulkDelete() {
  const allIds: string[] = []
  
  // Kumpulin ID dari thread yang dicentang
  filteredPosts.value.forEach(group => {
    if (selectedThreads.value.has(group.id)) {
      group.parts.forEach((p: any) => allIds.push(p.id))
    } else {
      // Kumpulin ID dari post standalone yang dicentang
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
        const res = await fetch('https://threads-automation-production-53ad.up.railway.app/api/v1/queue/bulk-delete', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ post_ids: allIds })
        })
        if (!res.ok) throw new Error('Bulk delete failed')
        showToast(`${allIds.length} posts deleted.`, 'info')
        
        selectedPosts.value.clear()
        selectedThreads.value.clear()
        await loadPosts()
      } catch (err: any) {
        showToast('Error: ' + err.message, 'error')
      } finally {
        isBulkDeleting.value = false
      }
    }
  })
}

// LOGIKA LAINNYA
const emptyMessage = computed(() => {
  if (activeFilter.value === 'scheduled') return 'No posts in queue.'
  if (activeFilter.value === 'published') return 'No published posts yet.'                                                     
  if (activeFilter.value === 'failed') return 'No failed posts.'
  return 'No posts found.'
})                                                                 

function countByStatus(status: string) {
  if (status === 'all') return posts.value.length
  if (status === 'failed') return posts.value.filter(p => ['error', 'failed', 'quota_exceeded'].includes(p.status)).length
  return posts.value.filter(p => p.status === status).length
}

function toggleExpand(groupId: string) {
  if (expandedThreads.value.has(groupId)) expandedThreads.value.delete(groupId)
  else expandedThreads.value.add(groupId)
}

function formatTime(isoString: string) {                             
  if (!isoString) return ''
  const d = new Date(isoString)
  return d.toLocaleString('en-US', { timeStyle: 'short' })
}                                                                  
function statusVariant(status: string) {
  if (status === 'published') return 'accent'                        
  if (['error', 'failed', 'quota_exceeded'].includes(status)) return 'danger'                                                           
  return 'default'
}

async function loadPosts() {
  loading.value = true
  posts.value = []                                                 
  selectedPosts.value.clear()
  selectedThreads.value.clear()
  
  const { data: { user } } = await supabase.auth.getUser()           
  if (!user) { loading.value = false; return }

  const { data: account } = await supabase.schema('threads').from('threads_accounts').select('id, ai_provider').eq('user_id', user.id).maybeSingle()                                                 
  if (!account) { loading.value = false; return }
  
  currentAccountId.value = account.id
  if (account.ai_provider) aiProvider.value = account.ai_provider

  const { data } = await supabase.schema('threads').from('scheduled_posts').select('*').eq('account_id', account.id).order('scheduled_for', { ascending: true }).limit(100)                                                                     
  if (data) posts.value = data                                       
  loading.value = false
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
    const res = await fetch('https://threads-automation-production-53ad.up.railway.app/api/v1/queue/edit', {
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
    await loadPosts()                                                
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
    const res = await fetch('https://threads-automation-production-53ad.up.railway.app/api/v1/rag/improve', {
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
    const res = await fetch(`https://threads-automation-production-53ad.up.railway.app/api/v1/queue/${id}`, { method: 'DELETE' })
    if (!res.ok) throw new Error('Failed to delete')
    showToast('Post deleted.', 'info')
    await loadPosts()
  } catch (err: any) {
    showToast('Delete failed: ' + err.message, 'error')
  }
}

async function handleRetryPost(id: string) {
  retryingId.value = id
  try {
    const res = await fetch('https://threads-automation-production-53ad.up.railway.app/api/v1/queue/retry', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ post_id: id })
    })
    if (!res.ok) throw new Error('Failed to retry')
    showToast('Post re-queued for publishing.', 'success')
    await loadPosts()
  } catch (err: any) {
    showToast('Retry failed: ' + err.message, 'error')
  } finally {
    retryingId.value = null
  }
}

onMounted(() => loadPosts())
</script>                                                          
