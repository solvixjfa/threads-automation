<template>
  <div class="space-y-5">
    <!-- HEADER -->
    <div class="flex items-center justify-between gap-3">
      <div>
        <h1 class="text-xl md:text-2xl font-bold tracking-tight">Pipeline Leads</h1>
        <p class="text-xs theme-text-muted mt-0.5">
          {{ leads.length }} total leads • <span class="text-amber-500 font-bold">{{ dueFollowUpCount }} perlu follow-up</span>
        </p>
      </div>

      <div class="flex items-center gap-2">
        <button
          @click="fetchLeads"
          :disabled="loading"
          class="p-2 rounded-lg border theme-border bg-[var(--bg)] theme-text-muted hover:theme-text"
          title="Refresh data"
        >
          <RefreshCw class="w-4 h-4" :class="{ 'animate-spin': loading }" />
        </button>

        <button
          @click="openCreateLeadModal"
          class="btn btn-primary btn-sm flex items-center gap-1.5 px-3.5 py-2"
        >
          <Plus class="w-4 h-4" />
          <span>Lead Baru</span>
        </button>
      </div>
    </div>

    <!-- ULTRA-FAST QUICK PASTE BAR -->
    <form @submit.prevent="quickAddLead" class="card p-3 flex flex-col sm:flex-row gap-2">
      <input
        v-model.trim="quickUrl"
        type="text"
        placeholder="Paste link Threads atau @username lalu simpan..."
        class="input flex-1 text-sm"
        required
      />
      <div class="flex gap-2">
        <select v-model="quickChannel" class="input text-xs font-bold flex-1 sm:w-40">
          <option v-for="ch in CHANNEL_OPTIONS" :key="ch" :value="ch">{{ ch }}</option>
        </select>
        <button type="submit" :disabled="saving || !quickUrl" class="btn btn-primary btn-sm px-4 shrink-0">
          {{ saving ? '...' : 'Simpan' }}
        </button>
      </div>
    </form>

    <!-- FOLLOW-UP PILLS & SEARCH -->
    <div class="space-y-2.5">
      <div class="flex gap-1.5 overflow-x-auto pb-1">
        <button
          v-for="tab in FOLLOWUP_TABS"
          :key="tab.value"
          @click="followUpFilter = tab.value"
          class="px-3 py-1.5 rounded-lg text-xs font-bold whitespace-nowrap border transition-colors flex items-center gap-1.5"
          :class="followUpFilter === tab.value
            ? 'bg-[var(--accent)] text-[var(--bg)] border-[var(--accent)]'
            : 'bg-[var(--bg)] theme-border theme-text-muted hover:theme-text'"
        >
          <span>{{ tab.label }}</span>
          <span class="text-[10px] opacity-80">({{ getFollowUpTabCount(tab.value) }})</span>
        </button>
      </div>

      <div class="flex gap-2">
        <div class="relative flex-1">
          <Search class="w-4 h-4 theme-text-muted absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            v-model.trim="searchQuery"
            type="text"
            placeholder="Cari @username, niche, atau catatan..."
            class="input w-full pl-9 text-sm"
          />
        </div>

        <button
          type="button"
          @click="showFilters = !showFilters"
          class="btn btn-secondary btn-sm px-3 flex items-center gap-1.5 shrink-0"
          :class="{ 'border-[var(--accent)]': activeFilterCount > 0 }"
        >
          <SlidersHorizontal class="w-3.5 h-3.5" />
          <span>Filter</span>
          <span v-if="activeFilterCount > 0" class="px-1.5 py-0.2 rounded-full text-[10px] bg-[var(--accent)] text-[var(--bg)]">
            {{ activeFilterCount }}
          </span>
        </button>
      </div>

      <!-- COLLAPSIBLE ADVANCED FILTERS -->
      <div v-if="showFilters" class="card p-3 grid grid-cols-1 sm:grid-cols-3 gap-2">
        <div>
          <label class="block text-[10px] font-bold uppercase theme-text-muted mb-1">Komunikasi</label>
          <select v-model="commFilter" class="input w-full text-xs">
            <option value="ALL">Semua Komunikasi</option>
            <option v-for="cs in COMM_STATUS_OPTIONS" :key="cs" :value="cs">{{ cs }}</option>
          </select>
        </div>
        <div>
          <label class="block text-[10px] font-bold uppercase theme-text-muted mb-1">Konversi</label>
          <select v-model="convFilter" class="input w-full text-xs">
            <option value="ALL">Semua Konversi</option>
            <option v-for="cv in CONV_STATUS_OPTIONS" :key="cv" :value="cv">{{ cv }}</option>
          </select>
        </div>
        <div>
          <label class="block text-[10px] font-bold uppercase theme-text-muted mb-1">Channel</label>
          <select v-model="channelFilter" class="input w-full text-xs">
            <option value="ALL">Semua Channel</option>
            <option v-for="ch in CHANNEL_OPTIONS" :key="ch" :value="ch">{{ ch }}</option>
          </select>
        </div>
      </div>
    </div>

    <!-- LOADING / DENIED / EMPTY -->
    <div v-if="loading" class="p-10 text-center text-sm theme-text-muted animate-pulse">
      Memuat daftar leads...
    </div>
    <div v-else-if="accessDenied" class="card p-8 text-center text-red-500 font-bold border-red-500 text-sm">
      Access Denied. Pastikan login dengan akun admin yang terdaftar di RLS Supabase.
    </div>
    <div v-else-if="filteredLeads.length === 0" class="card p-10 text-center text-sm theme-text-muted">
      Tidak ada lead yang sesuai dengan filter saat ini.
    </div>

    <!-- LEADS CARDS -->
    <div v-else class="space-y-3">
      <div
        v-for="lead in filteredLeads"
        :key="lead.id"
        class="card p-4 space-y-3"
      >
        <!-- CARD HEADER -->
        <div class="flex items-start justify-between gap-2">
          <div class="min-w-0 space-y-1">
            <div class="flex items-center gap-1.5 flex-wrap">
              <a
                :href="lead.threads_url"
                target="_blank"
                rel="noopener noreferrer"
                class="font-bold text-base hover:underline inline-flex items-center gap-1"
              >
                @{{ lead.threads_handle }}
                <ExternalLink class="w-3.5 h-3.5 theme-text-muted" />
              </a>

              <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-[var(--bg-sec)] border theme-border">
                {{ lead.outreach_channel || 'Cold DM' }}
              </span>

              <span
                class="text-[10px] font-bold px-2 py-0.5 rounded"
                :class="getInterestBadgeClass(lead.interest_level)"
              >
                {{ lead.interest_level || 'Medium' }}
              </span>

              <span v-if="lead.niche" class="text-[10px] px-2 py-0.5 rounded bg-[var(--bg-sec)] theme-text-muted">
                {{ lead.niche }}
              </span>
            </div>

            <div class="flex flex-wrap items-center gap-2 text-[11px] theme-text-muted">
              <span>Update: {{ formatRelativeTime(lead.last_contacted_at) }}</span>
              <span v-if="lead.next_followup_at" :class="getFollowUpBadgeClass(lead)" class="font-bold px-1.5 py-0.5 rounded">
                {{ getFollowUpLabel(lead) }} • {{ formatDateTime(lead.next_followup_at) }}
              </span>
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

        <!-- CONTEXT (ONLY IF FILLED) -->
        <div v-if="lead.pain_point || lead.next_action" class="space-y-1.5 text-xs bg-[var(--bg-sec)] p-2.5 rounded-lg border theme-border">
          <div v-if="lead.pain_point">
            <span class="font-bold theme-text-muted">Pain:</span> {{ lead.pain_point }}
          </div>
          <div v-if="lead.next_action">
            <span class="font-bold theme-text-muted">Next:</span> {{ lead.next_action }}
          </div>
        </div>

        <!-- INLINE QUICK NOTE -->
        <input
          v-model="lead.notes"
          @blur="saveQuickNotes(lead)"
          @keyup.enter="($event.target as HTMLInputElement).blur()"
          type="text"
          placeholder="Tulis catatan singkat..."
          class="w-full text-xs bg-[var(--bg-sec)] border theme-border rounded-lg px-3 py-2 focus:outline-none focus:border-[var(--accent)]"
        />

        <!-- DUAL STATUS SELECTORS -->
        <div class="grid grid-cols-2 gap-2">
          <div>
            <label class="block text-[10px] uppercase font-bold theme-text-muted mb-1">Komunikasi</label>
            <select
              :value="lead.comm_status"
              @change="updateLeadField(lead, 'comm_status', ($event.target as HTMLSelectElement).value)"
              class="input w-full text-xs font-bold py-2"
            >
              <option v-for="cs in COMM_STATUS_OPTIONS" :key="cs" :value="cs">{{ cs }}</option>
            </select>
          </div>
          <div>
            <label class="block text-[10px] uppercase font-bold theme-text-muted mb-1">Konversi</label>
            <select
              :value="lead.conversion_status"
              @change="updateLeadField(lead, 'conversion_status', ($event.target as HTMLSelectElement).value)"
              class="input w-full text-xs font-bold py-2"
            >
              <option v-for="cv in CONV_STATUS_OPTIONS" :key="cv" :value="cv">{{ cv }}</option>
            </select>
          </div>
        </div>

        <!-- CARD ACTIONS -->
        <div class="grid grid-cols-2 gap-2 pt-2 border-t theme-border">
          <button
            @click="openHistoryModal(lead)"
            class="btn btn-primary btn-sm flex items-center justify-center gap-1.5 py-2.5"
          >
            <History class="w-3.5 h-3.5" />
            <span>Riwayat ({{ interactionCounts[lead.id] || 0 }})</span>
          </button>

          <button
            @click="openEditLeadModal(lead)"
            class="btn btn-secondary btn-sm flex items-center justify-center gap-1.5 py-2.5"
          >
            <Edit3 class="w-3.5 h-3.5" />
            <span>Edit & Jadwal FU</span>
          </button>
        </div>
      </div>
    </div>

    <!-- MODAL CREATE / EDIT LEAD -->
    <Teleport to="body">
      <div v-if="showLeadModal" class="fixed inset-0 z-[100] flex items-end sm:items-center justify-center p-0 sm:p-4 bg-black/60 backdrop-blur-sm">
        <div class="card w-full sm:max-w-lg rounded-t-2xl sm:rounded-2xl p-5 space-y-4 bg-[var(--bg)] max-h-[92dvh] overflow-y-auto">
          <div class="flex items-center justify-between">
            <h3 class="text-base font-bold">
              {{ editingLead ? `Edit @${editingLead.threads_handle}` : 'Tambah Lead Baru' }}
            </h3>
            <button @click="closeLeadModal" class="p-1.5 theme-text-muted hover:theme-text">
              <X class="w-5 h-5" />
            </button>
          </div>

          <form @submit.prevent="saveLeadModal" class="space-y-3">
            <div>
              <label class="block text-xs font-bold mb-1">Link Threads atau @Username *</label>
              <input
                v-model.trim="leadForm.urlOrHandle"
                type="text"
                placeholder="https://www.threads.net/@username atau @username"
                class="input w-full text-sm"
                required
              />
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label class="block text-xs font-bold mb-1">Outreach Channel</label>
                <select v-model="leadForm.outreach_channel" class="input w-full text-sm">
                  <option v-for="ch in CHANNEL_OPTIONS" :key="ch" :value="ch">{{ ch }}</option>
                </select>
              </div>
              <div>
                <label class="block text-xs font-bold mb-1">Interest Level</label>
                <select v-model="leadForm.interest_level" class="input w-full text-sm">
                  <option v-for="lvl in INTEREST_OPTIONS" :key="lvl" :value="lvl">{{ lvl }}</option>
                </select>
              </div>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label class="block text-xs font-bold mb-1">Status Komunikasi</label>
                <select v-model="leadForm.comm_status" class="input w-full text-sm">
                  <option v-for="cs in COMM_STATUS_OPTIONS" :key="cs" :value="cs">{{ cs }}</option>
                </select>
              </div>
              <div>
                <label class="block text-xs font-bold mb-1">Status Konversi</label>
                <select v-model="leadForm.conversion_status" class="input w-full text-sm">
                  <option v-for="cv in CONV_STATUS_OPTIONS" :key="cv" :value="cv">{{ cv }}</option>
                </select>
              </div>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label class="block text-xs font-bold mb-1">Jadwal Follow-up</label>
                <div class="flex gap-1.5">
                  <input v-model="leadForm.next_followup_local" type="datetime-local" class="input w-full text-xs" />
                  <button
                    v-if="leadForm.next_followup_local"
                    type="button"
                    @click="leadForm.next_followup_local = ''"
                    class="btn btn-secondary btn-sm px-2 text-xs"
                  >
                    Clear
                  </button>
                </div>
              </div>
              <div>
                <label class="block text-xs font-bold mb-1">Niche / Industry</label>
                <input v-model.trim="leadForm.niche" type="text" placeholder="Kreator, UMKM, Coach..." class="input w-full text-sm" />
              </div>
            </div>

            <div>
              <label class="block text-xs font-bold mb-1">Pain Point</label>
              <input v-model.trim="leadForm.pain_point" type="text" placeholder="Masalah utama yang mereka hadapi..." class="input w-full text-sm" />
            </div>

            <div>
              <label class="block text-xs font-bold mb-1">Next Action</label>
              <input v-model.trim="leadForm.next_action" type="text" placeholder="Langkah tindak lanjut berikutnya..." class="input w-full text-sm" />
            </div>

            <div>
              <label class="block text-xs font-bold mb-1">Catatan Lead</label>
              <textarea v-model="leadForm.notes" rows="2" class="input w-full text-sm"></textarea>
            </div>

            <div class="flex justify-end gap-2 pt-2">
              <button type="button" @click="closeLeadModal" class="btn btn-secondary btn-sm">Batal</button>
              <button type="submit" :disabled="saving" class="btn btn-primary btn-sm">
                {{ saving ? 'Menyimpan...' : 'Simpan' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>

    <!-- MODAL INTERACTION HISTORY -->
    <Teleport to="body">
      <div v-if="historyLead" class="fixed inset-0 z-[100] flex items-end sm:items-center justify-center p-0 sm:p-4 bg-black/60 backdrop-blur-sm">
        <div class="card w-full sm:max-w-2xl rounded-t-2xl sm:rounded-2xl p-5 space-y-4 bg-[var(--bg)] max-h-[92dvh] flex flex-col">
          <div class="flex items-center justify-between shrink-0">
            <div>
              <h3 class="text-base font-bold">Riwayat: @{{ historyLead.threads_handle }}</h3>
              <p class="text-[11px] theme-text-muted">Log percakapan tersimpan kronologis tanpa menimpa catatan lama.</p>
            </div>
            <button @click="historyLead = null" class="p-1.5 theme-text-muted hover:theme-text">
              <X class="w-5 h-5" />
            </button>
          </div>

          <div class="flex-1 overflow-y-auto space-y-5 pr-1">
            <!-- LOG NEW INTERACTION FORM -->
            <form @submit.prevent="addInteraction" class="p-3.5 rounded-xl bg-[var(--bg-sec)] border theme-border space-y-3">
              <div class="text-xs font-bold uppercase tracking-wider">Catat Interaksi Baru</div>

              <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                <div>
                  <label class="block text-[11px] font-bold theme-text-muted mb-1">Tanggal & Jam</label>
                  <input v-model="interactionForm.date_local" type="datetime-local" class="input w-full text-xs" required />
                </div>
                <div>
                  <label class="block text-[11px] font-bold theme-text-muted mb-1">Jenis Interaksi</label>
                  <select v-model="interactionForm.interaction_type" class="input w-full text-xs">
                    <option v-for="it in INTERACTION_TYPES" :key="it" :value="it">{{ it }}</option>
                  </select>
                </div>
              </div>

              <div>
                <label class="block text-[11px] font-bold theme-text-muted mb-1">Pesan yang Dikirim</label>
                <textarea v-model="interactionForm.message_sent" rows="2" placeholder="Pesan yang dikirim ke prospek..." class="input w-full text-xs"></textarea>
              </div>

              <div>
                <label class="block text-[11px] font-bold theme-text-muted mb-1">Respons Prospek</label>
                <textarea v-model="interactionForm.prospect_response" rows="2" placeholder="Balasan prospek (kosongkan jika belum dibalas)..." class="input w-full text-xs"></textarea>
              </div>

              <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                <div>
                  <label class="block text-[11px] font-bold theme-text-muted mb-1">Hasil Percakapan</label>
                  <input v-model.trim="interactionForm.outcome_notes" type="text" placeholder="Kesimpulan obrolan..." class="input w-full text-xs" />
                </div>
                <div>
                  <label class="block text-[11px] font-bold theme-text-muted mb-1">Follow-up Berikutnya</label>
                  <input v-model="interactionForm.next_followup_local" type="datetime-local" class="input w-full text-xs" />
                </div>
              </div>

              <div class="flex justify-end">
                <button type="submit" :disabled="savingInteraction" class="btn btn-primary btn-sm flex items-center gap-1.5">
                  <Send class="w-3.5 h-3.5" />
                  {{ savingInteraction ? 'Menyimpan...' : 'Simpan Riwayat' }}
                </button>
              </div>
            </form>

            <!-- TIMELINE LIST -->
            <div class="space-y-2.5">
              <div class="text-xs font-bold uppercase tracking-wider theme-text-muted">
                Timeline ({{ interactions.length }})
              </div>

              <div v-if="loadingInteractions" class="py-6 text-center text-xs theme-text-muted animate-pulse">
                Memuat riwayat...
              </div>
              <div v-else-if="interactions.length === 0" class="py-6 text-center text-xs theme-text-muted border theme-border rounded-xl">
                Belum ada riwayat interaksi untuk lead ini.
              </div>

              <div
                v-else
                v-for="item in interactions"
                :key="item.id"
                class="p-3.5 rounded-xl border theme-border bg-[var(--bg)] space-y-2 text-xs"
              >
                <div class="flex items-center justify-between gap-2">
                  <div class="flex items-center gap-2">
                    <span class="font-bold px-2 py-0.5 rounded bg-[var(--accent)] text-[var(--bg)] text-[10px]">
                      {{ item.interaction_type }}
                    </span>
                    <span class="theme-text-muted text-[11px]">{{ formatDateTime(item.interaction_date) }}</span>
                  </div>
                  <button @click="deleteInteraction(item)" class="theme-text-muted hover:text-red-500 p-1">
                    <Trash2 class="w-3.5 h-3.5" />
                  </button>
                </div>

                <div v-if="item.message_sent" class="p-2.5 rounded bg-[var(--bg-sec)] whitespace-pre-line">
                  <span class="font-bold text-[10px] uppercase theme-text-muted block mb-0.5">Dikirim:</span>
                  {{ item.message_sent }}
                </div>

                <div v-if="item.prospect_response" class="p-2.5 rounded border theme-border whitespace-pre-line">
                  <span class="font-bold text-[10px] uppercase text-emerald-500 block mb-0.5">Respons Prospek:</span>
                  {{ item.prospect_response }}
                </div>

                <div v-if="item.outcome_notes">
                  <span class="font-bold theme-text-muted">Hasil:</span> {{ item.outcome_notes }}
                </div>

                <div v-if="item.next_followup_at" class="text-[11px] text-amber-500 font-bold">
                  Jadwal FU: {{ formatDateTime(item.next_followup_at) }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { supabase } from '../../lib/supabase'
import { useNotify } from '../../composables/useNotify'
import {
  Plus, ExternalLink, Trash2, Search, RefreshCw,
  SlidersHorizontal, History, Edit3, X, Send
} from 'lucide-vue-next'

interface CrmLead {
  id: string
  threads_handle: string
  threads_url: string
  status?: string
  notes: string
  niche: string
  outreach_channel: string
  pain_point: string
  interest_level: string
  comm_status: string
  conversion_status: string
  last_contacted_at: string
  next_followup_at: string | null
  next_action: string
  created_at: string
}

interface CrmInteraction {
  id: string
  lead_id: string
  interaction_date: string
  interaction_type: string
  message_sent: string
  prospect_response: string
  outcome_notes: string
  next_followup_at: string | null
}

const CHANNEL_OPTIONS = ['Cold DM', 'Contextual Comment', 'Contextual Reply', 'Inbound', 'Referral', 'Other']
const INTEREST_OPTIONS = ['Low', 'Medium', 'High']
const COMM_STATUS_OPTIONS = ['Not Contacted', 'Contacted', 'Replied', 'No Response', 'Not Interested', 'Follow-up Needed']
const CONV_STATUS_OPTIONS = ['Potential', 'Interested', 'Trial Started', 'Activated', 'Paid', 'Not Proceeding']
const INTERACTION_TYPES = ['DM', 'Comment', 'Reply', 'WhatsApp']

const FOLLOWUP_TABS = [
  { label: 'Semua', value: 'ALL' },
  { label: 'Overdue', value: 'OVERDUE' },
  { label: 'Hari Ini', value: 'TODAY' },
  { label: 'Upcoming', value: 'UPCOMING' },
  { label: 'Tanpa Jadwal', value: 'NONE' },
]

const { showToast } = useNotify()

const leads = ref<CrmLead[]>([])
const interactionCounts = ref<Record<string, number>>({})
const loading = ref(true)
const saving = ref(false)
const accessDenied = ref(false)

const quickUrl = ref('')
const quickChannel = ref('Cold DM')

const showFilters = ref(false)
const followUpFilter = ref('ALL')
const commFilter = ref('ALL')
const convFilter = ref('ALL')
const channelFilter = ref('ALL')
const searchQuery = ref('')

const showLeadModal = ref(false)
const editingLead = ref<CrmLead | null>(null)
const leadForm = ref({
  urlOrHandle: '',
  outreach_channel: 'Cold DM',
  niche: '',
  pain_point: '',
  interest_level: 'Medium',
  comm_status: 'Contacted',
  conversion_status: 'Potential',
  next_followup_local: '',
  next_action: '',
  notes: '',
})

const historyLead = ref<CrmLead | null>(null)
const interactions = ref<CrmInteraction[]>([])
const loadingInteractions = ref(false)
const savingInteraction = ref(false)
const interactionForm = ref({
  date_local: '',
  interaction_type: 'DM',
  message_sent: '',
  prospect_response: '',
  outcome_notes: '',
  next_followup_local: '',
})

const activeFilterCount = computed(() => {
  let c = 0
  if (commFilter.value !== 'ALL') c++
  if (convFilter.value !== 'ALL') c++
  if (channelFilter.value !== 'ALL') c++
  return c
})

function toLocalDatetimeInput(iso: string | null | undefined): string {
  if (!iso) return ''
  const d = new Date(iso)
  if (isNaN(d.getTime())) return ''
  const pad = (n: number) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`
}

function fromLocalDatetimeInput(localStr: string): string | null {
  if (!localStr) return null
  const d = new Date(localStr)
  return isNaN(d.getTime()) ? null : d.toISOString()
}

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

function getFollowUpCategory(lead: CrmLead): 'OVERDUE' | 'TODAY' | 'UPCOMING' | 'NONE' {
  if (!lead.next_followup_at) return 'NONE'
  const fuTime = new Date(lead.next_followup_at).getTime()
  const now = new Date()
  const startOfToday = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 0, 0, 0).getTime()
  const endOfToday = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 23, 59, 59, 999).getTime()

  if (fuTime < startOfToday) return 'OVERDUE'
  if (fuTime <= endOfToday) return 'TODAY'
  return 'UPCOMING'
}

const dueFollowUpCount = computed(() =>
  leads.value.filter(l => ['OVERDUE', 'TODAY'].includes(getFollowUpCategory(l))).length
)

function getFollowUpTabCount(tab: string): number {
  if (tab === 'ALL') return leads.value.length
  return leads.value.filter(l => getFollowUpCategory(l) === tab).length
}

function getFollowUpLabel(lead: CrmLead): string {
  const cat = getFollowUpCategory(lead)
  if (cat === 'OVERDUE') return 'OVERDUE'
  if (cat === 'TODAY') return 'HARI INI'
  return 'UPCOMING'
}

function getFollowUpBadgeClass(lead: CrmLead): string {
  const cat = getFollowUpCategory(lead)
  if (cat === 'OVERDUE') return 'bg-red-500/15 text-red-500'
  if (cat === 'TODAY') return 'bg-amber-500/15 text-amber-500'
  return 'bg-blue-500/15 text-blue-500'
}

function getInterestBadgeClass(level: string): string {
  if (level === 'High') return 'bg-emerald-500/15 text-emerald-500'
  if (level === 'Low') return 'bg-red-500/10 text-red-400'
  return 'bg-amber-500/15 text-amber-500'
}

const filteredLeads = computed(() => {
  return leads.value.filter(lead => {
    if (followUpFilter.value !== 'ALL' && getFollowUpCategory(lead) !== followUpFilter.value) return false
    if (commFilter.value !== 'ALL' && lead.comm_status !== commFilter.value) return false
    if (convFilter.value !== 'ALL' && lead.conversion_status !== convFilter.value) return false
    if (channelFilter.value !== 'ALL' && (lead.outreach_channel || 'Cold DM') !== channelFilter.value) return false

    if (searchQuery.value) {
      const q = searchQuery.value.toLowerCase().replace(/^@/, '')
      const haystack = [lead.threads_handle, lead.niche, lead.pain_point, lead.notes, lead.next_action]
        .filter(Boolean)
        .join(' ')
        .toLowerCase()
      if (!haystack.includes(q)) return false
    }
    return true
  })
})

function formatRelativeTime(iso: string) {
  if (!iso) return '-'
  const diffSec = Math.floor((Date.now() - new Date(iso).getTime()) / 1000)
  if (diffSec < 60) return 'Baru saja'
  const diffMin = Math.floor(diffSec / 60)
  if (diffMin < 60) return `${diffMin} mnt lalu`
  const diffHour = Math.floor(diffMin / 60)
  if (diffHour < 24) return `${diffHour} jam lalu`
  const diffDay = Math.floor(diffHour / 24)
  return `${diffDay} hari lalu`
}

function formatDateTime(iso: string | null) {
  if (!iso) return '-'
  return new Date(iso).toLocaleString('id-ID', {
    day: '2-digit',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit',
  })
}

async function fetchLeads() {
  loading.value = true
  accessDenied.value = false
  try {
    const [leadsRes, countsRes] = await Promise.all([
      supabase.from('crm_leads').select('*').order('last_contacted_at', { ascending: false }),
      supabase.from('crm_interactions').select('lead_id'),
    ])

    if (leadsRes.error) {
      if (leadsRes.error.code === '42501' || leadsRes.error.message.toLowerCase().includes('permission')) {
        accessDenied.value = true
        return
      }
      throw leadsRes.error
    }

    leads.value = (leadsRes.data || []) as CrmLead[]
    const map: Record<string, number> = {}
    for (const row of countsRes.data || []) {
      map[row.lead_id] = (map[row.lead_id] || 0) + 1
    }
    interactionCounts.value = map
  } catch (err: any) {
    showToast('Gagal memuat CRM: ' + err.message, 'error')
  } finally {
    loading.value = false
  }
}

async function quickAddLead() {
  if (!quickUrl.value) return
  const { handle, url } = parseThreadsInput(quickUrl.value)
  if (!handle) {
    showToast('Format link atau username tidak valid', 'error')
    return
  }

  const existing = leads.value.find(l => l.threads_handle === handle)
  if (existing) {
    showToast(`@${handle} sudah ada di CRM`, 'error')
    searchQuery.value = handle
    followUpFilter.value = 'ALL'
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
        status: 'Contacted',
        outreach_channel: quickChannel.value,
        comm_status: 'Contacted',
        conversion_status: 'Potential',
        interest_level: 'Medium',
        last_contacted_at: nowIso,
      })
      .select()
      .single()

    if (error) throw error
    if (data) leads.value.unshift(data as CrmLead)
    quickUrl.value = ''
    showToast(`@${handle} disimpan`, 'success')
  } catch (err: any) {
    showToast('Gagal menyimpan: ' + err.message, 'error')
  } finally {
    saving.value = false
  }
}

function openCreateLeadModal() {
  editingLead.value = null
  leadForm.value = {
    urlOrHandle: '',
    outreach_channel: 'Cold DM',
    niche: '',
    pain_point: '',
    interest_level: 'Medium',
    comm_status: 'Contacted',
    conversion_status: 'Potential',
    next_followup_local: '',
    next_action: '',
    notes: '',
  }
  showLeadModal.value = true
}

function openEditLeadModal(lead: CrmLead) {
  editingLead.value = lead
  leadForm.value = {
    urlOrHandle: lead.threads_url || `@${lead.threads_handle}`,
    outreach_channel: lead.outreach_channel || 'Cold DM',
    niche: lead.niche || '',
    pain_point: lead.pain_point || '',
    interest_level: lead.interest_level || 'Medium',
    comm_status: lead.comm_status || 'Contacted',
    conversion_status: lead.conversion_status || 'Potential',
    next_followup_local: toLocalDatetimeInput(lead.next_followup_at),
    next_action: lead.next_action || '',
    notes: lead.notes || '',
  }
  showLeadModal.value = true
}

function closeLeadModal() {
  showLeadModal.value = false
  editingLead.value = null
}

async function saveLeadModal() {
  if (!leadForm.value.urlOrHandle) return
  const { handle, url } = parseThreadsInput(leadForm.value.urlOrHandle)
  if (!handle) {
    showToast('Format link atau username tidak valid', 'error')
    return
  }

  saving.value = true
  try {
    const payload = {
      threads_handle: handle,
      threads_url: url,
      outreach_channel: leadForm.value.outreach_channel,
      niche: leadForm.value.niche,
      pain_point: leadForm.value.pain_point,
      interest_level: leadForm.value.interest_level,
      comm_status: leadForm.value.comm_status,
      conversion_status: leadForm.value.conversion_status,
      status: leadForm.value.comm_status,
      next_followup_at: fromLocalDatetimeInput(leadForm.value.next_followup_local),
      next_action: leadForm.value.next_action,
      notes: leadForm.value.notes,
    }

    if (editingLead.value) {
      const { data, error } = await supabase
        .from('crm_leads')
        .update(payload)
        .eq('id', editingLead.value.id)
        .select()
        .single()

      if (error) throw error
      const idx = leads.value.findIndex(l => l.id === editingLead.value?.id)
      if (idx !== -1 && data) leads.value[idx] = data as CrmLead
      showToast('Lead diperbarui', 'success')
    } else {
      const existing = leads.value.find(l => l.threads_handle === handle)
      if (existing) {
        showToast(`@${handle} sudah ada di CRM`, 'error')
        saving.value = false
        return
      }
      const { data, error } = await supabase
        .from('crm_leads')
        .insert({ ...payload, last_contacted_at: new Date().toISOString() })
        .select()
        .single()

      if (error) throw error
      if (data) leads.value.unshift(data as CrmLead)
      showToast(`@${handle} ditambahkan`, 'success')
    }
    closeLeadModal()
  } catch (err: any) {
    showToast('Gagal menyimpan: ' + err.message, 'error')
  } finally {
    saving.value = false
  }
}

async function updateLeadField(lead: CrmLead, field: 'comm_status' | 'conversion_status', value: string) {
  const prev = lead[field]
  if (prev === value) return
  const nowIso = new Date().toISOString()
  lead[field] = value
  lead.last_contacted_at = nowIso

  try {
    const updatePayload: Record<string, any> = {
      [field]: value,
      last_contacted_at: nowIso,
    }
    if (field === 'comm_status') updatePayload.status = value

    const { error } = await supabase
      .from('crm_leads')
      .update(updatePayload)
      .eq('id', lead.id)

    if (error) throw error
    showToast(`@${lead.threads_handle} -> ${value}`, 'success')
  } catch (err: any) {
    lead[field] = prev
    showToast('Gagal update: ' + err.message, 'error')
  }
}

async function saveQuickNotes(lead: CrmLead) {
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
  if (!confirm(`Hapus @${lead.threads_handle} beserta seluruh riwayatnya?`)) return
  try {
    const { error } = await supabase.from('crm_leads').delete().eq('id', lead.id)
    if (error) throw error
    leads.value = leads.value.filter(l => l.id !== lead.id)
    showToast(`@${lead.threads_handle} dihapus`, 'success')
  } catch (err: any) {
    showToast('Gagal menghapus: ' + err.message, 'error')
  }
}

async function openHistoryModal(lead: CrmLead) {
  historyLead.value = lead
  interactions.value = []
  interactionForm.value = {
    date_local: toLocalDatetimeInput(new Date().toISOString()),
    interaction_type: 'DM',
    message_sent: '',
    prospect_response: '',
    outcome_notes: '',
    next_followup_local: toLocalDatetimeInput(lead.next_followup_at),
  }

  loadingInteractions.value = true
  try {
    const { data, error } = await supabase
      .from('crm_interactions')
      .select('*')
      .eq('lead_id', lead.id)
      .order('interaction_date', { ascending: false })

    if (error) throw error
    interactions.value = (data || []) as CrmInteraction[]
    interactionCounts.value[lead.id] = interactions.value.length
  } catch (err: any) {
    showToast('Gagal memuat riwayat: ' + err.message, 'error')
  } finally {
    loadingInteractions.value = false
  }
}

async function addInteraction() {
  if (!historyLead.value) return
  savingInteraction.value = true
  try {
    const lead = historyLead.value
    const interactionIso = fromLocalDatetimeInput(interactionForm.value.date_local) || new Date().toISOString()
    const nextFuIso = fromLocalDatetimeInput(interactionForm.value.next_followup_local)

    const { data, error } = await supabase
      .from('crm_interactions')
      .insert({
        lead_id: lead.id,
        interaction_date: interactionIso,
        interaction_type: interactionForm.value.interaction_type,
        message_sent: interactionForm.value.message_sent.trim(),
        prospect_response: interactionForm.value.prospect_response.trim(),
        outcome_notes: interactionForm.value.outcome_notes,
        next_followup_at: nextFuIso,
      })
      .select()
      .single()

    if (error) throw error
    if (data) {
      interactions.value.unshift(data as CrmInteraction)
      interactionCounts.value[lead.id] = interactions.value.length
    }

    const autoComm = interactionForm.value.prospect_response.trim()
      ? 'Replied'
      : lead.comm_status === 'Not Contacted'
        ? 'Contacted'
        : lead.comm_status

    const leadUpdate: Record<string, any> = {
      last_contacted_at: interactionIso,
      comm_status: autoComm,
      status: autoComm,
    }
    if (nextFuIso !== null || interactionForm.value.next_followup_local === '') {
      leadUpdate.next_followup_at = nextFuIso
    }

    const { data: updatedLead } = await supabase
      .from('crm_leads')
      .update(leadUpdate)
      .eq('id', lead.id)
      .select()
      .single()

    if (updatedLead) {
      const idx = leads.value.findIndex(l => l.id === lead.id)
      if (idx !== -1) leads.value[idx] = updatedLead as CrmLead
      historyLead.value = updatedLead as CrmLead
    }

    interactionForm.value.message_sent = ''
    interactionForm.value.prospect_response = ''
    interactionForm.value.outcome_notes = ''
    showToast('Riwayat tersimpan', 'success')
  } catch (err: any) {
    showToast('Gagal menyimpan riwayat: ' + err.message, 'error')
  } finally {
    savingInteraction.value = false
  }
}

async function deleteInteraction(item: CrmInteraction) {
  if (!confirm('Hapus catatan interaksi ini?')) return
  try {
    const { error } = await supabase.from('crm_interactions').delete().eq('id', item.id)
    if (error) throw error
    interactions.value = interactions.value.filter(i => i.id !== item.id)
    if (historyLead.value) {
      interactionCounts.value[historyLead.value.id] = interactions.value.length
    }
    showToast('Log dihapus', 'success')
  } catch (err: any) {
    showToast('Gagal menghapus log: ' + err.message, 'error')
  }
}

onMounted(fetchLeads)
</script>
