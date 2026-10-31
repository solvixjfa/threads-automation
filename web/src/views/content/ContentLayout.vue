<template>
  <div class="w-full">
    <div class="mb-6">
      <h1 class="text-2xl font-bold tracking-tight flex items-center gap-2">
        <PenTool class="w-6 h-6 theme-text-muted hidden sm:block" />
        Content
      </h1>
      <p class="text-sm theme-text-muted mt-1">Create, remix, and schedule your threads</p>
    </div>

    <div class="border-b theme-border mb-6 w-full overflow-hidden">
      <nav class="flex gap-2 -mb-px overflow-x-auto hide-scrollbar w-full pb-1">
        <RouterLink to="/content/create" class="px-4 py-2.5 text-sm font-medium border-b-2 transition whitespace-nowrap flex-shrink-0 flex items-center gap-2 hover:bg-[var(--bg-hover)] rounded-t-lg" :class="tabClass('/content/create')">
          <Plus class="w-4 h-4" /> Create
        </RouterLink>
        <RouterLink to="/content/variant" class="px-4 py-2.5 text-sm font-medium border-b-2 transition whitespace-nowrap flex-shrink-0 flex items-center gap-2 hover:bg-[var(--bg-hover)] rounded-t-lg" :class="tabClass('/content/variant')">
          <Layers class="w-4 h-4" /> Variant
        </RouterLink>
        <RouterLink to="/content/queue" class="px-4 py-2.5 text-sm font-medium border-b-2 transition whitespace-nowrap flex-shrink-0 flex items-center gap-2 hover:bg-[var(--bg-hover)] rounded-t-lg" :class="tabClass('/content/queue')">
          <Clock class="w-4 h-4" /> Queue
        </RouterLink>
      </nav>
    </div>

    <RouterView />
  </div>
</template>

<script setup lang="ts">
import { RouterView, RouterLink, useRoute } from 'vue-router'
import { PenTool, Plus, Layers, Clock } from 'lucide-vue-next'
const route = useRoute()
function tabClass(path: string) {
  return route.path === path
    ? 'border-current theme-text bg-[var(--bg-sec)]'
    : 'border-transparent theme-text-muted hover:theme-text'
}
</script>
