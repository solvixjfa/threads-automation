<template>
  <div class="space-y-5">
    <div class="flex flex-wrap items-center justify-between gap-3">
      <div>
        <h1 class="text-xl md:text-2xl font-bold tracking-tight">Lead Radar</h1>
        <p class="text-xs theme-text-muted mt-0.5">
          Cari postingan Threads sesuai pain-point target market, balas di komentar publik, atau simpan 1-tap ke CRM.
        </p>
      </div>

      <div class="flex items-center gap-2">
        <select v-if="connectedAccounts.length > 0" v-model="selectedAccountId" class="input text-xs font-bold py-2">
          <option v-for="acc in connectedAccounts" :key="acc.id" :value="acc.id">@{{ acc.username }}</option>
        </select>
        <button
          @click="runSearch(true)"
          :disabled="loading || !selectedAccountId"
          class="p-2 rounded-lg border theme-border theme-bg theme-text-muted hover:theme-text"
          title="Refresh hasil pencarian"
        >
          <RefreshCw class="w-4 h-4" :class="{ 'animate-spin': loading }" />
        </button>
      </div>
    </div>

    <div class="card p-4 space-y-3">
      <div class="flex flex-wrap gap-1.5">
        <button
          v-for="kw in PRESET_KEYWORDS"
          :key="kw"
          type="button"
          @click="selectPresetKeyword(kw)"
          class="px-2.5 py-1 rounded-lg text-xs font-bold border transition-colors"
          :class="keyword === kw
            ? 'bg-[var(--accent)] text-[var(--accent-text)] border-[var(--accent)]'
            : 'theme-bg-sec theme-border theme-text-muted hover:theme-text'"
        >
          {{ kw }}
        </button>
      </div>

      <form @submit.prevent="runSearch(true)" class="flex flex-col sm:flex-row gap-2">
        <div class="relative flex-1">
          <Search class="w-4 h-4 theme-text-muted absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            v-model.trim="keyword"
            type="text"
            placeholder="Ketik kata kunci pain-point (misal: ide konten threads)..."
            class="input w-full pl-9 text-sm"
            required
          />
        </div>
        <div class="flex gap-2">
          <button
            type="submit"
            :disabled="loading || !keyword || !selectedAccountId"
            class="btn btn-primary btn-sm px-4 flex items-center justify-center gap-1.5 flex-1 sm:flex-initial"
          >
            <Radar class="w-4 h-4" />
            <span>{{ loading ? 'Mencari...' : 'Cari Prospek' }}</span>
          </button>
          <a
            :href="threadsWebSearchUrl"
            target="_blank"
            rel="noopener noreferrer"
            class="btn btn-secondary btn-sm px-3 flex items-center justify-center gap-1.5 shrink-0"
          >
            <ExternalLink class="w-3.5 h-3.5" />
            <span>Buka di Threads</span>
          </a>
        </div>
      </form>
    </div>

    <div v-if="apiNotice" class="card p-4 border-amber-500/40 space-y-3">
      <div class="text-xs leading-relaxed">
        <span class="font-bold text-amber-400 block mb-1">Info API Keyword Search (Mode Developer):</span>
        <span class="theme-text-muted">{{ apiNotice }}</span>
      </div>
      <div class="flex flex-wrap items-center gap-2">
        <a :href="threadsWebSearchUrl" target="_blank" rel="noopener noreferrer" class="btn btn-primary btn-sm text-xs inline-flex items-center gap-1.5">
          <ExternalLink class="w-3.5 h-3.5" />
          <span>Cari "{{ keyword }}" Langsung di Threads</span>
        </a>
      </div>
      <form @submit.prevent="quickImportHandle" class="pt-2 border-t theme-border flex flex-col sm:flex-row gap-2">
        <input
          v-model.trim="manualHandleInput"
          type="text"
          placeholder="Temukan prospek di Threads? Paste @username atau link profil di sini..."
          class="input flex-1 text-xs"
          required
        />
        <button type="submit" :disabled="savingManual || !manualHandleInput" class="btn btn-secondary btn-sm text-xs shrink-0">
          {{ savingManual ? 'Menyimpan...' : '+ Simpan ke CRM (Comment)' }}
        </button>
      </form>
    </div>

    <div v-if="loading" class="card p-10 text-center text-xs theme-text-muted animate-pulse">
      Memindai postingan Threads terbaru untuk "{{ keyword }}"...
    </div>

    <div v-else-if="posts.length === 0 && !apiNotice" class="card p-10 text-center text-xs theme-text-muted space-y-2">
      <p>Belum ada hasil postingan untuk kata kunci ini.</p>
      <a :href="threadsWebSearchUrl" target="_blank" rel="noopener noreferrer" class="btn btn-secondary btn-sm text-xs inline-flex items-center gap-1.5">
        <ExternalLink class="w-3.5 h-3.5" />
        <span>Buka Pencarian "{{ keyword }}" di Threads</span>
      </a>
    </div>

    <div v-else-if="posts.length > 0" class="space-y-3">
      <div class="text-xs theme-text-muted px-1">
        Ditemukan <span class="font-bold theme-text">{{ posts.length }}</span> postingan relevan
      </div>

      <div v-for="post in posts" :key="post.id" class="card p-4 space-y-3">
        <div class="flex items-start justify-between gap-2">
          <div class="flex items-center gap-2 flex-wrap min-w-0">
            <a :href="post.permalink || `https://www.threads.net/@${post.username}`" target="_blank" rel="noopener noreferrer" class="font-bold text-sm hover:underline inline-flex items-center gap-1">
              @{{ post.username }}
              <ExternalLink class="w-3 h-3 theme-text-muted" />
            </a>
            <span v-if="existingHandles.has((post.username || '').toLowerCase())" class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/15 text-emerald-400 border border-emerald-500/30">
              Sudah di CRM
            </span>
            <span v-if="post.timestamp" class="text-[11px] theme-text-muted">• {{ formatRelativeTime(post.timestamp) }}</span>
          </div>
          <div class="flex items-center gap-2 text-[11px] theme-text-muted shrink-0">
            <span v-if="typeof post.like_count === 'number'">♥ {{ post.like_count }}</span>
            <span v-if="typeof post.reply_count === 'number'">💬 {{ post.reply_count }}</span>
          </div>
        </div>

        <p class="text-xs sm:text-sm leading-relaxed whitespace-pre-line theme-bg-sec p-3 rounded-xl border theme-border">{{ post.text }}</p>

        <div class="grid grid-cols-2 gap-2 pt-1">
          <a :href="post.permalink || `https://www.threads.net/@${post.username}`" target="_blank" rel="noopener noreferrer" class="btn btn-secondary btn-sm flex items-center justify-center gap-1.5 py-2">
            <MessageCircle class="w-3.5 h-3.5" />
            <span>Buka Post & Komen</span>
          </a>
          <button
            type="button"
            @click="savePostToCrm(post)"
            :disabled="savingPostId === post.id || existingHandles.has((post.username || '').toLowerCase())"
            class="btn btn-primary btn-sm flex items-center justify-center gap-1.5 py-2"
          >
            <Check v-if="existingHandles.has((post.username || '').toLowerCase())" class="w-3.5 h-3.5" />
            <UserPlus v-else class="w-3.5 h-3.5" />
            <span>{{ existingHandles.has((post.username || '').toLowerCase()) ? 'Tersimpan di CRM' : savingPostId === post.id ? 'Menyimpan...' : '+ Masuk CRM' }}</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { supabase } from '../../lib/supabase'
import { useNotify } from '../../composables/useNotify'
import { Search, RefreshCw, ExternalLink, Radar, MessageCircle, UserPlus, Check } from 'lucide-vue-next'

interface ConnectedAccount { id: string; username: string }
interface RadarPost { id: string; username: string; text: string; permalink?: string; timestamp?: string; like_count?: number; reply_count?: number }

const PRESET_KEYWORDS = ['ide konten threads', 'capek bikin konten', 'jadwalin threads', 'jualan di threads', 'naikin engagement', 'admin sosmed', 'konten kreator']
const API_BASE = 'https://threads-automation-r9so.onrender.com/api/v1'
const { showToast } = useNotify()

const connectedAccounts = ref<ConnectedAccount[]>([])
const selectedAccountId = ref('')
const keyword = ref(PRESET_KEYWORDS[0])
const posts = ref<RadarPost[]>([])
const existingHandles = ref<Set<string>>(new Set())
const loading = ref(false)
const apiNotice = ref('')
const savingPostId = ref('')
const manualHandleInput = ref('')
const savingManual = ref(false)

const threadsWebSearchUrl = computed(() => `https://www.threads.net/search?q=${encodeURIComponent(keyword.value || 'ide konten threads')}&serp_type=default`)

async function initData() {
  try {
    const { data: { session } } = await supabase.auth.getSession()
    const headers: Record<string, string> = session ? { Authorization: `Bearer ${session.access_token}` } : {}
    const [usersRes, crmRes] = await Promise.all([
      fetch(`${API_BASE}/admin/users`, { headers }),
      supabase.from('crm_leads').select('threads_handle'),
    ])
    if (usersRes.ok) {
      const json = await usersRes.json()
      const list = (json.users || []).filter((u: any) => u.connection_status === 'connected' && u.username).map((u: any) => ({ id: u.id, username: u.username }))
      connectedAccounts.value = list
      if (list.length > 0 && !selectedAccountId.value) selectedAccountId.value = list[0].id
    }
    if (!crmRes.error && crmRes.data) {
      existingHandles.value = new Set(crmRes.data.map((r: any) => String(r.threads_handle || '').toLowerCase()).filter(Boolean))
    }
    if (selectedAccountId.value) await runSearch(false)
  } catch (err: any) {
    apiNotice.value = err?.message || 'Gagal memuat akun Threads.'
  }
}

function selectPresetKeyword(kw: string) {
  keyword.value = kw
  runSearch(true)
}

async function runSearch(forceRefresh: boolean) {
  if (!selectedAccountId.value || !keyword.value) return
  loading.value = true
  apiNotice.value = ''
  try {
    const params = new URLSearchParams({ account_id: selectedAccountId.value, region: 'ID', category: 'all', q: keyword.value, limit: '25', refresh: forceRefresh ? 'true' : 'false' })
    const res = await fetch(`${API_BASE}/trending/discover?${params.toString()}`)
    const data = await res.json()
    if (!res.ok) {
      posts.value = []
      apiNotice.value = (data?.detail || 'Endpoint pencarian belum aktif.') + ' — Di Meta App Dashboard (Mode Developer), centang permission threads_keyword_search lalu reconnect akun Threads sekali. Sementara itu klik tombol di bawah untuk langsung buka pencarian di Threads.'
      return
    }
    posts.value = (data.posts || []).filter((p: RadarPost) => p.username && p.text)
    if (posts.value.length === 0) {
      apiNotice.value = 'API tidak mengembalikan hasil baru untuk kata kunci ini (atau scope threads_keyword_search belum di-reconnect). Klik tombol di bawah untuk buka langsung di Threads.'
    }
  } catch (err: any) {
    posts.value = []
    apiNotice.value = err?.message || 'Gagal menghubungi server pencarian.'
  } finally {
    loading.value = false
  }
}

async function savePostToCrm(post: RadarPost) {
  const handle = (post.username || '').replace(/^@/, '').trim()
  if (!handle) return
  savingPostId.value = post.id
  try {
    const nowIso = new Date().toISOString()
    const cleanSnippet = (post.text || '').replace(/\s+/g, ' ').trim().slice(0, 220)
    const { error } = await supabase.from('crm_leads').insert({
      threads_handle: handle,
      threads_url: `https://www.threads.net/@${handle}`,
      status: 'Not Contacted',
      outreach_channel: 'Contextual Comment',
      comm_status: 'Not Contacted',
      conversion_status: 'Potential',
      interest_level: 'High',
      pain_point: cleanSnippet,
      notes: `Lead Radar (${keyword.value})`,
      last_contacted_at: nowIso,
    })
    if (error) throw error
    existingHandles.value.add(handle.toLowerCase())
    showToast(`@${handle} masuk ke Pipeline Leads!`, 'success')
  } catch (err: any) {
    showToast('Gagal menyimpan: ' + err.message, 'error')
  } finally {
    savingPostId.value = ''
  }
}

async function quickImportHandle() {
  const raw = manualHandleInput.value.trim()
  if (!raw) return
  const match = raw.match(/threads\.(?:net|com)\/@?([a-zA-Z0-9._]+)/i)
  const handle = (match ? match[1] : raw.replace(/^@/, '').split(/[/?#]/)[0]).trim()
  if (!handle) return
  if (existingHandles.value.has(handle.toLowerCase())) {
    showToast(`@${handle} sudah ada di CRM`, 'info')
    manualHandleInput.value = ''
    return
  }
  savingManual.value = true
  try {
    const nowIso = new Date().toISOString()
    const { error } = await supabase.from('crm_leads').insert({
      threads_handle: handle,
      threads_url: `https://www.threads.net/@${handle}`,
      status: 'Not Contacted',
      outreach_channel: 'Contextual Comment',
      comm_status: 'Not Contacted',
      conversion_status: 'Potential',
      interest_level: 'High',
      notes: `Lead Radar (${keyword.value})`,
      last_contacted_at: nowIso,
    })
    if (error) throw error
    existingHandles.value.add(handle.toLowerCase())
    manualHandleInput.value = ''
    showToast(`@${handle} tersimpan ke CRM`, 'success')
  } catch (err: any) {
    showToast('Gagal menyimpan: ' + err.message, 'error')
  } finally {
    savingManual.value = ''
  }
}

function formatRelativeTime(iso: string) {
  const diffMin = Math.floor((Date.now() - new Date(iso).getTime()) / 60000)
  if (diffMin < 1) return 'Baru saja'
  if (diffMin < 60) return `${diffMin}m lalu`
  const diffHour = Math.floor(diffMin / 60)
  if (diffHour < 24) return `${diffHour}j lalu`
  return new Date(iso).toLocaleDateString('id-ID', { day: 'numeric', month: 'short' })
}

onMounted(initData)
</script>
