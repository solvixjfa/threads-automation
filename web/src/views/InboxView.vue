<template>
  <div class="max-w-5xl mx-auto space-y-8">
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold text-white tracking-tight">Reply Inbox & Moderation</h1>
        <p class="text-zinc-400 text-sm mt-1">Pantau balasan masuk, klasifikasi otomatis, dan persetujuan auto-reply AI.</p>
      </div>

      <!-- Navigation Tabs -->
      <div class="flex items-center bg-zinc-900 border border-white/10 p-1 rounded-lg shrink-0">
        <button
          @click="activeTab = 'inbox'"
          :class="['px-4 py-1.5 text-xs font-medium rounded-md transition', activeTab === 'inbox' ? 'bg-white text-black' : 'text-zinc-400 hover:text-white']"
        >
          Semua Balasan ({{ inboxStore.replies.length }})
        </button>
        <button
          @click="activeTab = 'review'"
          :class="['px-4 py-1.5 text-xs font-medium rounded-md transition flex items-center gap-2', activeTab === 'review' ? 'bg-white text-black' : 'text-zinc-400 hover:text-white']"
        >
          <span>Pending Review</span>
          <span v-if="inboxStore.reviewLogs.length > 0" class="bg-black text-white border border-white/20 font-mono text-[10px] px-2 py-0.5 rounded-full">
            {{ inboxStore.reviewLogs.length }}
          </span>
        </button>
      </div>
    </div>

    <!-- TAB 1: ALL INBOX REPLIES -->
    <div v-if="activeTab === 'inbox'" class="space-y-4">
      <div v-if="inboxStore.replies.length === 0" class="bg-zinc-950/80 backdrop-blur-xl border border-white/10 rounded-xl p-12 text-center text-zinc-500 text-sm shadow-2xl">
        Belum ada balasan masuk dari pengguna.
      </div>

      <div v-else class="space-y-3">
        <div
          v-for="item in inboxStore.replies"
          :key="item.id"
          class="bg-zinc-950/80 backdrop-blur-xl border border-white/10 rounded-xl p-5 space-y-3 shadow-2xl transition hover:border-white/20"
        >
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <span class="font-semibold text-white text-sm">@{{ item.author_username }}</span>
              <span class="text-xs text-zinc-500">• {{ formatDate(item.replied_at) }}</span>
            </div>
            <span class="px-2 py-0.5 rounded border border-white/10 bg-black text-[10px] font-bold uppercase tracking-wider text-zinc-300">
              {{ item.classification }}
            </span>
          </div>
          <p class="text-sm text-zinc-300">{{ item.text }}</p>
        </div>
      </div>
    </div>

    <!-- TAB 2: PENDING AUTO-REPLY REVIEWS -->
    <div v-if="activeTab === 'review'" class="space-y-4">
      <div v-if="inboxStore.reviewLogs.length === 0" class="bg-zinc-950/80 backdrop-blur-xl border border-white/10 rounded-xl p-12 text-center text-zinc-500 text-sm shadow-2xl">
        Tidak ada draf balasan AI yang menunggu review.
      </div>

      <div v-else class="space-y-4">
        <div
          v-for="log in inboxStore.reviewLogs"
          :key="log.id"
          class="bg-zinc-950/80 backdrop-blur-xl border border-white/10 rounded-xl p-6 space-y-4 shadow-2xl"
        >
          <div class="p-4 bg-black border border-white/10 rounded-lg space-y-2">
            <span class="text-xs font-semibold text-zinc-400">@{{ log.reply?.author_username || 'Pengguna' }} berkomentar:</span>
            <p class="text-sm text-zinc-200 italic">"{{ log.reply?.text }}"</p>
          </div>

          <div class="space-y-2">
            <label class="text-xs font-medium text-white flex items-center justify-between">
              <span>Draf Balasan AI (Gemini)</span>
              <span class="text-[10px] text-zinc-500 uppercase tracking-wider">Review Mode</span>
            </label>
            <textarea
              v-model="log.final_text"
              rows="3"
              class="w-full bg-black border border-white/10 rounded-lg p-3 text-white text-sm focus:outline-none focus:border-white transition resize-none"
            ></textarea>
          </div>

          <div class="flex items-center justify-end gap-3 pt-2">
            <button
              @click="handleApprove(log)"
              class="bg-white hover:bg-zinc-200 text-black text-xs font-bold px-5 py-2.5 rounded-lg transition"
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

function formatDate(isoStr: string) {
  if (!isoStr) return ''
  return new Date(isoStr).toLocaleString('id-ID', { dateStyle: 'short', timeStyle: 'short' })
}

onMounted(() => {
  inboxStore.fetchReplies(activeAccountId.value)
  inboxStore.fetchPendingReviews(activeAccountId.value)
})
</script>
