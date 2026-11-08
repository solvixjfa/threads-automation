<template>
  <div>
    <div v-if="isRoot">
      <div class="mb-6">
        <h1 class="text-2xl font-bold tracking-tight flex items-center gap-2">
          <BarChart3 class="w-6 h-6 theme-text-muted hidden sm:block" />
          {{ $t('analytics.title') }}
        </h1>
        <p class="text-sm theme-text-muted mt-1">{{ $t('analytics.subtitle') }}</p>
      </div>

      <!-- Deep Analyze Banner -->
      <div v-if="analysisStatus && !analysisStatus.is_cached" class="mb-4 p-4 rounded-xl border-2 border-[var(--border-strong)] theme-bg-sec">
        <div class="flex items-start gap-3">
          <div class="w-10 h-10 rounded-lg flex items-center justify-center bg-[var(--text)] text-[var(--bg)] shrink-0">
            <Bot class="w-5 h-5" />
          </div>
          <div class="flex-1 min-w-0">
            <h3 class="text-sm font-bold mb-1">
              {{ analysisStatus.analyzed_posts === 0 ? $t('analytics.deep_notyet') : $t('analytics.deep_partial', { done: analysisStatus.analyzed_posts, total: analysisStatus.total_posts }) }}
            </h3>
            <p class="text-xs theme-text-muted mb-3">{{ $t('analytics.deep_desc') }}</p>

            <div class="flex flex-wrap items-center gap-2">
              <div class="inline-flex rounded-lg border theme-border overflow-hidden text-xs">
                <button
                  type="button"
                  @click="selectedModel = 'hemat'"
                  class="px-3 py-1.5 font-bold transition"
                  :class="selectedModel === 'hemat' ? 'bg-[var(--text)] text-[var(--bg)]' : 'theme-text-muted hover:theme-text'"
                  :disabled="isAnalyzing"
                >
                  {{ $t('analytics.deep_model_hemat') }}
                </button>
                <button
                  type="button"
                  @click="selectedModel = 'akurat'"
                  class="px-3 py-1.5 font-bold transition border-l theme-border"
                  :class="selectedModel === 'akurat' ? 'bg-[var(--text)] text-[var(--bg)]' : 'theme-text-muted hover:theme-text'"
                  :disabled="isAnalyzing"
                >
                  {{ $t('analytics.deep_model_akurat') }}
                </button>
              </div>

            <Button @click="runDeepAnalyze" :disabled="isAnalyzing" size="sm">
              <span v-if="isAnalyzing" class="w-3 h-3 border-2 border-current border-t-transparent rounded-full animate-spin mr-1.5"></span>
              <Bot v-else class="w-4 h-4 mr-1.5" />
              {{ isAnalyzing ? $t('analytics.deep_loading') : (analysisStatus.plan === 'trial' ? $t('analytics.deep_btn_trial') : $t('analytics.deep_btn')) }}
            </Button>
          </div>
        </div>
      </div>

      <!-- Deep Analyze Active Badge -->
      <div v-else-if="analysisStatus && analysisStatus.is_cached" class="mb-4 flex items-center gap-2 text-xs theme-text-muted">
        <CheckCircle2 class="w-4 h-4" style="color: #10b981;" />
        <span>{{ $t('analytics.deep_active', { n: analysisStatus.analyzed_posts }) }}</span>
      </div>

      <div class="space-y-2">
        <RouterLink
          v-for="item in menuItems"
          :key="item.path"
          :to="item.path"
          class="card p-4 flex items-center justify-between hover:border-[var(--border-strong)] transition group"
        >
          <div class="flex items-center gap-3">
            <div class="w-9 h-9 rounded-lg flex items-center justify-center theme-bg-sec border theme-border">
              <component :is="item.icon" class="w-4 h-4 theme-text-muted" />
            </div>
            <div>
              <p class="text-sm font-bold">{{ $t(item.labelKey) }}</p>
              <p class="text-[11px] theme-text-muted">{{ $t(item.descKey) }}</p>
            </div>
          </div>
          <ChevronRight class="w-4 h-4 theme-text-muted opacity-50 group-hover:opacity-100 transition" />
        </RouterLink>
      </div>
    </div>

    <div v-else>
      <button
        @click="$router.push('/analytics')"
        type="button"
        class="mb-4 -ml-2 flex items-center gap-1 px-2 py-1.5 rounded-md hover:theme-bg-hover transition theme-text-muted hover:theme-text text-sm font-medium"
      >
        <ChevronLeft class="w-4 h-4" />
        {{ $t('analytics.title') }}
      </button>
      <RouterView />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { supabase } from '../../lib/supabase'
import { Button } from '../../components/ui'
import { useRoute, RouterView, RouterLink } from 'vue-router'
import { BarChart3, Clock, Anchor, AlignLeft, Hash, ChevronRight, ChevronLeft, Bot, CheckCircle2 } from 'lucide-vue-next'

const route = useRoute()

const analysisStatus = ref<any>(null)
const isAnalyzing = ref(false)
const selectedModel = ref<'hemat' | 'akurat'>('hemat')
const currentAccountId = ref<string | null>(null)

async function fetchAnalysisStatus() {
  try {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) return
    const { data: acc } = await supabase.schema('threads').from('threads_accounts')
      .select('id').eq('user_id', user.id).maybeSingle()
    if (!acc) return
    currentAccountId.value = acc.id
    const res = await fetch(`https://threads-automation-r9so.onrender.com/api/v1/analytics/analysis-status/${acc.id}`)
    const data = await res.json()
    if (data.success) analysisStatus.value = data
  } catch (e) { console.warn('[analytics] status fetch', e) }
}

async function runDeepAnalyze() {
  if (!currentAccountId.value || isAnalyzing.value) return
  isAnalyzing.value = true
  try {
    const res = await fetch(`https://threads-automation-r9so.onrender.com/api/v1/analytics/deep-analyze/${currentAccountId.value}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ model: selectedModel.value })
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.detail || 'Failed')
    await fetchAnalysisStatus()
    window.location.reload()
  } catch (e: any) {
    alert('Deep Analyze gagal: ' + (e.message || 'Unknown error'))
  } finally {
    isAnalyzing.value = false
  }
}

onMounted(() => fetchAnalysisStatus())
const isRoot = computed(() => route.path === '/analytics' || route.path === '/analytics/')

const menuItems = [
  { path: '/analytics/best-time', icon: Clock, labelKey: 'analytics.tab_best', descKey: 'analytics.desc_best' },
  { path: '/analytics/hook', icon: Anchor, labelKey: 'analytics.tab_hook', descKey: 'analytics.desc_hook' },
  { path: '/analytics/length', icon: AlignLeft, labelKey: 'analytics.tab_length', descKey: 'analytics.desc_length' },
  { path: '/analytics/topic', icon: Hash, labelKey: 'analytics.tab_topic', descKey: 'analytics.desc_topic' },
]
</script>
