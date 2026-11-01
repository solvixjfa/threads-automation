<template>
  <div>
    <label v-if="label" class="label">{{ label }}</label>
    <input :type="type" :value="modelValue" :placeholder="placeholder" :disabled="disabled" class="input"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)" />
    <p v-if="hint" class="text-xs mt-1.5 theme-text-muted">{{ hint }}</p>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  modelValue?: string | number
  label?: string
  type?: string
  placeholder?: string
  hint?: string
  disabled?: boolean
}>(), { type: 'text', disabled: false })
defineEmits<{ (e: 'update:modelValue', v: string): void }>()
</script>
