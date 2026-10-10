<template>
  <div class="space-y-8">
    <div>
      <h1 class="text-2xl font-bold text-zinc-900 tracking-tight">Composer & Scheduler</h1>
      <p class="text-zinc-500 text-sm mt-1">Buat, evaluasi skor keterlibatan konten, dan jadwalkan postingan ke Threads.</p>
    </div>

    <!-- Form Bikin Post -->
    <div class="bg-white border border-zinc-200 rounded-2xl p-6 shadow-sm space-y-4">
      <div class="flex justify-between items-center">
        <span class="text-xs font-bold text-zinc-700 tracking-wide uppercase">Teks Postingan Threads</span>
        <span class="text-xs font-medium text-zinc-400">{{ postText.length }} / 500</span>
      </div>
      
      <textarea
        v-model="postText"
        rows="5"
        placeholder="Apa yang menarik hari ini? Tulis pemikiran, diskusi, atau pertanyaan..."
        class="w-full bg-zinc-50 border border-zinc-200 rounded-xl p-4 text-sm text-zinc-900 focus:outline-none focus:ring-2 focus:ring-black focus:bg-white transition resize-none"
        maxlength="500"
      ></textarea>

      <div class="flex flex-wrap items-center gap-3 pt-2">
        <button class="bg-zinc-100 hover:bg-zinc-200 text-zinc-700 text-xs font-bold py-2.5 px-4 rounded-lg transition border border-zinc-200">
          Cek Skor AI
        </button>
        
        <div class="flex-1 flex justify-end items-center gap-3">
          <input 
            v-model="scheduledDate" 
            type="datetime-local" 
            class="bg-zinc-50 border border-zinc-200 rounded-lg p-2.5 text-xs text-zinc-700 focus:outline-none focus:border-black transition"
          />
          <button 
            @click="schedulePost" 
            :disabled="!postText || isSaving"
            class="bg-black hover:bg-zinc-800 text-white text-xs font-bold py-2.5 px-6 rounded-lg transition shadow-md disabled:opacity-50"
          >
            {{ isSaving ? 'Menjadwalkan...' : 'Jadwalkan' }}
          </button>
        </div>
      </div>
    </div>

    <!-- List Antrean -->
    <div class="bg-white border border-zinc-200 rounded-2xl shadow-sm overflow-hidden">
      <div class="p-5 border-b border-zinc-100 bg-zinc-50/50">
        <span class="text-xs font-bold text-zinc-700 tracking-wide uppercase">Antrean Postingan Terjadwal</span>
      </div>
      
      <div v-if="loading" class="p-8 text-center text-xs text-zinc-400 font-medium">Memuat antrean...</div>
      
      <div v-else-if="posts.length === 0" class="p-8 text-center text-xs text-zinc-400 font-medium">
        Belum ada postingan yang dijadwalkan.
      </div>

      <div v-else class="divide-y divide-zinc-100">
        <div v-for="post in posts" :key="post.id" class="p-5 hover:bg-zinc-50 transition">
          <p class="text-sm font-medium text-zinc-900 mb-3 whitespace-pre-wrap">{{ post.text }}</p>
          <div class="flex items-center justify-between">
            <span class="text-xs text-zinc-500 font-medium">{{ formatDate(post.scheduled_for) }}</span>
            <span 
              class="px-2.5 py-1 text-[10px] font-bold uppercase tracking-wider rounded-md"
              :class="{
                'bg-zinc-100 text-zinc-600': post.status === 'scheduled',
                'bg-emerald-50 text-emerald-600 border border-emerald-200': post.status === 'published',
                'bg-rose-50 text-rose-600 border border-rose-200': ['error', 'failed'].includes(post.status)
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
const loading = ref(true)
const posts = ref<any[]>([])

function formatDate(isoString: string) {
  const d = new Date(isoString)
  return d.toLocaleString('id-ID', { dateStyle: 'medium', timeStyle: 'short' })
}

async function loadPosts() {
  const { data } = await supabase
    .from('scheduled_posts')
    .select('*')
    .order('created_at', { ascending: false })
    .limit(10)
  if (data) posts.value = data
  loading.value = false
}

async function schedulePost() {
  if (!postText.value || !scheduledDate.value) return alert('Isi teks dan pilih tanggal dulu.')
  isSaving.value = true
  
  try {
    const { data: accounts } = await supabase.from('threads_accounts').select('id').single()
    if (!accounts) throw new Error('Akun Threads belum tersambung. Hubungkan di Settings.')

    // Ubah local time ke UTC ISO string agar akurat
    const isoDate = new Date(scheduledDate.value).toISOString()

    const { error } = await supabase.from('scheduled_posts').insert({
      threads_account_id: accounts.id,
      text: postText.value,
      scheduled_for: isoDate,
      status: 'scheduled'
    })

    if (error) throw error
    postText.value = ''
    scheduledDate.value = ''
    await loadPosts()
  } catch (err: any) {
    alert(err.message)
  } finally {
    isSaving.value = false
  }
}

onMounted(() => {
  // Set default ke 1 jam ke depan
  const d = new Date()
  d.setHours(d.getHours() + 1)
  d.setMinutes(d.getMinutes() - d.getTimezoneOffset())
  scheduledDate.value = d.toISOString().slice(0, 16)
  loadPosts()
})
</script>
