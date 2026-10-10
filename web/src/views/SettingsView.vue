<template>
  <div class="space-y-8 max-w-5xl relative">
    <NotifyOverlay />

    <div>
      <h1 class="text-2xl font-bold text-slate-900 tracking-tight">Settings & RAG Knowledge Base</h1>
      <p class="text-slate-500 text-sm mt-1">Konfigurasi akun, aturan auto-reply, dan manajemen vector RAG per tenant.</p>
    </div>

    <!-- CARD 1: Connection Status -->
    <div class="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-4">
      <div class="flex items-center justify-between border-b border-slate-100 pb-4">
        <div>
          <h2 class="text-sm font-bold text-slate-900 uppercase tracking-wide">Koneksi Akun Threads</h2>
          <p class="text-xs text-slate-500 mt-0.5">Status tautan OAuth Meta Threads API.</p>
        </div>
        <span 
          class="px-2.5 py-1 text-[10px] font-bold uppercase tracking-wider rounded-md"
          :class="accountConnected ? 'bg-emerald-50 text-emerald-600 border border-emerald-100' : 'bg-amber-50 text-amber-600 border border-amber-100'"
        >
          {{ accountConnected ? 'Tersambung' : 'Belum Terhubung' }}
        </span>
      </div>

      <div class="flex items-center justify-between text-xs pt-1">
        <div>
          <p class="font-bold text-slate-800">{{ accountUsername ? `@${accountUsername}` : 'Tidak Ada Akun Aktif' }}</p>
          <p class="text-slate-500 text-[11px] mt-0.5">{{ accountConnected ? 'Sistem siap mempublikasikan postingan dan membaca interaksi.' : 'Hubungkan akun Threads kamu untuk mulai automasi.' }}</p>
        </div>
        <button 
          @click="connectThreads" 
          class="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded-lg transition shadow-sm text-xs"
        >
          {{ accountConnected ? 'Hubungkan Ulang' : 'Hubungkan Threads' }}
        </button>
      </div>
    </div>

    <!-- CARD 2: Auto Reply Operational Settings -->
    <div class="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-4">
      <div class="flex items-center justify-between border-b border-slate-100 pb-4">
        <div>
          <h2 class="text-sm font-bold text-slate-900 uppercase tracking-wide">Pengaturan Gemini AI Auto-Reply</h2>
          <p class="text-xs text-slate-500 mt-0.5">Atur aturan operasional dan gaya bahasa balasan komentar.</p>
        </div>
        <label class="relative inline-flex items-center cursor-pointer">
          <input type="checkbox" v-model="autoReply.enabled" class="sr-only peer">
          <div class="w-11 h-6 bg-slate-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600"></div>
        </label>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 pt-1">
        <div class="space-y-1">
          <label class="text-[11px] font-bold text-slate-700 uppercase">Mode Operasi</label>
          <select
            v-model="autoReply.mode"
            class="w-full bg-slate-50 border border-slate-200 rounded-xl p-3 text-xs text-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition"
          >
            <option value="review">Review Queue (Setujui manual dulu)</option>
            <option value="auto">Fully Automatic (Langsung respon)</option>
          </select>
        </div>

        <div class="space-y-1">
          <label class="text-[11px] font-bold text-slate-700 uppercase">Batas Maksimal / Jam</label>
          <input
            v-model.number="autoReply.max_per_hour"
            type="number"
            class="w-full bg-slate-50 border border-slate-200 rounded-xl p-3 text-xs text-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition"
          />
        </div>
      </div>

      <div class="space-y-1">
        <label class="text-[11px] font-bold text-slate-700 uppercase">Tone & Instruksi AI (Prompt)</label>
        <textarea
          v-model="autoReply.tone_prompt"
          rows="3"
          placeholder="Contoh: Balas dengan ramah, profesional, ringkas, dan tanpa menggurui..."
          class="w-full bg-slate-50 border border-slate-200 rounded-xl p-3 text-xs text-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition resize-none"
        ></textarea>
      </div>

      <div class="flex justify-end pt-2">
        <button
          @click="saveAutoReplySettings"
          :disabled="isSavingSettings"
          class="bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold py-2.5 px-6 rounded-xl transition shadow-md disabled:opacity-50 flex items-center gap-2"
        >
          <span v-if="isSavingSettings" class="w-3 h-3 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
          <span>{{ isSavingSettings ? 'Menyimpan...' : 'Simpan Pengaturan' }}</span>
        </button>
      </div>
    </div>

    <!-- CARD 3: Dedicated RAG Knowledge Base Management -->
    <div class="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-4">
      <div class="flex items-center justify-between border-b border-slate-100 pb-4">
        <div>
          <h2 class="text-sm font-bold text-slate-900 uppercase tracking-wide">Vector RAG Knowledge Base</h2>
          <p class="text-xs text-slate-500 mt-0.5">Semakin detail dokumen ini, semakin akurat AI dalam memahami konteks bisnismu.</p>
        </div>
        <span class="text-[10px] font-bold bg-indigo-50 text-indigo-700 border border-indigo-100 px-2.5 py-1 rounded-md uppercase">
          pgvector + embedding-004
        </span>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="space-y-1">
          <label class="text-[11px] font-bold text-slate-700 uppercase">Kategori</label>
          <select
            v-model="ragForm.category"
            class="w-full bg-slate-50 border border-slate-200 rounded-xl p-3 text-xs text-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition"
          >
            <option value="portfolio">Portfolio / Project</option>
            <option value="persona">Persona & Tone Rules</option>
            <option value="rules">Aturan Konten</option>
            <option value="faq">FAQ / Informasi Umum</option>
          </select>
        </div>

        <div class="md:col-span-2 space-y-1">
          <label class="text-[11px] font-bold text-slate-700 uppercase">Judul Dokumen</label>
          <input
            v-model="ragForm.title"
            type="text"
            placeholder="Contoh: Customer Churn Prediction / Aturan Personal Branding"
            class="w-full bg-slate-50 border border-slate-200 rounded-xl p-3 text-xs text-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition"
          />
        </div>
      </div>

      <div class="space-y-1">
        <label class="text-[11px] font-bold text-slate-700 uppercase">Isi Teks Dokumen (Fakta Bisnis / Detail Teknis)</label>
        <textarea
          v-model="ragForm.content"
          rows="5"
          placeholder="Tuliskan fakta spesifik, angka eksperimen, rincian produk, atau aturan yang wajib diingat AI..."
          class="w-full bg-slate-50 border border-slate-200 rounded-xl p-3 text-xs text-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition resize-none"
        ></textarea>
      </div>

      <div class="flex justify-end pt-2">
        <button
          @click="saveKnowledge"
          :disabled="isSavingRag || !ragForm.title || !ragForm.content"
          class="bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold py-2.5 px-6 rounded-xl transition shadow-md disabled:opacity-50 flex items-center gap-2"
        >
          <span v-if="isSavingRag" class="w-3 h-3 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
          <span>{{ isSavingRag ? 'Memproses Vector...' : 'Tambah ke Vector Database' }}</span>
        </button>
      </div>
    </div>

    <!-- CARD 4: Index List Dokumen RAG -->
    <div class="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">
      <div class="p-5 border-b border-slate-100 bg-slate-50 flex justify-between items-center">
        <div class="flex items-center gap-2">
          <span class="text-xs font-bold text-slate-700 uppercase tracking-wide">Indeks Dokumen Knowledge Base</span>
          <span class="text-xs font-bold bg-indigo-50 text-indigo-700 px-2 py-0.5 rounded-full">{{ ragItems.length }} Item</span>
        </div>
        <button @click="fetchKnowledge" class="text-xs font-bold text-indigo-600 hover:text-indigo-800">Refresh</button>
      </div>

      <div v-if="loadingRag" class="p-8 text-center text-xs text-slate-400 font-medium animate-pulse">Memuat indeks RAG...</div>

      <div v-else-if="ragItems.length === 0" class="p-8 text-center text-xs text-slate-400 font-medium">
        Belum ada dokumen RAG tersimpan. Tambahkan fakta/persona pertama kamu di atas.
      </div>

      <div v-else class="divide-y divide-slate-100">
        <div v-for="item in ragItems" :key="item.id" class="p-5 hover:bg-slate-50/80 transition space-y-2">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <span
                class="px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider rounded"
                :class="{
                  'bg-purple-50 text-purple-700 border border-purple-100': item.category === 'portfolio',
                  'bg-indigo-50 text-indigo-700 border border-indigo-100': item.category === 'persona',
                  'bg-amber-50 text-amber-700 border border-amber-100': item.category === 'rules',
                  'bg-emerald-50 text-emerald-700 border border-emerald-100': item.category === 'faq'
                }"
              >
                {{ item.category }}
              </span>
              <h3 class="text-xs font-bold text-slate-900">{{ item.title }}</h3>
              <span v-if="item.embedding" class="text-[9px] font-bold bg-emerald-50 text-emerald-600 border border-emerald-100 px-1.5 py-0.5 rounded">
                Indexed (768d)
              </span>
            </div>
            <button
              @click="confirmDeleteKnowledge(item.id, item.title)"
              class="text-xs font-bold text-rose-600 hover:text-rose-800 transition"
            >
              Hapus
            </button>
          </div>
          <p class="text-xs text-slate-600 whitespace-pre-wrap leading-relaxed bg-slate-50/50 p-3 rounded-xl border border-slate-100">
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
  const { data: account } = await supabase
    .schema('threads')
    .from('threads_accounts')
    .select('*')
    .limit(1)
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
  }
}

function connectThreads() {
  showToast('Gunakan link pendaftaran OAuth Threads untuk menghubungkan akun.', 'info')
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
    const { data: inserted, error } = await supabase
      .schema('threads')
      .from('brand_knowledge')
      .insert({
        account_id: accountId.value,
        category: ragForm.value.category,
        title: ragForm.value.title,
        content: ragForm.value.content
      })
      .select('id')
      .single()

    if (error) throw error

    if (inserted?.id) {
      await supabase.functions.invoke('embed-knowledge', {
        body: { id: inserted.id, content: ragForm.value.content }
      })
    }

    ragForm.value.title = ''
    ragForm.value.content = ''
    showToast('Dokumen berhasil ditambahkan & di-indexing ke Vector DB!', 'success')
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
