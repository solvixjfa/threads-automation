<template>
  <div class="w-full h-64 relative">
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

const chartData = computed(() => ({
  labels: props.data.map(d => d.date ? d.date.slice(5) : ''),
  datasets: [
    {
      label: 'Views',
      backgroundColor: '#e5e5e5',
      hoverBackgroundColor: '#ffffff',
      data: props.data.map(d => d.views || 0),
      borderRadius: 2,
      barPercentage: 0.7,
    },
    {
      label: 'Likes',
      backgroundColor: '#5c5c5c',
      hoverBackgroundColor: '#8a8a8a',
      data: props.data.map(d => d.likes || 0),
      borderRadius: 2,
      barPercentage: 0.7,
    }
  ]
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
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
