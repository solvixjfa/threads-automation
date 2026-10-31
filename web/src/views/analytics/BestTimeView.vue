<template>
  <div class="space-y-6">
    <Card>
      <template #header>
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-sm font-bold">{{ $t('analytics.best_title') }}</h2>
            <p class="text-xs theme-text-muted mt-0.5">{{ $t('analytics.best_subtitle') }}</p>
          </div>
          <Badge :variant="confidenceVariant">{{ confidenceLabel }}</Badge>
        </div>
      </template>

      <div v-if="loading" class="space-y-3">
        <div class="h-6 w-48 skeleton"></div>
        <div class="h-64 skeleton"></div>
      </div>

      <div v-else-if="error" class="text-center py-8">
        <p class="text-sm theme-text-muted mb-4">{{ error }}</p>
        <Button variant="secondary" size="sm" @click="loadData">{{ $t('common.retry') }}</Button>
      </div>

      <div v-else-if="totalPosts === 0" class="text-center py-8">
        <EmptyState :title="$t('analytics.not_enough')" :description="$t('analytics.not_enough_sub')" />
      </div>

      <div v-else class="space-y-6">
        <div class="flex flex-wrap gap-4 text-xs">
          <div><span class="theme-text-muted">{{ $t('analytics.total_analyzed') }}</span><span class="font-bold ml-1.5">{{ totalPosts }}</span></div>
          <div><span class="theme-text-muted">{{ $t('analytics.confidence') }}</span><span class="font-bold ml-1.5 capitalize">{{ confidenceLabel }}</span></div>
        </div>
        <BestTimeHeatmap :matrix="matrix" />
      </div>
    </Card>

    <Card v-if="!loading && !error && topSlots.length > 0">
      <template #header>
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-sm font-bold">{{ $t('analytics.top_slots') }}</h2>
            <p class="text-xs theme-text-muted mt-0.5">{{ $t('analytics.top_slots_sub') }}</p>
          </div>
        </div>
      </template>

      <div class="space-y-2">
        <div v-for="(slot, idx) in topSlots" :key="idx" class="flex items-center justify-between p-3 rounded-lg theme-bg-sec border theme-border">
          <div class="flex items-center gap-3">
            <div class="w-7 h-7 rounded-full flex items-center justify-center text-xs font-black theme-accent">{{ idx + 1 }}</div>
            <div>
              <div class="text-sm font-bold">{{ slot.weekday }}, {{ slot.hour }}</div>
              <div class="text-[11px] theme-text-muted">{{ $t('analytics.sample', { n: slot.sample_size }) }}</div>
            </div>
          </div>
          <div class="text-right">
            <div class="text-lg font-black">{{ (slot.er_pct || 0).toFixed(2) }}%</div>
            <div class="text-[10px] theme-text-muted uppercase font-bold">{{ $t('analytics.avg_er') }}</div>
          </div>
        </div>
      </div>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { supabase } from '../../lib/supabase'
import { useI18n } from 'vue-i18n'
import { Card, Badge, Button, EmptyState } from '../../components/ui'
import BestTimeHeatmap from '../../components/BestTimeHeatmap.vue'

const { t } = useI18n()
const loading = ref(true)
const error = ref('')
const matrix = ref<number[][]>(Array(7).fill(0).map(() => Array(24).fill(0)))
const topSlots = ref<any[]>([])
const totalPosts = ref(0)
const confidence = ref<'low' | 'medium' | 'high'>('low')

const confidenceLabel = computed(() => ({
  low: t('analytics.conf_low'), medium: t('analytics.conf_med'), high: t('analytics.conf_high'),
}[confidence.value]))

const confidenceVariant = computed(() => ({ low: 'default', medium: 'default', high: 'accent' }[confidence.value] as any))

async function loadData() {
  loading.value = true
  error.value = ''
  try {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) return
    const { data: acc } = await supabase.schema('threads').from('threads_accounts').select('id').eq('user_id', user.id).maybeSingle()
    if (!acc) throw new Error("Account not found")
    const res = await fetch(`https://threads-automation-r9so.onrender.com/api/v1/analytics/best-time/${acc.id}`)
    const data = await res.json()
    if (!res.ok) throw new Error(data.detail)
    matrix.value = data.matrix || Array(7).fill(0).map(() => Array(24).fill(0))
    topSlots.value = data.top_slots || []
    totalPosts.value = data.total_posts || 0
    confidence.value = data.confidence || 'low'
  } catch (err: any) { error.value = err.message } finally { loading.value = false }
}
onMounted(loadData)
</script>
