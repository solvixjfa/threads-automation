<template>
  <div class="space-y-6">
    <Card v-if="!loading && !error && nextBest" style="border-color: #e5e5e5; border-width: 2px;">
      <div class="p-5">
        <div class="text-[10px] font-bold uppercase tracking-wider theme-text-muted mb-2">🎯 Waktu Terbaik Berikutnya</div>
        <div class="text-2xl font-black mb-1">{{ nextBest.weekday }}, {{ nextBest.hour_start }}–{{ nextBest.hour_end }} WIB</div>
        <div class="text-sm theme-text-muted mb-3">{{ (nextBest.er_pct || 0).toFixed(2) }}% avg ER · {{ nextBest.sample_size }} posts ({{ nextBest.name }})</div>
        <Button size="sm" @click="scheduleAt(nextBest)">📅 Jadwalkan Sekarang</Button>
      </div>
    </Card>

    <Card v-if="!loading && !error && benchmark">
      <div class="p-5">
        <div class="text-sm font-bold mb-2">📊 Data Masih Sedikit</div>
        <p class="text-xs theme-text-muted mb-3">Terus posting minimal 2 minggu untuk unlock rekomendasi personal. Sementara, ini benchmark industri Threads:</p>
        <div class="text-xs space-y-1 mb-2">
          <div class="font-bold mt-2 mb-1">Weekday (Selasa–Kamis):</div>
          <div v-for="b in benchmark.weekday_peak" :key="b" class="pl-3">• {{ b }}</div>
          <div class="font-bold mt-2 mb-1">Weekend:</div>
          <div v-for="b in benchmark.weekend_peak" :key="b" class="pl-3">• {{ b }}</div>
        </div>
        <p class="text-[10px] opacity-60 italic mt-3">{{ benchmark.note }}</p>
      </div>
    </Card>

    <Card>
      <template #header>
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-sm font-bold flex items-center gap-2">
              <Clock class="w-4 h-4 theme-text-muted" />
              {{ $t('analytics.best_title') }}
            </h2>
            <p class="text-xs theme-text-muted mt-0.5">{{ $t('analytics.best_subtitle') }}</p>
          </div>
          <Badge :variant="confidenceVariant">{{ confidenceLabel }}</Badge>
        </div>
      </template>

      <div v-if="loading" class="space-y-3">
        <div class="h-6 w-48 skeleton"></div>
        <div class="h-64 skeleton"></div>
      </div>

      <div v-else-if="error" class="text-center py-8 flex flex-col items-center gap-3">
        <AlertCircle class="w-8 h-8 text-red-500 opacity-50" />
        <p class="text-sm theme-text-muted">{{ error }}</p>
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

    <Card v-if="!loading && !error">
      <template #header>
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-sm font-bold flex items-center gap-2">
              <TrendingUp class="w-4 h-4 theme-text-muted" />
              Best Time Per Day
            </h2>
            <p class="text-xs theme-text-muted mt-0.5">Rekomendasi blok waktu terbaik untuk Senin–Minggu</p>
          </div>
        </div>
      </template>

      <div class="space-y-2">
        <div v-for="(block, idx) in bestBlockPerDay" :key="idx"
             class="flex items-center justify-between p-3 rounded-lg border transition-colors"
             :class="block.has_data ? 'theme-bg-sec theme-border hover:border-[var(--border-strong)]' : 'theme-border opacity-50'">
          <div class="flex items-center gap-3 min-w-0 flex-1">
            <div class="w-7 h-7 rounded-full flex items-center justify-center text-xs font-black shrink-0"
                 :style="{ background: block.has_data ? '#e5e5e5' : '#262626', color: block.has_data ? '#0f0f0f' : '#8a8a8a' }">
              {{ idx + 1 }}
            </div>
            <div class="min-w-0">
              <div class="text-sm font-bold truncate">
                {{ block.weekday }}
                <template v-if="block.has_data"> · {{ block.hour_start }}–{{ block.hour_end }} <span class="text-[10px] theme-text-muted">({{ block.name }})</span></template>
                <template v-else><span class="theme-text-muted font-normal text-xs italic"> · Belum ada data</span></template>
              </div>
              <div class="text-[11px] theme-text-muted" v-if="block.has_data">
                {{ block.sample_size }} posts · {{ block.sample_size < 2 ? '⚠️ sample tipis' : '✓ cukup' }}
              </div>
            </div>
          </div>
          <div class="flex items-center gap-3 shrink-0" v-if="block.has_data">
            <div class="text-right">
              <div class="text-lg font-black">{{ (block.er_pct || 0).toFixed(2) }}%</div>
              <div class="text-[10px] theme-text-muted uppercase font-bold">Avg ER</div>
            </div>
            <Button size="sm" variant="secondary" @click="scheduleAt(block)">Jadwalkan</Button>
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
import { Clock, TrendingUp, AlertCircle } from 'lucide-vue-next'

const { t } = useI18n()
const loading = ref(true)
const error = ref('')
const matrix = ref<number[][]>(Array(7).fill(0).map(() => Array(24).fill(0)))
const topSlots = ref<any[]>([])
const bestBlockPerDay = ref<any[]>([])
const nextBest = ref<any>(null)
const benchmark = ref<any>(null)
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
    bestBlockPerDay.value = data.best_block_per_day || []
    nextBest.value = data.next_best || null
    benchmark.value = data.benchmark || null
    totalPosts.value = data.total_posts || 0
    confidence.value = data.confidence || 'low'
  } catch (err: any) { error.value = err.message } finally { loading.value = false }
}
function scheduleAt(slot: any) {
  if (!slot || !slot.has_data) return
  const now = new Date()
  const targetDow = slot.weekday_num
  const todayDow = now.getDay()
  let diff = (targetDow - todayDow + 7) % 7
  const h = parseInt((slot.hour_start || slot.hour || '00:00').split(':')[0])
  if (diff === 0 && h <= now.getHours()) diff = 7
  const target = new Date(now)
  target.setDate(target.getDate() + diff)
  target.setHours(h, 0, 0, 0)
  const pad = (n: number) => String(n).padStart(2, '0')
  const isoLocal = `${target.getFullYear()}-${pad(target.getMonth()+1)}-${pad(target.getDate())}T${pad(h)}:00`
  localStorage.setItem('ixiera_draft_time', isoLocal)
  window.location.href = '/content/create'
}

onMounted(loadData)
</script>
