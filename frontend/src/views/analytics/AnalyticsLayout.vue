<template>
  <div>
    <div class="mb-6">
      <h1 class="text-2xl font-bold tracking-tight flex items-center gap-2">
        <BarChart3 class="w-6 h-6 theme-text-muted hidden sm:block" />
        {{ $t('analytics.title') }}
      </h1>
      <p class="text-sm theme-text-muted mt-1">{{ $t('analytics.subtitle') }}</p>
    </div>

    <div class="border-b theme-border mb-6 w-full overflow-hidden">
      <nav class="flex gap-2 -mb-px overflow-x-auto hide-scrollbar w-full pb-1">
        <RouterLink to="/analytics/best-time" class="px-4 py-2.5 text-sm font-medium border-b-2 transition whitespace-nowrap flex-shrink-0 flex items-center gap-2 hover:bg-[var(--bg-hover)] rounded-t-lg" :class="tabClass('/analytics/best-time')">
          <Clock class="w-4 h-4" /> {{ $t('analytics.tab_best') }}
        </RouterLink>
        <RouterLink to="/analytics/hook" class="px-4 py-2.5 text-sm font-medium border-b-2 transition whitespace-nowrap flex-shrink-0 flex items-center gap-2 hover:bg-[var(--bg-hover)] rounded-t-lg" :class="tabClass('/analytics/hook')">
          <Anchor class="w-4 h-4" /> {{ $t('analytics.tab_hook') }}
        </RouterLink>
        <RouterLink to="/analytics/length" class="px-4 py-2.5 text-sm font-medium border-b-2 transition whitespace-nowrap flex-shrink-0 flex items-center gap-2 hover:bg-[var(--bg-hover)] rounded-t-lg" :class="tabClass('/analytics/length')">
          <AlignLeft class="w-4 h-4" /> {{ $t('analytics.tab_length') }}
        </RouterLink>
        <RouterLink to="/analytics/topic" class="px-4 py-2.5 text-sm font-medium border-b-2 transition whitespace-nowrap flex-shrink-0 flex items-center gap-2 hover:bg-[var(--bg-hover)] rounded-t-lg" :class="tabClass('/analytics/topic')">
          <Hash class="w-4 h-4" /> {{ $t('analytics.tab_topic') }}
        </RouterLink>
      </nav>
    </div>

    <RouterView />
  </div>
</template>

<script setup lang="ts">
import { RouterView, RouterLink, useRoute } from 'vue-router'
import { BarChart3, Clock, Anchor, AlignLeft, Hash } from 'lucide-vue-next'
const route = useRoute()
function tabClass(path: string) {
  return route.path === path ? 'border-current theme-text bg-[var(--bg-sec)]' : 'border-transparent theme-text-muted hover:theme-text'
}
</script>
