<template>
  <div class="space-y-6">
    <div class="flex flex-wrap justify-between items-center gap-4">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Admin Panel</h1>
        <p class="text-sm theme-text-muted mt-1">Manage users, plans, and credits.</p>
      </div>
      <button @click="loadData" :disabled="loading" class="btn btn-secondary btn-sm">Refresh</button>
    </div>

    <div v-if="loading" class="p-12 text-center text-sm theme-text-muted animate-pulse">Loading users...</div>
    <div v-else-if="!isAuthorized" class="card p-12 text-center text-red-500 font-bold border-red-500">Access Denied. Admin only.</div>

    <div v-else class="card overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-left text-sm">
          <thead class="theme-bg-sec border-b theme-border">
            <tr>
              <th class="p-4 font-bold text-xs uppercase theme-text-muted">User</th>
              <th class="p-4 font-bold text-xs uppercase theme-text-muted">Status</th>
              <th class="p-4 font-bold text-xs uppercase theme-text-muted">Plan</th>
              <th class="p-4 font-bold text-xs uppercase theme-text-muted">Expires</th>
              <th class="p-4 font-bold text-xs uppercase theme-text-muted">Credits</th>
              <th class="p-4 font-bold text-xs uppercase theme-text-muted text-right">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y theme-border">
            <tr v-for="u in users" :key="u.id" class="hover:bg-[var(--bg-sec)] transition-colors">
              <td class="p-4">
                <div class="font-bold">{{ u.email }}</div>
                <div class="text-xs theme-text-muted">@{{ u.username || 'unlinked' }}</div>
                <!-- PENDING REQUEST BADGE -->
                <div v-if="u.pending_plan" class="mt-1 inline-block bg-amber-500 text-white text-[9px] font-bold px-2 py-0.5 rounded">
                  Request: {{ getPlanLabel(u.pending_plan) }}
                </div>
              </td>
              <td class="p-4"><Badge :variant="u.connection_status === 'connected' ? 'success' : 'default'">{{ u.connection_status }}</Badge></td>
              <td class="p-4"><Badge :variant="u.plan !== 'none' ? 'accent' : 'default'">{{ getPlanLabel(u.plan) }}</Badge></td>
              <td class="p-4 text-xs">{{ u.plan_expires_at ? formatDate(u.plan_expires_at) : '-' }}</td>
              <td class="p-4 font-bold text-lg">{{ u.credit_balance }}</td>
              <td class="p-4 text-right space-x-2">
                <button @click="openExtendModal(u)" class="text-xs font-bold underline hover:theme-text-muted">Approve / Extend</button>
                <button @click="openCreditModal(u)" class="text-xs font-bold underline hover:theme-text-muted">Adjust</button>
                <button @click="openLedgerModal(u)" class="text-xs font-bold underline hover:theme-text-muted">Ledger</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- MODAL EXTEND PLAN -->
    <Teleport to="body">
      <div v-if="selectedUser && modalType === 'extend'" class="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
        <div class="card max-w-sm w-full p-6 space-y-4 bg-[var(--bg)]">
          <h3 class="text-lg font-bold">Approve / Extend Plan</h3>
          <p class="text-xs theme-text-muted">{{ selectedUser.email }}</p>
          <Select v-model="extendType" label="Plan Type" :options="[
            {label: 'Pro Credit (Rp49k)', value: 'paid_credit'}, 
            {label: 'Pro BYOK (Rp29k)', value: 'paid_byok'}
          ]" />
          <p class="text-xs theme-text-muted">Menambah 30 hari dan me-reset kredit.</p>
          <div class="flex justify-end gap-3 pt-2">
            <Button variant="secondary" @click="selectedUser = null">Cancel</Button>
            <Button @click="handleExtend" :loading="isProcessing">Confirm</Button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- MODAL ADJUST CREDITS & LEDGER (SAMA SEPERTI SEBELUMNYA) -->
    <Teleport to="body">
      <div v-if="selectedUser && modalType === 'credits'" class="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
        <div class="card max-w-sm w-full p-6 space-y-4 bg-[var(--bg)]">
          <h3 class="text-lg font-bold">Adjust Credits: {{ selectedUser.email }}</h3>
          <div class="space-y-1"><label class="label">Amount (+/-)</label><input v-model.number="creditAmount" type="number" class="input w-full" /></div>
          <div class="space-y-1"><label class="label">Note</label><input v-model="creditNote" type="text" class="input w-full" /></div>
          <div class="flex justify-end gap-3 pt-2"><Button variant="secondary" @click="selectedUser = null">Cancel</Button><Button @click="handleAdjustCredits" :disabled="!creditNote || !creditAmount">Save</Button></div>
        </div>
      </div>
    </Teleport>
    
    <Teleport to="body">
      <div v-if="selectedUser && modalType === 'ledger'" class="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
        <div class="card max-w-lg w-full p-6 space-y-4 bg-[var(--bg)] max-h-[80vh] flex flex-col">
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
import { ref, onMounted } from 'vue'
import { supabase } from '../lib/supabase'
import { useNotify } from '../composables/useNotify'
import { Button, Badge, Select } from '../components/ui'

const { showToast } = useNotify()
const users = ref<any[]>([])
const loading = ref(true)
const isAuthorized = ref(false)

const selectedUser = ref<any>(null)
const modalType = ref<'extend' | 'credits' | 'ledger' | null>(null)
const extendType = ref('paid_credit')
const creditAmount = ref<number | null>(null)
const creditNote = ref('')
const ledgerData = ref<any[]>([])
const isProcessing = ref(false)

const API_BASE = 'https://threads-automation-production-53ad.up.railway.app/api/v1/admin'

function getPlanLabel(plan: string) {
  if (!plan || plan === 'none') return 'Free'
  if (plan === 'trial') return 'Trial'
  if (plan === 'paid_credit') return 'Pro Credit'
  if (plan === 'paid_byok') return 'Pro BYOK'
  return plan
}

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
  // Kalau ada pending plan, otomatis pilih itu
  extendType.value = user.pending_plan || (user.plan === 'paid_byok' ? 'paid_byok' : 'paid_credit')
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
    showToast('Plan extended successfully.', 'success')
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
    showToast('Credits adjusted.', 'success')
    selectedUser.value = null
    await loadData()
  } catch (err: any) { showToast('Failed: ' + err.message, 'error') } finally { isProcessing.value = false }
}

onMounted(loadData)
</script>
