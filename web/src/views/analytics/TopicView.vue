<template>
  <Card>
    <template #header>
      <div class="flex items-center justify-between flex-wrap gap-3">
        <div>
          <h2 class="text-sm font-bold">{{ $t('analytics.topic_title') }}</h2>
          <p class="text-xs theme-text-muted mt-0.5">{{ $t('analytics.topic_sub') }}</p>
        </div>
        <div class="flex items-center gap-2 flex-wrap">
          <Badge variant="accent">{{ $t('analytics.smart_analysis') }}</Badge>
          <button 
            v-if="!enhanced" 
            @click="enhanceNames" 
            :disabled="isEnhancing || (!isUsingOwnKey && aiCredits <= 0)"
            class="text-xs font-bold px-3 py-1.5 rounded-lg border theme-border hover:theme-bg-sec transition flex items-center gap-1.5"
          >
            <span v-if="isEnhancing" class="w-3 h-3 border-2 border-current border-t-transparent rounded-full animate-spin"></span>
            <span v-else>✨</span>
            {{ isEnhancing ? 'Enhancing...' : (isUsingOwnKey ? 'Enhance with AI (Free)' : 'Enhance Names (1 Credit)') }}
          </button>
        </div>
      </div>
    </template>

    <div v-if="loading" class="h-40 skeleton"></div>
    
    <div v-else-if="data.length === 0" class="text-center py-8">
      <EmptyState :title="$t('analytics.not_enough')" :description="$t('analytics.no_data')" />
    </div>
    
    <div v-else class="space-y-4">
      <div v-for="(item, idx) in data" :key="idx" class="p-5 rounded-xl theme-bg-sec border theme-border space-y-3">
        <div class="flex justify-between items-start gap-3">
          <div class="flex-1 min-w-0">
            <h3 class="text-sm font-bold theme-text">{{ item.topic }}</h3>
            <p class="text-xs theme-text-muted mt-0.5">{{ $t('analytics.topic_posts', { n: item.count }) }}</p>
          </div>
          <div class="text-right shrink-0">
            <p class="text-xl font-black theme-text">{{ item.avg_er }}%</p>
            <p class="text-[10px] theme-text-muted uppercase font-bold">{{ $t('analytics.avg_er') }}</p>
          </div>
        </div>

        <div v-if="item.samples && item.samples.length > 0" class="pt-3 border-t theme-border space-y-2">
          <p class="text-[10px] font-bold uppercase tracking-wider theme-text-muted">{{ $t('analytics.sample_posts') }}</p>
          <div v-for="(sample, i) in item.samples" :key="i" class="text-xs leading-relaxed theme-text-muted pl-3 border-l-2 italic" style="border-color: var(--accent);">
            "{{ sample }}"
          </div>
        </div>

        <div v-if="item.keywords && item.keywords.length > 0" class="flex flex-wrap gap-1.5 pt-1">
          <span v-for="(kw, i) in item.keywords" :key="i" class="px-2 py-0.5 text-[10px] font-medium rounded-md theme-bg border theme-border theme-text-muted">{{ kw }}</span>
        </div>
      </div>
    </div>
  </Card>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { supabase } from '../../lib/supabase'
import { useNotify } from '../../composables/useNotify'
import { useI18n } from 'vue-i18n'
import { Card, Badge, EmptyState } from '../../components/ui'

const { t } = useI18n()
const { showToast } = useNotify()
const loading = ref(true)
const isEnhancing = ref(false)
const data = ref<any[]>([])
const enhanced = ref(false)
const aiCredits = ref(0)
const customGeminiKey = ref('')
const customGroqKey = ref('')
const currentAccountId = ref<string | null>(null)
const aiProvider = ref('groq')

const isUsingOwnKey = computed(() => {
  if (aiProvider.value === 'groq') return !!customGroqKey.value
  return !!customGeminiKey.value
})

async function loadData() {
  try {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) return
    const { data: acc } = await supabase.schema('threads').from('threads_accounts')
      .select('id, credit_balance, custom_gemini_key, custom_groq_key, ai_provider, topic_labels_cache, topic_labels_cached_at')
      .eq('user_id', user.id).maybeSingle()
    if (!acc) return
    
    currentAccountId.value = acc.id
    aiCredits.value = acc.credit_balance ?? 0
    customGeminiKey.value = acc.custom_gemini_key || ''
    customGroqKey.value = acc.custom_groq_key || ''
    if (acc.ai_provider) aiProvider.value = acc.ai_provider
    
    // Fetch clusters
    const res = await fetch(`https://threads-automation-production-53ad.up.railway.app/api/v1/analytics/topic-clusters/${acc.id}`)
    const resData = await res.json()
    if (resData.success) data.value = resData.data
    
    // Cek cache: kalau cache valid (<24 jam), langsung pakai
    if (acc.topic_labels_cache && acc.topic_labels_cached_at && data.value.length > 0) {
      const cachedAt = new Date(acc.topic_labels_cached_at).getTime()
      const hoursOld = (Date.now() - cachedAt) / (1000 * 60 * 60)
      
      if (hoursOld < 24) {
        const cachedNames: string[] = acc.topic_labels_cache
        if (Array.isArray(cachedNames) && cachedNames.length === data.value.length) {
          data.value = data.value.map((cluster, i) => ({
            ...cluster,
            topic: cachedNames[i] || cluster.topic
          }))
          enhanced.value = true
        }
      }
    }
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

async function enhanceNames() {
  if (!currentAccountId.value || data.value.length === 0) return
  isEnhancing.value = true
  try {
    const res = await fetch('https://threads-automation-production-53ad.up.railway.app/api/v1/rag/label-topics', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        account_id: currentAccountId.value,
        clusters: data.value.map(c => ({ count: c.count, samples: c.samples })),
        provider: aiProvider.value,
        model_name: null
      })
    })
    
    const result = await res.json()
    if (!res.ok) throw new Error(result.detail)
    
    const names: string[] = result.topics || []
    
    // Update UI
    data.value = data.value.map((cluster, i) => ({
      ...cluster,
      topic: names[i] || cluster.topic
    }))
    enhanced.value = true
    
    // Kurangi kredit lokal (kalau pakai SaaS key)
    if (!isUsingOwnKey.value) {
      aiCredits.value = Math.max(0, aiCredits.value - 1)
    }
    
    // Simpan ke cache di DB
    await supabase.schema('threads').from('threads_accounts').update({
      topic_labels_cache: names,
      topic_labels_cached_at: new Date().toISOString()
    }).eq('id', currentAccountId.value)
    
    showToast('Topic names enhanced!', 'success')
  } catch (err: any) {
    showToast('Enhance failed: ' + err.message, 'error')
  } finally {
    isEnhancing.value = false
  }
}

onMounted(loadData)
</script>
