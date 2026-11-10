<template>
  <div class="w-full h-64 relative touch-pan-y">
    <Line :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS, CategoryScale, LinearScale, LineElement, PointElement,
  Title, Tooltip, Legend, Filler
} from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, LineElement, PointElement, Title, Tooltip, Legend, Filler)

const props = defineProps<{ data: any[] }>()

const chartData = computed(() => ({
  labels: props.data.map(d => d.date ? d.date.slice(5) : ''),
  datasets: [
    {
      label: 'Views',
      data: props.data.map(d => d.views || 0),
      borderColor: '#e5e5e5',
      backgroundColor: (ctx: any) => {
        const chart = ctx.chart
        if (!chart.chartArea) return 'rgba(229,229,229,0.1)'
        const g = chart.ctx.createLinearGradient(0, chart.chartArea.top, 0, chart.chartArea.bottom)
        g.addColorStop(0, 'rgba(229,229,229,0.35)')
        g.addColorStop(1, 'rgba(229,229,229,0)')
        return g
      },
      borderWidth: 2,
      tension: 0.35,
      fill: true,
      pointRadius: 0,
      pointHoverRadius: 6,
      pointHoverBackgroundColor: '#ffffff',
      pointHoverBorderColor: '#0f0f0f',
      pointHoverBorderWidth: 2,
      pointHitRadius: 25,
    }
  ]
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: {
    mode: 'index' as const,
    intersect: false,
    axis: 'x' as const,
  },
  hover: {
    mode: 'index' as const,
    intersect: false,
  },
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
      position: 'nearest' as const,
      callbacks: {
        label: (ctx: any) => `${(ctx.parsed.y || 0).toLocaleString()} views`,
      }
    }
  },
  scales: {
    x: {
      grid: { display: false, drawBorder: false },
      ticks: { color: '#8a8a8a', font: { size: 10 }, maxRotation: 0, autoSkipPadding: 30 }
    },
    y: {
      grid: { color: '#1a1a1a', drawBorder: false },
      ticks: {
        color: '#8a8a8a',
        font: { size: 10 },
        callback: (v: any) => v >= 1000 ? (v/1000).toFixed(1) + 'K' : v,
      },
      beginAtZero: true
    }
  }
}
</script>
