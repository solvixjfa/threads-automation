<template>
  <div class="space-y-4 relative">                                                                                                        
    <Card padding="false">
      <div class="p-5 divider flex justify-between items-center theme-bg-sec">                                                                
        <div class="flex items-center gap-2">
          <span class="text-xs font-bold uppercase tracking-wide">Scheduled Queue</span>
          <Badge>{{ filteredPosts.length }} posts</Badge>
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
        <div v-for="post in filteredPosts" :key="post.id" class="p-5 space-y-3">
          <div class="flex items-start justify-between gap-4">                 
            <div class="flex-1 space-y-1">
              <div class="flex items-center gap-2 flex-wrap">
                <Badge :variant="statusVariant(post.status)">{{ post.status }}</Badge>
                <span v-if="post.sequence_number > 1" class="text-[10px] font-bold theme-text-muted">
                  Part {{ post.sequence_number }}                                  
                </span>
              </div>
              <p class="text-sm font-medium whitespace-pre-wrap">{{ post.text }}</p>
            </div>
          </div>

          <div class="flex items-center justify-between pt-1 text-xs gap-3 flex-wrap">
            <span class="theme-text-muted font-medium">{{ formatDate(post.scheduled_for) }}</span>
            
            <!-- AKSI UNTUK POSTINGAN TERJADWAL -->
            <div v-if="post.status === 'scheduled'" class="flex items-center gap-2">                                                                
              <Button variant="secondary" size="sm" @click="openEditModal(post)">Edit</Button>                                                      
              <Button variant="danger" size="sm" @click="confirmDeletePost(post.id)">Delete</Button>                                               
            </div>                                                             
            
            <!-- AKSI UNTUK POSTINGAN GAGAL -->
            <div v-else-if="['error', 'failed', 'quota_exceeded'].includes(post.status)" class="flex items-center gap-2">
              <Button size="sm" @click="handleRetryPost(post.id)" :loading="retryingId === post.id">Retry</Button>
            </div>

            <!-- LINK KE THREADS -->
            <a v-else-if="post.published_media_id"
              :href="'https://www.threads.net/post/' + post.published_media_id"                                                                     
              target="_blank"
              class="text-xs font-bold hover:underline"
            >
              View on Threads
            </a>                                                             
          </div>
        </div>
      </div>                                                           
    </Card>

    <!-- EDIT MODAL -->
    <Teleport to="body">                                                 
      <div v-if="editingPost" class="fixed inset-0 backdrop-blur-sm z-[100] flex items-center justify-center p-4" style="background: rgba(0,0,0,0.6);">
        <div class="card max-w-lg w-full p-6 space-y-4 shadow-2xl" style="background: var(--bg);">
          <h3 class="text-base font-bold theme-text">Edit Post</h3>                
          <Textarea v-model="editForm.text" :rows="5" :max-length="500" />
          <div class="space-y-1">
            <label class="label theme-text">New Schedule Time</label>
            <input v-model="editForm.scheduled_for" type="datetime-local" class="input" />
          </div>                                                             
          <div class="flex justify-end gap-3 pt-2">
            <Button variant="secondary" @click="editingPost = null">Cancel</Button>
            <Button @click="saveEdit" :disabled="isUpdating" :loading="isUpdating">
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
const posts = ref<any[]>([])
const retryingId = ref<string | null>(null)
const activeFilter = ref<'all' | 'scheduled' | 'published' | 'failed'>('scheduled')
const editingPost = ref<any>(null)                                 
const editForm = ref({ text: '', scheduled_for: '' })

const tabs = [
  { label: 'Scheduled', value: 'scheduled' as const },                 
  { label: 'Published', value: 'published' as const },
  { label: 'Failed', value: 'failed' as const },
  { label: 'All', value: 'all' as const },
]

const filteredPosts = computed(() => {
  if (activeFilter.value === 'all') return posts.value
  if (activeFilter.value === 'failed') {
    return posts.value.filter(p => ['error', 'failed', 'quota_exceeded'].includes(p.status))
  }                                                                  
  return posts.value.filter(p => p.status === activeFilter.value)
})

const emptyMessage = computed(() => {
  if (activeFilter.value === 'scheduled') return 'No posts in queue.'
  if (activeFilter.value === 'published') return 'No published posts yet.'                                                     
  if (activeFilter.value === 'failed') return 'No failed posts.'
  return 'No posts found.'
})                                                                 
function countByStatus(status: string) {
  if (status === 'all') return posts.value.length
  if (status === 'failed') {
    return posts.value.filter(p => ['error', 'failed', 'quota_exceeded'].includes(p.status)).length
  }                                                                  
  return posts.value.filter(p => p.status === status).length
}

function formatDate(isoString: string) {                             
  if (!isoString) return ''
  const d = new Date(isoString)
  return d.toLocaleString('en-US', { dateStyle: 'medium', timeStyle: 'short' })
}                                                                  
function statusVariant(status: string) {
  if (status === 'published') return 'accent'                        
  if (['error', 'failed', 'quota_exceeded'].includes(status)) return 'danger'                                                           
  return 'default'
}

async function loadPosts() {
  loading.value = true
  posts.value = []                                                 
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
    .from('scheduled_posts')                                           
    .select('*')
    .eq('account_id', account.id)
    .order('scheduled_for', { ascending: true })
    .limit(100)
                                                                     
  if (data) posts.value = data                                       
  loading.value = false
}
                                                                   
function openEditModal(post: any) {                                  
  editingPost.value = post
  editForm.value.text = post.text
  const d = new Date(post.scheduled_for)
  d.setMinutes(d.getMinutes() - d.getTimezoneOffset())
  editForm.value.scheduled_for = d.toISOString().slice(0, 16)
}

async function saveEdit() {
  if (!editingPost.value) return
  isUpdating.value = true
  try {
    // NEMBAK KE RAILWAY
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

    if (!res.ok) {
      const err = await res.json()
      throw new Error(err.detail)
    }

    editingPost.value = null
    showToast('Post updated successfully.', 'success')
    await loadPosts()                                                
  } catch (err: any) {
    showToast('Update failed: ' + err.message, 'error')               
  } finally {
    isUpdating.value = false
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
    const res = await fetch(`https://threads-automation-production-53ad.up.railway.app/api/v1/queue/${id}`, {
      method: 'DELETE'
    })

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
