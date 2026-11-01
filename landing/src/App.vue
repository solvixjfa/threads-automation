<template>
  <div class="min-h-screen w-full theme-bg theme-text">
    <RouterView />
  </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import { useTheme } from './composables/useTheme'
const { initTheme } = useTheme()
initTheme()
</script>
