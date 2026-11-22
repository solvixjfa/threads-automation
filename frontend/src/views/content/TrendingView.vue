<template>
  <div class="space-y-6 w-full max-w-full overflow-hidden">
    <div class="flex flex-wrap items-center justify-between gap-3">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Trending Topics</h1>
        <p class="text-xs theme-text-muted mt-1">
          Temukan topik tren & postingan viral, cek profil kreator, balas 1-klik dengan AI, atau jalankan auto-comment terukur.
        </p>
      </div>

      <div class="flex items-center gap-2 p-1 rounded-xl border theme-border theme-bg-sec">
        <button
          type="button"
          @click="activeTab = 'discover'"
          class="px-3 py-1.5 rounded-lg text-xs font-bold transition"
          :class="activeTab === 'discover' ? 'bg-[var(--text)] text-[var(--bg)]' : 'theme-text-muted hover:theme-text'"
        >
          Discover & AI Reply
        </button>
        <button
          type="button"
          @click="activeTab = 'auto'"
          class="px-3 py-1.5 rounded-lg text-xs font-bold transition"
          :class="activeTab === 'auto' ? 'bg-[var(--text)] text-[var(--bg)]' : 'theme-text-muted hover:theme-text'"
        >
          Auto-Comment
        </button>
      </div>
    </div>

    <!-- DISCOVER TAB -->
    <div v-if="activeTab === 'discover'" class="space-y-5">
      <Card>
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div>
            <label class="text-[11px] font-bold uppercase tracking-wide theme-text-muted block mb-1">Wilayah</label>
            <select v-model="region" class="input text-xs w-full">
              <option value="ID">Indonesia (ID)</option>
              <option value="GLOBAL">Global</option>
            </select>
          </div>
          <div>
            <label class="text-[11px] font-bold uppercase tracking-wide theme-text-muted block mb-1">Kategori</label>
            <select v-model="category" class="input text-xs w-full">
              <option value="all">Semua Topik</option>
              <option value="tech">Teknologi & AI</option>
              <option value="business">Bisnis & Marketing</option>
              <option value="finance">Keuangan & Investasi</option>
              <option value="lifestyle">Produktivitas & Karir</option>
            </select>
          </div>
          <div>
            <label class="text-[11px] font-bold uppercase tracking-wide theme-text-muted block mb-1">Kata Kunci</label>
            <div class="flex gap-2">
              <input
                v-model="searchQuery"
                @keyup.enter="loadTrending(false, false)"
                type="text"
                placeholder="Cari topik atau keyword..."
                class="input text-xs flex-1 min-w-0"
              />
              <Button size="sm" @click="loadTrending(false, false)" :loading="loadingPosts">Cari</Button>
              <Button size="sm" variant="secondary" @click="loadTrending(true, false)" :loading="loadingPosts">Refresh</Button>
            </div>
          </div>
        </div>

        <div class="flex flex-wrap items-center justify-between gap-2 mt-3 pt-3 border-t theme-border">
          <div class="flex flex-wrap items-center gap-1.5">
            <button
              v-for="chip in quickTopics"
              :key="chip"
              type="button"
              @click="selectQuickTopic(chip)"
              class="px-2.5 py-1 rounded-full text-[11px] font-medium border theme-border theme-bg-sec hover:opacity-85 transition"
            >
              #{{ chip }}
            </button>
          </div>
          <span v-if="cacheInfo" class="text-[11px] theme-text-muted">
            {{ cacheInfo }}
          </span>
        </div>
      </Card>

      <div v-if="sandboxOnly" class="p-3.5 rounded-xl border theme-border theme-bg-sec text-xs theme-text-muted">
        Info Meta API: Izin <strong>threads_keyword_search</strong> masih dalam mode Development/Pre-Review sehingga Meta hanya menampilkan postingan dari akun tester aplikasi. Setelah disetujui Meta App Review, postingan publik seluruh kreator Threads akan otomatis muncul.
      </div>

      <div v-if="loadingPosts" class="grid grid-cols-1 gap-3">
        <div v-for="n in 3" :key="n" class="card p-5 animate-pulse h-32"></div>
      </div>

      <EmptyState
        v-else-if="posts.length === 0"
        title="Belum ada data tren di cache"
        description="Pilih kategori atau ketik kata kunci lalu klik Cari untuk memuat hasil."
      />

      <div v-else class="space-y-3">
        <Card v-for="post in posts" :key="post.id" class="space-y-3">
          <div class="flex items-start justify-between gap-3">
            <div class="min-w-0">
              <div class="flex flex-wrap items-center gap-2">
                <button
                  type="button"
                  @click="openCreatorProfile(post.username)"
                  class="text-xs font-bold hover:underline truncate"
                >
                  @{{ post.username }}
                </button>
                <Badge v-if="post.topic_tag" variant="default">{{ post.topic_tag }}</Badge>
                <Badge v-if="post.already_replied" variant="accent">Sudah Dibalas</Badge>
              </div>
              <p v-if="post.timestamp" class="text-[11px] theme-text-muted mt-0.5">
                {{ formatDate(post.timestamp) }}
              </p>
            </div>
            <a
              v-if="post.permalink"
              :href="post.permalink"
              target="_blank"
              rel="noopener noreferrer"
              class="text-xs font-bold theme-text-muted hover:theme-text shrink-0"
            >
              Buka Post
            </a>
          </div>

          <p class="text-sm whitespace-pre-wrap leading-relaxed break-words">
            {{ post.text || '(Media post tanpa teks)' }}
          </p>

          <div class="flex flex-wrap items-center justify-between gap-2 pt-2 border-t theme-border">
            <div class="flex items-center gap-2">
              <Button
                size="sm"
                variant="secondary"
                :disabled="!post.text || generatingId === post.id"
                :loading="generatingId === post.id"
                @click="prepareAiReply(post)"
              >
                AI Reply
              </Button>
              <Button
                size="sm"
                variant="secondary"
                :disabled="!post.text"
                @click="sendToComposer(post)"
              >
                Jadikan Draf
              </Button>
            </div>
            <button
              type="button"
              @click="openCreatorProfile(post.username)"
              class="text-[11px] font-bold theme-text-muted hover:theme-text"
            >
              Lihat Profil
            </button>
          </div>

          <div v-if="activeReplyPostId === post.id" class="p-3.5 rounded-xl border theme-border theme-bg-sec space-y-2.5">
            <div class="flex items-center justify-between gap-2">
              <span class="text-[11px] font-bold uppercase tracking-wide theme-text-muted">Draf Balasan AI</span>
              <select v-model="replyStyle" class="input text-xs py-1 px-2" style="width: auto;">
                <option value="insight">Tambah Insight</option>
                <option value="question">Tanya Balik</option>
                <option value="value">Tips Singkat</option>
              </select>
            </div>
            <textarea
              v-model="draftReplyText"
              rows="3"
              class="textarea text-xs w-full"
              placeholder="Tulis atau edit balasan sebelum dikirim..."
            ></textarea>
            <div class="flex justify-end gap-2">
              <Button size="sm" variant="secondary" @click="activeReplyPostId = null">Batal</Button>
              <Button
                size="sm"
                :disabled="post.already_replied || !draftReplyText.trim() || sendingReplyId === post.id"
                :loading="sendingReplyId === post.id"
                @click="confirmSendReply(post)"
              >
                {{ post.already_replied ? 'Sudah Dibalas' : 'Kirim Balasan' }}
              </Button>
            </div>
          </div>
        </Card>
      </div>
    </div>

    <!-- AUTO-COMMENT TAB -->
    <div v-else class="space-y-5">
      <Card class="space-y-4">
        <div class="flex items-center justify-between gap-3">
          <div>
            <h2 class="text-sm font-bold uppercase tracking-wide">Aturan Auto-Comment</h2>
            <p class="text-xs theme-text-muted mt-0.5">
              Batas maksimal 1–10 komentar/jam, anti-duplikat per postingan, dan otomatis patuh pada Kill Switch akun.
            </p>
          </div>
          <label class="flex items-center gap-2 text-xs font-bold cursor-pointer">
            <input type="checkbox" v-model="campaign.is_active" class="w-4 h-4 rounded" />
            <span>{{ campaign.is_active ? 'Aktif' : 'Nonaktif' }}</span>
          </label>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div>
            <label class="text-[11px] font-bold uppercase tracking-wide theme-text-muted block mb-1">Wilayah Target</label>
            <select v-model="campaign.region" class="input text-xs w-full">
              <option value="ID">Indonesia (ID)</option>
              <option value="GLOBAL">Global</option>
            </select>
          </div>
          <div>
            <label class="text-[11px] font-bold uppercase tracking-wide theme-text-muted block mb-1">Kategori</label>
            <select v-model="campaign.category" class="input text-xs w-full">
              <option value="all">Semua Topik</option>
              <option value="tech">Teknologi & AI</option>
              <option value="business">Bisnis & Marketing</option>
              <option value="finance">Keuangan & Investasi</option>
              <option value="lifestyle">Produktivitas & Karir</option>
            </select>
          </div>
          <div>
            <label class="text-[11px] font-bold uppercase tracking-wide theme-text-muted block mb-1">Maks / Jam</label>
            <input v-model.number="campaign.max_per_hour" type="number" min="1" max="10" class="input text-xs w-full" />
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label class="text-[11px] font-bold uppercase tracking-wide theme-text-muted block mb-1">Keywords (pisah koma)</label>
            <input v-model="keywordsInput" type="text" placeholder="contoh: saas, ai tools, jualan online" class="input text-xs w-full" />
          </div>
          <div>
            <label class="text-[11px] font-bold uppercase tracking-wide theme-text-muted block mb-1">Gaya Balasan</label>
            <select v-model="campaign.reply_style" class="input text-xs w-full">
              <option value="insight">Tambah Insight</option>
              <option value="question">Tanya Balik</option>
              <option value="value">Tips Singkat</option>
            </select>
          </div>
        </div>

        <div class="flex flex-wrap justify-end gap-2 pt-2 border-t theme-border">
          <Button variant="secondary" @click="saveCampaign" :loading="savingCampaign">Simpan Aturan</Button>
          <Button @click="runCampaignNow" :loading="runningCampaign">Jalankan Sekarang</Button>
        </div>
      </Card>

      <Card class="space-y-3">
        <div class="flex items-center justify-between">
          <h2 class="text-sm font-bold uppercase tracking-wide">Riwayat Balasan & Outreach</h2>
          <button type="button" @click="loadLogs" class="text-xs font-bold theme-text-muted hover:theme-text">Refresh</button>
        </div>

        <div v-if="logs.length === 0" class="text-xs theme-text-muted py-4">
          Belum ada riwayat balasan dari menu Trending.
        </div>

        <div v-else class="space-y-2.5">
          <div v-for="item in logs" :key="item.id" class="p-3 rounded-xl border theme-border theme-bg-sec space-y-1">
            <div class="flex items-center justify-between gap-2 text-[11px]">
              <span class="font-bold">@{{ item.target_username || 'creator' }} • {{ item.mode }}</span>
              <span class="theme-text-muted">{{ formatDate(item.created_at) }}</span>
            </div>
            <p class="text-xs break-words">{{ item.reply_text }}</p>
          </div>
        </div>
      </Card>
    </div>

    <!-- CREATOR PROFILE MODAL -->
    <Teleport to="body">
      <div v-if="selectedProfile" class="fixed inset-0 z-[100] flex items-center justify-center p-4" style="background: rgba(0,0,0,0.65);">
        <div class="card max-w-md w-full p-5 space-y-3 shadow-2xl" style="background: var(--bg);">
          <div class="flex items-center justify-between pb-2 border-b theme-border">
            <h3 class="text-sm font-bold">@{{ selectedProfile.username }}</h3>
            <button type="button" @click="selectedProfile = null" class="text-xs font-bold theme-text-muted hover:theme-text">Tutup</button>
          </div>
          <p class="text-xs font-bold">{{ selectedProfile.name }}</p>
          <p v-if="selectedProfile.followers_count !== null && selectedProfile.followers_count !== undefined" class="text-[11px] theme-text-muted">
            Followers: {{ selectedProfile.followers_count }}
          </p>
          <p class="text-xs whitespace-pre-wrap leading-relaxed theme-text-muted">
            {{ selectedProfile.bio || 'Tidak ada bio publik.' }}
          </p>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { supabase } from '../../lib/supabase'
import { useNotify } from '../../composables/useNotify'
import { Card, Button, Badge, EmptyState } from '../../components/ui'

const API_BASE = 'https://threads-automation-r9so.onrender.com/api/v1/trending'
const router = useRouter()
const { showToast } = useNotify()

const accountId = ref<string | null>(null)
const activeTab = ref<'discover' | 'auto'>('discover')

const region = ref('ID')
const category = ref('all')
const searchQuery = ref('')
const quickTopics = ['AI', 'Bisnis', 'Startup', 'Marketing', 'Produktivitas']

const loadingPosts = ref(false)
const posts = ref<any[]>([])
const cacheInfo = ref('')
const sandboxOnly = ref(false)

const generatingId = ref<string | null>(null)
const activeReplyPostId = ref<string | null>(null)
const replyStyle = ref('insight')
const draftReplyText = ref('')
const sendingReplyId = ref<string | null>(null)

const selectedProfile = ref<any | null>(null)

const campaign = ref<any>({
  id: null,
  name: 'Auto Outreach',
  region: 'ID',
  category: 'all',
  keywords: [],
  reply_style: 'insight',
  max_per_hour: 3,
  is_active: false,
})
const keywordsInput = ref('')
const savingCampaign = ref(false)
const runningCampaign = ref(false)
const logs = ref<any[]>([])

function formatDate(iso: string) {
  if (!iso) return ''
  try {
    return new Date(iso).toLocaleString('id-ID', { dateStyle: 'short', timeStyle: 'short' })
  } catch {
    return iso
  }
}

async function resolveAccountId() {
  if (accountId.value) return accountId.value
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) throw new Error('User belum login')
  const { data: acc } = await supabase
    .schema('threads')
    .from('threads_accounts')
    .select('id')
    .eq('user_id', user.id)
    .maybeSingle()
  if (!acc?.id) throw new Error('Akun Threads belum terhubung')
  accountId.value = acc.id
  return acc.id
}

async function loadTrending(forceRefresh = false, cacheOnly = false) {
  loadingPosts.value = true
  try {
    const accId = await resolveAccountId()
    const params = new URLSearchParams({
      account_id: accId,
      region: region.value,
      category: category.value,
      q: searchQuery.value.trim(),
      limit: '20',
      refresh: forceRefresh ? 'true' : 'false',
      cache_only: cacheOnly ? 'true' : 'false',
    })
    const res = await fetch(`${API_BASE}/discover?${params.toString()}`)
    const data = await res.json()
    if (!res.ok) throw new Error(data.detail || 'Gagal memuat topik tren')
    posts.value = data.posts || []
    sandboxOnly.value = Boolean(data.sandbox_only)
    cacheInfo.value = data.cached ? 'Dari cache database (hemat kuota)' : 'Live dari Threads API (tersimpan ke cache 60 mnt)'
  } catch (err: any) {
    showToast(err.message || 'Gagal memuat trending', 'error')
  } finally {
    loadingPosts.value = false
  }
}

function selectQuickTopic(topic: string) {
  searchQuery.value = topic
  loadTrending(false, false)
}

async function openCreatorProfile(username: string) {
  if (!username) return
  try {
    const accId = await resolveAccountId()
    const res = await fetch(`${API_BASE}/profile/${encodeURIComponent(username)}?account_id=${accId}`)
    const data = await res.json()
    if (!res.ok) throw new Error(data.detail || 'Gagal memuat profil kreator')
    selectedProfile.value = data.profile
  } catch (err: any) {
    showToast(err.message || 'Gagal memuat profil', 'error')
  }
}

async function prepareAiReply(post: any) {
  generatingId.value = post.id
  activeReplyPostId.value = post.id
  try {
    const accId = await resolveAccountId()
    const res = await fetch(`${API_BASE}/generate-reply`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        account_id: accId,
        target_text: post.text,
        target_username: post.username || 'creator',
        reply_style: replyStyle.value,
      }),
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.detail || 'Gagal membuat draf balasan')
    draftReplyText.value = data.reply_text || ''
  } catch (err: any) {
    showToast(err.message || 'Gagal generate AI reply', 'error')
  } finally {
    generatingId.value = null
  }
}

async function confirmSendReply(post: any) {
  sendingReplyId.value = post.id
  try {
    const accId = await resolveAccountId()
    const res = await fetch(`${API_BASE}/reply`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        account_id: accId,
        target_media_id: post.id,
        reply_text: draftReplyText.value.trim(),
        target_username: post.username || '',
        target_text: post.text || '',
        target_permalink: post.permalink || '',
        mode: 'manual',
      }),
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.detail || 'Gagal mengirim balasan')
    post.already_replied = true
    activeReplyPostId.value = null
    draftReplyText.value = ''
    showToast('Balasan terkirim ke Threads!', 'success')
    await loadLogs()
  } catch (err: any) {
    showToast(err.message || 'Gagal kirim balasan', 'error')
  } finally {
    sendingReplyId.value = null
  }
}

function sendToComposer(post: any) {
  localStorage.setItem('draft_repurpose', post.text || '')
  router.push('/content/create')
}

async function loadCampaignAndLogs() {
  try {
    const accId = await resolveAccountId()
    const [campRes, logsRes] = await Promise.all([
      fetch(`${API_BASE}/campaigns?account_id=${accId}`),
      fetch(`${API_BASE}/logs?account_id=${accId}&limit=30`),
    ])
    const campData = await campRes.json()
    if (campRes.ok && campData.campaigns?.length) {
      const first = campData.campaigns[0]
      campaign.value = { ...first }
      keywordsInput.value = (first.keywords || []).join(', ')
    }
    const logsData = await logsRes.json()
    if (logsRes.ok) {
      logs.value = logsData.logs || []
    }
  } catch (err: any) {
    console.error(err)
  }
}

async function loadLogs() {
  try {
    const accId = await resolveAccountId()
    const res = await fetch(`${API_BASE}/logs?account_id=${accId}&limit=30`)
    const data = await res.json()
    if (res.ok) logs.value = data.logs || []
  } catch (err) {
    console.error(err)
  }
}

async function saveCampaign() {
  savingCampaign.value = true
  try {
    const accId = await resolveAccountId()
    const kwList = keywordsInput.value
      .split(',')
      .map((s) => s.trim())
      .filter(Boolean)
    const res = await fetch(`${API_BASE}/campaigns`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        id: campaign.value.id,
        account_id: accId,
        name: campaign.value.name || 'Auto Outreach',
        region: campaign.value.region,
        category: campaign.value.category,
        keywords: kwList,
        reply_style: campaign.value.reply_style,
        max_per_hour: campaign.value.max_per_hour,
        is_active: campaign.value.is_active,
      }),
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.detail || 'Gagal menyimpan aturan')
    if (data.campaign) campaign.value = { ...data.campaign }
    showToast('Aturan Auto-Comment tersimpan!', 'success')
  } catch (err: any) {
    showToast(err.message || 'Gagal simpan aturan', 'error')
  } finally {
    savingCampaign.value = false
  }
}

async function runCampaignNow() {
  runningCampaign.value = true
  try {
    const accId = await resolveAccountId()
    const res = await fetch(`${API_BASE}/campaigns/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ account_id: accId }),
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.detail || 'Gagal menjalankan auto-comment')
    showToast(`Selesai: ${data.sent ?? 0} balasan terkirim, ${data.skipped ?? 0} dilewati.`, 'success')
    await loadLogs()
  } catch (err: any) {
    showToast(err.message || 'Gagal menjalankan auto-comment', 'error')
  } finally {
    runningCampaign.value = false
  }
}

onMounted(async () => {
  await Promise.all([loadTrending(false, true), loadCampaignAndLogs()])
})
</script>
