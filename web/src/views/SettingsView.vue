<template>
  <div class="space-y-8 max-w-5xl relative">
    <NotifyOverlay />

    <div>
      <h1 class="text-2xl font-bold tracking-tight">Settings</h1>
      <p class="text-sm theme-text-muted mt-1">Konfigurasi akun, aturan auto-reply, dan manajemen vector RAG per tenant.</p>
    </div>

    <div class="card p-6 space-y-4">
      <div class="flex items-center justify-between pb-4 divider">
        <div>
          <h2 class="text-sm font-bold uppercase tracking-wide">Koneksi Akun Threads</h2>
          <p class="text-xs theme-text-muted mt-0.5">Status tautan OAuth Meta Threads API.</p>
        </div>
        <span
          class="px-2.5 py-1 text-[10px] font-bold uppercase tracking-wider rounded-md border"
          :class="accountConnected ? 'border theme-text' : 'border theme-text-muted'"
        >
          <span class="inline-block w-1.5 h-1.5 rounded-full mr-1.5" :style="{ background: accountConnected ? 'var(--success)' : 'var(--text-muted)' }"></span>
          {{ accountConnected ? 'Tersambung' : 'Belum Terhubung' }}
        </span>
      </div>

      <div class="flex items-center justify-between text-xs pt-1 gap-4">
        <div>
          <p class="font-bold">{{ accountUsername ? '@' + accountUsername : 'Tidak Ada Akun Aktif' }}</p>
          <p class="theme-text-muted text-[11px] mt-0.5">{{ accountConnected ? 'Sistem siap mempublikasikan postingan dan membaca interaksi.' : 'Hubungkan akun Threads kamu untuk mulai automasi.' }}</p>
        </div>
        <button @click="connectThreads" class="btn btn-primary btn-sm shrink-0">
          {{ accountConnected ? 'Hubungkan Ulang' : 'Hubungkan Threads' }}
        </button>
      </div>
    </div>

    <div class="card p-6 space-y-4">
      <div class="flex items-center justify-between pb-4 divider">
        <div>
          <h2 class="text-sm font-bold uppercase tracking-wide">Pengaturan Gemini AI Auto-Reply</h2>
          <p class="text-xs theme-text-muted mt-0.5">Atur aturan operasional dan gaya bahasa balasan komentar.</p>
        </div>
        <label class="relative inline-flex items-center cursor-pointer">
          <input type="checkbox" v-model="autoReply.enabled" class="sr-only peer">
          <div class="w-11 h-6 rounded-full transition theme-bg-hover peer-checked:theme-accent after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:rounded-full after:h-5 after:w-5 after:transition-all after:theme-bg peer-checked:after:translate-x-full"></div>
        </label>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 pt-1">
        <div class="space-y-1">
          <label class="label">Mode Operasi</label>
          <select v-model="autoReply.mode" class="input">
            <option value="review">Review Queue (Setujui manual dulu)</option>
            <option value="auto">Fully Automatic (Langsung respon)</option>
          </select>
        </div>

        <div class="space-y-1">
          <label class="label">Batas Maksimal / Jam</label>
          <input v-model.number="autoReply.max_per_hour" type="number" class="input" />
        </div>
      </div>

      <div class="space-y-1">
        <label class="label">Tone dan Instruksi AI (Prompt)</label>
        <textarea
          v-model="autoReply.tone_prompt"
          rows="3"
          placeholder="Contoh: Balas dengan ramah, profesional, ringkas, dan tanpa menggurui..."
          class="textarea"
        ></textarea>
      </div>

      <div class="flex justify-end pt-2">
        <button @click="saveAutoReplySettings" :disabled="isSavingSettings" class="btn btn-primary btn-sm">
          <span v-if="isSavingSettings" class="w-3 h-3 border-2 border-current border-t-transparent rounded-full animate-spin"></span>
          <span>{{ isSavingSettings ? 'Menyimpan...' : 'Simpan Pengaturan' }}</span>
        </button>
      </div>
    </div>

    <div class="card p-6 space-y-4">
      <div class="flex items-center justify-between pb-4 divider">
        <div>
          <h2 class="text-sm font-bold uppercase tracking-wide">Vector RAG Knowledge Base</h2>
          <p class="text-xs theme-text-muted mt-0.5">Semakin detail dokumen ini, semakin akurat AI memahami konteks bisnismu.</p>
        </div>
        <span class="badge badge-default">pgvector / 768d</span>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="space-y-1">
          <label class="label">Kategori</label>
          <select v-model="ragForm.category" class="input">
            <option value="portfolio">Portfolio / Project</option>
            <option value="persona">Persona dan Tone Rules</option>
            <option value="rules">Aturan Konten</option>
            <option value="faq">FAQ / Informasi Umum</option>
          </select>
        </div>

        <div class="md:col-span-2 space-y-1">
          <label class="label">Judul Dokumen</label>
          <input
            v-model="ragForm.title"
            type="text"
            placeholder="Contoh: Customer Churn Prediction / Aturan Personal Branding"
            class="input"
          />
        </div>
      </div>

      <div class="space-y-1">
        <label class="label">Isi Teks Dokumen (Fakta Bisnis / Detail Teknis)</label>
        <textarea
          v-model="ragForm.content"
          rows="5"
          placeholder="Tuliskan fakta spesifik, angka eksperimen, rincian produk, atau aturan yang wajib diingat AI..."
          class="textarea"
        ></textarea>
      </div>

      <div class="flex justify-end pt-2">
        <button
          @click="saveKnowledge"
          :disabled="isSavingRag || !ragForm.title || !ragForm.content"
          class="btn btn-primary btn-sm"
        >
          <span v-if="isSavingRag" class="w-3 h-3 border-2 border-current border-t-transparent rounded-full animate-spin"></span>
          <span>{{ isSavingRag ? 'Memproses Vector...' : 'Tambah ke Vector Database' }}</span>
        </button>
      </div>
    </div>

    <div class="card overflow-hidden">
      <div class="p-5 divider flex justify-between items-center theme-bg-sec">
        <div class="flex items-center gap-2">
          <span class="text-xs font-bold uppercase tracking-wide">Indeks Dokumen Knowledge Base</span>
          <span class="badge badge-default">{{ ragItems.length }} Item</span>
        </div>
        <button @click="fetchKnowledge" class="text-xs font-bold theme-text hover:underline">Refresh</button>
      </div>

      <div v-if="loadingRag" class="p-8 text-center text-xs theme-text-muted font-medium animate-pulse">Memuat indeks RAG...</div>

      <div v-else-if="ragItems.length === 0" class="p-8 text-center text-xs theme-text-muted font-medium">
        Belum ada dokumen RAG tersimpan. Tambahkan fakta atau persona pertama kamu di atas.
      </div>

      <div v-else class="list-divided">
        <div v-for="item in ragItems" :key="item.id" class="p-5 transition space-y-2 theme-bg-hover" style="background: transparent;">
          <div class="flex items-center justify-between gap-2">
            <div class="flex items-center gap-2 flex-wrap">
              <span class="badge badge-default">{{ item.category }}</span>
              <h3 class="text-xs font-bold">{{ item.title }}</h3>
              <span v-if="item.embedding" class="badge badge-default">Indexed</span>
            </div>
            <button
              @click="confirmDeleteKnowledge(item.id, item.title)"
              class="text-xs font-bold theme-text-muted hover:theme-text transition shrink-0"
            >
              Hapus
            </button>
          </div>
          <p class="text-xs theme-text-sec whitespace-pre-wrap leading-relaxed p-3 rounded-xl theme-bg-sec border theme-border">
            {{ item.content }}
          </p>
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

const accountConnected = ref(false)
const accountUsername = ref('')
const accountId = ref<string | null>(null)

const autoReply = ref({
  enabled: true,
  mode: 'review',
  max_per_hour: 10,
  tone_prompt: ''
})

const isSavingSettings = ref(false)
const isSavingRag = ref(false)
const loadingRag = ref(true)
const ragItems = ref<any[]>([])

const ragForm = ref({
  category: 'portfolio',
  title: '',
  content: ''
})

async function initAccountAndSettings() {
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) return

  const { data: account } = await supabase
    .schema('threads')
    .from('threads_accounts')
    .select('*')
    .eq('user_id', user.id)
    .maybeSingle()

  if (account) {
    accountId.value = account.id
    accountConnected.value = account.connection_status === 'connected'
    accountUsername.value = account.username || ''

    const { data: settings } = await supabase
      .schema('threads')
      .from('auto_reply_settings')
      .select('*')
      .eq('account_id', account.id)
      .maybeSingle()

    if (settings) {
      autoReply.value.enabled = settings.enabled ?? true
      autoReply.value.mode = settings.mode || 'review'
      autoReply.value.max_per_hour = settings.max_per_hour || 10
      autoReply.value.tone_prompt = settings.tone_prompt || ''
    }
  } else {
    accountId.value = null
    accountConnected.value = false
    accountUsername.value = ''
  }
}

async function connectThreads() {
  try {
    const { data, error } = await supabase.functions.invoke('threads-oauth-start')
    if (error) throw error
    if (data?.error) throw new Error(data.error)
    if (data?.url) {
      window.location.href = data.url
    }
  } catch (err: any) {
    showToast('Gagal memuat URL OAuth: ' + err.message, 'error')
  }
}

async function saveAutoReplySettings() {
  if (!accountId.value) return showToast('Hubungkan akun Threads terlebih dahulu.', 'error')
  isSavingSettings.value = true
  try {
    const { error } = await supabase
      .schema('threads')
      .from('auto_reply_settings')
      .upsert({
        account_id: accountId.value,
        enabled: autoReply.value.enabled,
        mode: autoReply.value.mode,
        max_per_hour: autoReply.value.max_per_hour,
        tone_prompt: autoReply.value.tone_prompt
      })

    if (error) throw error
    showToast('Pengaturan Auto Reply berhasil disimpan!', 'success')
  } catch (err: any) {
    showToast('Gagal menyimpan pengaturan: ' + err.message, 'error')
  } finally {
    isSavingSettings.value = false
  }
}

async function fetchKnowledge() {
  loadingRag.value = true
  if (!accountId.value) await initAccountAndSettings()
  if (!accountId.value) {
    loadingRag.value = false
    return
  }

  const { data, error } = await supabase
    .schema('threads')
    .from('brand_knowledge')
    .select('*')
    .eq('account_id', accountId.value)
    .order('created_at', { ascending: false })

  if (data && !error) {
    ragItems.value = data
  }
  loadingRag.value = false
}

async function saveKnowledge() {
  if (!ragForm.value.title || !ragForm.value.content) return showToast('Isi judul dan konten pengetahuan.', 'error')
  if (!accountId.value) return showToast('Akun Threads belum tersambung.', 'error')

  isSavingRag.value = true
  try {
    const response = await fetch('https://threads-automation-production-53ad.up.railway.app/api/v1/rag/embed', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        account_id: accountId.value,
        title: ragForm.value.title,
        content: ragForm.value.content,
        category: ragForm.value.category
      })
    })

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || 'Gagal memproses embedding di server')
    }

    ragForm.value.title = ''
    ragForm.value.content = ''
    showToast('Dokumen berhasil ditambahkan dan di-indexing ke Vector DB!', 'success')
    await fetchKnowledge()
  } catch (err: any) {
    showToast('Gagal menyimpan RAG: ' + err.message, 'error')
  } finally {
    isSavingRag.value = false
  }
}

function confirmDeleteKnowledge(id: string, title: string) {
  askConfirm({
    title: 'Hapus Dokumen RAG',
    message: `Apakah kamu yakin ingin menghapus "${title}" dari Vector Database?`,
    confirmText: 'Hapus Dokumen',
    onConfirm: () => deleteKnowledge(id)
  })
}

async function deleteKnowledge(id: string) {
  try {
    const { error } = await supabase
      .schema('threads')
      .from('brand_knowledge')
      .delete()
      .eq('id', id)

    if (error) throw error
    showToast('Dokumen pengetahuan berhasil dihapus.', 'info')
    await fetchKnowledge()
  } catch (err: any) {
    showToast('Gagal menghapus: ' + err.message, 'error')
  }
}

onMounted(async () => {
  await initAccountAndSettings()
  fetchKnowledge()
})
</script>
