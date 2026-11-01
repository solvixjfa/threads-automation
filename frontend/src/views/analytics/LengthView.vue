<template>
  <Card>
    <template #header>
      <h2 class="text-sm font-bold">{{ $t('analytics.length_title') }}</h2>
      <p class="text-xs theme-text-muted mt-0.5">{{ $t('analytics.length_sub') }}</p>
    </template>
    <div v-if="loading" class="h-40 skeleton"></div>
    <div v-else-if="data.length === 0" class="text-center py-8">
      <EmptyState :title="$t('analytics.not_enough')" :description="$t('analytics.no_data')" />
    </div>
    <div v-else class="space-y-3">
      <div v-for="item in data" :key="item.range" class="p-4 rounded-xl theme-bg-sec border theme-border flex justify-between items-center">
        <div>
          <p class="text-sm font-bold">{{ item.range }}</p>
          <p class="text-xs theme-text-muted">{{ $t('analytics.hook_posts', { n: item.count }) }}</p>
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
import { Card, EmptyState } from '../../components/ui'

const loading = ref(true)
const data = ref<any[]>([])

async function loadData() {
  try {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) return
    const { data: acc } = await supabase.schema('threads').from('threads_accounts').select('id').eq('user_id', user.id).maybeSingle()
    if (!acc) return
    const res = await fetch(`https://threads-automation-r9so.onrender.com/api/v1/analytics/length-performance/${acc.id}`)
    const resData = await res.json()
    if (resData.success) data.value = resData.data
  } catch (err) { console.error(err) } finally { loading.value = false }
}
onMounted(loadData)
</script>
