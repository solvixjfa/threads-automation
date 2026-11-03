<template>
  <div class="w-full">
    <div v-if="isRoot">
      <div class="mb-6">
        <h1 class="text-2xl font-bold tracking-tight flex items-center gap-2">
          <PenTool class="w-6 h-6 theme-text-muted hidden sm:block" />
          {{ $t('content.title') }}
        </h1>
        <p class="text-sm theme-text-muted mt-1">{{ $t('content.subtitle') }}</p>
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
        @click="$router.push('/content')"
        type="button"
        class="mb-4 -ml-2 flex items-center gap-1 px-2 py-1.5 rounded-md hover:theme-bg-hover transition theme-text-muted hover:theme-text text-sm font-medium"
      >
        <ChevronLeft class="w-4 h-4" />
        {{ $t('content.title') }}
      </button>
      <RouterView />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, RouterView, RouterLink } from 'vue-router'
import { PenTool, Plus, Layers, Clock, ChevronRight, ChevronLeft } from 'lucide-vue-next'

const route = useRoute()
const isRoot = computed(() => route.path === '/content' || route.path === '/content/')

const menuItems = [
  { path: '/content/create', icon: Plus, labelKey: 'content.tabs.create', descKey: 'content.desc_create' },
  { path: '/content/variant', icon: Layers, labelKey: 'content.tabs.variant', descKey: 'content.desc_variant' },
  { path: '/content/queue', icon: Clock, labelKey: 'content.tabs.queue', descKey: 'content.desc_queue' },
]
</script>
