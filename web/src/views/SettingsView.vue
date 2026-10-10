<template>
  <div class="space-y-8 max-w-5xl">
    <div>
      <h1 class="text-2xl font-bold text-slate-900 tracking-tight">Settings & RAG Knowledge Base</h1>
      <p class="text-slate-500 text-sm mt-1">Kelola instruksi persona, fakta portofolio, dan pengetahuan AI untuk penjadwalan & auto-reply.</p>
    </div>

    <!-- Section 1: Form Tambah Pengetahuan / RAG Context -->
    <div class="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-4">
      <div class="flex items-center justify-between border-b border-slate-100 pb-4">
        <div>
          <h2 class="text-sm font-bold text-slate-900 uppercase tracking-wide">Tambah Pengetahuan RAG Baru</h2>
          <p class="text-xs text-slate-500 mt-0.5">Dokumen ini otomatis dibaca Gemini saat membuat draf post atau membalas komentar.</p>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="space-y-1">
          <label class="text-[11px] font-bold text-slate-700 uppercase">Kategori</label>
          <select
            v-model="form.category"
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
            v-model="form.title"
            type="text"
            placeholder="Contoh: Customer Churn Prediction / Aturan Gaya Bahasa"
            class="w-full bg-slate-50 border border-slate-200 rounded-xl p-3 text-xs text-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition"
          />
        </div>
      </div>

      <div class="space-y-1">
        <label class="text-[11px] font-bold text-slate-700 uppercase">Isi Detail / Konten Fakta</label>
        <textarea
          v-model="form.content"
          rows="4"
          placeholder="Tulis fakta teknis, instruksi spesifik, angka hasil eksperimen, atau aturan yang wajib diikuti AI..."
          class="w-full bg-slate-50 border border-slate-200 rounded-xl p-3 text-xs text-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition resize-none"
        ></textarea>
      </div>

      <div class="flex justify-end pt-2">
        <button
          @click="saveKnowledge"
          :disabled="isSaving || !form.title || !form.content"
          class="bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold py-2.5 px-6 rounded-xl transition shadow-md disabled:opacity-50"
        >
          {{ isSaving ? 'Memproses...' : 'Simpan ke Knowledge Base' }}
        </button>
      </div>
    </div>

    <!-- Section 2: Daftar Dokumen RAG Tersimpan -->
    <div class="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">
      <div class="p-5 border-b border-slate-100 bg-slate-50 flex justify-between items-center">
        <div class="flex items-center gap-2">
          <span class="text-xs font-bold text-slate-700 uppercase tracking-wide">Daftar Dokumen RAG</span>
          <span class="text-xs font-bold bg-indigo-50 text-indigo-700 px-2 py-0.5 rounded-full">{{ items.length }} Item</span>
        </div>
        <button @click="fetchKnowledge" class="text-xs font-bold text-indigo-600 hover:text-indigo-800">Refresh</button>
      </div>

      <div v-if="loading" class="p-8 text-center text-xs text-slate-400 font-medium animate-pulse">Memuat data RAG...</div>

      <div v-else-if="items.length === 0" class="p-8 text-center text-xs text-slate-400 font-medium">
        Belum ada dokumen RAG tersimpan. Tambahkan fakta/persona pertama kamu di atas.
      </div>

      <div v-else class="divide-y divide-slate-100">
        <div v-for="item in items" :key="item.id" class="p-5 hover:bg-slate-50/80 transition space-y-2">
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
            </div>
            <button
              @click="deleteKnowledge(item.id)"
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

const loading = ref(true)
const isSaving = ref(false)
const items = ref<any[]>([])
const accountId = ref<string | null>(null)

const form = ref({
  category: 'portfolio',
  title: '',
  content: ''
})

async function getAccountId() {
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) return null

  const { data: account } = await supabase
    .schema('threads')
    .from('threads_accounts')
    .select('id')
    .limit(1)
    .maybeSingle()

  if (account) {
    accountId.value = account.id
  }
  return accountId.value
}

async function fetchKnowledge() {
  loading.value = true
  const accId = accountId.value || await getAccountId()
  if (!accId) {
    loading.value = false
    return
  }

  const { data, error } = await supabase
    .schema('threads')
    .from('brand_knowledge')
    .select('*')
    .eq('account_id', accId)
    .order('created_at', { ascending: false })

  if (data && !error) {
    items.value = data
  }
  loading.value = false
}

async function saveKnowledge() {
  if (!form.value.title || !form.value.content) return alert('Isi judul dan konten pengetahuan.')
  
  const accId = accountId.value || await getAccountId()
  if (!accId) return alert('Akun Threads belum tersambung. Sambungkan di dashboard dulu.')

  isSaving.value = true
  try {
    const { error } = await supabase
      .schema('threads')
      .from('brand_knowledge')
      .insert({
        account_id: accId,
        category: form.value.category,
        title: form.value.title,
        content: form.value.content
      })

    if (error) throw error

    form.value.title = ''
    form.value.content = ''
    await fetchKnowledge()
  } catch (err: any) {
    alert('Gagal simpan RAG: ' + err.message)
  } finally {
    isSaving.value = false
  }
}

async function deleteKnowledge(id: string) {
  if (!confirm('Hapus dokumen pengetahuan ini dari RAG?')) return
  try {
    const { error } = await supabase
      .schema('threads')
      .from('brand_knowledge')
      .delete()
      .eq('id', id)

    if (error) throw error
    await fetchKnowledge()
  } catch (err: any) {
    alert('Gagal hapus: ' + err.message)
  }
}

onMounted(() => {
  fetchKnowledge()
})
</script>
