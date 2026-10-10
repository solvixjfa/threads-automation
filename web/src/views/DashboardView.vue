<template>
  <div class="max-w-4xl space-y-6">
    <div>
      <h1 class="text-2xl font-bold text-zinc-900 tracking-tight">Dashboard</h1>
      <p class="text-zinc-500 text-sm mt-1">Ringkasan performa otomatisasi Threads lu.</p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="animate-pulse flex space-x-4">
      <div class="flex-1 h-24 bg-zinc-200 rounded-xl"></div>
      <div class="flex-1 h-24 bg-zinc-200 rounded-xl"></div>
    </div>

    <!-- Metric Cards Grid -->
    <div v-else class="grid grid-cols-2 md:grid-cols-4 gap-3 md:gap-4">
      <div class="p-4 bg-white border border-zinc-200 rounded-xl shadow-sm space-y-1">
        <span class="text-[10px] font-bold uppercase tracking-wider text-zinc-400">Terjadwal (Antre)</span>
        <p class="text-2xl font-black text-zinc-900">{{ metrics.scheduled }}</p>
      </div>

      <div class="p-4 bg-white border border-zinc-200 rounded-xl shadow-sm space-y-1">
        <span class="text-[10px] font-bold uppercase tracking-wider text-zinc-400">Sukses Terbit</span>
        <p class="text-2xl font-black text-emerald-600">{{ metrics.published }}</p>
      </div>

      <div class="p-4 bg-white border border-zinc-200 rounded-xl shadow-sm space-y-1">
        <span class="text-[10px] font-bold uppercase tracking-wider text-zinc-400">Gagal / Error</span>
        <p class="text-2xl font-black text-rose-600">{{ metrics.failed }}</p>
      </div>

      <div class="p-4 bg-white border border-zinc-200 rounded-xl shadow-sm space-y-1">
        <span class="text-[10px] font-bold uppercase tracking-wider text-zinc-400">Balasan Masuk</span>
        <p class="text-2xl font-black text-zinc-900">0</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { supabase } from '../lib/supabase'

const loading = ref(true)
const metrics = ref({ scheduled: 0, published: 0, failed: 0 })

onMounted(async () => {
  const { data, error } = await supabase.from('scheduled_posts').select('status')
  if (data && !error) {
    metrics.value.scheduled = data.filter(p => p.status === 'scheduled').length
    metrics.value.published = data.filter(p => p.status === 'published').length
    metrics.value.failed = data.filter(p => ['error', 'failed', 'quota_exceeded'].includes(p.status)).length
  }
  loading.value = false
})
</script>
