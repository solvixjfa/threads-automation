<template>
  <div class="space-y-4">
    <!-- HEADER -->
    <div class="flex flex-wrap items-center justify-between gap-3">
      <div>
        <h1 class="text-xl md:text-2xl font-bold tracking-tight">Email Leads</h1>
        <p class="text-xs theme-text-muted mt-0.5">
          Email pengunjung yang otomatis masuk dari formulir Live Chat ixiera.online.
        </p>
      </div>
      <div class="flex items-center gap-2">
        <button
          @click="exportCsv"
          :disabled="filteredLeads.length === 0"
          class="btn btn-secondary btn-sm text-xs flex items-center gap-1.5"
        >
          <Download class="w-3.5 h-3.5" />
          <span>Export CSV</span>
        </button>
        <button
          @click="fetchLeads"
          :disabled="loading"
          class="p-2 rounded-lg border theme-border theme-bg theme-text-muted hover:theme-text"
          title="Refresh data"
        >
          <RefreshCw class="w-4 h-4" :class="{ 'animate-spin': loading }" />
        </button>
      </div>
    </div>

    <!-- FILTER BAR -->
    <div class="card p-3 flex flex-col sm:flex-row gap-2.5">
      <div class="relative flex-1">
        <Search class="w-4 h-4 theme-text-muted absolute left-3 top-1/2 -translate-y-1/2" />
        <input
          v-model.trim="searchQuery"
          type="text"
          placeholder="Cari email, nama, atau pesan..."
          class="input w-full pl-9 text-xs"
        />
      </div>
      <select v-model="statusFilter" class="input text-xs font-bold sm:w-44">
        <option value="all">Semua ({{ leads.length }})</option>
        <option value="new">New ({{ countByStatus('new') }})</option>
        <option value="contacted">Contacted ({{ countByStatus('contacted') }})</option>
        <option value="converted">Converted ({{ countByStatus('converted') }})</option>
        <option value="unsubscribed">Unsubscribed ({{ countByStatus('unsubscribed') }})</option>
      </select>
    </div>

    <!-- LIST -->
    <div v-if="loading && leads.length === 0" class="card p-8 text-center text-xs theme-text-muted animate-pulse">
      Memuat daftar email leads...
    </div>

    <div v-else-if="filteredLeads.length === 0" class="card p-8 text-center text-xs theme-text-muted">
      Belum ada email lead pada filter ini.
    </div>

    <div v-else class="space-y-3">
      <div
        v-for="lead in filteredLeads"
        :key="lead.id"
        class="card p-4 space-y-3"
      >
        <div class="flex items-start justify-between gap-3">
          <div class="min-w-0 space-y-1">
            <div class="flex items-center gap-2 flex-wrap">
              <span class="font-bold text-sm break-all">{{ lead.email }}</span>
              <button
                @click="copyEmail(lead.email)"
                class="p-1 rounded border theme-border theme-bg-sec text-xs hover:opacity-80"
                title="Salin email"
              >
                <Check v-if="copiedEmail === lead.email" class="w-3 h-3 text-emerald-400" />
                <Copy v-else class="w-3 h-3 theme-text-muted" />
              </button>
              <span class="text-[10px] font-bold px-2 py-0.5 rounded theme-bg-sec border theme-border">
                {{ lead.visitor_name || 'Tanpa Nama' }}
              </span>
              <span
                v-if="lead.submission_count > 1"
                class="text-[10px] font-bold px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/30"
              >
                {{ lead.submission_count }}x chat
              </span>
            </div>

            <div class="text-[11px] theme-text-muted flex flex-wrap items-center gap-2">
              <span>Masuk: {{ formatDate(lead.updated_at) }}</span>
              <span v-if="lead.page_url">• {{ lead.page_url }}</span>
            </div>

            <p v-if="lead.first_message" class="text-xs theme-text-muted bg-[var(--bg-hover)] text-[var(--text-primary)] border theme-border rounded-lg px-3 py-2 mt-1.5">
              "{{ lead.first_message }}"
            </p>
          </div>

          <div class="flex items-center gap-1.5 shrink-0">
            <select
              :value="lead.status"
              @change="updateLead(lead.id, { status: ($event.target as HTMLSelectElement).value })"
              class="input text-xs font-bold py-1 px-2"
            >
              <option value="new">New</option>
              <option value="contacted">Contacted</option>
              <option value="converted">Converted</option>
              <option value="unsubscribed">Unsubscribed</option>
            </select>
            <button
              @click="deleteLead(lead.id)"
              class="p-1.5 rounded-lg border theme-border theme-text-muted hover:text-red-400"
              title="Hapus email"
            >
              <Trash2 class="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        <!-- INLINE NOTES -->
        <div class="flex gap-2">
          <input
            v-model="lead.notes"
            type="text"
            placeholder="Catatan follow-up admin..."
            class="input flex-1 text-xs py-1.5"
            @blur="updateLead(lead.id, { notes: lead.notes || '' })"
            @keyup.enter="updateLead(lead.id, { notes: lead.notes || '' })"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { supabase } from '../../lib/supabase'
import { RefreshCw, Download, Search, Copy, Check, Trash2 } from 'lucide-vue-next'

interface EmailLead {
  id: string
  email: string
  visitor_name: string | null
  source: string
  page_url: string | null
  first_message: string | null
  last_session_id: string | null
  status: 'new' | 'contacted' | 'converted' | 'unsubscribed'
  notes: string | null
  submission_count: number
  created_at: string
  updated_at: string
}

const API_BASE = 'https://threads-automation-r9so.onrender.com/api/v1/chat/admin'

const leads = ref<EmailLead[]>([])
const loading = ref(true)
const searchQuery = ref('')
const statusFilter = ref<'all' | 'new' | 'contacted' | 'converted' | 'unsubscribed'>('all')
const copiedEmail = ref('')

const filteredLeads = computed(() => {
  return leads.value.filter(l => {
    if (statusFilter.value !== 'all' && l.status !== statusFilter.value) return false
    if (!searchQuery.value) return true
    const q = searchQuery.value.toLowerCase()
    return (
      l.email.toLowerCase().includes(q) ||
      (l.visitor_name || '').toLowerCase().includes(q) ||
      (l.first_message || '').toLowerCase().includes(q)
    )
  })
})

function countByStatus(st: EmailLead['status']) {
  return leads.value.filter(l => l.status === st).length
}

async function getAuthHeaders(): Promise<Record<string, string>> {
  const { data: { session } } = await supabase.auth.getSession()
  return session
    ? { Authorization: `Bearer ${session.access_token}`, 'Content-Type': 'application/json' }
    : { 'Content-Type': 'application/json' }
}

async function fetchLeads() {
  loading.value = true
  try {
    const headers = await getAuthHeaders()
    const res = await fetch(`${API_BASE}/email-leads`, { headers })
    if (res.ok) {
      const json = await res.json()
      leads.value = (json.leads || []) as EmailLead[]
    }
  } finally {
    loading.value = false
  }
}

async function updateLead(id: string, payload: { status?: string; notes?: string }) {
  const headers = await getAuthHeaders()
  const res = await fetch(`${API_BASE}/email-leads/${id}`, {
    method: 'PATCH',
    headers,
    body: JSON.stringify(payload),
  })
  if (res.ok && payload.status) {
    const item = leads.value.find(l => l.id === id)
    if (item) item.status = payload.status as EmailLead['status']
  }
}

async function deleteLead(id: string) {
  const headers = await getAuthHeaders()
  const res = await fetch(`${API_BASE}/email-leads/${id}`, {
    method: 'DELETE',
    headers,
  })
  if (res.ok) {
    leads.value = leads.value.filter(l => l.id !== id)
  }
}

async function copyEmail(email: string) {
  await navigator.clipboard.writeText(email)
  copiedEmail.value = email
  setTimeout(() => {
    if (copiedEmail.value === email) copiedEmail.value = ''
  }, 1500)
}

function exportCsv() {
  const rows = [
    ['Email', 'Nama', 'Status', 'Sumber', 'Halaman', 'Pesan Awal', 'Waktu'],
    ...filteredLeads.value.map(l => [
      l.email,
      l.visitor_name || '',
      l.status,
      l.source,
      l.page_url || '',
      (l.first_message || '').replace(/"/g, '""'),
      l.updated_at,
    ]),
  ]
  const csv = rows.map(r => r.map(v => `"${v}"`).join(',')).join('\n')
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `ixiera-email-leads-${new Date().toISOString().slice(0, 10)}.csv`
  a.click()
  URL.revokeObjectURL(url)
}

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString('id-ID', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

onMounted(fetchLeads)
</script>
