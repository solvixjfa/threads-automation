<template>
  <Card>
    <template #header>
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-sm font-bold uppercase tracking-wide">Status Worker</h2>
          <p class="text-xs theme-text-muted mt-0.5">Monitoring otomatisasi background</p>
        </div>
        <div class="flex items-center gap-2">
          <span class="w-2 h-2 rounded-full" :style="{ background: overallColor }"></span>
          <span class="text-xs font-bold">{{ overallLabel }}</span>
        </div>
      </div>
    </template>

    <div v-if="loading" class="space-y-2">
      <div v-for="i in 2" :key="i" class="h-14 skeleton"></div>
    </div>

    <div v-else-if="error" class="text-center py-4">
      <p class="text-xs theme-text-muted mb-3">{{ error }}</p>
      <Button variant="secondary" size="sm" @click="loadData">Coba Lagi</Button>
    </div>

    <div v-else class="space-y-2">
      <div
        v-for="w in workers"
        :key="w.name"
        class="flex items-center justify-between p-3 rounded-lg theme-bg-sec border theme-border gap-3"
      >
        <div class="flex items-center gap-3 flex-1 min-w-0">
          <span class="w-2 h-2 rounded-full shrink-0" :style="{ background: statusColor(w.status) }"></span>
          <div class="min-w-0">
            <div class="text-xs font-bold truncate">{{ w.description }}</div>
            <div class="text-[10px] theme-text-muted">{{ formatAgo(w.last_run_ago_minutes) }}</div>
          </div>
        </div>
        <Badge :variant="badgeVariant(w.status)">{{ statusLabel(w.status) }}</Badge>
      </div>
    </div>

    <template #footer>
      <div class="flex justify-between items-center">
        <span class="text-[10px] theme-text-muted">{{ refreshedAt }}</span>
        <button @click="loadData" class="text-xs font-bold hover:underline">Refresh</button>
      </div>
    </template>
  </Card>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { supabase } from '../lib/supabase'
import { Card, Badge, Button } from './ui'

const loading = ref(true)
const error = ref('')
const workers = ref<any[]>([])
const overallStatus = ref<string>('unknown')
const refreshedAt = ref('')

async function loadData() {
  loading.value = true
  error.value = ''
  try {
    const { data, error: invokeErr } = await supabase.functions.invoke('get-worker-status')
    if (invokeErr) throw invokeErr
    if (!data?.success) throw new Error(data?.error || 'Gagal memuat status')
    workers.value = data.workers || []
    overallStatus.value = data.overall_status || 'unknown'
    refreshedAt.value = 'Refreshed: ' + new Date(data.generated_at).toLocaleTimeString('id-ID')
  } catch (err: any) {
    error.value = err.message || 'Terjadi kesalahan'
  } finally {
    loading.value = false
  }
}

function statusColor(s: string) {
  if (s === 'healthy') return 'var(--success)'
  if (s === 'warning') return '#f59e0b'
  if (s === 'error') return 'var(--danger)'
  return 'var(--text-muted)'
}

function statusLabel(s: string) {
  if (s === 'healthy') return 'Aktif'
  if (s === 'warning') return 'Terlambat'
  if (s === 'error') return 'Bermasalah'
  return 'N/A'
}

function badgeVariant(s: string) {
  if (s === 'healthy') return 'success'
  if (s === 'error') return 'danger'
  return 'default'
}

function formatAgo(min: number | null) {
  if (min === null) return 'Belum pernah berjalan'
  if (min < 1) return 'Baru saja'
  if (min < 60) return min + ' menit lalu'
  const h = Math.floor(min / 60)
  const m = min % 60
  if (h < 24) return h + ' jam ' + (m > 0 ? m + ' menit ' : '') + 'lalu'
  return Math.floor(h / 24) + ' hari lalu'
}

const overallLabel = computed(() => statusLabel(overallStatus.value))
const overallColor = computed(() => statusColor(overallStatus.value))

onMounted(loadData)
</script>
