<template>
  <div class="w-full h-48 relative">
    <Doughnut :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'

ChartJS.register(ArcElement, Tooltip, Legend)

const props = defineProps<{
  labels: string[]
  values: number[]
}>()

// Monochrome palette
const COLORS = ['#ffffff', '#a3a3a3', '#525252', '#262626', '#171717']

const chartData = computed(() => ({
  labels: props.labels,
  datasets: [
    {
      data: props.values,
      backgroundColor: COLORS.slice(0, props.labels.length),
      borderColor: '#0f0f0f',
      borderWidth: 2,
      hoverOffset: 4,
    }
  ]
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  cutout: '65%',
  plugins: {
    legend: {
      position: 'bottom' as const,
      labels: {
        color: '#8a8a8a',
        font: { size: 10 },
        boxWidth: 10,
        padding: 12,
      }
    },
    tooltip: {
      backgroundColor: '#0f0f0f',
      titleColor: '#ffffff',
      bodyColor: '#e5e5e5',
      borderColor: '#262626',
      borderWidth: 1,
      padding: 8,
    }
  }
}
</script>
