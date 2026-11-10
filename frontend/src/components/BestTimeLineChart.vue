<template>
  <div class="w-full h-64 relative">
    <Line :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler
} from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler)

const props = defineProps<{ matrix: number[][] }>()

// Hitung rata-rata ER per jam dari semua hari (Senin-Minggu)
const hourlyData = computed(() => {
  if (!props.matrix || props.matrix.length === 0) return Array(24).fill(0)
  const avgs = []
  for (let h = 0; h < 24; h++) {
    let sum = 0
    let count = 0
    for (let d = 0; d < 7; d++) {
      const val = props.matrix[d][h]
      if (val > 0) {
        sum += val
        count++
      }
    }
    avgs.push(count > 0 ? sum / count : 0)
  }
  return avgs
})

const chartData = computed(() => ({
  labels: Array.from({ length: 24 }, (_, i) => `${String(i).padStart(2, '0')}:00`),
  datasets: [
    {
      label: 'Avg ER (%)',
      data: hourlyData.value,
      borderColor: '#e5e5e5',
      backgroundColor: (ctx: any) => {
        const chart = ctx.chart
        if (!chart.chartArea) return 'transparent'
        const g = chart.ctx.createLinearGradient(0, chart.chartArea.top, 0, chart.chartArea.bottom)
        g.addColorStop(0, 'rgba(229,229,229,0.3)')
        g.addColorStop(1, 'rgba(229,229,229,0)')
        return g
      },
      borderWidth: 2,
      tension: 0.35,
      fill: true,
      pointRadius: 0,
      pointHoverRadius: 6,
      pointHoverBackgroundColor: '#e5e5e5',
      pointHoverBorderColor: '#0f0f0f',
      pointHoverBorderWidth: 2,
      pointHitRadius: 20,
    }
  ]
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: { mode: 'index' as const, intersect: false },
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: '#0f0f0f',
      titleColor: '#ffffff',
      bodyColor: '#e5e5e5',
      borderColor: '#262626',
      borderWidth: 1,
      padding: 10,
      displayColors: false,
      callbacks: {
        label: (ctx: any) => `${(ctx.parsed.y || 0).toFixed(2)}% ER`,
      }
    }
  },
  scales: {
    x: {
      grid: { display: false, drawBorder: false },
      ticks: { color: '#8a8a8a', font: { size: 10 }, maxRotation: 0, autoSkip: true, maxTicksLimit: 8 }
    },
    y: {
      grid: { color: '#1a1a1a', drawBorder: false },
      ticks: { color: '#8a8a8a', font: { size: 10 }, callback: (v: any) => v + '%' },
      beginAtZero: true
    }
  }
}
</script>
