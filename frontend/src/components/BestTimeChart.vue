<template>
  <div class="w-full h-80 relative">
    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend
} from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

const props = defineProps<{ data: any[] }>()
const emit = defineEmits<{ selectBlock: [block: any] }>()

const chartData = computed(() => ({
  labels: props.data.map(d => d.weekdayLabel),
  datasets: [
    {
      label: 'Avg ER (%)',
      backgroundColor: '#e5e5e5',
      hoverBackgroundColor: '#ffffff',
      data: props.data.map(d => d.er_pct || 0),
      borderRadius: 4,
      barPercentage: 0.7,
    }
  ]
}))

const chartOptions = {
  indexAxis: 'y' as const,
  responsive: true,
  onClick: (event: any, elements: any[]) => {
    if (elements.length > 0) {
      const idx = elements[0].index
      emit('selectBlock', props.data[idx])
    }
  },
  onHover: (event: any, elements: any[]) => {
    const canvas = event.native?.target
    if (canvas) canvas.style.cursor = elements.length > 0 ? 'pointer' : 'default'
  },
  maintainAspectRatio: false,
  layout: {
    padding: { right: 20 } // Biar sumbu X ada ruang
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
      callbacks: {
        label: (ctx: any) => ` ${(ctx.parsed.x || 0).toFixed(2)}% ER`,
      }
    }
  },
  scales: {
    x: {
      display: true,
      grid: { color: '#262626', drawBorder: false, drawTicks: false },
      ticks: { 
        display: true,
        color: '#8a8a8a', 
        font: { size: 10 }, 
        callback: (v: any) => v + '%' 
      },
      beginAtZero: true
    },
    y: {
      display: true,
      grid: { display: false, drawBorder: false },
      ticks: { color: '#e5e5e5', font: { size: 12, weight: 'bold' } }
    }
  }
}
</script>
