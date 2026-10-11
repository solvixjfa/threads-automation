<template>
  <div class="space-y-6">
    <div class="flex flex-wrap justify-between items-center gap-4">
      <div>
        <h1 class="text-2xl font-bold text-slate-900 tracking-tight">Dashboard & Analytics</h1>
        <p class="text-slate-500 text-sm mt-1">Ringkasan performa postingan dan metrik otomatisasi Threads.</p>
      </div>
      <button 
        @click="loadAllDashboardData" 
        :disabled="loading"
        class="text-xs font-bold bg-indigo-50 text-indigo-700 px-4 py-2.5 rounded-xl hover:bg-indigo-100 transition border border-indigo-100 disabled:opacity-50 flex items-center gap-2"
      >
        <span v-if="loading" class="w-3 h-3 border-2 border-indigo-600 border-t-transparent rounded-full animate-spin"></span>
        <span>Refresh Data</span>
      </button>
    </div>

    <!-- Admin System Health Banner (Hanya muncul jika user role Admin) -->
    <div v-if="adminHealth" class="bg-slate-900 text-white p-4 rounded-2xl flex flex-wrap justify-between items-center gap-3 text-xs shadow-md">
      <div class="flex items-center gap-3">
        <span class="w-2.5 h-2.5 rounded-full" :class="adminHealth.failed_posts > 0 || adminHealth.expiring_or_broken_tokens > 0 ? 'bg-amber-400 animate-pulse' : 'bg-emerald-400'"></span>
        <span>
          Status Admin: 
          <strong class="text-slate-200">{{ adminHealth.connected_accounts }} Akun Terhubung</strong> 
          <span v-if="adminHealth.failed_posts > 0" class="text-rose-300 ml-2">({{ adminHealth.failed_posts }} post gagal)</span>
          <span v-if="adminHealth.expiring_or_broken_tokens > 0" class="text-amber-300 ml-2">({{ adminHealth.expiring_or_broken_tokens }} token butuh reconnect)</span>
        </span>
      </div>
      <span class="text-slate-400 text-[10px]">Updated: {{ formatDate(adminHealth.timestamp) }}</span>
    </div>

    <div v-if="loading" class="animate-pulse space-y-4">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div v-for="i in 4" :key="i" class="h-28 bg-slate-200 rounded-2xl"></div>
      </div>
      <div class="h-48 bg-slate-200 rounded-2xl"></div>
    </div>

    <template v-else>
      <!-- CARD METRIK 1: Queue Status (Antrean DB) -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="p-5 bg-white border border-slate-200 rounded-2xl shadow-sm space-y-1">
          <span class="text-[10px] font-bold uppercase tracking-wider text-slate-400">Terjadwal</span>
          <p class="text-3xl font-black text-slate-900">{{ queueMetrics.scheduled }}</p>
        </div>

        <div class="p-5 bg-white border border-slate-200 rounded-2xl shadow-sm space-y-1">
          <span class="text-[10px] font-bold uppercase tracking-wider text-slate-400">Terbit</span>
          <p class="text-3xl font-black text-emerald-600">{{ queueMetrics.published }}</p>
        </div>

        <div class="p-5 bg-white border border-slate-200 rounded-2xl shadow-sm space-y-1">
          <span class="text-[10px] font-bold uppercase tracking-wider text-slate-400">Gagal</span>
          <p class="text-3xl font-black text-rose-600">{{ queueMetrics.failed }}</p>
        </div>

        <div class="p-5 bg-white border border-slate-200 rounded-2xl shadow-sm space-y-1">
          <span class="text-[10px] font-bold uppercase tracking-wider text-indigo-500">Avg Engagement</span>
          <p class="text-3xl font-black text-indigo-600">{{ overview.avg_engagement_rate }}%</p>
        </div>
      </div>

      <!-- CARD METRIK 2: Overview Performa Postingan Meta -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="p-4 bg-indigo-50/50 border border-indigo-100 rounded-xl space-y-1">
          <span class="text-[10px] font-bold uppercase tracking-wider text-indigo-700">Total Views</span>
          <p class="text-xl font-bold text-slate-900">{{ overview.total_views.toLocaleString('id-ID') }}</p>
        </div>
        <div class="p-4 bg-indigo-50/50 border border-indigo-100 rounded-xl space-y-1">
          <span class="text-[10px] font-bold uppercase tracking-wider text-indigo-700">Total Likes</span>
          <p class="text-xl font-bold text-slate-900">{{ overview.total_likes.toLocaleString('id-ID') }}</p>
        </div>
        <div class="p-4 bg-indigo-50/50 border border-indigo-100 rounded-xl space-y-1">
          <span class="text-[10px] font-bold uppercase tracking-wider text-indigo-700">Total Balasan</span>
          <p class="text-xl font-bold text-slate-900">{{ overview.total_replies.toLocaleString('id-ID') }}</p>
        </div>
        <div class="p-4 bg-indigo-50/50 border border-indigo-100 rounded-xl space-y-1">
          <span class="text-[10px] font-bold uppercase tracking-wider text-indigo-700">Total Reposts</span>
          <p class="text-xl font-bold text-slate-900">{{ overview.total_reposts.toLocaleString('id-ID') }}</p>
        </div>
      </div>

      <!-- TOP POSTS SECTION (Dari get-analytics) -->
      <div class="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-4">
        <div class="flex justify-between items-center border-b border-slate-100 pb-3">
          <h2 class="text-xs font-bold text-slate-900 uppercase tracking-wide">Top 5 Postingan Performa Terbaik</h2>
          <span class="text-[10px] font-bold text-slate-400">By Engagement Rate</span>
        </div>

        <div v-if="topPosts.length === 0" class="text-center py-8 text-xs text-slate-400">
          Belum ada data postingan terbit atau analitik belum tersinkronisasi.
        </div>

        <div v-else class="space-y-3">
          <div 
            v-for="post in topPosts" 
            :key="post.id" 
            class="p-4 bg-slate-50 border border-slate-100 rounded-xl flex flex-col md:flex-row md:items-center justify-between gap-3 hover:bg-slate-100/80 transition"
          >
            <div class="space-y-1 flex-1">
              <p class="text-xs font-medium text-slate-800 line-clamp-2">"{{ post.text }}"</p>
              <div class="flex items-center gap-3 text-[11px] text-slate-400">
                <span>{{ formatDate(post.posted_at) }}</span>
                <a v-if="post.permalink" :href="post.permalink" target="_blank" class="text-indigo-600 font-bold hover:underline">
                  Buka di Threads ↗
                </a>
              </div>
            </div>

            <div class="flex items-center gap-4 text-xs shrink-0 bg-white p-2.5 rounded-lg border border-slate-200">
              <div class="text-center px-2">
                <span class="block text-[9px] text-slate-400 uppercase font-bold">Views</span>
                <span class="font-bold text-slate-800">{{ post.metrics?.views || 0 }}</span>
              </div>
              <div class="text-center px-2 border-l border-slate-100">
                <span class="block text-[9px] text-slate-400 uppercase font-bold">Likes</span>
                <span class="font-bold text-slate-800">{{ post.metrics?.likes || 0 }}</span>
              </div>
              <div class="text-center px-2 border-l border-slate-100">
                <span class="block text-[9px] font-bold text-indigo-600 uppercase">ER</span>
                <span class="font-black text-indigo-600">{{ post.engagement_rate }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { supabase } from '../lib/supabase'

const loading = ref(true)

const queueMetrics = ref({
  scheduled: 0,
  published: 0,
  failed: 0
})

const overview = ref({
  total_posts: 0,
  total_views: 0,
  total_likes: 0,
  total_replies: 0,
  total_reposts: 0,
  avg_engagement_rate: 0
})

const topPosts = ref<any[]>([])
const adminHealth = ref<any>(null)

function formatDate(isoString: string) {
  if (!isoString) return ''
  return new Date(isoString).toLocaleString('id-ID', { dateStyle: 'medium', timeStyle: 'short' })
}

async function fetchQueueMetrics(accountId: string) {
  const { data } = await supabase
    .schema('threads')
    .from('scheduled_posts')
    .select('status')
    .eq('account_id', accountId)

  if (data) {
    queueMetrics.value.scheduled = data.filter(p => p.status === 'scheduled').length
    queueMetrics.value.published = data.filter(p => p.status === 'published').length
    queueMetrics.value.failed = data.filter(p => ['error', 'failed', 'quota_exceeded'].includes(p.status)).length
  }
}

async function loadAllDashboardData() {
  loading.value = true
  try {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) return

    // 1. Ambil akun Threads
    const { data: account } = await supabase
      .schema('threads')
      .from('threads_accounts')
      .select('id')
      .eq('user_id', user.id)
      .maybeSingle()

    if (account) {
      await fetchQueueMetrics(account.id)
    }

    // 2. Panggil Edge Function get-analytics (Otomatis ngirim Auth Header)
    const { data: analyticsData, error: analyticsErr } = await supabase.functions.invoke('get-analytics')
    if (!analyticsErr && analyticsData?.success) {
      if (analyticsData.overview) overview.value = analyticsData.overview
      if (analyticsData.top_posts) topPosts.value = analyticsData.top_posts
    }

    // 3. Panggil Edge Function admin-health (Aman dari crash jika role BUKAN admin)
    const { data: healthData, error: healthErr } = await supabase.functions.invoke('admin-health')
    if (!healthErr && healthData?.success && healthData?.health) {
      adminHealth.value = healthData.health
    } else {
      adminHealth.value = null // User biasa (non-admin) tidak melihat banner
    }

  } catch (err) {
    console.error('Error loading dashboard:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadAllDashboardData()
})
</script>
