<template>
  <div class="space-y-8">
    <div>
      <h1 class="text-2xl font-bold text-slate-900 tracking-tight">Composer & Scheduler</h1>
      <p class="text-slate-500 text-sm mt-1">Buat konten, cek skor AI, dan jadwalkan postingan Threads.</p>
    </div>

    <!-- Form Post -->
    <div class="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-4">
      <div class="flex justify-between items-center">
        <span class="text-xs font-bold text-slate-700 tracking-wide uppercase">Teks Postingan</span>
        <span class="text-xs font-medium" :class="postText.length > 450 ? 'text-amber-500' : 'text-slate-400'">{{ postText.length }} / 500</span>
      </div>

      <textarea
        v-model="postText"
        rows="5"
        placeholder="Tulis draf postingan di sini..."
        class="w-full bg-slate-50 border border-slate-200 rounded-xl p-4 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition resize-none"
        maxlength="500"
      ></textarea>

      <div class="flex flex-wrap items-center gap-3 pt-2">
        <button 
          @click="checkScore" 
          :disabled="isChecking || !postText"
          class="bg-indigo-50 hover:bg-indigo-100 text-indigo-700 text-xs font-bold py-2.5 px-4 rounded-lg transition border border-indigo-100 disabled:opacity-50"
        >
          {{ isChecking ? 'Menganalisa...' : 'Cek Skor AI' }}
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
            class="bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold py-2.5 px-6 rounded-lg transition shadow-md disabled:opacity-50"
          >
            {{ isSaving ? 'Memproses...' : 'Jadwalkan' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Antrean -->
    <div class="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">
      <div class="p-5 border-b border-slate-100 bg-slate-50">
        <span class="text-xs font-bold text-slate-700 tracking-wide uppercase">Antrean Terjadwal</span>
      </div>

      <div v-if="loading" class="p-8 text-center text-xs text-slate-400 font-medium animate-pulse">Memuat data...</div>
      
      <div v-else-if="posts.length === 0" class="p-8 text-center text-xs text-slate-400 font-medium">
        Belum ada postingan dalam antrean.
      </div>

      <div v-else class="divide-y divide-slate-100">
        <div v-for="post in posts" :key="post.id" class="p-5 hover:bg-slate-50 transition">
          <p class="text-sm font-medium text-slate-800 mb-3 whitespace-pre-wrap">{{ post.text }}</p>
          <div class="flex items-center justify-between">
            <span class="text-xs text-slate-500 font-medium">{{ formatDate(post.scheduled_for) }}</span>
            <span
              class="px-2.5 py-1 text-[10px] font-bold uppercase tracking-wider rounded-md"
              :class="{
                'bg-amber-50 text-amber-600 border border-amber-100': post.status === 'scheduled',
                'bg-emerald-50 text-emerald-600 border border-emerald-100': post.status === 'published',
                'bg-rose-50 text-rose-600 border border-rose-100': ['error', 'failed', 'quota_exceeded'].includes(post.status)
              }"
            >
              {{ post.status }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { supabase } from '../lib/supabase'

const postText = ref('')
const scheduledDate = ref('')
const isSaving = ref(false)
const isChecking = ref(false)
const loading = ref(true)
const posts = ref<any[]>([])

function formatDate(isoString: string) {
  const d = new Date(isoString)
  return d.toLocaleString('id-ID', { dateStyle: 'medium', timeStyle: 'short' })
}

async function loadPosts() {
  const { data } = await supabase
    .schema('threads')
    .from('scheduled_posts')
    .select('*')
    .order('created_at', { ascending: false })
    .limit(10)
  if (data) posts.value = data
  loading.value = false
}

async function checkScore() {
  isChecking.value = true
  try {
    const { data, error } = await supabase.functions.invoke('score-draft', {
      body: { text: postText.value }
    })
    if (error) throw error
    
    const scoreVal = data?.score ?? data?.result?.score ?? 'N/A'
    const feedbackVal = data?.feedback ?? data?.result?.feedback ?? data?.message ?? 'Tidak ada catatan.'
    
    alert(`Skor AI: ${scoreVal}/100\n\nCatatan:\n${feedbackVal}`)
  } catch (err: any) {
    alert('Gagal analisa AI: ' + err.message)
  } finally {
    isChecking.value = false
  }
}

async function schedulePost() {
  if (!postText.value || !scheduledDate.value) return alert('Isi teks dan tanggal dulu.')
  isSaving.value = true
  
  try {
    const { data: accounts, error: accErr } = await supabase
      .schema('threads')
      .from('threads_accounts')
      .select('id')
      .limit(1)
      .maybeSingle()
      
    if (accErr) throw new Error(accErr.message)
    if (!accounts) throw new Error('Akun Threads belum tersambung. Hubungkan di Settings.')

    const isoDate = new Date(scheduledDate.value).toISOString()

    // Menggunakan account_id sesuai nama kolom di database
    const { error } = await supabase
      .schema('threads')
      .from('scheduled_posts')
      .insert({
        account_id: accounts.id,
        text: postText.value,
        scheduled_for: isoDate,
        status: 'scheduled'
      })

    if (error) throw error
    postText.value = ''
    
    const d = new Date()
    d.setHours(d.getHours() + 1)
    d.setMinutes(d.getMinutes() - d.getTimezoneOffset())
    scheduledDate.value = d.toISOString().slice(0, 16)
    
    await loadPosts()
  } catch (err: any) {
    alert('Gagal simpan: ' + err.message)
  } finally {
    isSaving.value = false
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
