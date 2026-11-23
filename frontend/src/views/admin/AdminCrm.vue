<template>
  <div class="space-y-6">
    <!-- HEADER -->
    <div class="flex flex-wrap justify-between items-center gap-3">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Outreach CRM</h1>
        <p class="text-xs theme-text-muted mt-0.5">Catat leads Threads yang merespons atau potensial.</p>
      </div>
      <button @click="fetchLeads" :disabled="loading" class="btn btn-secondary btn-sm flex items-center gap-1.5">
        <RefreshCw class="w-3.5 h-3.5" :class="{ 'animate-spin': loading }" />
        Refresh
      </button>
    </div>

    <!-- QUICK STATS -->
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
      <div class="card p-3.5">
        <div class="text-[11px] uppercase font-bold theme-text-muted">Total Leads</div>
        <div class="text-2xl font-black mt-1">{{ leads.length }}</div>
      </div>
      <div class="card p-3.5">
        <div class="text-[11px] uppercase font-bold theme-text-muted">Perlu Follow-up</div>
        <div class="text-2xl font-black mt-1 text-amber-500">{{ followUpCount }}</div>
      </div>
      <div class="card p-3.5">
        <div class="text-[11px] uppercase font-bold theme-text-muted">Trial</div>
        <div class="text-2xl font-black mt-1">{{ trialCount }}</div>
      </div>
      <div class="card p-3.5">
        <div class="text-[11px] uppercase font-bold theme-text-muted">Closing</div>
        <div class="text-2xl font-black mt-1 text-emerald-500">{{ closingCount }}</div>
      </div>
    </div>

    <!-- QUICK ADD FORM -->
    <form @submit.prevent="addLead" class="card p-4 space-y-3">
      <div class="text-xs font-bold uppercase tracking-wider theme-text-muted">Tambah Lead Baru</div>
      <div class="grid grid-cols-1 md:grid-cols-12 gap-3">
        <div class="md:col-span-5">
          <input
            v-model.trim="newUrl"
            type="text"
            placeholder="Paste link Threads atau @username..."
            class="input w-full text-sm"
            required
          />
        </div>
        <div class="md:col-span-5">
          <input
            v-model.trim="newNotes"
            type="text"
            placeholder="Catatan singkat (niche, respon, kebutuhan)..."
            class="input w-full text-sm"
          />
        </div>
        <div class="md:col-span-2">
          <button type="submit" :disabled="saving || !newUrl" class="btn btn-primary w-full flex items-center justify-center gap-1.5 text-sm">
            <Plus class="w-4 h-4" />
            {{ saving ? 'Saving...' : 'Simpan' }}
          </button>
        </div>
      </div>

      <!-- PILIHAN STATUS AWAL -->
      <div class="flex flex-wrap items-center gap-1.5 pt-1">
        <span class="text-[11px] theme-text-muted mr-1">Status awal:</span>
        <button
          v-for="st in STATUS_OPTIONS"
          :key="st"
          type="button"
          @click="newStatus = st"
          class="px-2.5 py-1 rounded-md text-xs font-bold border transition-colors"
          :class="newStatus === st
            ? 'bg-[var(--accent)] text-[var(--bg)] border-[var(--accent)]'
            : 'theme-border theme-text-muted hover:theme-text'"
        >
          {{ st }}
        </button>
      </div>
    </form>

    <!-- FILTER & SEARCH -->
    <div class="space-y-3">
      <div class="flex gap-1.5 overflow-x-auto pb-1">
        <button
          v-for="tab in FILTER_TABS"
          :key="tab.value"
          @click="activeFilter = tab.value"
          class="px-3 py-1.5 rounded-lg text-xs font-bold whitespace-nowrap border transition-colors"
          :class="activeFilter === tab.value
            ? 'bg-[var(--accent)] text-[var(--bg)] border-[var(--accent)]'
            : 'bg-[var(--bg)] theme-border theme-text-muted hover:theme-text'"
        >
          {{ tab.label }}
        </button>
      </div>

      <div class="relative">
        <Search class="w-4 h-4 theme-text-muted absolute left-3 top-1/2 -translate-y-1/2" />
        <input
          v-model.trim="searchQuery"
          type="text"
          placeholder="Cari @username atau isi catatan..."
          class="input w-full pl-9 text-sm"
        />
      </div>
    </div>

    <!-- STATE LOADING / DENIED / EMPTY -->
    <div v-if="loading" class="p-10 text-center text-sm theme-text-muted animate-pulse">
      Memuat data leads...
    </div>
    <div v-else-if="accessDenied" class="card p-8 text-center text-red-500 font-bold border-red-500">
      Access Denied. Cek policy RLS Supabase atau email admin kamu.
    </div>
    <div v-else-if="filteredLeads.length === 0" class="card p-10 text-center text-sm theme-text-muted">
      Belum ada data leads di filter ini.
    </div>

    <!-- LEADS LIST -->
    <div v-else class="space-y-3">
      <div
        v-for="lead in filteredLeads"
        :key="lead.id"
        class="card p-4 space-y-3 transition-colors"
      >
        <div class="flex items-start justify-between gap-3">
          <div class="min-w-0">
            <div class="flex items-center gap-2 flex-wrap">
              <a
                :href="lead.threads_url"
                target="_blank"
                rel="noopener noreferrer"
                class="font-bold text-base hover:underline inline-flex items-center gap-1"
              >
                @{{ lead.threads_handle }}
                <ExternalLink class="w-3.5 h-3.5 theme-text-muted" />
              </a>
              <span
                class="text-[10px] font-bold px-2 py-0.5 rounded uppercase"
                :class="getStatusBadgeClass(lead.status)"
              >
                {{ lead.status }}
              </span>
            </div>
            <div class="text-[11px] theme-text-muted mt-0.5">
              Kontak terakhir: {{ formatRelativeTime(lead.last_contacted_at) }}
            </div>
          </div>

          <button
            @click="deleteLead(lead)"
            class="p-1.5 rounded-lg theme-text-muted hover:text-red-500 hover:bg-[var(--bg-sec)] transition-colors shrink-0"
            title="Hapus lead"
          >
            <Trash2 class="w-4 h-4" />
          </button>
        </div>

        <!-- INLINE EDITABLE NOTES -->
        <div>
          <input
            v-model="lead.notes"
            @blur="updateNotes(lead)"
            @keyup.enter="($event.target as HTMLInputElement).blur()"
            type="text"
            placeholder="Tambah catatan..."
            class="w-full text-xs bg-[var(--bg-sec)] border theme-border rounded-lg px-3 py-2 focus:outline-none focus:border-[var(--accent)]"
          />
        </div>

        <!-- 1-TAP STATUS SWITCHER -->
        <div class="flex flex-wrap gap-1.5 pt-1">
          <button
            v-for="st in STATUS_OPTIONS"
            :key="st"
            @click="updateStatus(lead, st)"
            class="px-2.5 py-1 rounded text-[11px] font-bold border transition-colors"
            :class="lead.status === st
              ? 'bg-[var(--accent)] text-[var(--bg)] border-[var(--accent)]'
              : 'theme-border theme-text-muted hover:theme-text'"
          >
            {{ st }}
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
import { Plus, ExternalLink, Trash2, Search, RefreshCw } from 'lucide-vue-next'

interface CrmLead {
  id: string
  threads_handle: string
  threads_url: string
  status: string
  notes: string
  last_contacted_at: string
  created_at: string
}

const STATUS_OPTIONS = ['Potensial', 'Bales', 'Trial', 'Closing Pro', 'Closing BYOK', 'Skip']

const FILTER_TABS = [
  { label: 'Semua', value: 'ALL' },
  { label: 'Follow-up (>2h)', value: 'FOLLOWUP' },
  { label: 'Potensial', value: 'Potensial' },
  { label: 'Bales', value: 'Bales' },
  { label: 'Trial', value: 'Trial' },
  { label: 'Closing', value: 'CLOSING' },
  { label: 'Skip', value: 'Skip' },
]

const { showToast } = useNotify()

const leads = ref<CrmLead[]>([])
const loading = ref(true)
const saving = ref(false)
const accessDenied = ref(false)

const newUrl = ref('')
const newNotes = ref('')
const newStatus = ref('Bales')
const activeFilter = ref('ALL')
const searchQuery = ref('')

function parseThreadsInput(raw: string): { handle: string; url: string } {
  const cleaned = raw.trim()
  const match = cleaned.match(/threads\.(?:net|com)\/@([a-zA-Z0-9._]+)/i)
  if (match && match[1]) {
    const handle = match[1].toLowerCase()
    const url = cleaned.startsWith('http') ? cleaned : `https://${cleaned}`
    return { handle, url }
  }
  const handle = cleaned.replace(/^@+/, '').split('/')[0].split('?')[0].toLowerCase()
  return {
    handle,
    url: `https://www.threads.net/@${handle}`,
  }
}

function isNeedsFollowUp(lead: CrmLead): boolean {
  if (!['Potensial', 'Bales', 'Trial'].includes(lead.status)) return false
  const diffMs = Date.now() - new Date(lead.last_contacted_at).getTime()
  return diffMs > 2 * 24 * 60 * 60 * 1000
}

const followUpCount = computed(() => leads.value.filter(isNeedsFollowUp).length)
const trialCount = computed(() => leads.value.filter(l => l.status === 'Trial').length)
const closingCount = computed(() =>
  leads.value.filter(l => l.status === 'Closing Pro' || l.status === 'Closing BYOK').length
)

const filteredLeads = computed(() => {
  return leads.value.filter(lead => {
    if (activeFilter.value === 'FOLLOWUP' && !isNeedsFollowUp(lead)) return false
    if (activeFilter.value === 'CLOSING' && !['Closing Pro', 'Closing BYOK'].includes(lead.status)) return false
    if (
      !['ALL', 'FOLLOWUP', 'CLOSING'].includes(activeFilter.value) &&
      lead.status !== activeFilter.value
    ) {
      return false
    }

    if (searchQuery.value) {
      const q = searchQuery.value.toLowerCase().replace(/^@/, '')
      const inHandle = lead.threads_handle.toLowerCase().includes(q)
      const inNotes = (lead.notes || '').toLowerCase().includes(q)
      if (!inHandle && !inNotes) return false
    }

    return true
  })
})

function getStatusBadgeClass(status: string) {
  if (status.startsWith('Closing')) return 'bg-emerald-500/15 text-emerald-500'
  if (status === 'Trial') return 'bg-blue-500/15 text-blue-500'
  if (status === 'Bales') return 'bg-amber-500/15 text-amber-500'
  if (status === 'Skip') return 'bg-red-500/10 text-red-400'
  return 'bg-[var(--bg-sec)] theme-text-muted'
}

function formatRelativeTime(iso: string) {
  if (!iso) return '-'
  const diffSec = Math.floor((Date.now() - new Date(iso).getTime()) / 1000)
  if (diffSec < 60) return 'Baru saja'
  const diffMin = Math.floor(diffSec / 60)
  if (diffMin < 60) return `${diffMin} menit lalu`
  const diffHour = Math.floor(diffMin / 60)
  if (diffHour < 24) return `${diffHour} jam lalu`
  const diffDay = Math.floor(diffHour / 24)
  return `${diffDay} hari lalu`
}

async function fetchLeads() {
  loading.value = true
  accessDenied.value = false
  try {
    const { data, error } = await supabase
      .from('crm_leads')
      .select('*')
      .order('last_contacted_at', { ascending: false })

    if (error) {
      if (error.code === '42501' || error.message.toLowerCase().includes('permission')) {
        accessDenied.value = true
        return
      }
      throw error
    }
    leads.value = (data || []) as CrmLead[]
  } catch (err: any) {
    showToast('Gagal memuat CRM: ' + err.message, 'error')
  } finally {
    loading.value = false
  }
}

async function addLead() {
  if (!newUrl.value) return
  const { handle, url } = parseThreadsInput(newUrl.value)
  if (!handle) {
    showToast('Format link atau username tidak valid', 'error')
    return
  }

  const existing = leads.value.find(l => l.threads_handle === handle)
  if (existing) {
    showToast(`@${handle} sudah ada di list (Status: ${existing.status})`, 'error')
    searchQuery.value = handle
    activeFilter.value = 'ALL'
    return
  }

  saving.value = true
  try {
    const nowIso = new Date().toISOString()
    const { data, error } = await supabase
      .from('crm_leads')
      .insert({
        threads_handle: handle,
        threads_url: url,
        status: newStatus.value,
        notes: newNotes.value,
        last_contacted_at: nowIso,
      })
      .select()
      .single()

    if (error) throw error
    if (data) {
      leads.value.unshift(data as CrmLead)
    }
    newUrl.value = ''
    newNotes.value = ''
    showToast(`@${handle} ditambahkan`, 'success')
  } catch (err: any) {
    showToast('Gagal menyimpan: ' + err.message, 'error')
  } finally {
    saving.value = false
  }
}

async function updateStatus(lead: CrmLead, status: string) {
  if (lead.status === status) return
  const prevStatus = lead.status
  const prevTime = lead.last_contacted_at
  const nowIso = new Date().toISOString()

  lead.status = status
  lead.last_contacted_at = nowIso

  try {
    const { error } = await supabase
      .from('crm_leads')
      .update({ status, last_contacted_at: nowIso })
      .eq('id', lead.id)

    if (error) throw error
    showToast(`@${lead.threads_handle} -> ${status}`, 'success')
  } catch (err: any) {
    lead.status = prevStatus
    lead.last_contacted_at = prevTime
    showToast('Gagal update status: ' + err.message, 'error')
  }
}

async function updateNotes(lead: CrmLead) {
  try {
    const { error } = await supabase
      .from('crm_leads')
      .update({ notes: lead.notes })
      .eq('id', lead.id)

    if (error) throw error
  } catch (err: any) {
    showToast('Gagal simpan catatan: ' + err.message, 'error')
  }
}

async function deleteLead(lead: CrmLead) {
  if (!confirm(`Hapus @${lead.threads_handle} dari CRM?`)) return
  try {
    const { error } = await supabase.from('crm_leads').delete().eq('id', lead.id)
    if (error) throw error
    leads.value = leads.value.filter(l => l.id !== lead.id)
    showToast(`@${lead.threads_handle} dihapus`, 'success')
  } catch (err: any) {
    showToast('Gagal menghapus: ' + err.message, 'error')
  }
}

onMounted(fetchLeads)
</script>
