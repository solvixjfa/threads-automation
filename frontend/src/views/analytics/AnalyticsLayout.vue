<template>
  <div>
    <div v-if="isRoot">
      <div class="mb-6">
        <h1 class="text-2xl font-bold tracking-tight flex items-center gap-2">
          <BarChart3 class="w-6 h-6 theme-text-muted hidden sm:block" />
          {{ $t('analytics.title') }}
        </h1>
        <p class="text-sm theme-text-muted mt-1">{{ $t('analytics.subtitle') }}</p>
      </div>

      <div class="space-y-2">
        <RouterLink
          v-for="item in menuItems"
          :key="item.path"
          :to="item.path"
          class="card p-4 flex items-center justify-between hover:border-[var(--border-strong)] transition group"
        >
          <div class="flex items-center gap-3">
            <div class="w-9 h-9 rounded-lg flex items-center justify-center theme-bg-sec border theme-border">
              <component :is="item.icon" class="w-4 h-4 theme-text-muted" />
            </div>
            <div>
              <p class="text-sm font-bold">{{ $t(item.labelKey) }}</p>
              <p class="text-[11px] theme-text-muted">{{ $t(item.descKey) }}</p>
            </div>
          </div>
          <ChevronRight class="w-4 h-4 theme-text-muted opacity-50 group-hover:opacity-100 transition" />
        </RouterLink>
      </div>
    </div>

    <div v-else>
      <button
        @click="$router.push('/analytics')"
        type="button"
        class="mb-4 -ml-2 flex items-center gap-1 px-2 py-1.5 rounded-md hover:theme-bg-hover transition theme-text-muted hover:theme-text text-sm font-medium"
      >
        <ChevronLeft class="w-4 h-4" />
        {{ $t('analytics.title') }}
      </button>
      <RouterView />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute, RouterView, RouterLink } from 'vue-router'
import { BarChart3, Clock, Anchor, AlignLeft, Hash, ChevronRight, ChevronLeft, Smile } from 'lucide-vue-next'

const route = useRoute()




const isRoot = computed(() => route.path === '/analytics' || route.path === '/analytics/')

const menuItems = [
  { path: '/analytics/best-time', icon: Clock, labelKey: 'analytics.tab_best', descKey: 'analytics.desc_best' },
  { path: '/analytics/hook', icon: Anchor, labelKey: 'analytics.tab_hook', descKey: 'analytics.desc_hook' },
  { path: '/analytics/length', icon: AlignLeft, labelKey: 'analytics.tab_length', descKey: 'analytics.desc_length' },
  { path: '/analytics/topic', icon: Hash, labelKey: 'analytics.tab_topic', descKey: 'analytics.desc_topic' },
  { path: '/analytics/sentiment', icon: Smile, labelKey: 'analytics.tab_sentiment', descKey: 'analytics.desc_sentiment' },
]
</script>
