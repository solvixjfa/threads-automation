<template>
  <div
    :class="isFullScreen
      ? 'fixed inset-0 z-[1000] flex flex-col'
      : 'fixed bottom-4 right-4 z-[990] flex flex-col items-end'"
  >
    <!-- CHAT WINDOW -->
    <div
      v-if="isOpen"
      :class="isFullScreen
        ? 'w-full h-[100dvh] rounded-none border-0 bg-[#0c0c0e] text-zinc-100 flex flex-col overflow-hidden'
        : 'mb-3 w-[calc(100vw-2rem)] sm:w-[370px] max-h-[78dvh] rounded-2xl border border-zinc-800 bg-[#0c0c0e] text-zinc-100 shadow-2xl flex flex-col overflow-hidden'"
    >
      <!-- HEADER -->
      <div class="px-4 py-3.5 bg-[#121215] border-b border-zinc-800 flex items-center justify-between gap-2 shrink-0">
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-xl bg-white text-black flex items-center justify-center font-black text-sm">
            IX
          </div>
          <div>
            <div class="text-sm font-bold leading-tight">Bantuan Ixiera</div>
            <div class="text-[11px] text-zinc-400 flex items-center gap-1.5 mt-0.5">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 inline-block"></span>
              <span>{{ mode === 'live' ? 'Terhubung dengan Admin' : 'Jawaban Instan & Admin' }}</span>
            </div>
          </div>
        </div>
        <div class="flex items-center gap-1">
          <button
            v-if="mode !== 'faq'"
            @click="switchToFaq"
            class="px-2 py-1 rounded-lg text-[11px] font-semibold text-zinc-300 hover:bg-zinc-800 transition-colors"
            title="Kembali ke menu pertanyaan"
          >
            Menu FAQ
          </button>
          <button
            @click="isFullScreen = !isFullScreen"
            class="p-1.5 rounded-lg text-zinc-400 hover:text-white hover:bg-zinc-800 transition-colors"
            :title="isFullScreen ? 'Perkecil jendela' : 'Layar penuh'"
            aria-label="Toggle layar penuh"
          >
            <Minimize2 v-if="isFullScreen" class="w-4 h-4" />
            <Maximize2 v-else class="w-4 h-4" />
          </button>
          <button
            @click="closeWidget"
            class="p-1.5 rounded-lg text-zinc-400 hover:text-white hover:bg-zinc-800 transition-colors"
            aria-label="Tutup chat"
          >
            <X class="w-4 h-4" />
          </button>
        </div>
      </div>

      <!-- MODE 1: ZERO-AI CLICKABLE FAQ FLOW -->
      <div v-if="mode === 'faq'" ref="faqBodyRef" class="flex-1 overflow-y-auto p-4 space-y-3">
        <div
          v-for="(item, idx) in faqHistory"
          :key="idx"
          class="flex flex-col"
          :class="item.from === 'user' ? 'items-end' : 'items-start'"
        >
          <div
            class="px-3.5 py-2.5 rounded-2xl text-xs leading-relaxed max-w-[88%] whitespace-pre-line"
            :class="item.from === 'user'
              ? 'bg-white text-black font-semibold rounded-br-sm'
              : 'bg-[#16161a] border border-zinc-800 text-zinc-200 rounded-bl-sm'"
          >
            {{ item.text }}
          </div>
        </div>

        <!-- ACTION BUTTONS -->
        <div class="pt-1 space-y-1.5">
          <div class="text-[10px] font-bold uppercase tracking-wider text-zinc-500 px-1">
            Pilih Topik Bantuan
          </div>
          <button
            v-for="opt in currentOptions"
            :key="opt.id"
            @click="handleFaqChoice(opt)"
            class="w-full text-left px-3.5 py-2.5 rounded-xl text-xs font-medium bg-[#141418] hover:bg-zinc-800/90 border border-zinc-800 hover:border-zinc-700 text-zinc-100 transition-colors flex items-center justify-between gap-2"
          >
            <span>{{ opt.label }}</span>
            <ChevronRight class="w-3.5 h-3.5 text-zinc-500 shrink-0" />
          </button>

          <button
            @click="openHandoverForm"
            class="w-full text-left px-3.5 py-2.5 rounded-xl text-xs font-bold bg-white text-black hover:bg-zinc-200 transition-colors flex items-center justify-between gap-2 mt-2"
          >
            <span class="flex items-center gap-2">
              <Headphones class="w-3.5 h-3.5" />
              <span>Chat dengan Admin</span>
            </span>
            <ChevronRight class="w-3.5 h-3.5 shrink-0" />
          </button>
        </div>
      </div>

      <!-- MODE 2: HUMAN HANDOVER FORM -->
      <form v-else-if="mode === 'handover'" @submit.prevent="submitHandover" class="flex-1 overflow-y-auto p-4 space-y-3">
        <div class="p-3 rounded-xl bg-[#16161a] border border-zinc-800 text-xs text-zinc-300 leading-relaxed">
          Tinggalkan pesan di bawah. Notifikasi langsung masuk ke Admin Ixiera dan balasan akan muncul di jendela chat ini.
        </div>

        <div>
          <label class="block text-[11px] font-bold text-zinc-400 mb-1">Nama Anda *</label>
          <input
            v-model.trim="formName"
            type="text"
            required
            maxlength="80"
            placeholder="Contoh: Raka"
            class="w-full px-3 py-2.5 rounded-xl bg-[#141418] border border-zinc-800 text-sm text-white focus:outline-none focus:border-zinc-500"
          />
        </div>

        <div>
          <label class="block text-[11px] font-bold text-zinc-400 mb-1">Email (Opsional, untuk balasan jika offline)</label>
          <input
            v-model.trim="formEmail"
            type="email"
            maxlength="120"
            placeholder="nama@email.com"
            class="w-full px-3 py-2.5 rounded-xl bg-[#141418] border border-zinc-800 text-sm text-white focus:outline-none focus:border-zinc-500"
          />
        </div>

        <div>
          <label class="block text-[11px] font-bold text-zinc-400 mb-1">Pertanyaan / Kendala *</label>
          <textarea
            v-model.trim="formMessage"
            rows="4"
            required
            maxlength="2000"
            placeholder="Tulis pertanyaan Anda di sini..."
            class="w-full px-3 py-2.5 rounded-xl bg-[#141418] border border-zinc-800 text-sm text-white focus:outline-none focus:border-zinc-500 resize-none"
          ></textarea>
        </div>

        <p v-if="errorMsg" class="text-[11px] text-red-400">{{ errorMsg }}</p>

        <button
          type="submit"
          :disabled="submitting || !formName || !formMessage"
          class="w-full py-3 rounded-xl bg-white text-black font-bold text-xs hover:bg-zinc-200 disabled:opacity-50 transition-colors flex items-center justify-center gap-1.5"
        >
          <Send class="w-3.5 h-3.5" />
          <span>{{ submitting ? 'Menghubungkan...' : 'Mulai Chat dengan Admin' }}</span>
        </button>
      </form>

      <!-- MODE 3: REAL-TIME LIVE CHAT WITH ADMIN -->
      <template v-else-if="mode === 'live'">
        <div ref="liveBodyRef" class="flex-1 overflow-y-auto p-4 space-y-3">
          <div
            v-for="m in liveMessages"
            :key="m.id"
            class="flex flex-col"
            :class="m.sender_role === 'visitor' ? 'items-end' : 'items-start'"
          >
            <div
              v-if="m.sender_role === 'bot'"
              class="text-[11px] text-zinc-400 italic px-3 py-1.5 rounded-lg bg-[#141418] border border-zinc-800 max-w-[85%]"
            >
              {{ m.message }}
            </div>
            <div
              v-else
              class="px-3.5 py-2.5 rounded-2xl text-sm leading-relaxed max-w-[85%] whitespace-pre-line break-words"
              :class="m.sender_role === 'visitor'
                ? 'bg-white text-black font-medium rounded-br-sm'
                : 'bg-[#16161a] border border-zinc-700 text-zinc-100 rounded-bl-sm'"
            >
              {{ m.message }}
            </div>
            <span class="text-[10px] text-zinc-500 mt-1 px-1">
              {{ m.sender_role === 'admin' ? 'Admin Ixiera' : m.sender_role === 'bot' ? 'Sistem' : 'Anda' }} • {{ formatClock(m.created_at) }}
            </span>
          </div>
        </div>

        <form @submit.prevent="sendLiveFollowUp" class="p-3 bg-[#121215] border-t border-zinc-800 flex gap-2 shrink-0">
          <input
            v-model.trim="liveInput"
            type="text"
            placeholder="Ketik balasan untuk Admin..."
            maxlength="2000"
            class="flex-1 px-3 py-2.5 rounded-xl bg-[#18181c] border border-zinc-800 text-sm text-white focus:outline-none focus:border-zinc-600"
          />
          <button
            type="submit"
            :disabled="submitting || !liveInput"
            class="px-4 py-2.5 rounded-xl bg-white text-black font-bold text-xs hover:bg-zinc-200 disabled:opacity-50 transition-colors shrink-0"
            aria-label="Kirim pesan"
          >
            <Send class="w-4 h-4" />
          </button>
        </form>
      </template>
    </div>

    <!-- FLOATING TRIGGER BUTTON -->
    <button
      v-if="!isFullScreen"
      @click="toggleWidget"
      class="h-12 px-4 rounded-full bg-white text-black font-bold text-xs shadow-xl hover:bg-zinc-200 active:scale-95 transition-all flex items-center gap-2 border border-zinc-300"
    >
      <MessageSquare class="w-4 h-4" />
      <span>{{ isOpen ? 'Tutup' : sessionId ? 'Chat Admin' : 'Tanya Ixiera' }}</span>
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { supabase } from '../lib/supabase'
import { MessageSquare, X, ChevronRight, Headphones, Send, Maximize2, Minimize2 } from 'lucide-vue-next'

interface FaqOption {
  id: string
  label: string
  answer: string
  nextIds: string[]
}

interface FaqHistoryItem {
  from: 'bot' | 'user'
  text: string
}

interface ChatMessage {
  id: string
  session_id: string
  sender_role: 'visitor' | 'admin' | 'bot'
  message: string
  created_at: string
}

const API_BASE = (import.meta.env.VITE_API_URL || 'https://threads-automation-r9so.onrender.com').replace(/\/$/, '')
const STORAGE_KEY = 'ixiera_support_session_v1'

const FAQ_NODES: Record<string, FaqOption> = {
  about: {
    id: 'about',
    label: 'Apa itu Ixiera & cara kerjanya?',
    answer:
      'Ixiera adalah platform automasi & AI untuk kreator maupun bisnis di Threads. Kamu bisa merencanakan konten dengan AI, menjadwalkan posting otomatis, membalas komentar sesuai Knowledge Base brand, dan memantau analitik jam terbaik.',
    nextIds: ['safety', 'pricing', 'multi_account'],
  },
  pricing: {
    id: 'pricing',
    label: 'Paket & Harga (Credit vs BYOK)',
    answer:
      'Tersedia 2 paket berlangganan 30 hari:\n• Pro Credit (Rp29.000): Dapat 100 kredit AI siap pakai (tanpa perlu API key sendiri), maksimal 10 akun Threads.\n• Pro BYOK (Rp19.000): Pakai API key Gemini/Groq milikmu sendiri tanpa batas kredit, maksimal 3 akun Threads.\nPengguna baru juga mendapat akses Free Trial.',
    nextIds: ['byok_diff', 'safety', 'about'],
  },
  byok_diff: {
    id: 'byok_diff',
    label: 'Apa bedanya Pro Credit dan Pro BYOK?',
    answer:
      'Di Pro Credit (Rp29.000), seluruh biaya AI sudah ditanggung kuota 100 kredit Ixiera. Di Pro BYOK (Rp19.000), kamu menempelkan API key gratis/berbayar dari Google AI Studio (Gemini) atau Groq di menu Profil sehingga biaya langganan lebih hemat.',
    nextIds: ['pricing', 'multi_account'],
  },
  safety: {
    id: 'safety',
    label: 'Apakah aman untuk akun Threads?',
    answer:
      'Aman. Ixiera terhubung lewat Meta Threads Graph API OAuth resmi—kami tidak pernah meminta atau menyimpan password akun Threads/Instagram kamu. Sistem juga dilengkapi batas kuota harian agar terhindar dari spam.',
    nextIds: ['multi_account', 'pricing'],
  },
  multi_account: {
    id: 'multi_account',
    label: 'Bisa kelola banyak akun sekaligus?',
    answer:
      'Bisa. Satu akun Ixiera mendukung multi-akun Threads dalam satu dashboard (hingga 3 akun di Pro BYOK dan 10 akun di Pro Credit) dengan pembagian paket & kredit yang otomatis tersinkronisasi.',
    nextIds: ['pricing', 'safety'],
  },
}

const ROOT_IDS = ['about', 'pricing', 'safety', 'multi_account']

const isOpen = ref(false)
const isFullScreen = ref(false)
const mode = ref<'faq' | 'handover' | 'live'>('faq')
const faqHistory = ref<FaqHistoryItem[]>([
  { from: 'bot', text: 'Halo! Ada yang bisa dibantu seputar Ixiera? Pilih topik di bawah atau langsung chat dengan Admin.' },
])
const currentOptions = ref<FaqOption[]>(ROOT_IDS.map(id => FAQ_NODES[id]))
const lastFaqTopic = ref<string>('')

const visitorToken = ref('')
const sessionId = ref('')
const formName = ref('')
const formEmail = ref('')
const formMessage = ref('')
const submitting = ref(false)
const errorMsg = ref('')

const liveMessages = ref<ChatMessage[]>([])
const liveInput = ref('')
const faqBodyRef = ref<HTMLElement | null>(null)
const liveBodyRef = ref<HTMLElement | null>(null)

let realtimeChannel: any = null
let pollTimer: number | null = null

function getOrCreateToken(): string {
  const key = 'ixiera_visitor_token'
  let token = localStorage.getItem(key)
  if (!token) {
    token = 'vis_' + Math.random().toString(36).slice(2) + Date.now().toString(36)
    localStorage.setItem(key, token)
  }
  return token
}

function scrollContainer(el: HTMLElement | null) {
  nextTick(() => {
    if (el) el.scrollTop = el.scrollHeight
  })
}

function closeWidget() {
  isFullScreen.value = false
  isOpen.value = false
}

function toggleWidget() {
  isOpen.value = !isOpen.value
  if (!isOpen.value) {
    isFullScreen.value = false
    return
  }
  if (sessionId.value) {
    mode.value = 'live'
    fetchLiveMessages()
    scrollContainer(liveBodyRef.value)
  } else {
    scrollContainer(faqBodyRef.value)
  }
}

function handleFaqChoice(opt: FaqOption) {
  lastFaqTopic.value = opt.label
  faqHistory.value.push({ from: 'user', text: opt.label })
  faqHistory.value.push({ from: 'bot', text: opt.answer })
  currentOptions.value = opt.nextIds.map(id => FAQ_NODES[id]).filter(Boolean)
  scrollContainer(faqBodyRef.value)
}

function openHandoverForm() {
  if (sessionId.value) {
    mode.value = 'live'
    fetchLiveMessages()
    return
  }
  errorMsg.value = ''
  mode.value = 'handover'
}

function switchToFaq() {
  mode.value = 'faq'
  scrollContainer(faqBodyRef.value)
}

async function submitHandover() {
  if (!formName.value || !formMessage.value || submitting.value) return
  submitting.value = true
  errorMsg.value = ''

  try {
    const res = await fetch(`${API_BASE}/api/v1/chat/start`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        visitor_token: visitorToken.value,
        visitor_name: formName.value,
        visitor_email: formEmail.value || null,
        page_url: window.location.href,
        faq_topic: lastFaqTopic.value || null,
        message: formMessage.value,
      }),
    })

    if (!res.ok) {
      throw new Error('Gagal mengirim pesan ke server')
    }

    const data = await res.json()
    if (data?.session?.id) {
      sessionId.value = data.session.id
      localStorage.setItem(
        STORAGE_KEY,
        JSON.stringify({
          sessionId: data.session.id,
          visitorName: formName.value,
        })
      )
      formMessage.value = ''
      mode.value = 'live'
      await fetchLiveMessages()
      subscribeRealtime(data.session.id)
    }
  } catch (err: any) {
    errorMsg.value = err?.message || 'Terjadi kesalahan. Coba kirim ulang.'
  } finally {
    submitting.value = false
  }
}

async function fetchLiveMessages() {
  if (!sessionId.value) return
  const { data, error } = await supabase
    .schema('threads')
    .from('chat_messages')
    .select('*')
    .eq('session_id', sessionId.value)
    .order('created_at', { ascending: true })

  if (!error && data) {
    liveMessages.value = data as ChatMessage[]
    scrollContainer(liveBodyRef.value)
  }
}

async function sendLiveFollowUp() {
  if (!sessionId.value || !liveInput.value || submitting.value) return
  const text = liveInput.value
  liveInput.value = ''
  submitting.value = true

  try {
    const res = await fetch(`${API_BASE}/api/v1/chat/message`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id: sessionId.value,
        visitor_token: visitorToken.value,
        message: text,
      }),
    })
    if (res.ok) {
      await fetchLiveMessages()
    }
  } finally {
    submitting.value = false
  }
}

function subscribeRealtime(sid: string) {
  if (realtimeChannel) {
    supabase.removeChannel(realtimeChannel)
  }
  realtimeChannel = supabase
    .channel(`visitor-chat-${sid}`)
    .on(
      'postgres_changes',
      {
        event: 'INSERT',
        schema: 'threads',
        table: 'chat_messages',
        filter: `session_id=eq.${sid}`,
      },
      (payload: any) => {
        const msg = payload.new as ChatMessage
        if (!liveMessages.value.some(m => m.id === msg.id)) {
          liveMessages.value.push(msg)
          scrollContainer(liveBodyRef.value)
        }
      }
    )
    .subscribe()
}

function formatClock(iso: string) {
  return new Date(iso).toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' })
}

onMounted(async () => {
  visitorToken.value = getOrCreateToken()
  const saved = localStorage.getItem(STORAGE_KEY)
  if (saved) {
    try {
      const parsed = JSON.parse(saved)
      if (parsed?.sessionId) {
        sessionId.value = parsed.sessionId
        formName.value = parsed.visitorName || ''
        await fetchLiveMessages()
        subscribeRealtime(parsed.sessionId)
      }
    } catch {
      localStorage.removeItem(STORAGE_KEY)
    }
  }

  pollTimer = window.setInterval(() => {
    if (isOpen.value && mode.value === 'live' && sessionId.value) {
      fetchLiveMessages()
    }
  }, 6000)
})

onUnmounted(() => {
  if (realtimeChannel) supabase.removeChannel(realtimeChannel)
  if (pollTimer) clearInterval(pollTimer)
})
</script>
