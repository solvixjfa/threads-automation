<template>
  <div>
    <div class="w-full h-56 relative">
      <Bar :data="chartData" :options="chartOptions" />
    </div>
    <div v-if="selectedBar" class="mt-3 flex items-center justify-between p-2.5 rounded-md theme-bg-sec border theme-border text-xs">
      <div class="flex items-center gap-3">
        <span class="font-bold">{{ selectedBar.date }}</span>
        <span class="theme-text-muted">Views <strong class="theme-text">{{ selectedBar.views }}</strong></span>
        <span class="theme-text-muted">Likes <strong class="theme-text">{{ selectedBar.likes }}</strong></span>
      </div>
      <button @click="selectedBar = null" class="theme-text-muted hover:theme-text text-lg leading-none">&times;</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend
} from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

const props = defineProps<{ data: any[] }>()

const selectedBar = ref<any>(null)

const chartData = computed(() => ({
  labels: props.data.map(d => d.date ? d.date.slice(5) : ''),
  datasets: [
    {
      label: 'Views',
      backgroundColor: '#e5e5e5',
      hoverBackgroundColor: '#ffffff',
      data: props.data.map(d => d.views || 0),
      borderRadius: 2,
      barPercentage: 0.85,
      maxBarThickness: 24,
    },
    {
      label: 'Likes',
      backgroundColor: '#5c5c5c',
      hoverBackgroundColor: '#8a8a8a',
      data: props.data.map(d => d.likes || 0),
      borderRadius: 2,
      barPercentage: 0.85,
      maxBarThickness: 24,
    }
  ]
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  onClick: (event: any, elements: any[]) => {
    if (elements.length > 0) {
      const idx = elements[0].index
      selectedBar.value = props.data[idx]
    } else {
      selectedBar.value = null
    }
  },
  onHover: (event: any, elements: any[]) => {
    const canvas = event.native?.target
    if (canvas) canvas.style.cursor = elements.length > 0 ? 'pointer' : 'default'
  },
  animation: { duration: 400 },
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: '#0f0f0f',
      titleColor: '#ffffff',
      bodyColor: '#e5e5e5',
      borderColor: '#262626',
      borderWidth: 1,
      padding: 10,
      displayColors: true,
    }
  },
  scales: {
    x: {
      grid: { display: false, drawBorder: false },
      ticks: { color: '#8a8a8a', font: { size: 10 }, maxRotation: 0, autoSkipPadding: 20 }
    },
    y: {
      grid: { color: '#262626', drawBorder: false },
      ticks: { color: '#8a8a8a', font: { size: 10 } },
      beginAtZero: true
    }
  }
}
</script>
