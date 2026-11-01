<template>
  <button :type="type" :disabled="disabled || loading" :class="['btn', variantClass, sizeClass]">
    <Spinner v-if="loading" size="sm" />
    <slot />
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import Spinner from './Spinner.vue'
const props = withDefaults(defineProps<{
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  type?: 'button' | 'submit' | 'reset'
  disabled?: boolean
  loading?: boolean
}>(), { variant: 'primary', size: 'md', type: 'button', disabled: false, loading: false })
const variantClass = computed(() => 'btn-' + props.variant)
const sizeClass = computed(() => props.size === 'md' ? '' : 'btn-' + props.size)
</script>
