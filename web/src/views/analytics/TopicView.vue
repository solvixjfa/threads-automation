<template>
  <Card>
    <template #header>
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-sm font-bold">{{ $t('analytics.topic_title') }}</h2>
          <p class="text-xs theme-text-muted mt-0.5">{{ $t('analytics.topic_sub') }}</p>
        </div>
        <Badge variant="accent">{{ $t('analytics.smart_analysis') }}</Badge>
      </div>
    </template>

    <div v-if="loading" class="h-40 skeleton"></div>
    
    <div v-else-if="data.length === 0" class="text-center py-8">
      <EmptyState :title="$t('analytics.not_enough')" :description="$t('analytics.no_data')" />
    </div>
    
    <div v-else class="space-y-4">
      <div v-for="(item, idx) in data" :key="idx" class="p-5 rounded-xl theme-bg-sec border theme-border space-y-3">
        <!-- HEADER: NAMA TOPIK + STATS -->
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

        <!-- SAMPLE POSTS: BIAR USER NGERTI ISINYA APA -->
        <div v-if="item.samples && item.samples.length > 0" class="pt-3 border-t theme-border space-y-2">
          <p class="text-[10px] font-bold uppercase tracking-wider theme-text-muted">{{ $t('analytics.sample_posts') }}</p>
          <div 
            v-for="(sample, i) in item.samples" 
            :key="i" 
            class="text-xs leading-relaxed theme-text-muted pl-3 border-l-2 italic"
            style="border-color: var(--accent);"
          >
            "{{ sample }}"
          </div>
        </div>

        <!-- KEYWORDS: SEBAGAI TAG KECIL -->
        <div v-if="item.keywords && item.keywords.length > 0" class="flex flex-wrap gap-1.5 pt-1">
          <span 
            v-for="(kw, i) in item.keywords" 
            :key="i" 
            class="px-2 py-0.5 text-[10px] font-medium rounded-md theme-bg border theme-border theme-text-muted"
          >
            {{ kw }}
          </span>
        </div>
      </div>
    </div>
  </Card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { supabase } from '../../lib/supabase'
import { useI18n } from 'vue-i18n'
import { Card, Badge, EmptyState } from '../../components/ui'

const { t } = useI18n()
const loading = ref(true)
const data = ref<any[]>([])

async function loadData() {
  try {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) return
    const { data: acc } = await supabase.schema('threads').from('threads_accounts').select('id').eq('user_id', user.id).maybeSingle()
    if (!acc) return
    
    const res = await fetch(`https://threads-automation-production-53ad.up.railway.app/api/v1/analytics/topic-clusters/${acc.id}`)
    const resData = await res.json()
    if (resData.success) data.value = resData.data
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}
onMounted(loadData)
</script>
