<template>
  <div class="space-y-6">
    <!-- NEXT BEST CARD -->
    <Card v-if="!loading && !error && nextBest" style="border-color: #e5e5e5; border-width: 2px;">
      <div class="p-5">
        <div class="flex items-center gap-1.5 text-[10px] font-bold uppercase tracking-wider theme-text-muted mb-2">
          <Target class="w-3 h-3" />
          <span>{{ $t('analytics.best_next_title') }}</span>
        </div>
        <div class="text-2xl font-black mb-1">
          {{ formatWeekday(nextBest.weekday_num) }}, {{ nextBest.hour_start }}–{{ nextBest.hour_end }} WIB
        </div>
        <div class="text-sm theme-text-muted mb-3">
          {{ (nextBest.er_pct || 0).toFixed(2) }}% {{ $t('analytics.avg_er') }} · {{ $t('analytics.hook_posts', { n: nextBest.sample_size }) }} ({{ formatTimeBlock(nextBest.name) }})
        </div>
        <Button size="sm" @click="scheduleAt(nextBest)">
          <Calendar class="w-4 h-4 mr-1.5" />
          {{ $t('analytics.schedule_now') }}
        </Button>
      </div>
    </Card>

    <!-- BENCHMARK CARD -->
    <Card v-if="!loading && !error && benchmark">
      <div class="p-5">
        <div class="flex items-center gap-2 text-sm font-bold mb-2">
          <BarChart3 class="w-4 h-4 theme-text-muted" />
          <span>{{ $t('analytics.lowdata_title') }}</span>
        </div>
        <p class="text-xs theme-text-muted mb-3">{{ $t('analytics.lowdata_desc') }}</p>
        <div class="text-xs space-y-1 mb-2">
          <div class="font-bold mt-2 mb-1">{{ $t('analytics.industry_best') }}</div>
          <div v-for="b in benchmark.weekday_peak" :key="b" class="pl-3">• {{ b }}</div>
          <div v-for="b in benchmark.weekend_peak" :key="b" class="pl-3">• {{ b }}</div>
        </div>
        <p class="text-[10px] opacity-60 italic mt-3">{{ $t('analytics.industry_note') }}</p>
      </div>
    </Card>

    <!-- HOURLY TREND -->
    <Card v-if="!loading && !error">
      <template #header>
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-sm font-bold flex items-center gap-2">
              <Clock class="w-4 h-4 theme-text-muted" />
              {{ $t('analytics.best_title') }}
            </h2>
            <p class="text-xs theme-text-muted mt-0.5">{{ $t('analytics.hourly_trend_sub') }}</p>
          </div>
          <Badge :variant="confidenceVariant">{{ confidenceLabel }}</Badge>
        </div>
      </template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { supabase } from '../../lib/supabase'
import { useI18n } from 'vue-i18n'
import { Card, Badge, Button, EmptyState } from '../../components/ui'
import BestTimeLineChart from '../../components/BestTimeLineChart.vue'
import BestTimeChart from '../../components/BestTimeChart.vue'
import { Clock, TrendingUp, AlertCircle, Target, Calendar, BarChart3 } from 'lucide-vue-next'

const { t } = useI18n()
const loading = ref(true)
const error = ref('')
const matrix = ref<number[][]>(Array(7).fill(0).map(() => Array(24).fill(0)))
const topSlots = ref<any[]>([])
const nextBest = ref<any>(null)
const benchmark = ref<any>(null)
const totalPosts = ref(0)
const confidence = ref<'low' | 'medium' | 'high'>('low')
const selectedBlock = ref<any>(null)

const confidenceLabel = computed(() => ({
  low: t('analytics.conf_low'), medium: t('analytics.conf_med'), high: t('analytics.conf_high'),
}[confidence.value]))

const confidenceVariant = computed(() => ({ low: 'default', medium: 'default', high: 'accent' }[confidence.value] as any))

const translatedSlots = computed(() => {
  if (!topSlots.value || topSlots.value.length === 0) return []
  return topSlots.value.map((s: any) => {
    let dayKey = 'sunday'
    if (s.weekday_num === 1) dayKey = 'monday'
    else if (s.weekday_num === 2) dayKey = 'tuesday'
    else if (s.weekday_num === 3) dayKey = 'wednesday'
    else if (s.weekday_num === 4) dayKey = 'thursday'
    else if (s.weekday_num === 5) dayKey = 'friday'
    else if (s.weekday_num === 6) dayKey = 'saturday'

    return {
      ...s,
      weekdayLabel: `${t('days.' + dayKey)} (${s.hour})`,
      displayHour: s.hour
    }
  })
})

function formatWeekday(dayNum: number) {
  const keys = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
  return t('days.' + keys[dayNum])
}

function formatTimeBlock(name: string) {
  return t('time_blocks.' + (name || '').toLowerCase().replace(' ', '_'))
}

function scheduleAt(slot: any) {
  if (!slot) return
  const now = new Date()
  const targetDow = slot.weekday_num
  const todayDow = now.getDay()
  let diff = (targetDow - todayDow + 7) % 7
  const hourStr = slot.hour || slot.hour_start || '08:00'
  const h = parseInt(hourStr.split(':')[0])
  if (diff === 0 && h <= now.getHours()) diff = 7
  const target = new Date(now)
  target.setDate(target.getDate() + diff)
  target.setHours(h, 0, 0, 0)
  const pad = (n: number) => String(n).padStart(2, '0')
  const isoLocal = `${target.getFullYear()}-${pad(target.getMonth()+1)}-${pad(target.getDate())}T${pad(h)}:00`
  localStorage.setItem('ixiera_draft_time', isoLocal)
  window.location.href = `/content/create?scheduled=${encodeURIComponent(isoLocal)}`
}

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
    nextBest.value = data.next_best || null
    benchmark.value = data.benchmark || null
    totalPosts.value = data.total_posts || 0
    confidence.value = data.confidence || 'low'
  } catch (err: any) { error.value = err.message } finally { loading.value = false }
}
onMounted(loadData)
</script>
