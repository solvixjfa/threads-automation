<template>
  <div class="space-y-8 relative">
    <NotifyOverlay />

    <div>
      <h1 class="text-2xl font-bold text-slate-900 tracking-tight">Composer & Thread Builder</h1>
      <p class="text-slate-500 text-sm mt-1">Tulis atau buat draf otomatis dengan AI, pecah utasan, dan jadwalkan postingan.</p>
    </div>

    <!-- AI Generator Section -->
    <div class="bg-indigo-50/60 border border-indigo-100 rounded-2xl p-6 shadow-sm space-y-4">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-indigo-600 animate-pulse"></span>
          <h2 class="text-xs font-bold text-indigo-900 uppercase tracking-wide">AI Post Generator (Gemini + RAG)</h2>
        </div>
        <button 
          @click="showAiPanel = !showAiPanel" 
          class="text-xs font-bold text-indigo-700 hover:text-indigo-900 transition"
        >
          {{ showAiPanel ? 'Sembunyikan Panel' : 'Buat Draf Otomatis' }}
        </button>
      </div>

      <div v-if="showAiPanel" class="space-y-4 pt-2">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
          <div class="md:col-span-2 space-y-1">
            <label class="text-[11px] font-bold text-slate-700 uppercase">Topik / Ide Singkat</label>
            <input
              v-model="aiTopic"
              type="text"
              placeholder="Masukan topik singkat (contoh: Eksperimen XGBoost buat prediksi churn)..."
              class="w-full bg-white border border-indigo-200 rounded-xl p-3 text-xs text-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition"
            />
          </div>
          <div class="space-y-1">
            <label class="text-[11px] font-bold text-slate-700 uppercase">Gaya Bahasa / Tone</label>
            <select
              v-model="aiTone"
              class="w-full bg-white border border-indigo-200 rounded-xl p-3 text-xs text-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition"
            >
              <option value="Edukasi & Insight Kasual">Edukasi & Insight</option>
              <option value="Storytelling Pengalaman">Storytelling</option>
              <option value="Hot Take & Diskusi">Hot Take / Opini</option>
              <option value="Pertanyaan / Q&A">Q&A / Memancing Diskusi</option>
            </select>
          </div>
        </div>

        <div class="flex justify-end">
          <button
            @click="generateAiIdeas"
            :disabled="isGenerating || !aiTopic"
            class="bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold py-2.5 px-6 rounded-xl transition shadow-sm disabled:opacity-50 flex items-center gap-2"
          >
            <span v-if="isGenerating" class="w-3 h-3 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
            <span>{{ isGenerating ? 'Mengekstrak RAG & Gemini...' : 'Hasilkan 3 Draf Post' }}</span>
          </button>
        </div>

        <!-- Render Hasil Opsi AI -->
        <div v-if="aiResults.length > 0" class="grid grid-cols-1 md:grid-cols-3 gap-3 pt-3 border-t border-indigo-100">
          <div
            v-for="item in aiResults"
            :key="item.id"
            class="bg-white border border-indigo-100 rounded-xl p-4 flex flex-col justify-between space-y-3 shadow-sm hover:border-indigo-300 transition"
          >
            <div class="space-y-1.5">
              <span class="text-[10px] font-bold text-indigo-600 uppercase tracking-wider bg-indigo-50 px-2 py-0.5 rounded">
                {{ item.title }}
              </span>
              <p class="text-xs text-slate-800 whitespace-pre-wrap leading-relaxed">{{ item.content }}</p>
            </div>
            <button
              @click="applyAiDraft(item.content)"
              class="w-full py-2 bg-slate-100 hover:bg-indigo-600 hover:text-white text-slate-700 text-xs font-bold rounded-lg transition"
            >
              Gunakan Draf Ini
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Form Main Composer -->
    <div class="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-4">
      <div class="flex justify-between items-center">
        <span class="text-xs font-bold text-slate-700 tracking-wide uppercase">Teks Postingan Utama</span>
        <div class="flex items-center gap-2">
          <span v-if="postText.length > 500" class="text-xs font-bold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded">
            Auto-Split Ready ({{ threadParts.length }} Parts)
          </span>
          <span class="text-xs font-medium" :class="postText.length > 500 ? 'text-indigo-600 font-bold' : 'text-slate-400'">
            {{ postText.length }} Chars
          </span>
        </div>
      </div>

      <textarea
        v-model="postText"
        @input="handleTextChange"
        rows="6"
        placeholder="Tulis draf postingan di sini. Jika lebih dari 500 karakter, sistem akan memecahnya menjadi utasan otomatis..."
        class="w-full bg-slate-50 border border-slate-200 rounded-xl p-4 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition resize-none"
      ></textarea>

      <!-- Multi-Part Preview -->
      <div v-if="threadParts.length > 1" class="space-y-3 pt-2 border-t border-slate-100">
        <span class="text-xs font-bold text-slate-700 uppercase tracking-wide">Pratinjau Utasan Thread ({{ threadParts.length }} Bagian)</span>
        <div v-for="(part, idx) in threadParts" :key="idx" class="p-3 bg-slate-50 border border-slate-200 rounded-xl space-y-1.5">
          <div class="flex justify-between items-center text-[11px] font-bold text-slate-500">
            <span>Bagian {{ idx + 1 }} dari {{ threadParts.length }}</span>
            <span :class="part.length > 500 ? 'text-rose-600 font-bold' : 'text-slate-400'">{{ part.length }} / 500</span>
          </div>
          <textarea
            v-model="threadParts[idx]"
            rows="3"
            class="w-full bg-white border border-slate-200 rounded-lg p-2.5 text-xs text-slate-800 focus:outline-none focus:ring-1 focus:ring-indigo-500 transition resize-none"
          ></textarea>
        </div>
      </div>

      <div class="flex flex-wrap items-center gap-3 pt-2">
        <button 
          @click="checkScore" 
          :disabled="isChecking || !postText"
          class="bg-indigo-50 hover:bg-indigo-100 text-indigo-700 text-xs font-bold py-2.5 px-4 rounded-lg transition border border-indigo-100 disabled:opacity-50 flex items-center gap-2"
        >
          <span v-if="isChecking" class="w-3 h-3 border-2 border-indigo-600 border-t-transparent rounded-full animate-spin"></span>
          <span>{{ isChecking ? 'Menganalisa...' : 'Cek Skor AI' }}</span>
        </button>

        <div class="flex-1 flex justify-end items-center gap-3">
          <input
            v-model="scheduledDate"
            type="datetime-local"
            class="bg-slate-50 border border-slate-200 rounded-lg p-2.5 text-xs text-slate-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition"
          />
          <button
            @click="schedulePost"
            :disabled="!postText || isSaving"
            class="bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold py-2.5 px-6 rounded-lg transition shadow-md disabled:opacity-50 flex items-center gap-2"
          >
            <span v-if="isSaving" class="w-3 h-3 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
            <span>{{ isSaving ? 'Memproses...' : (threadParts.length > 1 ? `Jadwalkan ${threadParts.length} Utasan` : 'Jadwalkan') }}</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Modal Skor AI Card -->
    <div v-if="scoreResult" class="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div class="bg-white border border-slate-200 rounded-2xl max-w-md w-full p-6 space-y-4 shadow-2xl">
        <div class="flex justify-between items-center border-b border-slate-100 pb-3">
          <h3 class="text-sm font-bold text-slate-900 uppercase tracking-wide">Hasil Analisa Skor AI</h3>
          <span class="text-lg font-extrabold text-indigo-600 bg-indigo-50 px-3 py-1 rounded-xl">
            {{ scoreResult.score }} / 100
          </span>
        </div>
        <div class="space-y-1">
          <label class="text-[11px] font-bold text-slate-500 uppercase">Catatan & Feedback:</label>
          <p class="text-xs text-slate-800 leading-relaxed bg-slate-50 p-3.5 rounded-xl border border-slate-100">
            {{ scoreResult.feedback }}
          </p>
        </div>
        <div class="flex justify-end pt-2">
          <button @click="scoreResult = null" class="px-5 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold rounded-lg transition">
            Tutup
          </button>
        </div>
      </div>
    </div>

    <!-- Antrean Postingan -->
    <div class="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">
      <div class="p-5 border-b border-slate-100 bg-slate-50 flex justify-between items-center">
        <span class="text-xs font-bold text-slate-700 tracking-wide uppercase">Antrean Terjadwal</span>
        <button @click="loadPosts" class="text-xs font-bold text-indigo-600 hover:text-indigo-800">Refresh</button>
      </div>

      <div v-if="loading" class="p-8 text-center text-xs text-slate-400 font-medium animate-pulse">Memuat data...</div>
      
      <div v-else-if="posts.length === 0" class="p-8 text-center text-xs text-slate-400 font-medium">
        Belum ada postingan dalam antrean.
      </div>

      <div v-else class="divide-y divide-slate-100">
        <div v-for="post in posts" :key="post.id" class="p-5 hover:bg-slate-50/80 transition space-y-3">
          <div class="flex items-start justify-between gap-4">
            <p class="text-sm font-medium text-slate-800 whitespace-pre-wrap flex-1">{{ post.text }}</p>
            <span
              class="shrink-0 px-2.5 py-1 text-[10px] font-bold uppercase tracking-wider rounded-md"
              :class="{
                'bg-amber-50 text-amber-600 border border-amber-100': post.status === 'scheduled',
                'bg-emerald-50 text-emerald-600 border border-emerald-100': post.status === 'published',
                'bg-rose-50 text-rose-600 border border-rose-100': ['error', 'failed', 'quota_exceeded'].includes(post.status)
              }"
            >
              {{ post.status }}
            </span>
          </div>

          <div class="flex items-center justify-between pt-1 text-xs">
            <span class="text-slate-500 font-medium">{{ formatDate(post.scheduled_for) }}</span>
            <div v-if="post.status === 'scheduled'" class="flex items-center gap-2">
              <button @click="openEditModal(post)" class="px-3 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold rounded-md transition">
                Edit
              </button>
              <button @click="confirmDeletePost(post.id)" class="px-3 py-1 bg-rose-50 hover:bg-rose-100 text-rose-600 font-bold rounded-md transition">
                Batal / Hapus
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Edit / Rewrite -->
    <div v-if="editingPost" class="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div class="bg-white border border-slate-200 rounded-2xl max-w-lg w-full p-6 space-y-4 shadow-2xl">
        <h3 class="text-lg font-bold text-slate-900">Edit / Rewrite Postingan</h3>
        <textarea
          v-model="editForm.text"
          rows="5"
          class="w-full bg-slate-50 border border-slate-200 rounded-xl p-3 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition resize-none"
          maxlength="500"
        ></textarea>
        <div class="space-y-1">
          <label class="text-xs font-bold text-slate-700">Waktu Tayang Baru</label>
          <input
            v-model="editForm.scheduled_for"
            type="datetime-local"
            class="w-full bg-slate-50 border border-slate-200 rounded-lg p-2.5 text-xs text-slate-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition"
          />
        </div>
        <div class="flex justify-end gap-3 pt-2">
          <button @click="editingPost = null" class="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-lg transition">
            Batal
          </button>
          <button @click="saveEdit" :disabled="isUpdating" class="px-5 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold rounded-lg transition disabled:opacity-50">
            {{ isUpdating ? 'Menyimpan...' : 'Simpan Perubahan' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { supabase } from '../lib/supabase'
import { useNotify } from '../composables/useNotify'
import NotifyOverlay from '../components/NotifyOverlay.vue'

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

function formatDate(isoString: string) {
  const d = new Date(isoString)
  return d.toLocaleString('id-ID', { dateStyle: 'medium', timeStyle: 'short' })
}

async function generateAiIdeas() {
  if (!aiTopic.value) return
  isGenerating.value = true
  aiResults.value = []
  
  try {
    const { data, error } = await supabase.functions.invoke('generate-post', {
      body: { topic: aiTopic.value, tone: aiTone.value }
    })

    if (error) throw error
    if (data?.error) throw new Error(data.error)

    if (data?.options) {
      aiResults.value = data.options
      showToast('3 Draf berhasil dibuat oleh AI!', 'success')
    }
  } catch (err: any) {
    showToast('Gagal AI Generator: ' + err.message, 'error')
  } finally {
    isGenerating.value = false
  }
}

function applyAiDraft(content: string) {
  postText.value = content
  handleTextChange()
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
  posts.value = [] // Reset state sebelum mengambil antrean

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
  if (!postText.value || !scheduledDate.value) return showToast('Isi teks dan tanggal terlebih dahulu.', 'error')
  isSaving.value = true
  
  try {
    const { data: accounts, error: accErr } = await supabase
      .schema('threads')
      .from('threads_accounts')
      .select('id')
      .limit(1)
      .maybeSingle()
      
    if (accErr) throw new Error(accErr.message)
    if (!accounts) throw new Error('Akun Threads belum tersambung.')

    const isoDate = new Date(scheduledDate.value).toISOString()
    const partsToSave = threadParts.value.length > 0 ? threadParts.value : [postText.value]

    let parentId: string | null = null

    for (let i = 0; i < partsToSave.length; i++) {
      const partText = partsToSave[i]
      const { data: insertedPost, error } = await supabase
        .schema('threads')
        .from('scheduled_posts')
        .insert({
          account_id: accounts.id,
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
    message: 'Apakah kamu yakin ingin membatalkan & menghapus postingan ini?',
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
})
</script>
