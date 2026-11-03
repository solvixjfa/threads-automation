<template>
  <div class="space-y-6">
    <Card v-if="!loading && !error && bestBucket" style="border-color: #e5e5e5; border-width: 2px;">
      <div class="p-5">
        <div class="flex items-center gap-1.5 text-[10px] font-bold uppercase tracking-wider theme-text-muted mb-2">
          <Target class="w-3 h-3" />
          <span>{{ $t('analytics.length_best_label') }}</span>
        </div>
        <div class="text-2xl font-black mb-1">{{ bestBucket.bucket }} {{ $t('analytics.chars') }}</div>
        <div class="text-sm theme-text-muted mb-3">
          {{ bestBucket.avg_er.toFixed(2) }}% {{ $t('analytics.avg_er') }} &middot; {{ $t('analytics.hook_posts', { n: bestBucket.count }) }}
        </div>
        <Button size="sm" @click="createWithLength(bestBucket)">
          <PenLine class="w-4 h-4" />
          <span>{{ $t('analytics.length_create_btn') }}</span>
        </Button>
      </div>
    </Card>

    <Card v-if="!loading && !error && benchmark">
      <div class="p-5">
        <div class="flex items-center gap-2 text-sm font-bold mb-2">
          <BarChart3 class="w-4 h-4 theme-text-muted" />
          <span>{{ $t('analytics.length_lowdata_title') }}</span>
        </div>
        <p class="text-xs theme-text-muted mb-3">{{ $t('analytics.length_lowdata_desc') }}</p>
        <div class="text-xs pl-3">&bull; {{ benchmark.best_bucket }} {{ $t('analytics.chars') }} ({{ $t('analytics.avg_er') }} {{ benchmark.avg_er }})</div>
        <p class="text-[10px] opacity-60 italic mt-3">{{ $t('analytics.length_benchmark_note') }}</p>
      </div>
    </Card>

    <Card v-if="!loading && !error && data.length > 0">
      <template #header>
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-sm font-bold flex items-center gap-2">
              <AlignLeft class="w-4 h-4 theme-text-muted" />
              {{ $t('analytics.length_title') }}
            </h2>
            <p class="text-xs theme-text-muted mt-0.5">{{ $t('analytics.length_sub') }}</p>
          </div>
          <Badge :variant="confidenceVariant">{{ confidenceLabel }}</Badge>
        </div>
      </template>

      <div class="space-y-2">
        <div v-for="item in data" :key="item.bucket" class="p-4 rounded-xl border flex justify-between items-center"
             :class="item.count === 0 ? 'theme-border opacity-50' : 'theme-bg-sec theme-border'">
          <div class="flex items-center gap-3 min-w-0 flex-1">
            <div class="w-20 text-[11px] font-bold shrink-0">{{ item.bucket }} {{ $t('analytics.chars') }}</div>
            <div class="text-[11px] theme-text-muted">
              {{ $t('analytics.hook_posts', { n: item.count }) }}
              <span v-if="item.count > 0 && item.count < 3" class="ml-1">&mdash; {{ $t('analytics.sample_thin') }}</span>
            </div>
          </div>
          <div class="flex items-center gap-3 shrink-0">
            <div class="text-right">
              <div class="text-lg font-black">{{ item.avg_er.toFixed(2) }}%</div>
              <div class="text-[10px] theme-text-muted uppercase font-bold">{{ $t('analytics.avg_er') }}</div>
            </div>
            <Button v-if="item.count > 0" size="sm" variant="secondary" @click="createWithLength(item)">
              {{ $t('analytics.length_create_btn') }}
            </Button>
          </div>
        </div>
      </div>

      <div class="mt-6 pt-4 border-t theme-border">
        <div class="text-xs font-bold theme-text-muted mb-3 uppercase tracking-wider">{{ $t('analytics.hook_visual') }}</div>
        <div class="space-y-2">
          <div v-for="item in data" :key="'chart-' + item.bucket" class="flex items-center gap-3">
            <div class="w-20 text-[11px] font-bold">{{ item.bucket }}</div>
            <div class="flex-1 h-5 rounded-sm overflow-hidden" style="background: #0f0f0f;">
              <div class="h-full transition-all" :style="{ width: (item.avg_er / maxEr * 100) + '%', background: item.count === 0 ? '#262626' : '#e5e5e5' }"></div>
            </div>
            <div class="w-16 text-right text-[11px] font-black">{{ item.avg_er.toFixed(1) }}%</div>
          </div>
        </div>
      </div>
    </Card>

    <Card v-if="loading"><div class="h-40 skeleton"></div></Card>
    <Card v-else-if="error">
      <div class="text-center py-8 flex flex-col items-center gap-3">
        <AlertCircle class="w-8 h-8 opacity-50" />
        <p class="text-sm theme-text-muted">{{ error }}</p>
        <Button variant="secondary" size="sm" @click="loadData">{{ $t('common.retry') }}</Button>
      </div>
    </Card>
    <Card v-else-if="data.length === 0 && !benchmark">
      <EmptyState :title="$t('analytics.not_enough')" :description="$t('analytics.no_data')" />
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { supabase } from '../../lib/supabase'
import { useI18n } from 'vue-i18n'
import { Card, Badge, Button, EmptyState } from '../../components/ui'
import { Target, BarChart3, AlignLeft, AlertCircle, PenLine } from 'lucide-vue-next'

const { t } = useI18n()
const loading = ref(true)
const error = ref('')
const data = ref<any[]>([])
const bestBucket = ref<any>(null)
const benchmark = ref<any>(null)
const totalPosts = ref(0)
const confidence = ref<'low' | 'medium' | 'high'>('low')

const confidenceLabel = computed(() => ({
  low: t('analytics.conf_low'), medium: t('analytics.conf_med'), high: t('analytics.conf_high'),
}[confidence.value]))
const confidenceVariant = computed(() => ({ low: 'default', medium: 'default', high: 'accent' }[confidence.value] as any))

const maxEr = computed(() => {
  if (data.value.length === 0) return 1
  return Math.max(...data.value.map(d => d.avg_er), 1)
})

function createWithLength(item: any) {
  if (!item || !item.bucket) return
  window.location.href = `/content/create?length=${encodeURIComponent(item.bucket)}`
}

async function loadData() {
  loading.value = true
  error.value = ''
  try {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) return
    const { data: acc } = await supabase.schema('threads').from('threads_accounts').select('id').eq('user_id', user.id).maybeSingle()
    if (!acc) throw new Error("Account not found")
    const res = await fetch(`https://threads-automation-r9so.onrender.com/api/v1/analytics/length-performance/${acc.id}`)
    const resData = await res.json()
    if (!res.ok) throw new Error(resData.detail || 'Failed to load')
    data.value = resData.data || []
    bestBucket.value = resData.best_bucket || null
    benchmark.value = resData.benchmark || null
    totalPosts.value = resData.total_posts || 0
    confidence.value = resData.confidence || 'low'
  } catch (err: any) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}
onMounted(loadData)
</script>
