<template>
  <span :class="['badge', 'badge-' + variant]"><slot /></span>
</template>

<script setup lang="ts">
withDefaults(defineProps<{ variant?: 'default' | 'accent' | 'success' | 'danger' }>(), { variant: 'default' })
</script>
