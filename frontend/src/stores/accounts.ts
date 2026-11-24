import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { supabase } from '../lib/supabase'

export interface ThreadsAccount {
  id: string
  user_id: string
  threads_user_id: string | null
  username: string | null
  profile_picture_url: string | null
  connection_status: string
  token_expires_at: string | null
  last_synced_at?: string | null
  last_error?: string | null
  kill_switch: boolean
  plan: string
  pending_plan: string | null
  plan_started_at: string | null
  plan_expires_at: string | null
  credit_balance: number
  custom_gemini_key: string | null
  custom_groq_key: string | null
  ai_provider?: string | null
  role: string
  created_at: string
}

const STORAGE_KEY = 'ixiera_active_account_id'

export function getMaxAccountsByPlan(plan: string, role = 'user'): number {
  if (role === 'admin') return 50
  if (plan === 'paid_credit') return 10
  if (plan === 'paid_byok') return 3
  return 1
}

export const useAccountStore = defineStore('accounts', () => {
  const accounts = ref<ThreadsAccount[]>([])
  const activeAccountId = ref<string>(localStorage.getItem(STORAGE_KEY) || '')
  const loading = ref(false)
  const initialized = ref(false)
  const isSyncing = ref(false)
  const syncStatusText = ref('')
  const profilePlan = ref<string>('free')
  const profileRole = ref<string>('user')

  const activeAccount = computed<ThreadsAccount | null>(() => {
    if (!accounts.value.length) return null
    return accounts.value.find(a => a.id === activeAccountId.value) || accounts.value[0]
  })

  const effectiveRole = computed<string>(() => {
    if (accounts.value.some(a => a.role === 'admin') || profileRole.value === 'admin') {
      return 'admin'
    }
    return 'user'
  })

  const effectivePlan = computed<string>(() => {
    let best = profilePlan.value || 'free'
    for (const acc of accounts.value) {
      if (acc.plan === 'paid_credit') return 'paid_credit'
      if (acc.plan === 'paid_byok' && best !== 'paid_credit') best = 'paid_byok'
      else if (acc.plan === 'trial' && (best === 'free' || best === 'none')) best = 'trial'
    }
    return best === 'none' ? 'free' : best
  })

  const maxAccounts = computed<number>(() => {
    return getMaxAccountsByPlan(effectivePlan.value, effectiveRole.value)
  })

  const canAddAccount = computed<boolean>(() => {
    return accounts.value.length < maxAccounts.value
  })

  async function syncAccountData(accountId?: string, minDelayMs = 2500) {
    const targetId = accountId || activeAccountId.value
    if (!targetId) return
    const targetAcc = accounts.value.find(a => a.id === targetId)
    isSyncing.value = true
    syncStatusText.value = targetAcc?.username
      ? `Menyinkronkan data @${targetAcc.username}...`
      : 'Menyinkronkan data akun...'

    try {
      await Promise.all([
        supabase.functions.invoke('worker-metrics', {
          body: { account_id: targetId },
        }),
        new Promise(resolve => setTimeout(resolve, minDelayMs)),
      ])
      await fetchAccounts(true)
    } catch (err) {
      console.warn('[useAccountStore] syncAccountData warning:', err)
    } finally {
      isSyncing.value = false
      syncStatusText.value = ''
    }
  }

  async function setActiveAccount(id: string, withSync = false) {
    if (!id) return
    const changed = activeAccountId.value !== id
    activeAccountId.value = id
    localStorage.setItem(STORAGE_KEY, id)
    if (withSync && changed) {
      await syncAccountData(id, 2500)
    }
  }

  async function fetchAccounts(force = false): Promise<ThreadsAccount[]> {
    if (loading.value && !force) return accounts.value
    loading.value = true
    try {
      const { data: { user } } = await supabase.auth.getUser()
      if (!user) {
        accounts.value = []
        initialized.value = true
        return []
      }

      const [accsRes, profRes] = await Promise.all([
        supabase
          .schema('threads')
          .from('threads_accounts')
          .select('*')
          .eq('user_id', user.id)
          .order('created_at', { ascending: true }),
        supabase
          .schema('threads')
          .from('profiles')
          .select('plan, role')
          .eq('id', user.id)
          .maybeSingle()
      ])

      if (profRes.data) {
        profilePlan.value = profRes.data.plan || 'free'
        profileRole.value = profRes.data.role || 'user'
      }

      const list = (accsRes.data || []) as ThreadsAccount[]
      accounts.value = list

      if (list.length > 0) {
        const exists = list.some(a => a.id === activeAccountId.value)
        if (!exists) {
          activeAccountId.value = list[0].id
          localStorage.setItem(STORAGE_KEY, list[0].id)
        }
      } else {
        activeAccountId.value = ''
        localStorage.removeItem(STORAGE_KEY)
      }

      initialized.value = true
      return list
    } catch (err) {
      console.error('[useAccountStore] fetchAccounts error:', err)
      return accounts.value
    } finally {
      loading.value = false
    }
  }

  async function ensureActiveAccount(): Promise<ThreadsAccount | null> {
    if (!initialized.value || accounts.value.length === 0) {
      await fetchAccounts()
    }
    return activeAccount.value
  }

  function reset() {
    accounts.value = []
    activeAccountId.value = ''
    initialized.value = false
    isSyncing.value = false
    syncStatusText.value = ''
    localStorage.removeItem(STORAGE_KEY)
  }

  return {
    accounts,
    activeAccountId,
    activeAccount,
    loading,
    initialized,
    isSyncing,
    syncStatusText,
    effectivePlan,
    effectiveRole,
    maxAccounts,
    canAddAccount,
    setActiveAccount,
    syncAccountData,
    fetchAccounts,
    ensureActiveAccount,
    reset,
  }
})
