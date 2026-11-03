<template>
  <div class="relative w-full">
    <input
      :type="visible ? 'text' : 'password'"
      :value="modelValue"
      :placeholder="placeholder"
      class="input w-full pr-10"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    />
    <button
      type="button"
      @click="visible = !visible"
      class="absolute right-3 top-1/2 -translate-y-1/2 theme-text-muted opacity-60 hover:opacity-100 transition"
      tabindex="-1"
      :aria-label="visible ? 'Hide password' : 'Show password'"
    >
      <EyeOff v-if="visible" class="w-4 h-4" />
      <Eye v-else class="w-4 h-4" />
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Eye, EyeOff } from 'lucide-vue-next'

defineProps<{ modelValue: string; placeholder?: string }>()
defineEmits<{ 'update:modelValue': [value: string] }>()

const visible = ref(false)
</script>
