<template>
  <div class="space-y-1 relative" ref="dropdownRef">
    <label v-if="label" class="label">{{ label }}</label>
    <button 
      type="button"
      @click="toggle"
      :disabled="disabled"
      class="input w-full flex items-center justify-between text-left transition-colors"
      :class="{ 'opacity-50 cursor-not-allowed': disabled }"
    >
      <span class="truncate" :class="!selectedLabel ? 'theme-text-muted' : 'theme-text'">
        {{ selectedLabel || placeholder || 'Select...' }}
      </span>
      <svg class="w-4 h-4 shrink-0 transition-transform theme-text-muted" :class="{ 'rotate-180': isOpen }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </button>

    <div 
      v-if="isOpen" 
      class="absolute z-50 w-full mt-1 rounded-lg border theme-border shadow-lg overflow-hidden"
      style="background: var(--bg);"
    >
      <ul class="max-h-60 overflow-y-auto py-1">
        <li 
          v-for="opt in options" 
          :key="opt.value"
          @click="select(opt.value)"
          class="px-3 py-2 text-sm cursor-pointer hover:theme-bg-sec transition-colors truncate"
          :class="modelValue === opt.value ? 'font-bold theme-text' : 'theme-text-muted'"
        >
          {{ opt.label }}
        </li>
        <li v-if="options.length === 0" class="px-3 py-2 text-sm theme-text-muted italic">
          No options available
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps<{
  modelValue: string
  options: { label: string, value: string }[]
  label?: string
  placeholder?: string
  disabled?: boolean
}>()

const emit = defineEmits(['update:modelValue'])

const isOpen = ref(false)
const dropdownRef = ref<HTMLElement | null>(null)

const selectedLabel = computed(() => {
  const opt = props.options.find(o => o.value === props.modelValue)
  return opt ? opt.label : ''
})

function toggle() {
  if (!props.disabled) isOpen.value = !isOpen.value
}

function select(val: string) {
  emit('update:modelValue', val)
  isOpen.value = false
}

function handleClickOutside(e: MouseEvent) {
  if (dropdownRef.value && !dropdownRef.value.contains(e.target as Node)) {
    isOpen.value = false
  }
}

onMounted(() => document.addEventListener('click', handleClickOutside))
onUnmounted(() => document.removeEventListener('click', handleClickOutside))
</script>
