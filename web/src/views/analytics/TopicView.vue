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
    <div v-else class="space-y-3">
      <div v-for="(item, idx) in data" :key="idx" class="p-4 rounded-xl theme-bg-sec border theme-border flex justify-between items-center">
        <div>
          <p class="text-sm font-bold">{{ item.topic }}</p>
          <p class="text-xs theme-text-muted">{{ $t('analytics.topic_posts', { n: item.count }) }}</p>
        </div>
        <div class="text-right">
          <p class="text-lg font-black">{{ item.avg_er }}%</p>
          <p class="text-[10px] theme-text-muted uppercase font-bold">{{ $t('analytics.avg_er') }}</p>
        </div>
      </div>
    </div>
  </Card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { supabase } from '../../lib/supabase'
import { Card, Badge, EmptyState } from '../../components/ui'

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
  } catch (err) { console.error(err) } finally { loading.value = false }
}
onMounted(loadData)
</script>
