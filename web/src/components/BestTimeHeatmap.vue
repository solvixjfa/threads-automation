<template>
  <div class="space-y-3">
    <div class="flex items-center justify-between">
      <div class="text-xs theme-text-muted">Jam (24h)</div>
      <div class="flex items-center gap-2 text-[10px] theme-text-muted">
        <span>Rendah</span>
        <span class="flex gap-0.5">
          <span v-for="lvl in 5" :key="lvl" class="w-3 h-3 rounded-sm border theme-border" :style="cellStyle(lvl - 1)"></span>
        </span>
        <span>Tinggi</span>
      </div>
    </div>

    <div class="overflow-x-auto -mx-4 px-4">
      <div class="inline-block min-w-full">
        <div class="flex">
          <div class="flex flex-col gap-1 pr-2 shrink-0">
            <div class="h-6"></div>
            <div
              v-for="(wd, i) in weekdayLabels"
              :key="i"
              class="h-7 flex items-center text-[10px] font-bold theme-text-muted"
              :style="{ width: '36px' }"
            >
              {{ wd }}
            </div>
          </div>

          <div class="flex-1">
            <div class="flex gap-0.5 pb-1">
              <div
                v-for="h in 24"
                :key="h"
                class="w-7 text-center text-[9px] font-bold theme-text-muted"
              >
                {{ (h - 1).toString().padStart(2, '0') }}
              </div>
            </div>

            <div class="space-y-1">
              <div
                v-for="(wd, d) in weekdayLabels"
                :key="d"
                class="flex gap-0.5"
              >
                <div
                  v-for="h in 24"
                  :key="h"
                  class="w-7 h-7 rounded-sm border transition cursor-pointer relative group"
                  :style="cellStyle(getLevel(d, h - 1))"
                  @click="showTooltip(d, h - 1, $event)"
                >
                  <div
                    v-if="activeTooltip && activeTooltip.day === d && activeTooltip.hour === h - 1"
                    class="absolute z-30 bottom-full left-1/2 -translate-x-1/2 mb-2 px-2.5 py-1.5 rounded-md text-[10px] whitespace-nowrap pointer-events-none theme-accent shadow-lg"
                  >
                    <div class="font-bold">{{ wd }}, {{ (h - 1).toString().padStart(2, '0') }}:00</div>
                    <div v-if="matrix[d][h - 1] > 0">ER {{ matrix[d][h - 1].toFixed(2) }}%</div>
                    <div v-else class="opacity-70">Belum ada data</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps<{
  matrix: number[][]
}>()

const weekdayLabels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

const activeTooltip = ref<{ day: number; hour: number } | null>(null)

function getLevel(day: number, hour: number): number {
  if (!props.matrix || !props.matrix[day]) return 0
  const er = props.matrix[day][hour] || 0
  if (er <= 0) return 0

  const allVals: number[] = []
  props.matrix.forEach(row => row.forEach(v => { if (v > 0) allVals.push(v) }))
  if (allVals.length === 0) return 0

  allVals.sort((a, b) => a - b)
  const p20 = allVals[Math.floor(allVals.length * 0.2)] || 0
  const p40 = allVals[Math.floor(allVals.length * 0.4)] || 0
  const p60 = allVals[Math.floor(allVals.length * 0.6)] || 0
  const p80 = allVals[Math.floor(allVals.length * 0.8)] || 0

  if (er <= p20) return 1
  if (er <= p40) return 2
  if (er <= p60) return 3
  if (er <= p80) return 4
  return 5
}

function cellStyle(level: number) {
  if (level === 0) {
    return { background: 'var(--bg-hover)', borderColor: 'var(--border)' }
  }
  const opacity = [0, 0.2, 0.4, 0.6, 0.8, 1][level] || 0
  return {
    background: `color-mix(in srgb, var(--accent) ${opacity * 100}%, var(--bg-hover))`,
    borderColor: level >= 4 ? 'var(--accent)' : 'var(--border)'
  }
}

function showTooltip(day: number, hour: number, _event: MouseEvent) {
  if (activeTooltip.value && activeTooltip.value.day === day && activeTooltip.value.hour === hour) {
    activeTooltip.value = null
  } else {
    activeTooltip.value = { day, hour }
  }
}

function handleGlobalClick(e: MouseEvent) {
  const target = e.target as HTMLElement
  if (!target.closest('.w-7.h-7')) {
    activeTooltip.value = null
  }
}

onMounted(() => document.addEventListener('click', handleGlobalClick))
onUnmounted(() => document.removeEventListener('click', handleGlobalClick))
</script>
