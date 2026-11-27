<template>
  <div class="min-h-screen w-full theme-bg theme-text">
    <RouterView />
    <SupportChatWidget />
  </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import { useTheme } from './composables/useTheme'
import SupportChatWidget from './components/SupportChatWidget.vue'

const { initTheme } = useTheme()
initTheme()
</script>
