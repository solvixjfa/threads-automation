<template>
  <div class="w-full h-64 relative touch-pan-y">
    <Line :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS, CategoryScale, LinearScale, LineElement, PointElement,
  Title, Tooltip, Legend, Filler
} from 'chart.js'
import { useTheme } from '../composables/useTheme'

ChartJS.register(CategoryScale, LinearScale, LineElement, PointElement, Title, Tooltip, Legend, Filler)

const props = defineProps<{ data: any[] }>()

const { theme } = useTheme()
const themeVersion = ref(0)
watch(theme, () => { themeVersion.value++ })

function cssVar(name: string, fallback: string): string {
  if (typeof window === 'undefined') return fallback
  const val = getComputedStyle(document.documentElement).getPropertyValue(name).trim()
  return val || fallback
}

const chartData = computed(() => {
  themeVersion.value
  const isDark = theme.value === 'dark'
  const textColor = cssVar('--text', isDark ? '#e5e5e5' : '#000000')
  const baseRGB = isDark ? '229,229,229' : '0,0,0'

  return {
    labels: props.data.map(d => {
      if (!d.date) return ''
      const parts = d.date.split('-') // ['2026','11','09']
      if (parts.length < 3) return d.date
      const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
      const m = months[parseInt(parts[1]) - 1] || parts[1]
      const day = parseInt(parts[2])
      return `${m} ${day}`
    }),
    datasets: [{
      label: 'Views',
      data: props.data.map(d => d.views || 0),
      borderColor: textColor,
      backgroundColor: (ctx: any) => {
        const chart = ctx.chart
        if (!chart.chartArea) return 'transparent'
        const g = chart.ctx.createLinearGradient(0, chart.chartArea.top, 0, chart.chartArea.bottom)
        g.addColorStop(0, `rgba(${baseRGB},0.3)`)
        g.addColorStop(1, `rgba(${baseRGB},0)`)
        return g
      },
      borderWidth: 2,
      tension: 0.35,
      fill: true,
      pointRadius: 0,
      pointHoverRadius: 6,
      pointHoverBackgroundColor: textColor,
      pointHoverBorderColor: cssVar('--bg', isDark ? '#0f0f0f' : '#ffffff'),
      pointHoverBorderWidth: 2,
      pointHitRadius: 25,
    }]
  }
})

const chartOptions = computed(() => {
  themeVersion.value
  const isDark = theme.value === 'dark'
  const textMuted = cssVar('--text-muted', isDark ? '#8a8a8a' : '#666666')
  const borderColor = cssVar('--border', isDark ? '#262626' : '#e5e5e5')

  return {
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
        backgroundColor: isDark ? '#0f0f0f' : '#ffffff',
        titleColor: isDark ? '#ffffff' : '#000000',
        bodyColor: isDark ? '#e5e5e5' : '#333333',
        borderColor: borderColor,
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
        ticks: { color: textMuted, font: { size: 10 }, maxRotation: 0, autoSkipPadding: 30 }
      },
      y: {
        grid: { color: isDark ? '#1a1a1a' : '#f0f0f0', drawBorder: false },
        ticks: {
          color: textMuted,
          font: { size: 10 },
          callback: (v: any) => v >= 1000 ? (v/1000).toFixed(1) + 'K' : v,
        },
        beginAtZero: true
      }
    }
  }
})
</script>
