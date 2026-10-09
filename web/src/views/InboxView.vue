<template>
  <div class="max-w-5xl mx-auto space-y-8">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-slate-100">Reply Inbox & Moderation</h1>
        <p class="text-slate-400 text-sm mt-1">Pantau balasan masuk, klasifikasi otomatis, dan persetujuan auto-reply AI.</p>
      </div>

      <!-- Navigation Tabs -->
      <div class="flex items-center bg-slate-900 border border-slate-800 p-1 rounded-lg">
        <button
          @click="activeTab = 'inbox'"
          :class="['px-4 py-1.5 text-xs font-medium rounded-md transition', activeTab === 'inbox' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200']"
        >
          Semua Balasan ({{ inboxStore.replies.length }})
        </button>
        <button
          @click="activeTab = 'review'"
          :class="['px-4 py-1.5 text-xs font-medium rounded-md transition flex items-center gap-2', activeTab === 'review' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200']"
        >
          <span>Pending Review AI</span>
          <span v-if="inboxStore.reviewLogs.length > 0" class="bg-amber-500 text-slate-950 font-extrabold text-[10px] px-1.5 py-0.2 rounded-full">
            {{ inboxStore.reviewLogs.length }}
          </span>
        </button>
      </div>
    </div>

    <!-- TAB 1: ALL INBOX REPLIES -->
    <div v-if="activeTab === 'inbox'" class="space-y-4">
      <div v-if="inboxStore.replies.length === 0" class="bg-slate-900 border border-slate-800 rounded-xl p-12 text-center text-slate-500 text-sm">
        Belum ada balasan masuk dari pengguna.
      </div>

      <div v-else class="space-y-3">
        <div
          v-for="item in inboxStore.replies"
          :key="item.id"
          class="bg-slate-900 border border-slate-800/80 rounded-xl p-5 space-y-3 shadow-lg"
        >
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <span class="font-semibold text-slate-200 text-sm">@{{ item.author_username }}</span>
              <span class="text-xs text-slate-500">• {{ formatDate(item.replied_at) }}</span>
            </div>
            <span :class="['px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider', getBadgeColor(item.classification)]">
              {{ item.classification }}
            </span>
          </div>

          <p class="text-sm text-slate-300">{{ item.text }}</p>
        </div>
      </div>
    </div>

    <!-- TAB 2: PENDING AUTO-REPLY REVIEWS -->
    <div v-if="activeTab === 'review'" class="space-y-4">
      <div v-if="inboxStore.reviewLogs.length === 0" class="bg-slate-900 border border-slate-800 rounded-xl p-12 text-center text-slate-500 text-sm">
        Tidak ada draf balasan AI yang menunggu review.
      </div>

      <div v-else class="space-y-4">
        <div
          v-for="log in inboxStore.reviewLogs"
          :key="log.id"
          class="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4 shadow-xl"
        >
          <!-- User Question -->
          <div class="p-3.5 bg-slate-950 border border-slate-800 rounded-lg space-y-1">
            <span class="text-xs font-semibold text-indigo-400">@{{ log.reply?.author_username || 'Pengguna' }} bertanya/berkomentar:</span>
            <p class="text-xs text-slate-300 italic">"{{ log.reply?.text }}"</p>
          </div>

          <!-- AI Generated Draft Editor -->
          <div class="space-y-2">
            <label class="text-xs font-medium text-slate-300 flex items-center justify-between">
              <span>Draf Balasan AI (Gemini):</span>
              <span class="text-[10px] text-amber-400">Review Mode Active</span>
            </label>
            <textarea
              v-model="log.final_text"
              rows="3"
              class="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-slate-200 text-xs focus:outline-none focus:ring-1 focus:ring-indigo-500"
            ></textarea>
          </div>

          <!-- Actions -->
          <div class="flex items-center justify-end gap-3 pt-1">
            <button
              @click="handleApprove(log)"
              class="bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-medium px-4 py-2 rounded-lg transition shadow-md shadow-emerald-600/20"
            >
              Approve & Send
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useInboxStore, AutoReplyLog } from '../stores/inbox'

const inboxStore = useInboxStore()
const activeTab = ref<'inbox' | 'review'>('inbox')
const activeAccountId = ref('00000000-0000-0000-0000-000000000000')

async function handleApprove(log: AutoReplyLog) {
  const res = await inboxStore.approveAndSendReply(log.id, log.final_text)
  if (res.success) {
    alert('Balasan disetujui dan dikirim!')
  }
}

function getBadgeColor(classification: string) {
  switch (classification) {
    case 'question': return 'bg-indigo-950 border border-indigo-800 text-indigo-300'
    case 'praise': return 'bg-emerald-950 border border-emerald-800 text-emerald-300'
    case 'spam': return 'bg-amber-950 border border-amber-800 text-amber-300'
    case 'toxic': return 'bg-rose-950 border border-rose-800 text-rose-300'
    default: return 'bg-slate-800 text-slate-400'
  }
}

function formatDate(isoStr: string) {
  if (!isoStr) return ''
  return new Date(isoStr).toLocaleString('id-ID', {
    dateStyle: 'short',
    timeStyle: 'short'
  })
}

onMounted(() => {
  inboxStore.fetchReplies(activeAccountId.value)
  inboxStore.fetchPendingReviews(activeAccountId.value)
})
</script>
