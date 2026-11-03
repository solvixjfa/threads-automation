<template>
  <div class="relative w-full">
    <input
      :type="visible ? 'text' : 'password'"
      :value="modelValue"
      :placeholder="placeholder"
      class="input w-full pr-12 py-3 text-base"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    />
    <button
      type="button"
      @click.stop="toggle"
      class="absolute right-2 top-1/2 -translate-y-1/2 p-2 theme-text-muted opacity-60 hover:opacity-100 transition"
      tabindex="-1"
      :aria-label="visible ? 'Hide password' : 'Show password'"
    >
      <EyeOff v-if="visible" class="w-5 h-5" />
      <Eye v-else class="w-5 h-5" />
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Eye, EyeOff } from 'lucide-vue-next'

defineProps<{ modelValue: string; placeholder?: string }>()
defineEmits<{ 'update:modelValue': [value: string] }>()

const visible = ref(false)
function toggle() {
  visible.value = !visible.value
}
</script>
