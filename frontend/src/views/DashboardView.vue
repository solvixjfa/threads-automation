<template>
  <div class="space-y-6 w-full max-w-full overflow-hidden">
    <!-- HEADER -->
    <div class="flex flex-wrap justify-between items-center gap-4 w-full">
      <div class="min-w-0">
        <h1 class="text-2xl font-bold tracking-tight">{{ $t('dashboard.title') }}</h1>
        <p class="text-sm theme-text-muted mt-1 break-words">
          {{ $t('dashboard.subtitle') }}
          <span v-if="lastSyncedAt" class="text-xs theme-text-muted block mt-0.5">
            {{ $t('dashboard.last_sync') }}: {{ formatDate(lastSyncedAt) }}
          </span>
        </p>
      </div>
      <div class="flex items-center gap-3">
        <button
          @click="handleManualRefresh"
          :disabled="loading || refreshing || syncCooldown > 0"
          class="btn btn-secondary btn-sm whitespace-nowrap"
        >
          <span v-if="refreshing || loading" class="w-3 h-3 border-2 border-current border-t-transparent rounded-full animate-spin"></span>
          <RefreshCw v-else-if="syncCooldown > 0" class="w-3.5 h-3.5 opacity-50" />
          <RefreshCw v-else class="w-3.5 h-3.5" />
          <span v-if="syncCooldown > 0">Tunggu {{ syncCooldown }}s</span>
          <span v-else>{{ refreshing ? $t('common.syncing') : $t('dashboard.refresh_data') }}</span>
        </button>
      </div>
    </div>

    <!-- TOAST -->
    <div v-if="toastMessage" class="card p-3 flex justify-between items-center text-xs border-strong w-full theme-bg-sec">
      <span class="break-words font-medium">{{ toastMessage }}</span>
      <button @click="toastMessage = ''" class="font-bold theme-text-muted hover:theme-text ml-2">{{ $t('common.close') }}</button>
    </div>

    <!-- TRIAL ALERT -->
    <div v-if="trialInfo" class="card p-4 w-full border-l-4 flex flex-col md:flex-row md:items-center justify-between gap-3"
         :style="{ borderLeftColor: trialInfo.daysLeft <= 3 ? 'var(--danger)' : 'var(--warning)' }">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-lg flex items-center justify-center theme-bg-sec border theme-border shrink-0">
          <AlertCircle class="w-4 h-4" :style="{ color: trialInfo.daysLeft <= 3 ? 'var(--danger)' : 'var(--warning)' }" />
        </div>
        <div class="min-w-0">
          <p class="text-sm font-bold">
            {{ trialInfo.daysLeft === 0 ? 'Trial berakhir hari ini' : `Trial berakhir dalam ${trialInfo.daysLeft} hari` }}
          </p>
          <p class="text-[11px] theme-text-muted">{{ trialInfo.credits }} credits tersisa</p>
        </div>
      </div>
      <RouterLink to="/profile/ai" class="btn btn-secondary btn-sm whitespace-nowrap shrink-0">
        Lihat Plan →
      </RouterLink>
    </div>

    <!-- PENDING REPLIES -->
    <div v-if="pendingRepliesCount > 0" class="card p-4 w-full border-l-4 flex flex-col md:flex-row md:items-center justify-between gap-3" style="border-left-color: var(--warning);">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-lg flex items-center justify-center theme-bg-sec border theme-border shrink-0">
          <MessageCircle class="w-4 h-4 theme-text-muted" />
        </div>
        <div class="min-w-0">
          <p class="text-sm font-bold">{{ pendingRepliesCount }} komentar menunggu balasan</p>
          <p class="text-[11px] theme-text-muted">Balas sekarang biar engagement naik</p>
        </div>
      </div>
      <RouterLink to="/comment" class="btn btn-primary btn-sm whitespace-nowrap shrink-0">
        Balas →
      </RouterLink>
    </div>

    <!-- NEXT BEST TIME -->
    <div v-if="nextBestTime" class="card p-4 w-full border-l-4 flex flex-col md:flex-row md:items-center justify-between gap-3" style="border-left-color: var(--text-primary);">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-lg flex items-center justify-center theme-bg-sec border theme-border shrink-0">
          <Clock class="w-4 h-4 theme-text-muted" />
        </div>
        <div class="min-w-0">
          <p class="text-sm font-bold">Waktu terbaik hari ini: {{ nextBestTime.hour_start }}–{{ nextBestTime.hour_end }}</p>
          <p class="text-[11px] theme-text-muted">{{ nextBestTime.er_pct.toFixed(2) }}% avg ER · {{ nextBestTime.sample_size }} post</p>
        </div>
      </div>
      <RouterLink :to="`/content/create`" class="btn btn-secondary btn-sm whitespace-nowrap shrink-0">
        Buat Post →
      </RouterLink>
    </div>

    <!-- ADMIN HEALTH -->
    <div v-if="adminHealth" class="card p-4 flex flex-wrap justify-between items-center gap-3 text-xs w-full">
      <div class="flex items-center gap-3">
        <span class="w-2.5 h-2.5 rounded-full flex-shrink-0" :style="{ background: adminHealth.failed_posts > 0 || adminHealth.expiring_or_broken_tokens > 0 ? 'var(--danger)' : 'var(--success)', animation: adminHealth.failed_posts > 0 || adminHealth.expiring_or_broken_tokens > 0 ? 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite' : 'none' }"></span>
        <span class="break-words">
          {{ $t('dashboard.admin_status') }}
          <strong class="theme-text">{{ adminHealth.connected_accounts }} {{ $t('dashboard.connected_accounts') }}</strong>
          <span v-if="adminHealth.failed_posts > 0" class="theme-text-muted ml-2">({{ adminHealth.failed_posts }} {{ $t('dashboard.failed_posts_count') }})</span>
          <span v-if="adminHealth.expiring_or_broken_tokens > 0" class="theme-text-muted ml-2">({{ adminHealth.expiring_or_broken_tokens }} {{ $t('dashboard.tokens_need_reconnect') }})</span>
        </span>
      </div>
      <span class="theme-text-muted text-[10px]">{{ $t('dashboard.updated') }}: {{ formatDate(adminHealth.timestamp) }}</span>
    </div>

    <!-- LOADING SKELETON -->
    <div v-if="loading" class="animate-pulse space-y-4 w-full">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3 w-full">
        <div v-for="i in 4" :key="i" class="h-28 skeleton w-full rounded-xl"></div>
      </div>
      <div class="h-48 skeleton w-full rounded-xl"></div>
    </div>

    <!-- MAIN CONTENT -->
    <template v-else>
      <!-- TIME RANGE TOGGLE -->
      <div class="flex items-center justify-between flex-wrap gap-2 w-full">
        <h2 class="text-xs font-bold uppercase tracking-wider theme-text-muted">Ringkasan</h2>
        <div class="inline-flex rounded-lg border theme-border overflow-hidden">
          <button
            v-for="r in [7, 14, 30]"
            :key="r"
            @click="timeRange = r as 7 | 14 | 30"
            class="px-3 py-1.5 text-[11px] font-bold transition"
            :class="timeRange === r ? 'bg-[var(--text)] text-[var(--bg)]' : 'theme-text-muted hover:theme-text'"
          >
            {{ r }}D
          </button>
        </div>
      </div>

      <!-- STATS ROW 1 -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3 w-full max-w-full">
        <div class="card p-4 md:p-5 w-full min-w-0 overflow-hidden relative group transition-colors">
          <div class="absolute top-4 right-4 opacity-5 group-hover:opacity-10 transition-opacity theme-text">
            <CalendarClock class="w-12 h-12" />
          </div>
          <span class="text-[10px] font-bold uppercase tracking-wider theme-text-muted block truncate mb-1">{{ $t('dashboard.stat_scheduled') }}</span>
          <p class="text-2xl md:text-3xl font-black truncate">{{ queueMetrics.scheduled }}</p>
        </div>
        <div class="card p-4 md:p-5 w-full min-w-0 overflow-hidden relative group transition-colors">
          <div class="absolute top-4 right-4 opacity-5 group-hover:opacity-10 transition-opacity theme-text">
            <CheckCircle2 class="w-12 h-12" />
          </div>
          <span class="text-[10px] font-bold uppercase tracking-wider theme-text-muted block truncate mb-1">{{ $t('dashboard.stat_published') }}</span>
          <p class="text-2xl md:text-3xl font-black truncate">{{ queueMetrics.published }}</p>
        </div>
        <div class="card p-4 md:p-5 w-full min-w-0 overflow-hidden relative group transition-colors">
          <div class="absolute top-4 right-4 opacity-5 group-hover:opacity-10 transition-opacity theme-text">
            <AlertCircle class="w-12 h-12" />
          </div>
          <span class="text-[10px] font-bold uppercase tracking-wider theme-text-muted block truncate mb-1">{{ $t('dashboard.stat_failed') }}</span>
          <p class="text-2xl md:text-3xl font-black truncate">{{ queueMetrics.failed }}</p>
        </div>
        <div class="card p-4 md:p-5 w-full min-w-0 overflow-hidden relative group transition-colors">
          <div class="absolute top-4 right-4 opacity-5 group-hover:opacity-10 transition-opacity theme-text">
            <Activity class="w-12 h-12" />
          </div>
          <span class="text-[10px] font-bold uppercase tracking-wider theme-text-muted block truncate mb-1">{{ $t('dashboard.stat_avg_engagement') }}</span>
          <p class="text-2xl md:text-3xl font-black truncate">{{ overview.avg_engagement_rate }}%</p>
        </div>
      </div>

      <!-- STATS ROW 2 -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3 w-full max-w-full">
        <div class="card p-4 space-y-1 theme-bg-sec w-full min-w-0 overflow-hidden flex items-center justify-between gap-2">
          <div class="min-w-0">
            <span class="text-[10px] font-bold uppercase tracking-wider theme-text-muted block truncate">{{ $t('dashboard.stat_total_views') }}</span>
            <p class="text-lg md:text-xl font-bold truncate">{{ overview.total_views.toLocaleString() }}</p>
          </div>
          <Eye class="w-5 h-5 theme-text-muted shrink-0" />
        </div>
        <div class="card p-4 space-y-1 theme-bg-sec w-full min-w-0 overflow-hidden flex items-center justify-between gap-2">
          <div class="min-w-0">
            <span class="text-[10px] font-bold uppercase tracking-wider theme-text-muted block truncate">{{ $t('dashboard.stat_total_likes') }}</span>
            <p class="text-lg md:text-xl font-bold truncate">{{ overview.total_likes.toLocaleString() }}</p>
          </div>
          <Heart class="w-5 h-5 theme-text-muted shrink-0" />
        </div>
        <div class="card p-4 space-y-1 theme-bg-sec w-full min-w-0 overflow-hidden flex items-center justify-between gap-2">
          <div class="min-w-0">
            <span class="text-[10px] font-bold uppercase tracking-wider theme-text-muted block truncate">{{ $t('dashboard.stat_total_replies') }}</span>
            <p class="text-lg md:text-xl font-bold truncate">{{ overview.total_replies.toLocaleString() }}</p>
          </div>
          <MessageCircle class="w-5 h-5 theme-text-muted shrink-0" />
        </div>
        <div class="card p-4 space-y-1 theme-bg-sec w-full min-w-0 overflow-hidden flex items-center justify-between gap-2">
          <div class="min-w-0">
            <span class="text-[10px] font-bold uppercase tracking-wider theme-text-muted block truncate">{{ $t('dashboard.stat_total_reposts') }}</span>
            <p class="text-lg md:text-xl font-bold truncate">{{ overview.total_reposts.toLocaleString() }}</p>
          </div>
          <Repeat2 class="w-5 h-5 theme-text-muted shrink-0" />
        </div>
      </div>

      <!-- FOLLOWERS CARD -->
      <div class="card p-4 md:p-5 w-full flex items-center justify-between gap-3">
        <div class="min-w-0">
          <span class="text-[10px] font-bold uppercase tracking-wider theme-text-muted block">{{ $t('dashboard.followers') || 'Followers' }}</span>
          <p class="text-2xl md:text-3xl font-black truncate">{{ (followers.current || 0).toLocaleString() }}</p>
        </div>
        <div class="text-right shrink-0">
          <p class="text-xs font-bold flex items-center justify-end gap-1">
            <span>{{ (followers.delta_7d || 0) >= 0 ? '↑' : '↓' }}</span>
            <span>{{ (followers.delta_7d || 0) >= 0 ? '+' : '' }}{{ followers.delta_7d || 0 }}</span>
            <span class="text-[10px] theme-text-muted font-normal">(7d)</span>
          </p>
          <p class="text-[10px] theme-text-muted mt-0.5">
            {{ (followers.delta_30d || 0) >= 0 ? '+' : '' }}{{ followers.delta_30d || 0 }} (30d)
          </p>
        </div>
      </div>

      <!-- CHART SECTION -->
      <div class="card p-4 md:p-6 space-y-4 w-full max-w-full overflow-hidden">
        <div class="flex flex-wrap justify-between items-center pb-3 divider gap-2">
          <div>
            <h2 class="text-xs font-bold uppercase tracking-wide flex items-center gap-2">
              <BarChart3 class="w-4 h-4 theme-text-muted" />
              {{ $t('dashboard.daily_trends_title') }}
            </h2>
            <p class="text-[11px] theme-text-muted mt-0.5">{{ $t('dashboard.daily_trends_subtitle') }}</p>
          </div>
          <div class="flex items-center gap-4 text-[10px] font-bold flex-shrink-0">
            <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full" style="background: var(--accent);"></span> Views</span>
            <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full" style="background: var(--text-muted);"></span> Likes</span>
          </div>
        </div>

        <div v-if="dailyInsights.length === 0" class="text-center py-10 text-xs theme-text-muted flex flex-col items-center justify-center gap-3">
          <div class="w-12 h-12 rounded-full theme-bg-sec flex items-center justify-center">
            <LineChart class="w-6 h-6 opacity-30" />
          </div>
          {{ $t('dashboard.no_daily_data') }}
        </div>

        <div v-else class="space-y-2 pt-2 w-full max-w-full">
          <div class="w-full h-48 pt-2 pb-2 overflow-x-auto">
            <svg :viewBox="`0 0 ${dailyInsights.length * 16} 160`" class="w-full h-full" preserveAspectRatio="none" style="min-width: 300px;">
              <g v-for="(day, i) in dailyInsights" :key="day.date">
                <!-- Bar Views -->
                <rect
                  :x="i * 16 + 1"
                  :y="160 - getBarHeight(day.views, maxDailyViews) * 1.4"
                  width="7"
                  :height="getBarHeight(day.views, maxDailyViews) * 1.4"
                  fill="var(--text)"
                  rx="1"
                />
                <!-- Bar Likes -->
                <rect
                  :x="i * 16 + 9"
                  :y="160 - getBarHeight(day.likes, maxDailyViews) * 1.4"
                  width="7"
                  :height="getBarHeight(day.likes, maxDailyViews) * 1.4"
                  fill="var(--text-muted)"
                  rx="1"
                  opacity="0.6"
                />
                <!-- Label tanggal -->
                <text
                  v-if="i % Math.max(1, Math.floor(dailyInsights.length / 6)) === 0"
                  :x="i * 16 + 8"
                  y="158"
                  text-anchor="middle"
                  class="text-[6px]"
                  fill="var(--text-muted)"
                >{{ formatDayLabel(day.date) }}</text>
              </g>
            </svg>
          </div>
        </div>
      </div>

      <!-- FAILED POSTS -->
      <div v-if="failedPosts.length > 0" class="card p-4 md:p-6 space-y-4 w-full max-w-full overflow-hidden">
        <div class="flex justify-between items-center pb-3 divider">
          <h2 class="text-xs font-bold uppercase tracking-wide flex items-center gap-2">
            <span class="w-2 h-2 rounded-full animate-ping" style="background: var(--danger);"></span>
            {{ $t('dashboard.failed_posts_title') }} ({{ failedPosts.length }})
          </h2>
          <span class="text-[10px] font-bold theme-text-muted">{{ $t('dashboard.needs_attention') }}</span>
        </div>
        <div class="space-y-3">
          <div v-for="post in failedPosts" :key="post.id" class="p-4 card flex flex-col md:flex-row md:items-center justify-between gap-3 w-full">
            <div class="space-y-1 flex-1 min-w-0">
              <p class="text-xs font-medium line-clamp-2 break-words">{{ post.text }}</p>
            </div>
            <button @click="handleRetryPost(post.id)" :disabled="retryingPostId === post.id" class="btn btn-secondary btn-sm shrink-0 w-full md:w-auto">
              <span v-if="retryingPostId === post.id" class="w-3 h-3 border-2 border-current border-t-transparent rounded-full animate-spin"></span>
              <RotateCcw v-else class="w-3.5 h-3.5" />
              <span>{{ retryingPostId === post.id ? $t('common.processing') : $t('dashboard.retry_btn') }}</span>
            </button>
          </div>
        </div>
      </div>

      <!-- TOP POSTS -->
      <div class="card p-4 md:p-6 space-y-4 w-full max-w-full overflow-hidden">
        <div class="flex flex-wrap justify-between items-center pb-3 divider gap-3">
          <h2 class="text-xs font-bold uppercase tracking-wide flex items-center gap-2">
            <Trophy class="w-4 h-4 theme-text-muted" />
            {{ $t('dashboard.top_posts_title') }}
          </h2>
          <div class="flex items-center gap-1 p-1 rounded-lg theme-bg border theme-border overflow-x-auto max-w-full hide-scrollbar flex-shrink-0">
            <button @click="activeTab = 'newest'" class="px-3 py-1 text-[10px] font-bold rounded-md transition-all whitespace-nowrap flex-shrink-0" :class="activeTab === 'newest' ? 'bg-[var(--bg-primary)] text-[var(--text-primary)] shadow-sm border theme-border' : 'theme-text-muted hover:theme-text border border-transparent'">{{ $t('dashboard.tab_newest') }}</button>
            <button @click="activeTab = 'views'" class="px-3 py-1 text-[10px] font-bold rounded-md transition-all whitespace-nowrap flex-shrink-0" :class="activeTab === 'views' ? 'bg-[var(--bg-primary)] text-[var(--text-primary)] shadow-sm border theme-border' : 'theme-text-muted hover:theme-text border border-transparent'">{{ $t('dashboard.tab_views') }}</button>
            <button @click="activeTab = 'er'" class="px-3 py-1 text-[10px] font-bold rounded-md transition-all whitespace-nowrap flex-shrink-0" :class="activeTab === 'er' ? 'bg-[var(--bg-primary)] text-[var(--text-primary)] shadow-sm border theme-border' : 'theme-text-muted hover:theme-text border border-transparent'">{{ $t('dashboard.tab_engagement') }}</button>
          </div>
        </div>

        <div v-if="allPosts.length === 0" class="text-center py-8 text-xs theme-text-muted flex flex-col items-center gap-2">
          <FileText class="w-8 h-8 opacity-20" />
          {{ $t('dashboard.no_posts') }}
        </div>
        <div v-else class="space-y-3">
          <div v-for="post in filteredTopPosts" :key="post.id" class="p-4 card card-hover flex flex-col md:flex-row md:items-center justify-between gap-3 theme-bg-sec w-full max-w-full overflow-hidden group">
            <div class="space-y-1 flex-1 min-w-0">
              <p class="text-xs font-medium line-clamp-2 break-words w-full">{{ post.text }}</p>
              <div class="flex items-center gap-3 text-[11px] theme-text-muted flex-wrap mt-1">
                <span class="flex items-center gap-1"><Clock class="w-3 h-3" /> {{ formatDate(post.posted_at) }}</span>
                <a v-if="safePermalink(post.permalink)" :href="safePermalink(post.permalink)!" target="_blank" rel="noopener noreferrer" class="font-bold theme-text hover:underline flex items-center gap-1">
                  <ExternalLink class="w-3 h-3" /> Buka di Threads
                </a>
              </div>
            </div>
            <!-- Metrics box -->
            <div class="flex items-center text-xs shrink-0 p-2 rounded-lg theme-bg theme-border border w-full md:w-auto justify-between md:justify-around gap-3 max-w-full">
              <div class="text-center px-1 flex-1 min-w-0">
                <span class="block text-[9px] theme-text-muted uppercase font-bold truncate">Views</span>
                <span class="font-bold truncate">{{ post.metrics?.views ?? 0 }}</span>
              </div>
              <div class="text-center px-1 border-l theme-border flex-1 min-w-0">
                <span class="block text-[9px] theme-text-muted uppercase font-bold truncate">Likes</span>
                <span class="font-bold truncate">{{ post.metrics?.likes ?? 0 }}</span>
              </div>
              <div class="text-center px-1 border-l theme-border flex-1 min-w-0">
                <span class="block text-[9px] theme-text-muted uppercase font-bold truncate">ER</span>
                <span class="font-black truncate">{{ post.engagement_rate ?? 0 }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch} from 'vue'
import { RouterLink } from 'vue-router'
import { supabase } from '../lib/supabase'
import { useNotify } from '../composables/useNotify'
import { useI18n } from 'vue-i18n'
import { 
  CalendarClock, CheckCircle2, AlertCircle, Activity, Eye, Heart, 
  MessageCircle, Repeat2, BarChart3, LineChart, RotateCcw, 
  Trophy, FileText, Clock, ExternalLink, RefreshCw
} from 'lucide-vue-next'

const { showToast } = useNotify()
const { t } = useI18n()

const loading = ref(true)
const refreshing = ref(false)
const retryingPostId = ref<string | null>(null)
const toastMessage = ref('')
const currentAccountId = ref<string | null>(null)
const lastSyncedAt = ref<string | null>(null)
const activeTab = ref('newest')

// COOLDOWN STATE
const syncCooldown = ref(0)
let cooldownInterval: ReturnType<typeof setInterval> | null = null

const queueMetrics = ref({ scheduled: 0, published: 0, failed: 0 })
const trialInfo = ref<any>(null)
const pendingRepliesCount = ref(0)
const nextBestTime = ref<any>(null)
const followers = ref<any>({ current: 0, delta_7d: 0, delta_30d: 0 })
const overview = ref({ total_posts: 0, total_views: 0, total_likes: 0, total_replies: 0, total_reposts: 0, avg_engagement_rate: 0 })
const allPosts = ref<any[]>([])
const dailyInsights = ref<any[]>([])
const timeRange = ref<7 | 14 | 30>(30)
const failedPosts = ref<any[]>([])
const adminHealth = ref<any>(null)

function applyRangeTotals() {
  if (!dailyInsights.value.length) return
  const cutoff = new Date()
  cutoff.setDate(cutoff.getDate() - timeRange.value)
  cutoff.setHours(0, 0, 0, 0)
  const filtered = dailyInsights.value.filter((d: any) => new Date(d.date) >= cutoff)
  if (!filtered.length) return

  overview.value.total_views = filtered.reduce((s: number, d: any) => s + (d.views || 0), 0)
  overview.value.total_likes = filtered.reduce((s: number, d: any) => s + (d.likes || 0), 0)
  overview.value.total_reposts = filtered.reduce((s: number, d: any) => s + (d.reposts || 0), 0)
}

function safePermalink(url: string | null | undefined): string | null {
  if (!url) return null
  return url.replace('://www.threads.net/', '://www.threads.com/')
             .replace('://threads.net/', '://www.threads.com/')
             .replace('://threads.com/', '://www.threads.com/')
}

const filteredTopPosts = computed(() => {
  let sorted = [...allPosts.value]
  if (activeTab.value === 'newest') sorted.sort((a, b) => new Date(b.posted_at).getTime() - new Date(a.posted_at).getTime())
  else if (activeTab.value === 'views') sorted.sort((a, b) => (b.metrics?.views || 0) - (a.metrics?.views || 0))
  else if (activeTab.value === 'er') sorted.sort((a, b) => (b.engagement_rate || 0) - (a.engagement_rate || 0))
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
  return new Date(isoString).toLocaleString(undefined, { dateStyle: 'medium', timeStyle: 'short' })
}

function formatDayLabel(dateStr: string) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleDateString(undefined, { day: 'numeric', month: 'numeric' })
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
  const { data } = await supabase.schema('threads').from('account_insights_daily').select('date, views, likes, replies, reposts').eq('account_id', accountId).order('date', { ascending: false }).limit(90)
  if (data) dailyInsights.value = [...data].reverse()
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
      
      // Tembak sinkron profile & metrics secara paralel
      fetch('https://threads-automation-r9so.onrender.com/api/v1/metrics/sync-profile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ account_id: account.id })
      }).catch(err => console.log('Profile sync error:', err))

      await Promise.all([fetchQueueMetricsAndFailed(account.id), fetchDailyInsights(account.id)])

      // Trial info
      try {
        const { data: accInfo } = await supabase.schema('threads').from('threads_accounts')
          .select('plan, plan_expires_at, credit_balance')
          .eq('id', account.id).maybeSingle()
        if (accInfo && accInfo.plan === 'trial' && accInfo.plan_expires_at) {
          const daysLeft = Math.ceil((new Date(accInfo.plan_expires_at).getTime() - Date.now()) / 86400000)
          if (daysLeft >= 0 && daysLeft <= 7) {
            trialInfo.value = { daysLeft, credits: accInfo.credit_balance || 0 }
          }
        }
      } catch (e) { console.warn('[dashboard] trial info', e) }

      // Followers stats
      try {
        const fRes = await fetch(`https://threads-automation-r9so.onrender.com/api/v1/analytics/followers/${account.id}`)
        const fData = await fRes.json()
        if (fData.success) followers.value = fData
      } catch (e) { console.warn('[dashboard] followers', e) }

      // Pending replies count
      try {
        const { count } = await supabase.schema('threads').from('auto_reply_logs')
          .select('id', { count: 'exact', head: true })
          .eq('account_id', account.id)
          .eq('status', 'pending_review')
        pendingRepliesCount.value = count || 0
      } catch (e) { console.warn('[dashboard] pending count', e) }

      // Next best time today
      try {
        const btRes = await fetch(`https://threads-automation-r9so.onrender.com/api/v1/analytics/best-time/${account.id}`)
        const btData = await btRes.json()
        if (btData.success && Array.isArray(btData.best_block_per_day)) {
          const todayIdx = new Date().getDay()
          const todayBlock = btData.best_block_per_day[todayIdx]
          if (todayBlock && todayBlock.has_data && todayBlock.sample_size >= 1) {
            nextBestTime.value = todayBlock
          }
        }
      } catch (e) { console.warn('[dashboard] best time', e) }
    }
    const { data: analyticsData, error: analyticsErr } = await supabase.functions.invoke('get-analytics')
    if (!analyticsErr && analyticsData?.success) {
      if (analyticsData.overview) overview.value = analyticsData.overview
      if (analyticsData.all_posts) allPosts.value = analyticsData.all_posts
    }

    // Override total_replies: exclude own replies (edge function gak filter)
    try {
      const { count } = await supabase.schema('threads').from('replies')
        .select('id', { count: 'exact', head: true })
        .eq('account_id', account.id)
        .eq('is_own', false)
      overview.value.total_replies = count || 0
      applyRangeTotals()
    } catch (e) { console.warn('[dashboard] total replies override', e) }
    const { data: healthData, error: healthErr } = await supabase.functions.invoke('admin-health')
    if (!healthErr && healthData?.success && healthData?.health) adminHealth.value = healthData.health
    else adminHealth.value = null
  } catch (err) {
    console.error('Error loading dashboard:', err)
  } finally {
    loading.value = false
  }
}

async function handleRetryPost(postId: string) {
  retryingPostId.value = postId
  try {
    const res = await fetch('https://threads-automation-r9so.onrender.com/api/v1/queue/retry', {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ post_id: postId })
    })
    if (!res.ok) throw new Error(t('dashboard.toast_retry_failed'))
    toastMessage.value = t('dashboard.toast_retry_success')
    if (currentAccountId.value) await fetchQueueMetricsAndFailed(currentAccountId.value)
  } catch (err: any) {
    toastMessage.value = err.message
  } finally {
    retryingPostId.value = null
  }
}

async function handleManualRefresh() {
  refreshing.value = true
  toastMessage.value = 'Memuat ulang data dari database...'
  try {
    await loadAllDashboardData()
    toastMessage.value = 'Data berhasil dimuat ulang dari cache.'
    setTimeout(() => { toastMessage.value = '' }, 3000)
  } catch (err: any) {
    toastMessage.value = 'Gagal memuat data: ' + err.message
  } finally {
    refreshing.value = false
  }
}

watch(timeRange, () => applyRangeTotals())

onMounted(() => loadAllDashboardData())
onUnmounted(() => {
  if (cooldownInterval) clearInterval(cooldownInterval)
})
</script>
