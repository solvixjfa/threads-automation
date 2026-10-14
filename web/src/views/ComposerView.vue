<template>
  <div class="space-y-8 relative">
    <NotifyOverlay />

    <div>
      <h1 class="text-2xl font-bold tracking-tight">Composer</h1>
      <p class="text-sm theme-text-muted mt-1">Tulis atau buat draf otomatis dengan AI, pecah utasan, dan jadwalkan postingan.</p>
    </div>

    <Card>
      <template #header>
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full animate-pulse" style="background: var(--accent);"></span>
            <h2 class="text-xs font-bold uppercase tracking-wide">AI Post Generator</h2>
          </div>
          <button
            @click="showAiPanel = !showAiPanel"
            class="text-xs font-bold theme-text hover:underline"
          >
            {{ showAiPanel ? 'Sembunyikan Panel' : 'Buat Draf Otomatis' }}
          </button>
        </div>
      </template>

      <div v-if="showAiPanel" class="space-y-4">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
          <div class="md:col-span-2">
            <Input
              v-model="aiTopic"
              label="Topik / Ide Singkat"
              placeholder="Masukan topik singkat (contoh: Pembuatan website di Ixiera)..."
            />
          </div>
          <div class="space-y-1">
            <label class="label">Gaya Bahasa / Tone</label>
            <select v-model="aiTone" class="input">
              <option value="Edukasi & Insight Kasual">Edukasi dan Insight</option>
              <option value="Storytelling Pengalaman">Storytelling</option>
              <option value="Hot Take & Diskusi">Hot Take / Opini</option>
              <option value="Pertanyaan / Q&A">Q&A / Memancing Diskusi</option>
              <option value="Custom Prompt">Custom / Instruksi Bebas</option>
            </select>
          </div>

          <div v-if="aiTone === 'Custom Prompt'" class="md:col-span-3">
            <Textarea
              v-model="customPrompt"
              label="Instruksi Khusus (Custom Prompt)"
              :rows="3"
              placeholder="Contoh: Tulis dalam bahasa gaul, sebutkan ixiera.id 2 kali, dan akhiri dengan pertanyaan memancing..."
            />
          </div>
        </div>

        <div class="flex justify-end">
          <Button
            @click="generateAiIdeas"
            :disabled="isGenerating || !aiTopic || (aiTone === 'Custom Prompt' && !customPrompt)"
            :loading="isGenerating"
          >
            {{ isGenerating ? 'Mengekstrak RAG...' : 'Hasilkan 3 Draf Post' }}
          </Button>
        </div>

        <div v-if="aiResults.length > 0" class="grid grid-cols-1 md:grid-cols-3 gap-3 pt-3 divider">
          <div
            v-for="item in aiResults"
            :key="item.id"
            class="card card-hover p-4 flex flex-col justify-between space-y-3"
          >
            <div class="space-y-1.5">
              <Badge variant="accent">{{ item.title }}</Badge>
              <p class="text-xs whitespace-pre-wrap leading-relaxed">{{ item.content }}</p>
            </div>
            <Button variant="secondary" size="sm" @click="applyAiDraft(item.content)">
              Gunakan Draf Ini
            </Button>
          </div>
        </div>
      </div>
    </Card>

    <Card>
      <div class="flex justify-between items-center mb-4">
        <span class="text-xs font-bold uppercase tracking-wide">Teks Postingan Utama</span>
        <div class="flex items-center gap-2">
          <Badge v-if="postText.length > 500" variant="accent">
            Auto-Split ({{ threadParts.length }} Parts)
          </Badge>
          <span class="text-xs font-medium" :class="postText.length > 500 ? 'theme-text font-bold' : 'theme-text-muted'">
            {{ postText.length }} Chars
          </span>
        </div>
      </div>

      <Textarea
        v-model="postText"
        :rows="6"
        placeholder="Tulis draf postingan di sini. Jika lebih dari 500 karakter, sistem akan memecahnya menjadi utasan otomatis..."
      />

      <div v-if="threadParts.length > 1" class="space-y-3 pt-3 divider mt-4">
        <span class="text-xs font-bold uppercase tracking-wide">Pratinjau Utasan Thread ({{ threadParts.length }} Bagian)</span>
        <div v-for="(part, idx) in threadParts" :key="idx" class="p-3 rounded-xl theme-bg-sec border theme-border space-y-1.5">
          <div class="flex justify-between items-center text-[11px] font-bold theme-text-muted">
            <span>Bagian {{ idx + 1 }} dari {{ threadParts.length }}</span>
            <span :class="part.length > 500 ? 'font-bold' : ''" :style="part.length > 500 ? 'color: var(--danger);' : ''">
              {{ part.length }} / 500
            </span>
          </div>
          <textarea
            v-model="threadParts[idx]"
            rows="3"
            class="textarea text-xs"
          ></textarea>
        </div>
      </div>

      <div class="flex flex-wrap items-center gap-3 mt-4">
        <Button
          variant="secondary"
          @click="checkScore"
          :disabled="isChecking || !postText"
          :loading="isChecking"
        >
          {{ isChecking ? 'Menganalisa...' : 'Cek Skor AI' }}
        </Button>

        <div class="flex-1 flex justify-end items-center gap-3 flex-wrap">
          <input
            v-model="scheduledDate"
            type="datetime-local"
            class="input"
            style="width: auto;"
          />
          <Button
            @click="schedulePost"
            :disabled="!postText || !scheduledDate || isSaving"
            :loading="isSaving"
          >
            {{ isSaving ? 'Memproses...' : (threadParts.length > 1 ? 'Jadwalkan ' + threadParts.length + ' Utasan' : 'Jadwalkan') }}
          </Button>
        </div>
      </div>
    </Card>

    <Card padding="false">
      <div class="p-5 divider flex justify-between items-center theme-bg-sec">
        <span class="text-xs font-bold uppercase tracking-wide">Antrean Terjadwal</span>
        <button @click="loadPosts" class="text-xs font-bold hover:underline">Refresh</button>
      </div>

      <div v-if="loading" class="p-8 text-center text-xs theme-text-muted font-medium animate-pulse">Memuat data...</div>

      <div v-else-if="posts.length === 0" class="p-8 text-center text-xs theme-text-muted font-medium">
        Belum ada postingan dalam antrean.
      </div>

      <div v-else class="list-divided">
        <div v-for="post in posts" :key="post.id" class="p-5 space-y-3">
          <div class="flex items-start justify-between gap-4">
            <p class="text-sm font-medium whitespace-pre-wrap flex-1">{{ post.text }}</p>
            <Badge :variant="statusVariant(post.status)">{{ post.status }}</Badge>
          </div>
          <div class="flex items-center justify-between pt-1 text-xs">
            <span class="theme-text-muted font-medium">{{ formatDate(post.scheduled_for) }}</span>
            <div v-if="post.status === 'scheduled'" class="flex items-center gap-2">
              <Button variant="secondary" size="sm" @click="openEditModal(post)">Edit</Button>
              <Button variant="danger" size="sm" @click="confirmDeletePost(post.id)">Hapus</Button>
            </div>
          </div>
        </div>
      </div>
    </Card>

    <Teleport to="body">
      <div v-if="scoreResult" class="fixed inset-0 backdrop-blur-sm z-[100] flex items-center justify-center p-4" style="background: rgba(0,0,0,0.6);">
        <div class="card max-w-md w-full p-6 space-y-4">
          <div class="flex justify-between items-center pb-3 divider">
            <h3 class="text-sm font-bold uppercase tracking-wide">Hasil Analisa Skor AI</h3>
            <Badge variant="accent">{{ scoreResult.score }} / 100</Badge>
          </div>
          <div class="space-y-1">
            <label class="label">Catatan dan Feedback</label>
            <p class="text-xs leading-relaxed theme-bg-sec p-3.5 rounded-xl border theme-border">
              {{ scoreResult.feedback }}
            </p>
          </div>
          <div class="flex justify-end pt-2">
            <Button @click="scoreResult = null">Tutup</Button>
          </div>
        </div>
      </div>
    </Teleport>

    <Teleport to="body">
      <div v-if="editingPost" class="fixed inset-0 backdrop-blur-sm z-[100] flex items-center justify-center p-4" style="background: rgba(0,0,0,0.6);">
        <div class="card max-w-lg w-full p-6 space-y-4">
          <h3 class="text-base font-bold">Edit / Rewrite Postingan</h3>
          <Textarea v-model="editForm.text" :rows="5" :max-length="500" />
          <div class="space-y-1">
            <label class="label">Waktu Tayang Baru</label>
            <input v-model="editForm.scheduled_for" type="datetime-local" class="input" />
          </div>
          <div class="flex justify-end gap-3 pt-2">
            <Button variant="secondary" @click="editingPost = null">Batal</Button>
            <Button @click="saveEdit" :disabled="isUpdating" :loading="isUpdating">
              {{ isUpdating ? 'Menyimpan...' : 'Simpan Perubahan' }}
            </Button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { supabase } from '../lib/supabase'
import { useNotify } from '../composables/useNotify'
import NotifyOverlay from '../components/NotifyOverlay.vue'
import { Card, Button, Input, Textarea, Badge } from '../components/ui'

const { showToast, askConfirm } = useNotify()

const postText = ref('')
const threadParts = ref<string[]>([])
const scheduledDate = ref('')
const isSaving = ref(false)
const isChecking = ref(false)
const isUpdating = ref(false)
const loading = ref(true)
const posts = ref<any[]>([])

const showAiPanel = ref(true)
const aiTopic = ref('')
const aiTone = ref('Edukasi & Insight Kasual')
const customPrompt = ref('')
const isGenerating = ref(false)
const aiResults = ref<any[]>([])
const scoreResult = ref<any>(null)

const editingPost = ref<any>(null)
const editForm = ref({ text: '', scheduled_for: '' })

function splitTextIntoParts(text: string, maxLen = 480): string[] {
  if (text.length <= maxLen) return [text]
  const paragraphs = text.split(/\n+/)
  const parts: string[] = []
  let current = ''

  for (const p of paragraphs) {
    if ((current + '\n\n' + p).trim().length <= maxLen) {
      current = current ? current + '\n\n' + p : p
    } else {
      if (current) parts.push(current.trim())
      if (p.length <= maxLen) {
        current = p
      } else {
        const sentences = p.match(/[^.!?]+[.!?]+/g) || [p]
        for (const s of sentences) {
          if ((current + ' ' + s).trim().length <= maxLen) {
            current = current ? current + ' ' + s : s
          } else {
            if (current) parts.push(current.trim())
            current = s
          }
        }
      }
    }
  }
  if (current) parts.push(current.trim())
  return parts
}

function handleTextChange() {
  threadParts.value = splitTextIntoParts(postText.value)
}

watch(postText, handleTextChange)

function formatDate(isoString: string) {
  const d = new Date(isoString)
  return d.toLocaleString('id-ID', { dateStyle: 'medium', timeStyle: 'short' })
}

function statusVariant(status: string) {
  if (status === 'scheduled') return 'default'
  if (status === 'published') return 'accent'
  if (['error', 'failed', 'quota_exceeded'].includes(status)) return 'danger'
  return 'default'
}

async function generateAiIdeas() {
  if (!aiTopic.value) return
  isGenerating.value = true
  aiResults.value = []

  try {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) throw new Error('Pengguna belum terautentikasi')

    const { data: account } = await supabase
      .schema('threads')
      .from('threads_accounts')
      .select('id')
      .eq('user_id', user.id)
      .maybeSingle()

    if (!account) throw new Error('Akun Threads belum tersambung')

    const response = await fetch('https://threads-automation-production-53ad.up.railway.app/api/v1/rag/generate-post', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        account_id: account.id,
        topic: aiTopic.value,
        tone: aiTone.value,
        custom_prompt: aiTone.value === 'Custom Prompt' ? customPrompt.value : undefined
      })
    })

    if (!response.ok) {
      const errData = await response.json()
      throw new Error(errData.detail || 'Gagal memproses draf di backend')
    }

    const resData = await response.json()
    if (resData?.options) {
      aiResults.value = resData.options
      showToast('3 Draf berbasis RAG berhasil dibuat oleh AI!', 'success')
    }
  } catch (err: any) {
    showToast('Gagal AI Generator: ' + err.message, 'error')
  } finally {
    isGenerating.value = false
  }
}

function applyAiDraft(content: string) {
  postText.value = content
  showToast('Draf AI berhasil diterapkan ke Composer.', 'info')
}

async function checkScore() {
  isChecking.value = true
  try {
    const { data, error } = await supabase.functions.invoke('score-draft', {
      body: { text: postText.value }
    })
    if (error) throw error
    if (data?.error) throw new Error(data.error)

    scoreResult.value = {
      score: data?.score ?? 80,
      feedback: data?.feedback ?? 'Teks sudah cukup natural.'
    }
  } catch (err: any) {
    showToast('Gagal analisa AI: ' + err.message, 'error')
  } finally {
    isChecking.value = false
  }
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
    .order('created_at', { ascending: false })
    .limit(20)

  if (data) posts.value = data
  loading.value = false
}

async function schedulePost() {
  if (!postText.value || !scheduledDate.value) {
    return showToast('Isi teks dan tanggal terlebih dahulu.', 'error')
  }
  isSaving.value = true

  try {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) throw new Error('Pengguna belum terautentikasi')

    const { data: account, error: accErr } = await supabase
      .schema('threads')
      .from('threads_accounts')
      .select('id')
      .eq('user_id', user.id)
      .maybeSingle()

    if (accErr) throw new Error(accErr.message)
    if (!account) throw new Error('Akun Threads belum tersambung.')

    const isoDate = new Date(scheduledDate.value).toISOString()
    const partsToSave = threadParts.value.length > 0 ? threadParts.value : [postText.value]

    let parentId: string | null = null

    for (let i = 0; i < partsToSave.length; i++) {
      const partText = partsToSave[i]
      const { data: insertedPost, error } = await supabase
        .schema('threads')
        .from('scheduled_posts')
        .insert({
          account_id: account.id,
          text: partText,
          scheduled_for: isoDate,
          status: 'scheduled',
          idempotency_key: crypto.randomUUID(),
          parent_id: parentId,
          sequence_number: i + 1
        })
        .select('id')
        .single()

      if (error) throw error
      if (i === 0 && insertedPost) {
        parentId = insertedPost.id
      }
    }

    postText.value = ''
    threadParts.value = []
    showToast('Postingan berhasil dijadwalkan!', 'success')
    await loadPosts()
  } catch (err: any) {
    showToast('Gagal menyimpan: ' + err.message, 'error')
  } finally {
    isSaving.value = false
  }
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
    message: 'Apakah kamu yakin ingin membatalkan dan menghapus postingan ini?',
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

onMounted(() => {
  const d = new Date()
  d.setHours(d.getHours() + 1)
  d.setMinutes(d.getMinutes() - d.getTimezoneOffset())
  scheduledDate.value = d.toISOString().slice(0, 16)
  loadPosts()

  const savedDraft = localStorage.getItem('draft_repurpose')
  if (savedDraft) {
    postText.value = savedDraft
    localStorage.removeItem('draft_repurpose')
  }
})
</script>
