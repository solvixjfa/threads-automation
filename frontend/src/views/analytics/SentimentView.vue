<template>
  <div class="space-y-6">
    <Card v-if="!loading && !error && bestSentiment" style="border-color: #e5e5e5; border-width: 2px;">
      <div class="p-5">
        <div class="flex items-center gap-1.5 text-[10px] font-bold uppercase tracking-wider theme-text-muted mb-2">
          <Sparkles class="w-3 h-3" />
          <span>{{ $t('analytics.sentiment_best_label') }}</span>
        </div>
        <div class="text-2xl font-black mb-1">{{ $t('analytics.sent_' + bestSentiment.sentiment) }}</div>
        <div class="text-sm theme-text-muted mb-3">
          {{ bestSentiment.avg_er.toFixed(2) }}% {{ $t('analytics.avg_er') }} &middot; {{ $t('analytics.hook_posts', { n: bestSentiment.count }) }}
        </div>
        <p class="text-xs theme-text-muted">{{ $t('analytics.sentiment_best_desc') }}</p>
      </div>
    </Card>

    <Card v-if="!loading && !error && data.length > 0">
      <template #header>
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-sm font-bold flex items-center gap-2">
              <Smile class="w-4 h-4 theme-text-muted" />
              {{ $t('analytics.sentiment_title') }}
            </h2>
            <p class="text-xs theme-text-muted mt-0.5">{{ $t('analytics.sentiment_sub') }}</p>
          </div>
        </div>
      </template>

      <div class="space-y-4">
        <div v-for="item in data" :key="item.sentiment" class="p-4 rounded-xl border theme-bg-sec theme-border flex justify-between items-center">
          <div class="flex items-center gap-3">
            <component :is="getIcon(item.sentiment)" class="w-5 h-5 theme-text-muted" />
            <div>
              <p class="text-sm font-bold capitalize">{{ $t('analytics.sent_' + item.sentiment) }}</p>
              <p class="text-[11px] theme-text-muted">{{ $t('analytics.hook_posts', { n: item.count }) }}</p>
            </div>
          </div>
          <div class="text-right">
            <p class="text-lg font-black">{{ item.avg_er.toFixed(2) }}%</p>
            <p class="text-[10px] theme-text-muted uppercase font-bold">{{ $t('analytics.avg_er') }}</p>
          </div>
        </div>
      </div>

      <!-- Visual Bar Chart -->
      <div class="mt-6 pt-4 border-t theme-border">
        <div class="text-xs font-bold theme-text-muted mb-3 uppercase tracking-wider">{{ $t('analytics.hook_visual') }}</div>
        <div class="space-y-2">
          <div v-for="item in sortedForChart" :key="'chart-' + item.sentiment" class="flex items-center gap-3">
            <div class="w-20 text-[11px] font-bold capitalize">{{ $t('analytics.sent_' + item.sentiment) }}</div>
            <div class="flex-1 h-5 rounded-sm overflow-hidden" style="background: #0f0f0f;">
              <div class="h-full transition-all" :style="{ width: (item.avg_er / maxEr * 100) + '%', background: '#e5e5e5' }"></div>
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
    <Card v-else-if="data.length === 0">
      <EmptyState :title="$t('analytics.not_enough')" :description="$t('analytics.no_data')" />
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { supabase } from '../../lib/supabase'
import { useI18n } from 'vue-i18n'
import { Card, Button, EmptyState } from '../../components/ui'
import { Smile, Meh, Frown, Sparkles, AlertCircle } from 'lucide-vue-next'

const { t } = useI18n()
const loading = ref(true)
const error = ref('')
const data = ref<any[]>([])
const bestSentiment = ref<any>(null)

function getIcon(sentiment: string) {
  if (sentiment === 'positive') return Smile
  if (sentiment === 'negative') return Frown
  return Meh
}

const sortedForChart = computed(() => {
  return [...data.value].sort((a, b) => b.avg_er - a.avg_er)
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
    
    const res = await fetch(`https://threads-automation-r9so.onrender.com/api/v1/analytics/sentiment-performance/${acc.id}`)
    const resData = await res.json()
    if (!res.ok) throw new Error(resData.detail || 'Failed to load')
    
    data.value = resData.data || []
    if (data.value.length > 0) {
      const valid = data.value.filter(d => d.count >= 2)
      if (valid.length > 0) {
        bestSentiment.value = [...valid].sort((a, b) => b.avg_er - a.avg_er)[0]
      }
    }
  } catch (err: any) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}
onMounted(loadData)
</script>
