<template>
  <div class="max-w-5xl mx-auto space-y-8">
    <div>
      <h1 class="text-2xl font-bold text-white tracking-tight">Analytics & Overview</h1>
      <p class="text-zinc-400 text-sm mt-1">Ringkasan performa postingan dan metrik akun Threads kamu.</p>
    </div>

    <!-- Stats Overview Cards -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
      <div class="bg-zinc-950/80 backdrop-blur-xl border border-white/10 p-5 rounded-xl space-y-1">
        <span class="text-xs text-zinc-500 uppercase tracking-wider font-semibold">Total Scheduled</span>
        <p class="text-2xl font-bold text-white font-mono">{{ stats.scheduled }}</p>
      </div>
      <div class="bg-zinc-950/80 backdrop-blur-xl border border-white/10 p-5 rounded-xl space-y-1">
        <span class="text-xs text-zinc-500 uppercase tracking-wider font-semibold">Total Published</span>
        <p class="text-2xl font-bold text-white font-mono">{{ stats.published }}</p>
      </div>
      <div class="bg-zinc-950/80 backdrop-blur-xl border border-white/10 p-5 rounded-xl space-y-1">
        <span class="text-xs text-zinc-500 uppercase tracking-wider font-semibold">Replies Received</span>
        <p class="text-2xl font-bold text-white font-mono">{{ stats.replies }}</p>
      </div>
      <div class="bg-zinc-950/80 backdrop-blur-xl border border-white/10 p-5 rounded-xl space-y-1">
        <span class="text-xs text-zinc-500 uppercase tracking-wider font-semibold">Pending Auto-Reply</span>
        <p class="text-2xl font-bold text-white font-mono">{{ stats.pendingReviews }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { supabase } from '../lib/supabase'

const stats = ref({
  scheduled: 0,
  published: 0,
  replies: 0,
  pendingReviews: 0
})

async function fetchOverview() {
  try {
    const { data: accData } = await supabase
      .schema('threads')
      .from('threads_accounts')
      .select('id')
      .limit(1)
      .maybeSingle()

    if (!accData?.id) return

    const [schedRes, pubRes, repRes, revRes] = await Promise.all([
      supabase.schema('threads').from('scheduled_posts').select('id', { count: 'exact', head: true }).eq('account_id', accData.id).eq('status', 'scheduled'),
      supabase.schema('threads').from('scheduled_posts').select('id', { count: 'exact', head: true }).eq('account_id', accData.id).eq('status', 'published'),
      supabase.schema('threads').from('replies').select('id', { count: 'exact', head: true }).eq('account_id', accData.id),
      supabase.schema('threads').from('auto_reply_logs').select('id', { count: 'exact', head: true }).eq('account_id', accData.id).eq('status', 'pending_review')
    ])

    stats.value = {
      scheduled: schedRes.count || 0,
      published: pubRes.count || 0,
      replies: repRes.count || 0,
      pendingReviews: revRes.count || 0
    }
  } catch (err) {
    console.error('Error loading dashboard stats:', err)
  }
}

onMounted(() => {
  fetchOverview()
})
</script>
