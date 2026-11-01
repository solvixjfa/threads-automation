<template>
  <div>
    <label v-if="label" class="label">{{ label }}</label>
    <textarea :value="modelValue" :placeholder="placeholder" :rows="rows" :disabled="disabled" class="textarea"
      @input="$emit('update:modelValue', ($event.target as HTMLTextAreaElement).value)"></textarea>
    <div v-if="hint || maxLength" class="flex justify-between text-xs mt-1.5 theme-text-muted">
      <span>{{ hint }}</span>
      <span v-if="maxLength">{{ (modelValue || '').length }} / {{ maxLength }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  modelValue?: string
  label?: string
  placeholder?: string
  rows?: number
  maxLength?: number
  hint?: string
  disabled?: boolean
}>(), { rows: 6, disabled: false })
defineEmits<{ (e: 'update:modelValue', v: string): void }>()
</script>
