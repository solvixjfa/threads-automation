<template>
  <div>
    <div class="mb-6">
      <h1 class="text-2xl font-bold tracking-tight">Content</h1>
      <p class="text-sm theme-text-muted mt-1">Create, remix, and schedule your threads</p>
    </div>

    <div class="border-b theme-border mb-6">
      <nav class="flex gap-1 -mb-px overflow-x-auto">
        <RouterLink to="/content/create" class="px-4 py-2.5 text-sm font-medium border-b-2 transition whitespace-nowrap" :class="tabClass('/content/create')">Create</RouterLink>
        <RouterLink to="/content/variant" class="px-4 py-2.5 text-sm font-medium border-b-2 transition whitespace-nowrap" :class="tabClass('/content/variant')">Variant</RouterLink>
        <RouterLink to="/content/queue" class="px-4 py-2.5 text-sm font-medium border-b-2 transition whitespace-nowrap" :class="tabClass('/content/queue')">Queue</RouterLink>
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
