<template>
  <div class="space-y-6">
    <Card>
      <template #header>
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-sm font-bold">Best Time to Post</h2>
            <p class="text-xs theme-text-muted mt-0.5">Engagement rate heatmap by day and hour (WIB)</p>
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
        <Button variant="secondary" size="sm" @click="loadData">Try Again</Button>
      </div>

      <div v-else-if="totalPosts === 0" class="text-center py-8">
        <EmptyState
          title="Not enough data"
          description="You need published posts with metrics to calculate your best time recommendations."
        />
      </div>

      <div v-else class="space-y-6">
        <div class="flex flex-wrap gap-4 text-xs">
          <div>
            <span class="theme-text-muted">Total posts analyzed:</span>
            <span class="font-bold ml-1.5">{{ totalPosts }}</span>
          </div>
          <div>
            <span class="theme-text-muted">Confidence:</span>
            <span class="font-bold ml-1.5 capitalize">{{ confidence }}</span>
          </div>
        </div>

        <BestTimeHeatmap :matrix="matrix" />
      </div>
    </Card>

    <Card v-if="!loading && !error && topSlots.length > 0">
      <template #header>
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-sm font-bold">Top 5 Best Slots</h2>
            <p class="text-xs theme-text-muted mt-0.5">Based on historical average engagement rate</p>
          </div>
        </div>
      </template>

      <div class="space-y-2">
        <div v-for="(slot, idx) in topSlots" :key="idx" class="flex items-center justify-between p-3 rounded-lg theme-bg-sec border theme-border">
          <div class="flex items-center gap-3">
            <div class="w-7 h-7 rounded-full flex items-center justify-center text-xs font-black theme-accent">
              {{ idx + 1 }}
            </div>
            <div>
              <div class="text-sm font-bold">{{ slot.weekday }}, {{ slot.hour }}</div>
              <div class="text-[11px] theme-text-muted">Sample: {{ slot.sample_size }} posts</div>
            </div>
          </div>
          <div class="text-right">
            <div class="text-lg font-black">{{ (slot.er_pct || 0).toFixed(2) }}%</div>
            <div class="text-[10px] theme-text-muted uppercase font-bold">Avg ER</div>
          </div>
        </div>
      </div>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { supabase } from '../../lib/supabase'
import { Card, Badge, Button, EmptyState } from '../../components/ui'
import BestTimeHeatmap from '../../components/BestTimeHeatmap.vue'

const loading = ref(true)
const error = ref('')
const matrix = ref<number[][]>(Array(7).fill(0).map(() => Array(24).fill(0)))
const topSlots = ref<any[]>([])
const totalPosts = ref(0)
const confidence = ref<'low' | 'medium' | 'high'>('low')

const confidenceLabel = computed(() => ({
  low: 'Limited Data', medium: 'Fairly Accurate', high: 'Accurate',
}[confidence.value]))

const confidenceVariant = computed(() => ({
  low: 'default', medium: 'default', high: 'accent',
}[confidence.value] as any))

async function loadData() {
  loading.value = true
  error.value = ''
  try {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) return
    
    const { data: acc } = await supabase.schema('threads').from('threads_accounts').select('id').eq('user_id', user.id).maybeSingle()
    if (!acc) throw new Error("Account not found")

    const res = await fetch(`https://threads-automation-production-53ad.up.railway.app/api/v1/analytics/best-time/${acc.id}`)
    const data = await res.json()
    if (!res.ok) throw new Error(data.detail || 'Failed to load data')

    matrix.value = data.matrix || Array(7).fill(0).map(() => Array(24).fill(0))
    topSlots.value = data.top_slots || []
    totalPosts.value = data.total_posts || 0
    confidence.value = data.confidence || 'low'
  } catch (err: any) {
    error.value = err.message || 'An error occurred'
  } finally {
    loading.value = false
  }
}

onMounted(loadData)
</script>
