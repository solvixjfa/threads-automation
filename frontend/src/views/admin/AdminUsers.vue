<template>
  <div class="space-y-6">
    <div class="flex flex-wrap justify-between items-center gap-4">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Users & Plans</h1>
        <p class="text-sm theme-text-muted mt-1">Manage users, multi-account quotas, plans, and shared credits.</p>
      </div>
      <button @click="loadData" :disabled="loading" class="btn btn-secondary btn-sm">Refresh</button>
    </div>

    <!-- FILTER BAR -->
    <div v-if="isAuthorized" class="flex flex-col sm:flex-row gap-2.5">
      <input
        v-model.trim="searchQuery"
        type="text"
        placeholder="Cari email atau @username..."
        class="input flex-1 text-sm"
      />
      <div class="flex gap-1.5 overflow-x-auto pb-1">
        <button
          v-for="tab in FILTER_TABS"
          :key="tab.value"
          @click="filterMode = tab.value"
          class="px-3 py-1.5 rounded-lg text-xs font-bold whitespace-nowrap border transition-colors"
          :class="filterMode === tab.value
            ? 'bg-[var(--accent)] text-[var(--accent-text)] border-[var(--accent)]'
            : 'theme-bg theme-border theme-text-muted hover:theme-text'"
        >
          {{ tab.label }} ({{ getFilterCount(tab.value) }})
        </button>
      </div>
    </div>

    <div v-if="loading" class="p-12 text-center text-sm theme-text-muted animate-pulse">Loading users...</div>
    <div v-else-if="!isAuthorized" class="card p-12 text-center text-red-500 font-bold border-red-500">Access Denied. Admin only.</div>

    <div v-else class="card overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-left text-sm">
          <thead class="theme-bg-sec border-b theme-border">
            <tr>
              <th class="p-4 font-bold text-xs uppercase theme-text-muted">User & Akun</th>
              <th class="p-4 font-bold text-xs uppercase theme-text-muted">Status</th>
              <th class="p-4 font-bold text-xs uppercase theme-text-muted">Plan</th>
              <th class="p-4 font-bold text-xs uppercase theme-text-muted">Expires</th>
              <th class="p-4 font-bold text-xs uppercase theme-text-muted">Credits</th>
              <th class="p-4 font-bold text-xs uppercase theme-text-muted text-right">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y theme-border">
            <tr v-for="u in filteredUsers" :key="u.id" class="hover:bg-[var(--bg-sec)] transition-colors">
              <td class="p-4">
                <div class="font-bold">{{ u.email }}</div>
                <div class="flex items-center gap-1.5 flex-wrap mt-0.5">
                  <span class="text-xs theme-text-muted">@{{ u.username || 'unlinked' }}</span>
                  <span
                    class="text-[10px] font-bold px-1.5 py-0.5 rounded border theme-border"
                    :class="(u.account_count || 1) > 1 ? 'bg-blue-500/15 text-blue-400 border-blue-500/30' : 'theme-text-muted'"
                  >
                    {{ u.account_count || 1 }}/{{ getQuotaLimit(u.plan, u.role) }} akun
                  </span>
                </div>
                <div v-if="u.pending_plan" class="mt-1 inline-block bg-amber-500 text-white text-[9px] font-bold px-2 py-0.5 rounded">
                  Request: {{ getPlanLabel(u.pending_plan) }}
                </div>
              </td>
              <td class="p-4">
                <Badge :variant="u.connection_status === 'connected' ? 'success' : 'default'">{{ u.connection_status }}</Badge>
                <div v-if="u.last_error" class="text-[10px] text-red-500 font-bold mt-1" :title="u.last_error">Error</div>
              </td>
              <td class="p-4"><Badge :variant="u.plan !== 'none' ? 'accent' : 'default'">{{ getPlanLabel(u.plan) }}</Badge></td>
              <td class="p-4 text-xs">{{ u.plan_expires_at ? formatDate(u.plan_expires_at) : '-' }}</td>
              <td class="p-4 font-bold text-lg">{{ (u.credit_balance || 0).toLocaleString('id-ID') }}</td>
              <td class="p-4 text-right space-x-2 whitespace-nowrap">
                <button @click="openExtendModal(u)" class="text-xs font-bold underline hover:theme-text-muted">Approve / Extend</button>
                <button @click="openCreditModal(u)" class="text-xs font-bold underline hover:theme-text-muted">Adjust</button>
                <button @click="openLedgerModal(u)" class="text-xs font-bold underline hover:theme-text-muted">Ledger</button>
                <button @click="handleForceSync(u)" :disabled="isProcessing" class="text-xs font-bold text-blue-500 underline hover:text-blue-700 disabled:opacity-50">Sync</button>
                <button @click="handleDowngrade(u)" :disabled="isProcessing" class="text-xs font-bold text-red-500 underline hover:text-red-700 disabled:opacity-50">Downgrade</button>
              </td>
            </tr>
            <tr v-if="filteredUsers.length === 0">
              <td colspan="6" class="p-8 text-center text-xs theme-text-muted">Tidak ada akun yang cocok dengan filter.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- MODAL EXTEND PLAN -->
    <Teleport to="body">
      <div v-if="selectedUser && modalType === 'extend'" class="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
        <div class="card max-w-sm w-full p-6 space-y-4 bg-[var(--bg-primary)]">
          <h3 class="text-lg font-bold">Approve / Extend Plan</h3>
          <p class="text-xs theme-text-muted">{{ selectedUser.email }} (@{{ selectedUser.username }})</p>
          <Select v-model="extendType" label="Plan Type" :options="[
            {label: 'Free Trial (15.000 Credits, 7 Hari, Maks 1 Akun)', value: 'trial'},
            {label: 'Starter (Rp59k, 100.000 Credits, Maks 2 Akun)', value: 'starter'},
            {label: 'Pro (Rp99k, 300.000 Credits, Maks 5 Akun)', value: 'pro'},
            {label: 'Business (Rp179k, 750.000 Credits, Maks 20 Akun)', value: 'business'},
            {label: 'Agency BYOK (Rp249k, Unlimited, Maks 50 Akun)', value: 'agency'},
            {label: 'Pro Credit Legacy (100.000 Credits, Maks 10 Akun)', value: 'paid_credit'},
            {label: 'Pro BYOK Legacy (Unlimited, Maks 3 Akun)', value: 'paid_byok'}
          ]" />
          <p class="text-xs theme-text-muted">
            Menambah masa aktif dan me-reset kredit.
            <span v-if="(selectedUser.account_count || 1) > 1" class="font-bold text-blue-400">
              Otomatis sinkron ke seluruh {{ selectedUser.account_count }} akun milik user ini.
            </span>
          </p>
          <div class="flex justify-end gap-3 pt-2">
            <Button variant="secondary" @click="selectedUser = null">Cancel</Button>
            <Button @click="handleExtend" :loading="isProcessing">Confirm</Button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- MODAL ADJUST CREDITS -->
    <Teleport to="body">
      <div v-if="selectedUser && modalType === 'credits'" class="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
        <div class="card max-w-sm w-full p-6 space-y-4 bg-[var(--bg-primary)]">
          <h3 class="text-lg font-bold">Adjust Credits: {{ selectedUser.email }}</h3>
          <p v-if="(selectedUser.account_count || 1) > 1" class="text-xs text-blue-400 font-bold">
            Saldo kredit bersama akan diperbarui untuk seluruh {{ selectedUser.account_count }} akun user ini.
          </p>
          <div class="space-y-1"><label class="label">Amount (+/-)</label><input v-model.number="creditAmount" type="number" class="input w-full" /></div>
          <div class="space-y-1"><label class="label">Note</label><input v-model="creditNote" type="text" class="input w-full" /></div>
          <div class="flex justify-end gap-3 pt-2"><Button variant="secondary" @click="selectedUser = null">Cancel</Button><Button @click="handleAdjustCredits" :disabled="!creditNote || !creditAmount">Save</Button></div>
        </div>
      </div>
    </Teleport>

    <!-- MODAL LEDGER -->
    <Teleport to="body">
      <div v-if="selectedUser && modalType === 'ledger'" class="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
        <div class="card max-w-lg w-full p-6 space-y-4 bg-[var(--bg-primary)] max-h-[80vh] flex flex-col">
          <h3 class="text-lg font-bold">Credit Ledger: {{ selectedUser.email }}</h3>
          <div class="flex-1 overflow-y-auto space-y-2 pr-2">
            <div v-for="l in ledgerData" :key="l.id" class="flex justify-between items-center p-3 rounded-lg theme-bg-sec border theme-border text-xs">
              <div><div class="font-bold" :class="l.delta > 0 ? 'text-green-500' : 'text-red-500'">{{ l.delta > 0 ? '+' : '' }}{{ l.delta }}</div><div class="theme-text-muted">{{ l.reason }}</div></div>
              <div class="theme-text-muted text-right">{{ formatDate(l.created_at) }}</div>
            </div>
          </div>
          <div class="flex justify-end pt-2"><Button variant="secondary" @click="selectedUser = null">Close</Button></div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { supabase } from '../../lib/supabase'
import { useNotify } from '../../composables/useNotify'
import { Button, Badge, Select } from '../../components/ui'

const FILTER_TABS = [
  { label: 'Semua', value: 'all' },
  { label: 'Pending', value: 'pending' },
  { label: 'Multi-Account', value: 'multi' },
  { label: 'Pro', value: 'pro' },
]

const { showToast } = useNotify()
const users = ref<any[]>([])
const loading = ref(true)
const isAuthorized = ref(false)
const searchQuery = ref('')
const filterMode = ref('all')

const selectedUser = ref<any>(null)
const modalType = ref<'extend' | 'credits' | 'ledger' | null>(null)
const extendType = ref('pro')
const creditAmount = ref<number | null>(null)
const creditNote = ref('')
const ledgerData = ref<any[]>([])
const isProcessing = ref(false)

const API_BASE = 'https://threads-automation-r9so.onrender.com/api/v1/admin'

function getQuotaLimit(plan: string, role = 'user'): number {
  if (role === 'admin') return 50
  if (plan === 'agency') return 50
  if (plan === 'business') return 20
  if (plan === 'pro') return 5
  if (plan === 'starter') return 2
  if (plan === 'paid_credit') return 10
  if (plan === 'paid_byok') return 3
  return 1
}

function getPlanLabel(plan: string) {
  if (!plan || plan === 'none') return 'Free'
  if (plan === 'trial') return 'Trial'
  if (plan === 'starter') return 'Starter'
  if (plan === 'pro') return 'Pro'
  if (plan === 'business') return 'Business'
  if (plan === 'agency') return 'Agency (BYOK)'
  if (plan === 'paid_credit') return 'Pro Credit'
  if (plan === 'paid_byok') return 'Pro BYOK'
  return plan
}

function matchesFilter(u: any, mode: string): boolean {
  if (mode === 'pending') return !!u.pending_plan
  if (mode === 'multi') return (u.account_count || 1) > 1
  if (mode === 'pro') return ['starter', 'pro', 'business', 'agency', 'paid_credit', 'paid_byok'].includes(u.plan)
  return true
}

function getFilterCount(mode: string): number {
  return users.value.filter(u => matchesFilter(u, mode)).length
}

const filteredUsers = computed(() => {
  return users.value.filter(u => {
    if (!matchesFilter(u, filterMode.value)) return false
    if (searchQuery.value) {
      const q = searchQuery.value.toLowerCase().replace(/^@/, '')
      const hay = `${u.email || ''} ${u.username || ''}`.toLowerCase()
      if (!hay.includes(q)) return false
    }
    return true
  })
})

function formatDate(iso: string) {
  if (!iso) return ''
  return new Date(iso).toLocaleString('id-ID', { dateStyle: 'short', timeStyle: 'short' })
}

async function getAuthHeader() {
  const { data: { session } } = await supabase.auth.getSession()
  return session ? { 'Authorization': `Bearer ${session.access_token}` } : {}
}

async function loadData() {
  loading.value = true
  try {
    const headers = await getAuthHeader()
    if (!headers.Authorization) throw new Error("Not logged in")
    const res = await fetch(`${API_BASE}/users`, { headers })
    if (res.status === 403 || res.status === 401) { isAuthorized.value = false; return }
    const data = await res.json()
    if (data.success) {
      isAuthorized.value = true
      users.value = data.users
    }
  } catch (err: any) { showToast('Failed: ' + err.message, 'error') } finally { loading.value = false }
}

function openExtendModal(user: any) {
  selectedUser.value = user
  extendType.value = user.pending_plan || (['starter', 'pro', 'business', 'agency', 'paid_credit', 'paid_byok'].includes(user.plan) ? user.plan : 'pro')
  modalType.value = 'extend'
}

function openCreditModal(user: any) {
  selectedUser.value = user
  creditAmount.value = null
  creditNote.value = ''
  modalType.value = 'credits'
}

async function openLedgerModal(user: any) {
  selectedUser.value = user
  modalType.value = 'ledger'
  ledgerData.value = []
  try {
    const headers = await getAuthHeader()
    const res = await fetch(`${API_BASE}/ledger/${user.id}`, { headers })
    const data = await res.json()
    if (data.success) ledgerData.value = data.ledger
  } catch (err) {}
}

async function handleExtend() {
  if (!selectedUser.value) return
  isProcessing.value = true
  try {
    const headers = await getAuthHeader()
    const res = await fetch(`${API_BASE}/extend`, {
      method: 'POST', headers: { ...headers, 'Content-Type': 'application/json' },
      body: JSON.stringify({ account_id: selectedUser.value.id, plan_type: extendType.value })
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.detail)
    showToast('Plan extended across all user accounts.', 'success')
    selectedUser.value = null
    await loadData()
  } catch (err: any) { showToast('Failed: ' + err.message, 'error') } finally { isProcessing.value = false }
}

async function handleAdjustCredits() {
  if (!selectedUser.value || !creditAmount.value || !creditNote.value) return
  isProcessing.value = true
  try {
    const headers = await getAuthHeader()
    const res = await fetch(`${API_BASE}/adjust-credits`, {
      method: 'POST', headers: { ...headers, 'Content-Type': 'application/json' },
      body: JSON.stringify({ account_id: selectedUser.value.id, delta: creditAmount.value, note: creditNote.value })
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.detail)
    showToast('Shared credits adjusted.', 'success')
    selectedUser.value = null
    await loadData()
  } catch (err: any) { showToast('Failed: ' + err.message, 'error') } finally { isProcessing.value = false }
}

async function handleForceSync(user: any) {
  if (!confirm(`Tarik data Meta (Avatar & Username) manual untuk @${user.username}?`)) return
  isProcessing.value = true
  try {
    const headers = await getAuthHeader()
    const res = await fetch(`${API_BASE}/force-sync`, {
      method: 'POST', headers: { ...headers, 'Content-Type': 'application/json' },
      body: JSON.stringify({ account_id: user.id, plan_type: 'sync' })
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.detail)
    showToast('Sync berhasil!', 'success')
    await loadData()
  } catch (err: any) { showToast('Failed: ' + err.message, 'error') } finally { isProcessing.value = false }
}

async function handleDowngrade(user: any) {
  const count = user.account_count || 1
  if (!confirm(`Yakin downgrade ${user.email} (${count} akun) ke Free? Kredit akan di-reset ke 0.`)) return
  isProcessing.value = true
  try {
    const headers = await getAuthHeader()
    const res = await fetch(`${API_BASE}/downgrade`, {
      method: 'POST', headers: { ...headers, 'Content-Type': 'application/json' },
      body: JSON.stringify({ account_id: user.id, plan_type: 'none' })
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.detail)
    showToast('User berhasil di-downgrade ke Free.', 'success')
    await loadData()
  } catch (err: any) { showToast('Failed: ' + err.message, 'error') } finally { isProcessing.value = false }
}

onMounted(loadData)
</script>
