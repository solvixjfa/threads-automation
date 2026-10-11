<template>
  <div class="space-y-6">
    <div class="flex flex-wrap justify-between items-center gap-4">
      <div>
        <h1 class="text-2xl font-bold text-slate-900 tracking-tight">Dashboard & Analytics</h1>
        <p class="text-slate-500 text-sm mt-1">
          Ringkasan performa postingan dan metrik otomatisasi Threads.
          <span v-if="lastSyncedAt" class="text-xs text-indigo-600 block mt-0.5">
            Sync terakhir: {{ formatDate(lastSyncedAt) }}
          </span>
        </p>
      </div>

      <div class="flex items-center gap-3">
        <button 
          @click="handleManualRefresh" 
          :disabled="loading || refreshing"
          class="text-xs font-bold bg-indigo-50 text-indigo-700 px-4 py-2.5 rounded-xl hover:bg-indigo-100 transition border border-indigo-100 disabled:opacity-50 flex items-center gap-2 shadow-sm"
        >
          <span v-if="refreshing || loading" class="w-3 h-3 border-2 border-indigo-600 border-t-transparent rounded-full animate-spin"></span>
          <span>{{ refreshing ? 'Sinkronisasi Meta...' : 'Refresh Data' }}</span>
        </button>
      </div>
    </div>

    <!-- Toast Notification -->
    <div v-if="toastMessage" class="p-3 bg-amber-50 border border-amber-200 text-amber-800 rounded-xl text-xs flex justify-between items-center">
      <span>{{ toastMessage }}</span>
      <button @click="toastMessage = ''" class="font-bold text-amber-900 hover:underline text-sm ml-2">✕</button>
    </div>

    <!-- Admin System Health Banner -->
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
      <!-- CARD METRIK 1: Queue Status -->
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

      <!-- CARD METRIK 2: Overview Performa Meta -->
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

      <!-- GRAFIK TREN HARIAN -->
      <div class="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-4">
        <div class="flex justify-between items-center border-b border-slate-100 pb-3">
          <div>
            <h2 class="text-xs font-bold text-slate-900 uppercase tracking-wide">Tren Pertumbuhan Harian</h2>
            <p class="text-[11px] text-slate-400 mt-0.5">Akumulasi Views & Likes harian</p>
          </div>
          <div class="flex items-center gap-4 text-[10px] font-bold">
            <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-indigo-600"></span> Views</span>
            <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span> Likes</span>
          </div>
        </div>

        <div v-if="dailyInsights.length === 0" class="text-center py-10 text-xs text-slate-400">
          Belum ada riwayat harian tersimpan. Data akan terakumulasi otomatis setiap hari.
        </div>

        <div v-else class="space-y-2 pt-2">
          <div class="h-48 flex items-end gap-2 sm:gap-4 pt-12 pb-2 px-2 border-b border-slate-100 overflow-x-auto">
            <div 
              v-for="day in dailyInsights" 
              :key="day.date" 
              class="flex-1 min-w-[40px] flex flex-col items-center gap-1.5 h-full justify-end group relative"
            >
              <div class="absolute -top-9 opacity-0 group-hover:opacity-100 group-active:opacity-100 transition-opacity bg-slate-800 text-white text-[9px] px-2 py-1 rounded-md shadow-md whitespace-nowrap pointer-events-none z-20">
                {{ day.views }} views • {{ day.likes }} likes
              </div>

              <div class="w-full max-w-[20px] flex items-end gap-1 h-full justify-center">
                <div 
                  class="w-full bg-indigo-600 rounded-t transition-all group-hover:bg-indigo-700"
                  :style="{ height: getBarHeight(day.views, maxDailyViews) }"
                ></div>
                <div 
                  class="w-full bg-emerald-500 rounded-t transition-all group-hover:bg-emerald-600"
                  :style="{ height: getBarHeight(day.likes, maxDailyViews) }"
                ></div>
              </div>

              <span class="text-[9px] font-bold text-slate-400 truncate w-full text-center">
                {{ formatDayLabel(day.date) }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- QUEUE CONTROL: DAFTAR POSTINGAN GAGAL -->
      <div v-if="failedPosts.length > 0" class="bg-rose-50/60 border border-rose-200 rounded-2xl p-6 shadow-sm space-y-4">
        <div class="flex justify-between items-center border-b border-rose-100 pb-3">
          <h2 class="text-xs font-bold text-rose-900 uppercase tracking-wide flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-rose-600 animate-ping"></span>
            Postingan Gagal Terbit ({{ failedPosts.length }})
          </h2>
          <span class="text-[10px] font-bold text-rose-500">Butuh Perhatian</span>
        </div>

        <div class="space-y-3">
          <div 
            v-for="post in failedPosts" 
            :key="post.id"
            class="p-4 bg-white border border-rose-200 rounded-xl flex flex-col md:flex-row md:items-center justify-between gap-3 shadow-xs"
          >
            <div class="space-y-1 flex-1">
              <p class="text-xs font-medium text-slate-800 line-clamp-2">"{{ post.text }}"</p>
            </div>

            <button 
              @click="handleRetryPost(post.id)"
              :disabled="retryingPostId === post.id"
              class="shrink-0 text-xs font-bold bg-rose-600 text-white px-3.5 py-2 rounded-lg hover:bg-rose-700 transition disabled:opacity-50 flex items-center gap-1.5 shadow-sm"
            >
              <span v-if="retryingPostId === post.id" class="w-3 h-3 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
              <span>{{ retryingPostId === post.id ? 'Memproses...' : 'Coba Lagi' }}</span>
            </button>
          </div>
        </div>
      </div>

      <!-- TOP POSTS SECTION -->
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
                <span>{{ formatDate(post.posted_at || post.created_at) }}</span>
                <a v-if="post.permalink" :href="post.permalink" target="_blank" class="text-indigo-600 font-bold hover:underline">
                  Buka di Threads ↗
                </a>
              </div>
            </div>

            <div class="flex items-center gap-4 text-xs shrink-0 bg-white p-2.5 rounded-lg border border-slate-200">
              <div class="text-center px-2">
                <span class="block text-[9px] text-slate-400 uppercase font-bold">Views</span>
                <span class="font-bold text-slate-800">{{ post.metrics?.views ?? post.views ?? 0 }}</span>
              </div>
              <div class="text-center px-2 border-l border-slate-100">
                <span class="block text-[9px] text-slate-400 uppercase font-bold">Likes</span>
                <span class="font-bold text-slate-800">{{ post.metrics?.likes ?? post.likes ?? 0 }}</span>
              </div>
              <div class="text-center px-2 border-l border-slate-100">
                <span class="block text-[9px] font-bold text-indigo-600 uppercase">ER</span>
                <span class="font-black text-indigo-600">{{ post.engagement_rate ?? 0 }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { supabase } from '../lib/supabase'

const loading = ref(true)
const refreshing = ref(false)
const retryingPostId = ref<string | null>(null)
const toastMessage = ref('')
const currentAccountId = ref<string | null>(null)
const lastSyncedAt = ref<string | null>(null)

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
const dailyInsights = ref<any[]>([])
const failedPosts = ref<any[]>([])
const adminHealth = ref<any>(null)

const maxDailyViews = computed(() => {
  if (dailyInsights.value.length === 0) return 100
  const max = Math.max(...dailyInsights.value.map(d => d.views || 0))
  return max > 0 ? max : 100
})

function getBarHeight(val: number, max: number) {
  if (!val || !max) return '4px'
  const pct = Math.round((val / max) * 78)
  return `${Math.max(pct, 6)}%`
}

function formatDate(isoString: string) {
  if (!isoString) return ''
  return new Date(isoString).toLocaleString('id-ID', { dateStyle: 'medium', timeStyle: 'short' })
}

function formatDayLabel(dateStr: string) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleDateString('id-ID', { day: 'numeric', month: 'numeric' })
}

async function fetchQueueMetricsAndFailed(accountId: string) {
  const { data } = await supabase
    .schema('threads')
    .from('scheduled_posts')
    .select('*')
    .eq('account_id', accountId)

  if (data) {
    queueMetrics.value.scheduled = data.filter(p => p.status === 'scheduled').length
    queueMetrics.value.published = data.filter(p => p.status === 'published').length
    queueMetrics.value.failed = data.filter(p => ['error', 'failed', 'quota_exceeded'].includes(p.status)).length

    failedPosts.value = data.filter(p => ['error', 'failed', 'quota_exceeded'].includes(p.status))
  }
}

async function fetchDailyInsights(accountId: string) {
  const { data } = await supabase
    .schema('threads')
    .from('account_insights_daily')
    .select('date, views, likes, replies, reposts')
    .eq('account_id', accountId)
    .order('date', { ascending: true })
    .limit(14)

  if (data) {
    dailyInsights.value = data
  }
}

async function loadAllDashboardData() {
  loading.value = true
  toastMessage.value = ''
  try {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) return

    const { data: account } = await supabase
      .schema('threads')
      .from('threads_accounts')
      .select('id, last_synced_at')
      .eq('user_id', user.id)
      .maybeSingle()

    if (account) {
      currentAccountId.value = account.id
      lastSyncedAt.value = account.last_synced_at
      await Promise.all([
        fetchQueueMetricsAndFailed(account.id),
        fetchDailyInsights(account.id)
      ])
    }

    const { data: analyticsData, error: analyticsErr } = await supabase.functions.invoke('get-analytics')
    if (!analyticsErr && analyticsData?.success) {
      if (analyticsData.overview) overview.value = analyticsData.overview
      if (analyticsData.top_posts) topPosts.value = analyticsData.top_posts
    }

    const { data: healthData, error: healthErr } = await supabase.functions.invoke('admin-health')
    if (!healthErr && healthData?.success && healthData?.health) {
      adminHealth.value = healthData.health
    } else {
      adminHealth.value = null
    }

  } catch (err) {
    console.error('Error loading dashboard:', err)
  } finally {
    loading.value = false
  }
}

async function handleRetryPost(postId: string) {
  retryingPostId.value = postId
  try {
    const { error } = await supabase.functions.invoke('admin-manage-queue', {
      body: { action: 'retry', post_id: postId }
    })

    if (error) {
      toastMessage.value = 'Gagal memicu retry: ' + error.message
    } else {
      toastMessage.value = 'Postingan berhasil dikirim ulang ke antrean terbit.'
      if (currentAccountId.value) {
        await fetchQueueMetricsAndFailed(currentAccountId.value)
      }
    }
  } catch (err: any) {
    toastMessage.value = 'Terjadi kesalahan: ' + err.message
  } finally {
    retryingPostId.value = null
  }
}

async function handleManualRefresh() {
  if (!currentAccountId.value) {
    await loadAllDashboardData()
    return
  }

  refreshing.value = true
  toastMessage.value = ''

  try {
    const { error: syncErr } = await supabase.functions.invoke('worker-metrics', {
      body: { account_id: currentAccountId.value }
    })

    if (syncErr) {
      toastMessage.value = 'Gagal memicu sinkronisasi: ' + syncErr.message
    } else {
      toastMessage.value = 'Sinkronisasi metrik berhasil diperbarui dari Meta!'
      await loadAllDashboardData()
    }
  } catch (err: any) {
    toastMessage.value = 'Terjadi kesalahan saat refresh: ' + err.message
  } finally {
    refreshing.value = false
  }
}

onMounted(() => {
  loadAllDashboardData()
})
</script>
