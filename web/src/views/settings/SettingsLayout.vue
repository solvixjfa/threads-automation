<template>
  <div>
    <div class="mb-6">
      <h1 class="text-2xl font-bold tracking-tight">{{ $t('settings.title') }}</h1>
      <p class="text-sm theme-text-muted mt-1">{{ $t('settings.subtitle') }}</p>
    </div>

    <div class="border-b theme-border mb-6">
      <nav class="flex gap-1 -mb-px overflow-x-auto">
        <RouterLink to="/settings/account" class="px-4 py-2.5 text-sm font-medium border-b-2 transition whitespace-nowrap" :class="tabClass('/settings/account')">{{ $t('settings.tabs.account') }}</RouterLink>
        <RouterLink to="/settings/auto-reply" class="px-4 py-2.5 text-sm font-medium border-b-2 transition whitespace-nowrap" :class="tabClass('/settings/auto-reply')">{{ $t('settings.tabs.auto_reply') }}</RouterLink>
        <RouterLink to="/settings/templates" class="px-4 py-2.5 text-sm font-medium border-b-2 transition whitespace-nowrap" :class="tabClass('/settings/templates')">{{ $t('settings.tabs.templates') }}</RouterLink>
        <RouterLink to="/settings/knowledge" class="px-4 py-2.5 text-sm font-medium border-b-2 transition whitespace-nowrap" :class="tabClass('/settings/knowledge')">{{ $t('settings.tabs.knowledge') }}</RouterLink>
        <RouterLink to="/settings/ai" class="px-4 py-2.5 text-sm font-medium border-b-2 transition whitespace-nowrap" :class="tabClass('/settings/ai')">{{ $t('settings.tabs.ai') }}</RouterLink>
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
