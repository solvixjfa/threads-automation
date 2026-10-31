<template>
  <div :class="['card transition-all duration-300', { 'hover:shadow-lg hover:-translate-y-0.5 border-[var(--border-strong)]': hover, 'p-5': padding }]">
    <div v-if="$slots.header" class="mb-4"><slot name="header" /></div>
    <slot />
    <div v-if="$slots.footer" class="mt-4 pt-4 divider"><slot name="footer" /></div>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{ hover?: boolean; padding?: boolean }>(), { hover: false, padding: true })
</script>
