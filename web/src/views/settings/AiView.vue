<template>
  <div class="space-y-6">
    <Card>
      <template #header>
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-sm font-bold">AI & Billing</h2>
            <p class="text-xs theme-text-muted mt-0.5">Manage your plan and API keys.</p>
          </div>
          <Badge :variant="hasCustomKey ? 'success' : 'default'">
            {{ hasCustomKey ? 'BYOK Active' : planName }}
          </Badge>
        </div>
      </template>

      <div v-if="loading" class="space-y-3">
        <div class="h-10 skeleton"></div>
        <div class="h-20 skeleton"></div>
      </div>

      <template v-else>
        <!-- PLAN STATUS -->
        <div class="p-4 rounded-xl border theme-border bg-[var(--bg-sec)] space-y-3 mb-6">
          <div class="flex justify-between items-center">
            <h3 class="text-sm font-bold">Current Plan</h3>
            <span v-if="planExpiresAt" class="text-xs theme-text-muted">Expires: {{ formatDate(planExpiresAt) }}</span>
          </div>
          
          <div class="flex items-center gap-4">
            <div class="flex-1">
              <div class="text-2xl font-black">{{ hasCustomKey ? 'Unlimited' : planName }}</div>
              <div v-if="!hasCustomKey && plan !== 'none'" class="text-sm theme-text-muted mt-1">
                {{ creditBalance }} Credits Remaining
              </div>
              <div v-if="plan === 'none'" class="text-sm theme-text-muted mt-1">
                Your plan has expired. Please renew to use AI features.
              </div>
            </div>
            <div class="text-right space-y-1">
              <div class="text-xs theme-text-muted">Harga:</div>
              <div class="font-bold">Rp49.000 (Kredit)</div>
              <div class="font-bold text-xs">Rp29.000 (BYOK)</div>
            </div>
          </div>
        </div>

        <!-- BYOK SECTION -->
        <div class="space-y-3">
          <h3 class="text-sm font-bold">Use Your Own API Key (BYOK)</h3>
          <p class="text-xs theme-text-muted">
            Using your own API key means AI actions won't deduct your credits.
          </p>
          <div class="space-y-2">
            <div class="flex gap-2">
              <input v-model="customKey" type="password" placeholder="Paste your API Key here..." class="input flex-1" />
              <Button @click="saveKey" :disabled="saving || !accountId" :loading="saving">Save</Button>
            </div>
            <p class="text-[11px] theme-text-muted">Key is stored securely and never shown to others.</p>
          </div>
        </div>
      </template>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { supabase } from '../../lib/supabase'
import { useNotify } from '../../composables/useNotify'
import { Card, Button, Badge } from '../../components/ui'

const { showToast } = useNotify()
const loading = ref(true)
const saving = ref(false)
const accountId = ref<string | null>(null)

const plan = ref('none')
const planExpiresAt = ref<string | null>(null)
const creditBalance = ref(0)
const customKey = ref('')
const hasCustomKey = ref(false)

const planName = computed(() => {
  if (plan.value === 'trial') return 'Trial'
  if (plan.value === 'paid_credit') return 'Paid (Credits)'
  if (plan.value === 'paid_byok') return 'Paid (BYOK)'
  return 'No Plan'
})

function formatDate(iso: string) {
  if (!iso) return ''
  return new Date(iso).toLocaleDateString('id-ID', { dateStyle: 'medium' })
}

async function load() {
  loading.value = true
  try {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) return

    const { data: account, error } = await supabase
      .schema('threads').from('threads_accounts')
      .select('id, plan, plan_expires_at, credit_balance, custom_gemini_key')
      .eq('user_id', user.id).maybeSingle()

    if (error) throw error

    if (account) {
      accountId.value = account.id
      plan.value = account.plan || 'none'
      planExpiresAt.value = account.plan_expires_at
      creditBalance.value = account.credit_balance || 0
      customKey.value = account.custom_gemini_key || ''
      hasCustomKey.value = !!account.custom_gemini_key
    }
  } catch (err: any) {
    showToast('Failed to load settings: ' + err.message, 'error')
  } finally {
    loading.value = false
  }
}

async function saveKey() {
  if (!accountId.value) return
  saving.value = true
  try {
    // Simpan API Key (nanti backend yang urus enkripsi)
    const { error } = await supabase
      .schema('threads').from('threads_accounts')
      .update({ custom_gemini_key: customKey.value.trim() || null })
      .eq('id', accountId.value)

    if (error) throw error
    
    hasCustomKey.value = !!customKey.value.trim()
    showToast('API Key saved.', 'success')
  } catch (err: any) {
    showToast('Failed to save API Key: ' + err.message, 'error')
  } finally {
    saving.value = false
  }
}

onMounted(load)
</script>
