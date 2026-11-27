<template>
  <div class="space-y-4">
    <!-- HEADER -->
    <div class="flex items-center justify-between gap-3">
      <div>
        <h1 class="text-xl md:text-2xl font-bold tracking-tight">Live Chat</h1>
        <p class="text-xs theme-text-muted mt-0.5">
          Balas pertanyaan pengunjung dari ixiera.online secara real-time.
        </p>
      </div>
      <div class="flex items-center gap-2">
        <select v-model="statusFilter" class="input text-xs font-bold">
          <option value="open">Open ({{ openCount }})</option>
          <option value="closed">Closed ({{ closedCount }})</option>
          <option value="all">Semua ({{ sessions.length }})</option>
        </select>
        <button
          @click="fetchSessions"
          :disabled="loading"
          class="p-2 rounded-lg border theme-border theme-bg theme-text-muted hover:theme-text"
          title="Refresh sesi"
        >
          <RefreshCw class="w-4 h-4" :class="{ 'animate-spin': loading }" />
        </button>
      </div>
    </div>

    <!-- SPLIT LAYOUT -->
    <div class="grid grid-cols-1 md:grid-cols-12 gap-4 min-h-[70dvh]">
      <!-- SESSION LIST -->
      <div
        class="md:col-span-4 card overflow-hidden flex flex-col"
        :class="{ 'hidden md:flex': selectedSession }"
      >
        <div class="p-3 border-b theme-border text-xs font-bold uppercase tracking-wider theme-text-muted">
          Daftar Percakapan ({{ filteredSessions.length }})
        </div>

        <div v-if="loading && sessions.length === 0" class="p-8 text-center text-xs theme-text-muted animate-pulse">
          Memuat sesi chat...
        </div>

        <div v-else-if="filteredSessions.length === 0" class="p-8 text-center text-xs theme-text-muted">
          Belum ada sesi chat pada filter ini.
        </div>

        <div v-else class="divide-y theme-border overflow-y-auto flex-1">
          <button
            v-for="s in filteredSessions"
            :key="s.id"
            @click="selectSession(s)"
            class="w-full text-left p-3.5 hover:theme-bg-sec transition-colors flex items-start justify-between gap-2"
            :class="{ 'theme-bg-sec border-l-2 border-l-[var(--accent)]': selectedSession?.id === s.id }"
          >
            <div class="min-w-0 flex-1">
              <div class="flex items-center gap-2">
                <span class="font-bold text-sm truncate">{{ s.visitor_name }}</span>
                <span
                  v-if="s.unread_admin > 0"
                  class="px-1.5 py-0.5 text-[10px] font-black rounded-full bg-emerald-500 text-black"
                >
                  {{ s.unread_admin }}
                </span>
              </div>
              <div class="text-[11px] theme-text-muted truncate mt-0.5">
                {{ s.visitor_email || 'Tanpa email' }}
              </div>
              <div class="text-[10px] theme-text-muted mt-1">
                {{ formatRelativeTime(s.last_message_at) }}
              </div>
            </div>
            <span
              class="text-[10px] font-bold uppercase px-2 py-0.5 rounded border shrink-0"
              :class="s.status === 'open'
                ? 'border-emerald-500/40 text-emerald-400 bg-emerald-500/10'
                : 'theme-border theme-text-muted'"
            >
              {{ s.status }}
            </span>
          </button>
        </div>
      </div>

      <!-- CHAT THREAD -->
      <div
        class="md:col-span-8 card flex flex-col overflow-hidden h-[75dvh] md:h-[72dvh]"
        :class="{ 'hidden md:flex': !selectedSession }"
      >
        <div v-if="!selectedSession" class="flex-1 flex flex-col items-center justify-center p-8 text-center theme-text-muted">
          <MessageCircle class="w-8 h-8 mb-2 opacity-50" />
          <p class="text-sm font-bold">Pilih percakapan di sebelah kiri</p>
          <p class="text-xs mt-1">Pesan pengunjung akan muncul otomatis secara real-time.</p>
        </div>

        <template v-else>
          <!-- THREAD HEADER -->
          <div class="p-3.5 border-b theme-border flex items-center justify-between gap-3 shrink-0">
            <div class="flex items-center gap-2.5 min-w-0">
              <button
                @click="selectedSession = null"
                class="md:hidden p-1.5 rounded-lg border theme-border theme-bg-sec"
                aria-label="Kembali"
              >
                <ArrowLeft class="w-4 h-4" />
              </button>
              <div class="min-w-0">
                <div class="font-bold text-sm truncate">{{ selectedSession.visitor_name }}</div>
                <div class="text-[11px] theme-text-muted truncate">
                  {{ selectedSession.visitor_email || 'Tanpa email' }}
                  <span v-if="selectedSession.page_url"> • {{ selectedSession.page_url }}</span>
                </div>
              </div>
            </div>

            <button
              @click="toggleSessionStatus"
              class="btn btn-secondary btn-sm text-xs shrink-0"
            >
              {{ selectedSession.status === 'open' ? 'Tutup Sesi' : 'Buka Lagi' }}
            </button>
          </div>

          <!-- MESSAGES BODY -->
          <div ref="messagesContainer" class="flex-1 overflow-y-auto p-4 space-y-3">
            <div
              v-for="m in messages"
              :key="m.id"
              class="flex flex-col"
              :class="m.sender_role === 'admin' ? 'items-end' : 'items-start'"
            >
              <div
                v-if="m.sender_role === 'bot'"
                class="text-[11px] theme-text-muted italic px-3 py-1.5 rounded-lg theme-bg-sec border theme-border max-w-[85%]"
              >
                {{ m.message }}
              </div>
              <div
                v-else
                class="px-3.5 py-2.5 rounded-2xl text-sm max-w-[82%] whitespace-pre-line break-words"
                :class="m.sender_role === 'admin'
                  ? 'bg-[var(--accent)] text-[var(--bg)] font-medium rounded-br-sm'
                  : 'theme-bg-sec border theme-border theme-text rounded-bl-sm'"
              >
                {{ m.message }}
              </div>
              <span class="text-[10px] theme-text-muted mt-1 px-1">
                {{ m.sender_role === 'admin' ? 'Admin' : selectedSession.visitor_name }} • {{ formatClock(m.created_at) }}
              </span>
            </div>
          </div>

          <!-- REPLY INPUT -->
          <form @submit.prevent="sendReply" class="p-3 border-t theme-border flex gap-2 shrink-0">
            <input
              v-model.trim="replyText"
              type="text"
              placeholder="Tulis balasan sebagai Admin..."
              class="input flex-1 text-sm"
              :disabled="sending"
            />
            <button
              type="submit"
              :disabled="sending || !replyText"
              class="btn btn-primary btn-sm px-4 flex items-center gap-1.5 shrink-0"
            >
              <Send class="w-4 h-4" />
              <span>Kirim</span>
            </button>
          </form>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { supabase } from '../../lib/supabase'
import { RefreshCw, MessageCircle, ArrowLeft, Send } from 'lucide-vue-next'

interface ChatSession {
  id: string
  visitor_token: string
  visitor_name: string
  visitor_email: string | null
  page_url: string | null
  status: 'open' | 'closed'
  unread_admin: number
  last_message_at: string
  created_at: string
}

interface ChatMessage {
  id: string
  session_id: string
  sender_role: 'visitor' | 'admin' | 'bot'
  message: string
  created_at: string
}

const sessions = ref<ChatSession[]>([])
const selectedSession = ref<ChatSession | null>(null)
const messages = ref<ChatMessage[]>([])
const statusFilter = ref<'open' | 'closed' | 'all'>('open')
const loading = ref(true)
const sending = ref(false)
const replyText = ref('')
const messagesContainer = ref<HTMLElement | null>(null)

let realtimeChannel: any = null
let pollTimer: number | null = null

const openCount = computed(() => sessions.value.filter(s => s.status === 'open').length)
const closedCount = computed(() => sessions.value.filter(s => s.status === 'closed').length)

const filteredSessions = computed(() => {
  if (statusFilter.value === 'all') return sessions.value
  return sessions.value.filter(s => s.status === statusFilter.value)
})

function playChime() {
  try {
    const AudioCtx = window.AudioContext || (window as any).webkitAudioContext
    if (!AudioCtx) return
    const ctx = new AudioCtx()
    const osc = ctx.createOscillator()
    const gain = ctx.createGain()
    osc.type = 'sine'
    osc.frequency.setValueAtTime(880, ctx.currentTime)
    gain.gain.setValueAtTime(0.08, ctx.currentTime)
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.25)
    osc.connect(gain)
    gain.connect(ctx.destination)
    osc.start()
    osc.stop(ctx.currentTime + 0.25)
  } catch {
    // Ignore autoplay restriction
  }
}

function scrollToBottom() {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

async function fetchSessions() {
  loading.value = true
  try {
    const { data, error } = await supabase
      .schema('threads')
      .from('chat_sessions')
      .select('*')
      .order('last_message_at', { ascending: false })
      .limit(100)

    if (!error && data) {
      sessions.value = data as ChatSession[]
      if (selectedSession.value) {
        const updated = sessions.value.find(s => s.id === selectedSession.value?.id)
        if (updated) selectedSession.value = updated
      }
    }
  } finally {
    loading.value = false
  }
}

async function loadMessages(sessionId: string) {
  const { data, error } = await supabase
    .schema('threads')
    .from('chat_messages')
    .select('*')
    .eq('session_id', sessionId)
    .order('created_at', { ascending: true })

  if (!error && data) {
    messages.value = data as ChatMessage[]
    scrollToBottom()
  }
}

async function markSessionRead(sessionId: string) {
  await supabase
    .schema('threads')
    .from('chat_sessions')
    .update({ unread_admin: 0 })
    .eq('id', sessionId)

  const target = sessions.value.find(s => s.id === sessionId)
  if (target) target.unread_admin = 0
}

async function selectSession(session: ChatSession) {
  selectedSession.value = session
  await loadMessages(session.id)
  if (session.unread_admin > 0) {
    await markSessionRead(session.id)
  }
}

async function sendReply() {
  if (!selectedSession.value || !replyText.value || sending.value) return
  const text = replyText.value
  const sessionId = selectedSession.value.id
  sending.value = true
  replyText.value = ''

  try {
    const { data, error } = await supabase
      .schema('threads')
      .from('chat_messages')
      .insert({
        session_id: sessionId,
        sender_role: 'admin',
        message: text,
      })
      .select()
      .single()

    if (!error && data) {
      if (!messages.value.some(m => m.id === data.id)) {
        messages.value.push(data as ChatMessage)
      }
      await supabase
        .schema('threads')
        .from('chat_sessions')
        .update({
          last_message_at: new Date().toISOString(),
          unread_admin: 0,
        })
        .eq('id', sessionId)
      scrollToBottom()
    }
  } finally {
    sending.value = false
  }
}

async function toggleSessionStatus() {
  if (!selectedSession.value) return
  const nextStatus = selectedSession.value.status === 'open' ? 'closed' : 'open'
  const { error } = await supabase
    .schema('threads')
    .from('chat_sessions')
    .update({ status: nextStatus })
    .eq('id', selectedSession.value.id)

  if (!error) {
    selectedSession.value.status = nextStatus
    const item = sessions.value.find(s => s.id === selectedSession.value?.id)
    if (item) item.status = nextStatus
  }
}

function formatClock(iso: string) {
  return new Date(iso).toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' })
}

function formatRelativeTime(iso: string) {
  const diffMin = Math.floor((Date.now() - new Date(iso).getTime()) / 60000)
  if (diffMin < 1) return 'Baru saja'
  if (diffMin < 60) return `${diffMin} menit lalu`
  const diffHour = Math.floor(diffMin / 60)
  if (diffHour < 24) return `${diffHour} jam lalu`
  return new Date(iso).toLocaleDateString('id-ID', { day: 'numeric', month: 'short' })
}

onMounted(async () => {
  await fetchSessions()

  realtimeChannel = supabase
    .channel('admin-live-chat')
    .on(
      'postgres_changes',
      { event: 'INSERT', schema: 'threads', table: 'chat_messages' },
      async (payload: any) => {
        const msg = payload.new as ChatMessage
        if (msg.sender_role === 'visitor') {
          playChime()
        }
        if (selectedSession.value && msg.session_id === selectedSession.value.id) {
          if (!messages.value.some(m => m.id === msg.id)) {
            messages.value.push(msg)
            scrollToBottom()
          }
          if (msg.sender_role === 'visitor') {
            await markSessionRead(msg.session_id)
          }
        }
        await fetchSessions()
      }
    )
    .on(
      'postgres_changes',
      { event: '*', schema: 'threads', table: 'chat_sessions' },
      async () => {
        await fetchSessions()
      }
    )
    .subscribe()

  pollTimer = window.setInterval(async () => {
    await fetchSessions()
    if (selectedSession.value) {
      await loadMessages(selectedSession.value.id)
    }
  }, 6000)
})

onUnmounted(() => {
  if (realtimeChannel) supabase.removeChannel(realtimeChannel)
  if (pollTimer) clearInterval(pollTimer)
})
</script>
