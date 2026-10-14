<template>
  <div v-if="open" @click="$emit('close')" class="md:hidden fixed inset-0 z-40" style="background: rgba(0,0,0,0.5);"></div>

  <aside
    :class="open ? 'translate-x-0' : '-translate-x-full'"
    class="md:translate-x-0 fixed md:static inset-y-0 left-0 z-50 w-64 flex flex-col transition-transform duration-300 ease-in-out border-r theme-border theme-bg"
  >
    <div class="h-16 hidden md:flex items-center px-5 border-b theme-border">
      <div class="w-7 h-7 flex items-center justify-center rounded text-xs font-black theme-accent">IX</div>
      <span class="ml-3 font-bold tracking-tight">ixiera.id</span>
    </div>

    <div class="md:hidden h-16 flex items-center justify-between px-4 border-b theme-border">
      <div class="flex items-center gap-2">
        <div class="w-7 h-7 flex items-center justify-center rounded text-xs font-black theme-accent">IX</div>
        <span class="font-bold tracking-tight text-sm">ixiera.id</span>
      </div>
      <button @click="$emit('close')" class="p-2 rounded-md theme-bg-hover">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>

    <nav class="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
      <RouterLink
        v-for="item in items"
        :key="item.path"
        :to="item.path"
        @click="$emit('close')"
        class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition"
        :class="[
          isActive(item.path)
            ? 'theme-bg-hover theme-text font-semibold'
            : 'theme-text-sec hover:theme-bg-hover hover:theme-text'
        ]"
      >
        <component :is="item.icon" class="w-4 h-4 shrink-0" />
        <span>{{ item.label }}</span>
      </RouterLink>
    </nav>

    <div class="p-3 border-t theme-border space-y-1">
      <button
        @click="toggleTheme"
        class="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium theme-text-sec hover:theme-bg-hover hover:theme-text transition"
      >
        <svg v-if="theme === 'light'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
        </svg>
        <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
        </svg>
        <span>{{ theme === 'light' ? 'Dark mode' : 'Light mode' }}</span>
      </button>

      <div class="px-3 py-2 text-xs truncate theme-text-muted">{{ email }}</div>

      <button @click="$emit('logout')" class="w-full text-left px-3 py-2 rounded-lg text-sm font-semibold transition" style="color: var(--danger);">
        Sign out
      </button>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { h } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { useTheme } from '../composables/useTheme'

defineProps<{ open: boolean; email?: string }>()
defineEmits<{ (e: 'close'): void; (e: 'logout'): void }>()

const route = useRoute()
const { theme, toggle: toggleTheme } = useTheme()

function isActive(path: string) {
  if (path === '/dashboard') return route.path === '/dashboard'
  return route.path.startsWith(path)
}

const IconDashboard = () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z' })
])

const IconContent = () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z' })
])

const IconComment = () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z' })
])

const IconAnalytics = () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z' })
])

const IconSettings = () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z' }),
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M15 12a3 3 0 11-6 0 3 3 0 016 0z' })
])

const items = [
  { label: 'Dashboard', path: '/dashboard', icon: IconDashboard },
  { label: 'Content', path: '/content', icon: IconContent },
  { label: 'Comment', path: '/comment', icon: IconComment },
  { label: 'Analytics', path: '/analytics', icon: IconAnalytics },
  { label: 'Settings', path: '/settings', icon: IconSettings },
]
</script>
