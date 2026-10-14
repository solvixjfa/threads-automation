<template>
  <div class="space-y-6">
    <Card>
      <template #header>
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-sm font-bold">Best Time to Post</h2>
            <p class="text-xs theme-text-muted mt-0.5">Heatmap engagement rate per hari dan jam</p>
          </div>
          <Badge :variant="confidenceVariant">{{ confidenceLabel }}</Badge>
        </div>
      </template>

      <div v-if="loading" class="space-y-3">
        <div class="h-6 w-48 skeleton"></div>
        <div class="h-64 skeleton"></div>
      </div>

      <div v-else-if="error" class="text-center py-8">
        <p class="text-sm theme-text-muted mb-4">{{ error }}</p>
        <Button variant="secondary" size="sm" @click="loadData">Coba Lagi</Button>
      </div>

      <div v-else-if="totalPosts === 0" class="text-center py-8">
        <EmptyState
          title="Belum cukup data"
          description="Butuh minimal beberapa post yang sudah terbit dan punya metrik untuk menghitung rekomendasi waktu terbaik."
        />
      </div>

      <div v-else class="space-y-6">
        <div class="flex flex-wrap gap-4 text-xs">
          <div>
            <span class="theme-text-muted">Total post dianalisis:</span>
            <span class="font-bold ml-1.5">{{ totalPosts }}</span>
          </div>
          <div>
            <span class="theme-text-muted">Confidence:</span>
            <span class="font-bold ml-1.5 capitalize">{{ confidence }}</span>
          </div>
        </div>

        <BestTimeHeatmap :matrix="matrix" />
      </div>
    </Card>

    <Card v-if="!loading && !error && topSlots.length > 0">
      <template #header>
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-sm font-bold">Top 5 Slot Terbaik</h2>
            <p class="text-xs theme-text-muted mt-0.5">Berdasarkan rata-rata engagement rate historis</p>
          </div>
        </div>
      </template>

      <div class="space-y-2">
        <div
          v-for="(slot, idx) in topSlots"
          :key="idx"
          class="flex items-center justify-between p-3 rounded-lg theme-bg-sec border theme-border"
        >
          <div class="flex items-center gap-3">
            <div class="w-7 h-7 rounded-full flex items-center justify-center text-xs font-black theme-accent">
              {{ idx + 1 }}
            </div>
            <div>
              <div class="text-sm font-bold">{{ slot.weekday }}, {{ String(slot.hour).padStart(2, '0') }}:00</div>
              <div class="text-[11px] theme-text-muted">
                Sample: {{ slot.sample_size }} post
              </div>
            </div>
          </div>
          <div class="text-right">
            <div class="text-lg font-black">{{ slot.avg_er.toFixed(2) }}%</div>
            <div class="text-[10px] theme-text-muted uppercase font-bold">Avg ER</div>
          </div>
        </div>
      </div>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { supabase } from '../../lib/supabase'
import { Card, Badge, Button, EmptyState } from '../../components/ui'
import BestTimeHeatmap from '../../components/BestTimeHeatmap.vue'

const loading = ref(true)
const error = ref('')
const matrix = ref<number[][]>(Array(7).fill(0).map(() => Array(24).fill(0)))
const topSlots = ref<any[]>([])
const totalPosts = ref(0)
const confidence = ref<'low' | 'medium' | 'high'>('low')

const confidenceLabel = computed(() => ({
  low: 'Data Terbatas',
  medium: 'Cukup Akurat',
  high: 'Akurat',
}[confidence.value]))

const confidenceVariant = computed(() => ({
  low: 'default',
  medium: 'default',
  high: 'accent',
}[confidence.value] as any))

async function loadData() {
  loading.value = true
  error.value = ''
  try {
    const { data, error: invokeErr } = await supabase.functions.invoke('get-best-time')
    if (invokeErr) throw invokeErr
    if (!data?.success) throw new Error(data?.error || 'Gagal memuat data')

    matrix.value = data.matrix || Array(7).fill(0).map(() => Array(24).fill(0))
    topSlots.value = data.top_slots || []
    totalPosts.value = data.total_posts || 0
    confidence.value = data.confidence || 'low'
  } catch (err: any) {
    error.value = err.message || 'Terjadi kesalahan'
  } finally {
    loading.value = false
  }
}

onMounted(loadData)
</script>
