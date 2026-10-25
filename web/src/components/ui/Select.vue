<template>
  <div class="space-y-1">
    <label v-if="label" class="label">{{ label }}</label>
    <select 
      :value="modelValue" 
      @change="$emit('update:modelValue', ($event.target as HTMLSelectElement).value)"
      class="input w-full"
    >
      <option disabled value="">{{ placeholder || 'Select an option' }}</option>
      <option v-for="opt in options" :key="opt.value" :value="opt.value">
        {{ opt.label }}
      </option>
    </select>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  modelValue: string
  options: { label: string, value: string }[]
  label?: string
  placeholder?: string
}>()

defineEmits(['update:modelValue'])
</script>
