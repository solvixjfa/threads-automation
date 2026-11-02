<template>
  <div class="space-y-6">
    <Card v-if="!loading && !error && bestInsight" style="border-color: #e5e5e5; border-width: 2px;">
      <div class="p-5">
        <div class="flex items-center gap-1.5 text-[10px] font-bold uppercase tracking-wider theme-text-muted mb-2">
          <Target class="w-3 h-3" />
          <span>Hook Terbaik Anda</span>
        </div>
        <div class="text-2xl font-black mb-1">{{ bestInsight.type }}</div>
        <div class="text-sm theme-text-muted mb-3">
          {{ bestInsight.avg_er.toFixed(2) }}% avg ER &middot; {{ bestInsight.count }} posts
        </div>
        <p class="text-xs theme-text-muted">
          Tipe hook ini performa terbaik di akun Anda. Coba tulis post baru dengan pola ini.
        </p>
      </div>
    </Card>

    <Card v-if="!loading && !error && benchmark">
      <div class="p-5">
        <div class="flex items-center gap-2 text-sm font-bold mb-2">
          <BarChart3 class="w-4 h-4 theme-text-muted" />
          <span>Data Masih Sedikit</span>
        </div>
        <p class="text-xs theme-text-muted mb-3">
          Terus posting minimal 2 minggu untuk unlock insight personal. Sementara, ini benchmark industri Threads:
        </p>
        <div class="text-xs space-y-1 mb-2">
          <div class="font-bold mt-2 mb-1">Hook Industri Terbaik:</div>
          <div class="pl-3">&bull; {{ benchmark.best_hook }} (avg ER {{ benchmark.avg_er }})</div>
        </div>
        <p class="text-[10px] opacity-60 italic mt-3">{{ benchmark.note }}</p>
      </div>
    </Card>

    <Card v-if="!loading && !error && data.length > 0">
      <template #header>
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-sm font-bold flex items-center gap-2">
              <Sparkles class="w-4 h-4 theme-text-muted" />
              Hook Performance
            </h2>
            <p class="text-xs theme-text-muted mt-0.5">
              Bandingkan performa tipe hook berdasarkan {{ totalPosts }} post
            </p>
          </div>
          <Badge :variant="confidenceVariant">{{ confidenceLabel }}</Badge>
        </div>
      </template>

      <div class="space-y-2">
        <div v-for="item in data" :key="item.type" class="p-4 rounded-xl border flex justify-between items-center"
             :class="item.type === 'Statement' ? 'theme-border opacity-60' : 'theme-bg-sec theme-border'">
          <div class="flex items-center gap-3 min-w-0 flex-1">
            <div class="w-8 h-8 rounded-full flex items-center justify-center text-xs font-black shrink-0"
                 :style="{ background: item.type === 'Statement' ? '#262626' : '#e5e5e5', color: item.type === 'Statement' ? '#8a8a8a' : '#0f0f0f' }">
              {{ item.type.charAt(0) }}
            </div>
            <div class="min-w-0">
              <div class="text-sm font-bold truncate">{{ item.type }}</div>
              <div class="text-[11px] theme-text-muted">
                {{ item.count }} posts
                <span v-if="item.count < 3" class="ml-1">&mdash; sample tipis</span>
              </div>
            </div>
          </div>
          <div class="text-right shrink-0 ml-3">
            <div class="text-lg font-black">{{ item.avg_er.toFixed(2) }}%</div>
            <div class="text-[10px] theme-text-muted uppercase font-bold">Avg ER</div>
          </div>
        </div>
      </div>

      <div class="mt-6 pt-4 border-t theme-border">
        <div class="text-xs font-bold theme-text-muted mb-3 uppercase tracking-wider">Perbandingan Visual</div>
        <div class="space-y-2">
          <div v-for="item in sortedForChart" :key="'chart-' + item.type" class="flex items-center gap-3">
            <div class="w-20 text-[11px] font-bold truncate">{{ item.type }}</div>
            <div class="flex-1 h-5 rounded-sm overflow-hidden" style="background: #0f0f0f;">
              <div class="h-full transition-all" :style="{ width: (item.avg_er / maxEr * 100) + '%', background: item.type === 'Statement' ? '#3a3a3a' : '#e5e5e5' }"></div>
            </div>
            <div class="w-16 text-right text-[11px] font-black">{{ item.avg_er.toFixed(1) }}%</div>
          </div>
        </div>
      </div>
    </Card>

    <Card v-if="loading">
      <div class="h-40 skeleton"></div>
    </Card>
    <Card v-else-if="error">
      <div class="text-center py-8 flex flex-col items-center gap-3">
        <AlertCircle class="w-8 h-8 opacity-50" />
        <p class="text-sm theme-text-muted">{{ error }}</p>
        <Button variant="secondary" size="sm" @click="loadData">Coba Lagi</Button>
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
import { Target, BarChart3, Sparkles, AlertCircle } from 'lucide-vue-next'

const { t } = useI18n()
const loading = ref(true)
const error = ref('')
const data = ref<any[]>([])
const bestInsight = ref<any>(null)
const benchmark = ref<any>(null)
const totalPosts = ref(0)
const confidence = ref<'low' | 'medium' | 'high'>('low')

const confidenceLabel = computed(() => ({
  low: 'Data Kurang', medium: 'Cukup', high: 'Valid',
}[confidence.value]))

const confidenceVariant = computed(() => ({ low: 'default', medium: 'default', high: 'accent' }[confidence.value] as any))

const sortedForChart = computed(() => {
  const arr = [...data.value]
  arr.sort((a, b) => b.avg_er - a.avg_er)
  return arr
})

const maxEr = computed(() => {
  if (data.value.length === 0) return 1
  return Math.max(...data.value.map(d => d.avg_er), 1)
})

async function loadData() {
  loading.value = true
  error.value = ''
  try {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) return
    const { data: acc } = await supabase.schema('threads').from('threads_accounts').select('id').eq('user_id', user.id).maybeSingle()
    if (!acc) throw new Error("Account not found")
    const res = await fetch(`https://threads-automation-r9so.onrender.com/api/v1/analytics/hook-performance/${acc.id}`)
    const resData = await res.json()
    if (!res.ok) throw new Error(resData.detail || 'Failed to load')
    data.value = resData.data || []
    bestInsight.value = resData.best_insight || null
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
