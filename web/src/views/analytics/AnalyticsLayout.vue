<template>
  <div>
    <div class="mb-6">
      <h1 class="text-2xl font-bold tracking-tight">Analytics</h1>
      <p class="text-sm theme-text-muted mt-1">Deep dive into your Threads performance</p>
    </div>

    <div class="border-b theme-border mb-6">
      <nav class="flex gap-1 -mb-px overflow-x-auto">
        <RouterLink to="/analytics/best-time" class="px-4 py-2.5 text-sm font-medium border-b-2 transition whitespace-nowrap" :class="tabClass('/analytics/best-time')">Best Time</RouterLink>
        <RouterLink to="/analytics/hook" class="px-4 py-2.5 text-sm font-medium border-b-2 transition whitespace-nowrap" :class="tabClass('/analytics/hook')">Hook</RouterLink>
        <RouterLink to="/analytics/length" class="px-4 py-2.5 text-sm font-medium border-b-2 transition whitespace-nowrap" :class="tabClass('/analytics/length')">Length</RouterLink>
        <RouterLink to="/analytics/topic" class="px-4 py-2.5 text-sm font-medium border-b-2 transition whitespace-nowrap" :class="tabClass('/analytics/topic')">Topic</RouterLink>
      </nav>
    </div>

    <RouterView />
  </div>
</template>

<script setup lang="ts">
import { RouterView, RouterLink, useRoute } from 'vue-router'
const route = useRoute()
function tabClass(path: string) {
  return route.path === path
    ? 'border-current theme-text'
    : 'border-transparent theme-text-muted hover:theme-text'
}
</script>
