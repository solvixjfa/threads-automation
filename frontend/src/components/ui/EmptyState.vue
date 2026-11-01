<template>
  <div class="text-center py-12 px-6">
    <div class="w-12 h-12 mx-auto mb-4 rounded-full flex items-center justify-center theme-bg-hover">
      <svg class="w-6 h-6 theme-text-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
      </svg>
    </div>
    <h3 class="text-sm font-semibold mb-1">{{ title }}</h3>
    <p v-if="description" class="text-xs theme-text-muted mb-4 max-w-xs mx-auto">{{ description }}</p>
    <slot />
  </div>
</template>

<script setup lang="ts">
defineProps<{ title: string; description?: string }>()
</script>
