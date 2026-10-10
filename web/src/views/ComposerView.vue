<template>
  <div class="max-w-5xl mx-auto space-y-8">
    <div>
      <h1 class="text-2xl font-bold text-white tracking-tight">Composer & Scheduler</h1>
      <p class="text-zinc-400 text-sm mt-1">Buat, evaluasi skor keterlibatan konten, dan jadwalkan postingan ke Threads.</p>
    </div>

    <!-- Banner Peringatan jika Belum Konek Akun -->
    <div v-if="!activeAccountId && !loadingAccount" class="bg-zinc-900 border border-amber-500/30 p-4 rounded-xl flex items-center justify-between">
      <div class="text-xs text-amber-200">
        <span class="font-bold">Akun Threads Belum Terhubung:</span> Silakan hubungkan akun Threads kamu di halaman Settings untuk mulai menjadwalkan postingan.
      </div>
      <RouterLink to="/settings" class="bg-white text-black text-xs font-bold px-3 py-1.5 rounded hover:bg-zinc-200 transition">
        Ke Settings
      </RouterLink>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Editor Column (2/3) -->
      <div class="lg:col-span-2 space-y-6">
        <div class="bg-zinc-950/80 backdrop-blur-xl border border-white/10 rounded-xl p-6 shadow-2xl space-y-4">
          <div class="flex items-center justify-between">
            <label class="text-xs font-semibold text-zinc-300 uppercase tracking-wider">Teks Postingan Threads</label>
            <span :class="['text-xs font-mono', textLength > 500 ? 'text-rose-400 font-bold' : 'text-zinc-500']">
              {{ textLength }} / 500
            </span>
          </div>

          <textarea
            v-model="postText"
            rows="6"
            placeholder="Apa yang menarik hari ini? Tulis pemikiran, diskusi, atau pertanyaan..."
            class="w-full bg-black border border-white/10 rounded-lg p-4 text-white placeholder-zinc-600 focus:outline-none focus:border-white text-sm resize-none transition"
          ></textarea>

          <div class="flex flex-wrap items-center justify-between gap-4 pt-2">
            <button
              @click="handleScore"
              :disabled="!postText.trim() || composerStore.scoring"
              class="inline-flex items-center gap-2 bg-zinc-900 hover:bg-zinc-800 text-white text-xs font-medium px-4 py-2.5 rounded-lg border border-white/10 transition disabled:opacity-40"
            >
              <svg v-if="composerStore.scoring" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
              <span>{{ composerStore.scoring ? 'Menganalisis...' : 'Cek Skor AI' }}</span>
            </button>

            <div class="flex items-center gap-3">
              <input
                type="datetime-local"
                v-model="scheduledTime"
                class="bg-black border border-white/10 text-zinc-300 text-xs rounded-lg px-3 py-2 focus:outline-none focus:border-white"
              />
              <button
                @click="handleSchedule"
                :disabled="!postText.trim() || textLength > 500 || !scheduledTime || composerStore.loading || !activeAccountId"
                class="bg-white hover:bg-zinc-200 text-black text-xs font-semibold px-5 py-2.5 rounded-lg transition disabled:opacity-40"
              >
                {{ composerStore.loading ? 'Menyimpan...' : 'Jadwalkan' }}
              </button>
            </div>
          </div>
        </div>

        <!-- Scheduled Queue List -->
        <div class="bg-zinc-950/80 backdrop-blur-xl border border-white/10 rounded-xl p-6 shadow-2xl space-y-4">
          <h2 class="text-sm font-semibold text-white uppercase tracking-wider">Antrean Postingan Terjadwal</h2>

          <div v-if="composerStore.scheduledPosts.length === 0" class="text-center py-8 text-zinc-600 text-xs border border-dashed border-white/10 rounded-lg">
            Belum ada postingan yang dijadwalkan.
          </div>

          <div v-else class="space-y-3">
            <div
              v-for="item in composerStore.scheduledPosts"
              :key="item.id"
              class="p-4 bg-black border border-white/10 rounded-lg flex items-start justify-between gap-4"
            >
              <div class="space-y-2">
                <p class="text-sm text-zinc-200 whitespace-pre-line line-clamp-2">{{ item.text }}</p>
                <div class="flex items-center gap-3 text-xs text-zinc-500">
                  <span>{{ formatDate(item.scheduled_for) }}</span>
                  <span class="px-2 py-0.5 rounded bg-zinc-900 border border-white/10 text-white uppercase text-[10px] font-mono">
                    {{ item.status }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- AI Score Inspector Column (1/3) -->
      <div class="space-y-6">
        <div class="bg-zinc-950/80 backdrop-blur-xl border border-white/10 rounded-xl p-6 shadow-2xl space-y-4">
          <h2 class="text-sm font-semibold text-white uppercase tracking-wider">AI Engagement Score</h2>

          <div v-if="!composerStore.lastScore && !composerStore.scoring" class="text-center py-8 text-zinc-600 text-xs">
            Klik <strong class="text-zinc-400">"Cek Skor AI"</strong> untuk menganalisis potensi viral dan saran hook postingan kamu.
          </div>

          <div v-if="composerStore.scoring" class="py-8 text-center text-zinc-500 text-xs animate-pulse">
            AI sedang menganalisis struktur kalimat, hook, dan keterbacaan...
          </div>

          <div v-if="composerStore.lastScore" class="space-y-4">
            <div class="flex items-center justify-between p-4 bg-black rounded-lg border border-white/10">
              <span class="text-xs text-zinc-400 font-medium">Skor Kualitas</span>
              <span :class="['text-3xl font-extrabold font-mono', getScoreColor(composerStore.lastScore.score)]">
                {{ composerStore.lastScore.score }}/100
              </span>
            </div>

            <div v-if="composerStore.lastScore.suggestions.length > 0" class="space-y-2">
              <span class="text-xs font-semibold text-zinc-300">Saran Perbaikan:</span>
              <ul class="space-y-2">
                <li
                  v-for="(sugg, idx) in composerStore.lastScore.suggestions"
                  :key="idx"
                  class="text-xs text-zinc-300 bg-zinc-900 border border-white/10 p-3 rounded-lg flex items-start gap-2"
                >
                  <span class="text-white font-mono">•</span>
                  <span>{{ sugg }}</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useComposerStore } from '../stores/composer'
import { supabase } from '../lib/supabase'

const composerStore = useComposerStore()

const postText = ref('')
const scheduledTime = ref('')
const activeAccountId = ref<string | null>(null)
const loadingAccount = ref(true)

const textLength = computed(() => postText.value.length)

async function fetchActiveAccount() {
  loadingAccount.value = true
  try {
    // Tarik akun Threads asli yang terhubung di DB
    const { data, error } = await supabase
      .schema('threads')
      .from('threads_accounts')
      .select('id')
      .order('created_at', { ascending: false })
      .limit(1)
      .maybeSingle()

    if (error) throw error

    if (data?.id) {
      activeAccountId.value = data.id
      await composerStore.fetchScheduledPosts(data.id)
    }
  } catch (err) {
    console.error('Failed to resolve active Threads account:', err)
  } finally {
    loadingAccount.value = false
  }
}

function handleScore() {
  composerStore.scoreDraft(postText.value, activeAccountId.value || '')
}

async function handleSchedule() {
  if (!postText.value.trim() || !scheduledTime.value || !activeAccountId.value) return

  const res = await composerStore.createScheduledPost({
    account_id: activeAccountId.value,
    text: postText.value,
    scheduled_for: new Date(scheduledTime.value).toISOString()
  })

  if (res.success) {
    postText.value = ''
    scheduledTime.value = ''
    composerStore.lastScore = null
  }
}

function getScoreColor(score: number) {
  if (score >= 80) return 'text-emerald-400'
  if (score >= 60) return 'text-amber-400'
  return 'text-rose-400'
}

function formatDate(isoStr: string) {
  return new Date(isoStr).toLocaleString('id-ID', {
    dateStyle: 'medium',
    timeStyle: 'short'
  })
}

onMounted(() => {
  const nextHour = new Date(Date.now() + 60 * 60 * 1000)
  scheduledTime.value = nextHour.toISOString().slice(0, 16)
  fetchActiveAccount()
})
</script>
