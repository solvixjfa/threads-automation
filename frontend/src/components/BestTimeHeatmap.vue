<template>
  <div class="space-y-3">
    <div class="flex items-center justify-between">
      <div class="text-xs theme-text-muted">
        <span class="font-bold">{{ $t("analytics.heatmap_row") }}</span>
        <span class="ml-2">{{ $t("analytics.heatmap_time") }}</span>
      </div>
      <div class="flex items-center gap-2 text-[10px] theme-text-muted">
        <span>{{ $t("analytics.heatmap_low") }}</span>
        <span class="flex gap-0.5">
          <span v-for="lvl in 5" :key="lvl" class="w-3 h-3 rounded-sm border theme-border" :style="cellStyle(lvl - 1)"></span>
        </span>
        <span>{{ $t("analytics.heatmap_high") }}</span>
      </div>
    </div>

    <div class="overflow-x-auto -mx-4 px-4">
      <div class="inline-block min-w-full">
        <div class="flex">
          <div class="flex flex-col gap-1 pr-2 shrink-0">
            <div class="h-6 flex items-center text-[9px] font-bold theme-text-muted" style="width: 36px;">{{ $t("analytics.heatmap_day") }}</div>
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
                  class="heatmap-cell w-7 h-7 rounded-sm border transition cursor-pointer"
                  :style="cellStyle(getLevel(d, h - 1))"
                  @click="openTooltip(d, h - 1, $event)"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <Teleport to="body">
      <div
        v-if="tooltip.visible"
        class="fixed z-[999] px-2.5 py-1.5 rounded-md text-[10px] whitespace-nowrap pointer-events-none theme-accent shadow-lg"
        :style="{ top: tooltip.y + 'px', left: tooltip.x + 'px', transform: 'translate(-50%, -120%)' }"
      >
        <div class="font-bold">{{ tooltip.weekday }}, jam {{ String(tooltip.hour).padStart(2, '0') }}:00 WIB</div>
        <div v-if="tooltip.er > 0">ER {{ tooltip.er.toFixed(2) }}%</div>
        <div v-else class="opacity-70">Belum ada data</div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted, computed } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const props = defineProps<{
  matrix: number[][]
}>()

const weekdayLabels = computed(() => ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'].map(d => t('days.' + d).substring(0, 3)))

const tooltip = reactive({
  visible: false,
  x: 0,
  y: 0,
  weekday: '',
  hour: 0,
  er: 0,
})

let hideTimer: number | null = null

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
    return { background: '#0f0f0f', borderColor: '#262626' }
  }
  // Monokrom grayscale: level 1 = gelap, level 5 = terang
  const grays: Record<number, string> = {
    1: '#1f1f1f', 2: '#3a3a3a', 3: '#5c5c5c', 4: '#8a8a8a', 5: '#e5e5e5'
  }
  return {
    background: grays[level] || grays[1],
    borderColor: level >= 4 ? '#e5e5e5' : '#262626'
  }
}

function openTooltip(day: number, hour: number, event: MouseEvent) {
  const target = event.currentTarget as HTMLElement
  const rect = target.getBoundingClientRect()
  tooltip.x = rect.left + rect.width / 2
  tooltip.y = rect.top
  tooltip.weekday = weekdayLabels[day]
  tooltip.hour = hour
  tooltip.er = props.matrix[day]?.[hour] || 0
  tooltip.visible = true

  if (hideTimer) window.clearTimeout(hideTimer)
  hideTimer = window.setTimeout(() => {
    tooltip.visible = false
  }, 2500)
}

function handleGlobalClick(e: MouseEvent) {
  const target = e.target as HTMLElement
  if (!target.classList.contains('heatmap-cell')) {
    tooltip.visible = false
  }
}

onMounted(() => document.addEventListener('click', handleGlobalClick))
onUnmounted(() => {
  document.removeEventListener('click', handleGlobalClick)
  if (hideTimer) window.clearTimeout(hideTimer)
})
</script>
