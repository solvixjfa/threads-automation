<template>
  <div class="max-w-5xl mx-auto space-y-8">
    <div>
      <h1 class="text-2xl font-bold text-slate-100">Composer & Scheduler</h1>
      <p class="text-slate-400 text-sm mt-1">Buat, evaluasi skor keterlibatan konten, dan jadwalkan postingan ke Threads.</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Editor Column (2/3) -->
      <div class="lg:col-span-2 space-y-6">
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-4">
          <div class="flex items-center justify-between">
            <label class="text-sm font-medium text-slate-300">Teks Postingan Threads</label>
            <span :class="['text-xs font-mono', textLength > 500 ? 'text-red-400 font-bold' : 'text-slate-400']">
              {{ textLength }} / 500
            </span>
          </div>

          <textarea
            v-model="postText"
            rows="6"
            placeholder="Apa yang menarik hari ini? Tulis pemikiran, diskusi, atau pertanyaan..."
            class="w-full bg-slate-950 border border-slate-800 rounded-lg p-4 text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 text-sm resize-none"
          ></textarea>

          <div class="flex flex-wrap items-center justify-between gap-4 pt-2">
            <button
              @click="handleScore"
              :disabled="!postText.trim() || composerStore.scoring"
              class="inline-flex items-center gap-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-sm font-medium px-4 py-2 rounded-lg border border-slate-700 transition disabled:opacity-50"
            >
              <span v-if="composerStore.scoring" class="animate-spin text-xs">🌀</span>
              <span>{{ composerStore.scoring ? 'Menganalisis...' : '⚡ Cek Skor AI' }}</span>
            </button>

            <div class="flex items-center gap-3">
              <input
                type="datetime-local"
                v-model="scheduledTime"
                class="bg-slate-950 border border-slate-800 text-slate-300 text-xs rounded-lg px-3 py-2 focus:outline-none focus:ring-1 focus:ring-indigo-500"
              />
              <button
                @click="handleSchedule"
                :disabled="!postText.trim() || textLength > 500 || !scheduledTime || composerStore.loading"
                class="bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-medium px-5 py-2 rounded-lg transition disabled:opacity-50 shadow-lg shadow-indigo-600/20"
              >
                {{ composerStore.loading ? 'Menyimpan...' : 'Jadwalkan' }}
              </button>
            </div>
          </div>
        </div>

        <!-- Scheduled Queue List -->
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-4">
          <h2 class="text-base font-semibold text-slate-200">Antrean Postingan Terjadwal</h2>
          
          <div v-if="composerStore.scheduledPosts.length === 0" class="text-center py-8 text-slate-500 text-sm border border-dashed border-slate-800 rounded-lg">
            Belum ada postingan yang dijadwalkan.
          </div>

          <div v-else class="space-y-3">
            <div
              v-for="item in composerStore.scheduledPosts"
              :key="item.id"
              class="p-4 bg-slate-950/60 border border-slate-800/80 rounded-lg flex items-start justify-between gap-4"
            >
              <div class="space-y-1">
                <p class="text-sm text-slate-200 whitespace-pre-line line-clamp-2">{{ item.text }}</p>
                <div class="flex items-center gap-3 text-xs text-slate-400">
                  <span>📅 {{ formatDate(item.scheduled_for) }}</span>
                  <span class="px-2 py-0.5 rounded bg-slate-800 border border-slate-700 text-indigo-300 uppercase text-[10px]">
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
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-4">
          <h2 class="text-base font-semibold text-slate-200">AI Engagement Score</h2>

          <div v-if="!composerStore.lastScore && !composerStore.scoring" class="text-center py-8 text-slate-500 text-xs">
            Klik <strong class="text-slate-400">"Cek Skor AI"</strong> untuk menganalisis potensi viral dan saran hook postingan kamu.
          </div>

          <div v-if="composerStore.scoring" class="py-8 text-center text-slate-400 text-xs animate-pulse">
            AI sedang menganalisis struktur kalimat, hook, dan keterbacaan...
          </div>

          <div v-if="composerStore.lastScore" class="space-y-4">
            <div class="flex items-center justify-between p-4 bg-slate-950 rounded-lg border border-slate-800">
              <span class="text-xs text-slate-400 font-medium">Skor Kualitas</span>
              <span :class="['text-3xl font-extrabold', getScoreColor(composerStore.lastScore.score)]">
                {{ composerStore.lastScore.score }}/100
              </span>
            </div>

            <div v-if="composerStore.lastScore.suggestions.length > 0" class="space-y-2">
              <span class="text-xs font-semibold text-slate-300">Saran Perbaikan:</span>
              <ul class="space-y-2">
                <li
                  v-for="(sugg, idx) in composerStore.lastScore.suggestions"
                  :key="idx"
                  class="text-xs text-slate-400 bg-amber-950/20 border border-amber-900/30 text-amber-200/80 p-2.5 rounded-lg flex items-start gap-2"
                >
                  <span class="text-amber-400">💡</span>
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
import { useComposerStore } from '../stores/composer'

const composerStore = useComposerStore()

const postText = ref('')
const scheduledTime = ref('')
const activeAccountId = ref('00000000-0000-0000-0000-000000000000') // Placeholder account ID

const textLength = computed(() => postText.value.length)

function handleScore() {
  composerStore.scoreDraft(postText.value, activeAccountId.value)
}

async function handleSchedule() {
  if (!postText.value.trim() || !scheduledTime.value) return

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
  // Set default schedule time +1 hour from now
  const nextHour = new Date(Date.now() + 60 * 60 * 1000)
  scheduledTime.value = nextHour.toISOString().slice(0, 16)
})
</script>
