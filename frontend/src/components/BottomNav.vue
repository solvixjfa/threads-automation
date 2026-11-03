<template>
  <nav
    class="md:hidden fixed bottom-0 left-0 right-0 z-40 theme-bg border-t theme-border"
    style="padding-bottom: env(safe-area-inset-bottom);"
  >
    <div class="flex items-center justify-around h-16 max-w-lg mx-auto">
      <RouterLink
        v-for="item in items"
        :key="item.path"
        :to="item.path"
        class="flex flex-col items-center justify-center gap-0.5 px-2 py-1 transition flex-1 h-full"
        :class="isActive(item.path) ? 'theme-text' : 'theme-text-muted'"
      >
        <component
          :is="item.icon"
          class="w-5 h-5"
          :class="isActive(item.path) ? 'opacity-100' : 'opacity-60'"
        />
        <span class="text-[10px] font-medium leading-tight">{{ $t(item.labelKey) }}</span>
      </RouterLink>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { RouterLink, useRoute } from 'vue-router'
import { LayoutDashboard, FileText, MessageCircle, BarChart3, Settings } from 'lucide-vue-next'

const route = useRoute()

const items = [
  { labelKey: 'menu.dashboard', path: '/dashboard', icon: LayoutDashboard },
  { labelKey: 'menu.content', path: '/content', icon: FileText },
  { labelKey: 'menu.comments', path: '/comment', icon: MessageCircle },
  { labelKey: 'menu.analytics', path: '/analytics', icon: BarChart3 },
  { labelKey: 'menu.profile', path: '/profile', icon: Settings },
]

function isActive(path: string) {
  return route.path.startsWith(path)
}
</script>
