<template>
  <div>
    <div class="mb-6">
      <h1 class="text-2xl font-bold tracking-tight">{{ $t('analytics.title') }}</h1>
      <p class="text-sm theme-text-muted mt-1">{{ $t('analytics.subtitle') }}</p>
    </div>

    <div class="border-b theme-border mb-6">
      <nav class="flex gap-1 -mb-px overflow-x-auto">
        <RouterLink to="/analytics/best-time" class="px-4 py-2.5 text-sm font-medium border-b-2 transition whitespace-nowrap" :class="tabClass('/analytics/best-time')">{{ $t('analytics.tab_best') }}</RouterLink>
        <RouterLink to="/analytics/hook" class="px-4 py-2.5 text-sm font-medium border-b-2 transition whitespace-nowrap" :class="tabClass('/analytics/hook')">{{ $t('analytics.tab_hook') }}</RouterLink>
        <RouterLink to="/analytics/length" class="px-4 py-2.5 text-sm font-medium border-b-2 transition whitespace-nowrap" :class="tabClass('/analytics/length')">{{ $t('analytics.tab_length') }}</RouterLink>
        <RouterLink to="/analytics/topic" class="px-4 py-2.5 text-sm font-medium border-b-2 transition whitespace-nowrap" :class="tabClass('/analytics/topic')">{{ $t('analytics.tab_topic') }}</RouterLink>
      </nav>
    </div>

    <RouterView />
  </div>
</template>

<script setup lang="ts">
import { RouterView, RouterLink, useRoute } from 'vue-router'
const route = useRoute()
function tabClass(path: string) {
  return route.path === path ? 'border-current theme-text' : 'border-transparent theme-text-muted hover:theme-text'
}
</script>
