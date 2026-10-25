<template>
  <div class="space-y-6">
    <div class="flex flex-wrap justify-between items-center gap-4">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Dashboard</h1>
        <p class="text-sm theme-text-muted mt-1">
          Ringkasan performa postingan dan metrik otomatisasi Threads.
          <span v-if="lastSyncedAt" class="text-xs theme-text-muted block mt-0.5">
            Sync terakhir: {{ formatDate(lastSyncedAt) }}
          </span>
        </p>
      </div>

      <div class="flex items-center gap-3">
        <button
          @click="handleManualRefresh"
          :disabled="loading || refreshing"
          class="btn btn-secondary btn-sm"
        >
          <span v-if="refreshing || loading" class="w-3 h-3 border-2 border-current border-t-transparent rounded-full animate-spin"></span>
          <span>{{ refreshing ? 'Sinkronisasi...' : 'Refresh Data' }}</span>
        </button>
      </div>
    </div>

    <div v-if="toastMessage" class="card p-3 flex justify-between items-center text-xs border-strong">
      <span>{{ toastMessage }}</span>
      <button @click="toastMessage = ''" class="font-bold theme-text-muted hover:theme-text ml-2">Tutup</button>
    </div>

    <div v-if="adminHealth" class="card p-4 flex flex-wrap justify-between items-center gap-3 text-xs">
      <div class="flex items-center gap-3">
        <span class="w-2.5 h-2.5 rounded-full" :class="adminHealth.failed_posts > 0 || adminHealth.expiring_or_broken_tokens > 0 ? 'bg-amber-500 animate-pulse' : 'bg-emerald-500'"></span>
        <span>
          Status Admin:
          <strong class="theme-text">{{ adminHealth.connected_accounts }} Akun Terhubung</strong>
          <span v-if="adminHealth.failed_posts > 0" class="theme-text-muted ml-2">({{ adminHealth.failed_posts }} post gagal)</span>
          <span v-if="adminHealth.expiring_or_broken_tokens > 0" class="theme-text-muted ml-2">({{ adminHealth.expiring_or_broken_tokens }} token butuh reconnect)</span>
        </span>
      </div>
      <span class="theme-text-muted text-[10px]">Updated: {{ formatDate(adminHealth.timestamp) }}</span>
    </div>

    <div v-if="loading" class="animate-pulse space-y-4">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div v-for="i in 4" :key="i" class="h-28 skeleton"></div>
      </div>
      <div class="h-48 skeleton"></div>
    </div>

    <template v-else>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="card p-5 space-y-1">
          <span class="text-[10px] font-bold uppercase tracking-wider theme-text-muted">Terjadwal</span>
          <p class="text-3xl font-black">{{ queueMetrics.scheduled }}</p>
        </div>

        <div class="card p-5 space-y-1">
          <span class="text-[10px] font-bold uppercase tracking-wider theme-text-muted">Terbit</span>
          <p class="text-3xl font-black">{{ queueMetrics.published }}</p>
        </div>

        <div class="card p-5 space-y-1">
          <span class="text-[10px] font-bold uppercase tracking-wider theme-text-muted">Gagal</span>
          <p class="text-3xl font-black">{{ queueMetrics.failed }}</p>
        </div>

        <div class="card p-5 space-y-1">
          <span class="text-[10px] font-bold uppercase tracking-wider theme-text-muted">Avg Engagement</span>
          <p class="text-3xl font-black">{{ overview.avg_engagement_rate }}%</p>
        </div>
      </div>

      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="card p-4 space-y-1 theme-bg-sec">
          <span class="text-[10px] font-bold uppercase tracking-wider theme-text-muted">Total Views</span>
          <p class="text-xl font-bold">{{ overview.total_views.toLocaleString('id-ID') }}</p>
        </div>
        <div class="card p-4 space-y-1 theme-bg-sec">
          <span class="text-[10px] font-bold uppercase tracking-wider theme-text-muted">Total Likes</span>
          <p class="text-xl font-bold">{{ overview.total_likes.toLocaleString('id-ID') }}</p>
        </div>
        <div class="card p-4 space-y-1 theme-bg-sec">
          <span class="text-[10px] font-bold uppercase tracking-wider theme-text-muted">Total Balasan</span>
          <p class="text-xl font-bold">{{ overview.total_replies.toLocaleString('id-ID') }}</p>
        </div>
        <div class="card p-4 space-y-1 theme-bg-sec">
          <span class="text-[10px] font-bold uppercase tracking-wider theme-text-muted">Total Reposts</span>
          <p class="text-xl font-bold">{{ overview.total_reposts.toLocaleString('id-ID') }}</p>
        </div>
      </div>

      <div class="card p-6 space-y-4">
        <div class="flex justify-between items-center pb-3 divider">
          <div>
            <h2 class="text-xs font-bold uppercase tracking-wide">Tren Pertumbuhan Harian</h2>
            <p class="text-[11px] theme-text-muted mt-0.5">Akumulasi Views dan Likes harian</p>
          </div>
          <div class="flex items-center gap-4 text-[10px] font-bold">
            <span class="flex items-center gap-1.5">
              <span class="w-2.5 h-2.5 rounded-full" style="background: var(--accent);"></span>
              Views
            </span>
            <span class="flex items-center gap-1.5">
              <span class="w-2.5 h-2.5 rounded-full" style="background: var(--text-muted);"></span>
              Likes
            </span>
          </div>
        </div>

        <div v-if="dailyInsights.length === 0" class="text-center py-10 text-xs theme-text-muted">
          Belum ada riwayat harian tersimpan. Data akan terakumulasi otomatis setiap hari.
        </div>

        <div v-else class="space-y-2 pt-2">
          <div class="h-48 flex items-end gap-2 sm:gap-4 pt-12 pb-2 px-2 divider overflow-x-auto">
            <div
              v-for="day in dailyInsights"
              :key="day.date"
              class="flex-1 min-w-[40px] flex flex-col items-center gap-1.5 h-full justify-end group relative"
            >
              <div class="absolute -top-9 opacity-0 group-hover:opacity-100 group-active:opacity-100 transition-opacity text-[9px] px-2 py-1 rounded-md whitespace-nowrap pointer-events-none z-20 theme-accent">
                {{ day.views }} views / {{ day.likes }} likes
              </div>

              <div class="w-full max-w-[20px] flex items-end gap-1 h-full justify-center">
                <div
                  class="w-full rounded-t transition-all"
                  :style="{ height: getBarHeight(day.views, maxDailyViews), background: 'var(--accent)' }"
                ></div>
                <div
                  class="w-full rounded-t transition-all"
                  :style="{ height: getBarHeight(day.likes, maxDailyViews), background: 'var(--text-muted)' }"
                ></div>
              </div>

              <span class="text-[9px] font-bold theme-text-muted truncate w-full text-center">
                {{ formatDayLabel(day.date) }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div v-if="failedPosts.length > 0" class="card p-6 space-y-4">
        <div class="flex justify-between items-center pb-3 divider">
          <h2 class="text-xs font-bold uppercase tracking-wide flex items-center gap-2">
            <span class="w-2 h-2 rounded-full animate-ping" style="background: var(--danger);"></span>
            Postingan Gagal Terbit ({{ failedPosts.length }})
          </h2>
          <span class="text-[10px] font-bold theme-text-muted">Butuh Perhatian</span>
        </div>

        <div class="space-y-3">
          <div
            v-for="post in failedPosts"
            :key="post.id"
            class="p-4 card flex flex-col md:flex-row md:items-center justify-between gap-3"
          >
            <div class="space-y-1 flex-1">
              <p class="text-xs font-medium line-clamp-2">{{ post.text }}</p>
            </div>

            <button
              @click="handleRetryPost(post.id)"
              :disabled="retryingPostId === post.id"
              class="btn btn-primary btn-sm shrink-0"
            >
              <span v-if="retryingPostId === post.id" class="w-3 h-3 border-2 border-current border-t-transparent rounded-full animate-spin"></span>
              <span>{{ retryingPostId === post.id ? 'Memproses...' : 'Coba Lagi' }}</span>
            </button>
          </div>
        </div>
      </div>

      <div class="card p-6 space-y-4">
        <div class="flex flex-wrap justify-between items-center pb-3 divider gap-3">
          <h2 class="text-xs font-bold uppercase tracking-wide">Top 5 Postingan</h2>
          
          <div class="flex items-center gap-1 p-1 rounded-lg theme-bg border theme-border">
            <button 
              @click="activeTab = 'newest'"
              class="px-3 py-1 text-[10px] font-bold rounded-md transition-colors"
              :class="activeTab === 'newest' ? 'bg-white text-slate-900 shadow-sm' : 'theme-text-muted hover:theme-text'"
            >Terbaru</button>
            <button 
              @click="activeTab = 'views'"
              class="px-3 py-1 text-[10px] font-bold rounded-md transition-colors"
              :class="activeTab === 'views' ? 'bg-white text-slate-900 shadow-sm' : 'theme-text-muted hover:theme-text'"
            >Views Terbanyak</button>
            <button 
              @click="activeTab = 'er'"
              class="px-3 py-1 text-[10px] font-bold rounded-md transition-colors"
              :class="activeTab === 'er' ? 'bg-white text-slate-900 shadow-sm' : 'theme-text-muted hover:theme-text'"
            >Engagement</button>
          </div>
        </div>

        <div v-if="allPosts.length === 0" class="text-center py-8 text-xs theme-text-muted">
          Belum ada data postingan terbit atau analitik belum tersinkronisasi.
        </div>

        <div v-else class="space-y-3">
          <div
            v-for="post in filteredTopPosts"
            :key="post.id"
            class="p-4 card card-hover flex flex-col md:flex-row md:items-center justify-between gap-3 theme-bg-sec"
          >
            <div class="space-y-1 flex-1">
              <p class="text-xs font-medium line-clamp-2">{{ post.text }}</p>
              <div class="flex items-center gap-3 text-[11px] theme-text-muted">
                <span>{{ formatDate(post.posted_at) }}</span>
                <a v-if="post.permalink" :href="post.permalink" target="_blank" class="font-bold theme-text hover:underline">
                  Buka di Threads
                </a>
              </div>
            </div>

            <div class="flex items-center gap-4 text-xs shrink-0 p-2.5 rounded-lg theme-bg theme-border border">
              <div class="text-center px-2">
                <span class="block text-[9px] theme-text-muted uppercase font-bold">Views</span>
                <span class="font-bold">{{ post.metrics?.views ?? 0 }}</span>
              </div>
              <div class="text-center px-2 border-l theme-border">
                <span class="block text-[9px] theme-text-muted uppercase font-bold">Likes</span>
                <span class="font-bold">{{ post.metrics?.likes ?? 0 }}</span>
              </div>
              <div class="text-center px-2 border-l theme-border">
                <span class="block text-[9px] theme-text-muted uppercase font-bold">ER</span>
                <span class="font-black">{{ post.engagement_rate ?? 0 }}%</span>
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
const activeTab = ref('newest')

const queueMetrics = ref({ scheduled: 0, published: 0, failed: 0 })
const overview = ref({ total_posts: 0, total_views: 0, total_likes: 0, total_replies: 0, total_reposts: 0, avg_engagement_rate: 0 })
const allPosts = ref<any[]>([])
const dailyInsights = ref<any[]>([])
const failedPosts = ref<any[]>([])
const adminHealth = ref<any>(null)

const filteredTopPosts = computed(() => {
  let sorted = [...allPosts.value]
  if (activeTab.value === 'newest') {
    sorted.sort((a, b) => new Date(b.posted_at).getTime() - new Date(a.posted_at).getTime())
  } else if (activeTab.value === 'views') {
    sorted.sort((a, b) => (b.metrics?.views || 0) - (a.metrics?.views || 0))
  } else if (activeTab.value === 'er') {
    sorted.sort((a, b) => (b.engagement_rate || 0) - (a.engagement_rate || 0))
  }
  return sorted.slice(0, 5)
})

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
  const { data } = await supabase.schema('threads').from('scheduled_posts').select('*').eq('account_id', accountId)
  if (data) {
    queueMetrics.value.scheduled = data.filter(p => p.status === 'scheduled').length
    queueMetrics.value.published = data.filter(p => p.status === 'published').length
    queueMetrics.value.failed = data.filter(p => ['error', 'failed', 'quota_exceeded'].includes(p.status)).length
    failedPosts.value = data.filter(p => ['error', 'failed', 'quota_exceeded'].includes(p.status))
  }
}

async function fetchDailyInsights(accountId: string) {
  const { data } = await supabase.schema('threads').from('account_insights_daily').select('date, views, likes, replies, reposts').eq('account_id', accountId).order('date', { ascending: true }).limit(14)
  if (data) dailyInsights.value = data
}

async function loadAllDashboardData() {
  loading.value = true
  toastMessage.value = ''
  try {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) return
    const { data: account } = await supabase.schema('threads').from('threads_accounts').select('id, last_synced_at').eq('user_id', user.id).maybeSingle()

    if (account) {
      currentAccountId.value = account.id
      lastSyncedAt.value = account.last_synced_at
      await Promise.all([fetchQueueMetricsAndFailed(account.id), fetchDailyInsights(account.id)])
    }

    const { data: analyticsData, error: analyticsErr } = await supabase.functions.invoke('get-analytics')
    if (!analyticsErr && analyticsData?.success) {
      if (analyticsData.overview) overview.value = analyticsData.overview
      if (analyticsData.all_posts) allPosts.value = analyticsData.all_posts 
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
    const { error } = await supabase.functions.invoke('admin-manage-queue', { body: { action: 'retry', post_id: postId } })
    if (error) {
      toastMessage.value = 'Gagal memicu retry: ' + error.message
    } else {
      toastMessage.value = 'Postingan berhasil dikirim ulang ke antrean terbit.'
      if (currentAccountId.value) await fetchQueueMetricsAndFailed(currentAccountId.value)
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
    // GANTI URL INI DENGAN URL RAILWAY LU
    const response = await fetch('https://threads-automation-production-53ad.up.railway.app//api/v1/metrics/sync', { method: 'POST' })

    if (!response.ok) throw new Error('Gagal memicu sinkronisasi backend')

    toastMessage.value = 'Sinkronisasi berjalan di latar belakang. Data akan segera diperbarui.'
    
    setTimeout(async () => {
        await loadAllDashboardData()
        refreshing.value = false
    }, 3000)

  } catch (err: any) {
    toastMessage.value = 'Terjadi kesalahan: ' + err.message
    refreshing.value = false
  }
}

onMounted(() => {
  loadAllDashboardData()
})
</script>
