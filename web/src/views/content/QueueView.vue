<template>
  <div class="space-y-4">
    <Card padding="false">
      <div class="p-5 divider flex justify-between items-center theme-bg-sec">
        <div class="flex items-center gap-2">
          <span class="text-xs font-bold uppercase tracking-wide">Antrean Terjadwal</span>
          <Badge>{{ filteredPosts.length }} post</Badge>
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
        Memuat antrean...
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
            <div v-if="post.status === 'scheduled'" class="flex items-center gap-2">
              <Button variant="secondary" size="sm" @click="openEditModal(post)">Edit</Button>
              <Button variant="danger" size="sm" @click="confirmDeletePost(post.id)">Hapus</Button>
            </div>
            <a
              v-else-if="post.published_media_id"
              :href="'https://www.threads.net/post/' + post.published_media_id"
              target="_blank"
              class="text-xs font-bold hover:underline"
            >
              Lihat di Threads
            </a>
          </div>
        </div>
      </div>
    </Card>

    <Teleport to="body">
      <div v-if="editingPost" class="fixed inset-0 backdrop-blur-sm z-[100] flex items-center justify-center p-4" style="background: rgba(0,0,0,0.6);">
        <div class="card max-w-lg w-full p-6 space-y-4">
          <h3 class="text-base font-bold">Edit Postingan</h3>
          <Textarea v-model="editForm.text" :rows="5" :max-length="500" />
          <div class="space-y-1">
            <label class="label">Waktu Tayang Baru</label>
            <input v-model="editForm.scheduled_for" type="datetime-local" class="input" />
          </div>
          <div class="flex justify-end gap-3 pt-2">
            <Button variant="secondary" @click="editingPost = null">Batal</Button>
            <Button @click="saveEdit" :disabled="isUpdating" :loading="isUpdating">
              {{ isUpdating ? 'Menyimpan...' : 'Simpan' }}
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
const activeFilter = ref<'all' | 'scheduled' | 'published' | 'failed'>('scheduled')
const editingPost = ref<any>(null)
const editForm = ref({ text: '', scheduled_for: '' })

const tabs = [
  { label: 'Antrean', value: 'scheduled' as const },
  { label: 'Terbit', value: 'published' as const },
  { label: 'Gagal', value: 'failed' as const },
  { label: 'Semua', value: 'all' as const },
]

const filteredPosts = computed(() => {
  if (activeFilter.value === 'all') return posts.value
  if (activeFilter.value === 'failed') {
    return posts.value.filter(p => ['error', 'failed', 'quota_exceeded'].includes(p.status))
  }
  return posts.value.filter(p => p.status === activeFilter.value)
})

const emptyMessage = computed(() => {
  if (activeFilter.value === 'scheduled') return 'Belum ada postingan dalam antrean.'
  if (activeFilter.value === 'published') return 'Belum ada postingan yang terbit.'
  if (activeFilter.value === 'failed') return 'Tidak ada postingan yang gagal.'
  return 'Belum ada postingan.'
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
  return d.toLocaleString('id-ID', { dateStyle: 'medium', timeStyle: 'short' })
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
    const isoDate = new Date(editForm.value.scheduled_for).toISOString()
    const { error } = await supabase
      .schema('threads')
      .from('scheduled_posts')
      .update({
        text: editForm.value.text,
        scheduled_for: isoDate
      })
      .eq('id', editingPost.value.id)

    if (error) throw error
    editingPost.value = null
    showToast('Postingan berhasil diperbarui.', 'success')
    await loadPosts()
  } catch (err: any) {
    showToast('Gagal update: ' + err.message, 'error')
  } finally {
    isUpdating.value = false
  }
}

function confirmDeletePost(id: string) {
  askConfirm({
    title: 'Hapus Postingan Terjadwal',
    message: 'Apakah kamu yakin ingin menghapus postingan ini?',
    confirmText: 'Hapus Post',
    onConfirm: () => deletePost(id)
  })
}

async function deletePost(id: string) {
  try {
    const { error } = await supabase
      .schema('threads')
      .from('scheduled_posts')
      .delete()
      .eq('id', id)

    if (error) throw error
    showToast('Postingan berhasil dihapus.', 'info')
    await loadPosts()
  } catch (err: any) {
    showToast('Gagal menghapus: ' + err.message, 'error')
  }
}

onMounted(() => loadPosts())
</script>
