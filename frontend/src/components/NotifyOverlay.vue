<template>
  <Teleport to="body">
    <Transition name="fade">
      <div
        v-if="toast.show"
        class="fixed bottom-6 right-6 z-[999] px-5 py-3.5 rounded-xl shadow-2xl flex items-center gap-3 border text-xs font-bold transition-all"
        :style="toastStyle"
      >
        <span
          class="w-2.5 h-2.5 rounded-full shrink-0"
          :style="{ background: toastDotColor }"
          :class="{ 'animate-pulse': toast.type === 'error' }"
        ></span>
        <span>{{ toast.message }}</span>
      </div>
    </Transition>

    <Transition name="fade">
      <div v-if="confirmModal.show" class="fixed inset-0 backdrop-blur-sm z-[999] flex items-center justify-center p-4" style="background: rgba(0,0,0,0.6);">
        <div class="card max-w-sm w-full p-6 space-y-4" style="box-shadow: 0 20px 40px -12px rgba(0,0,0,0.2);">
          <div class="space-y-1">
            <h3 class="text-sm font-bold uppercase tracking-wide">{{ confirmModal.title }}</h3>
            <p class="text-xs theme-text-sec leading-relaxed">{{ confirmModal.message }}</p>
          </div>
          <div class="flex justify-end gap-3 pt-2">
            <Button variant="secondary" @click="closeConfirm">
              {{ confirmModal.cancelText }}
            </Button>
            <Button variant="danger" @click="handleConfirm">
              {{ confirmModal.confirmText }}
            </Button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useNotify } from '../composables/useNotify'
import { Button } from './ui'

const { toast, confirmModal, closeConfirm, handleConfirm } = useNotify()

const toastStyle = computed(() => {
  if (toast.value.type === 'error') {
    return {
      background: 'color-mix(in srgb, var(--danger) 15%, var(--bg-elevated))',
      borderColor: 'color-mix(in srgb, var(--danger) 40%, transparent)',
      color: 'var(--text-primary)',
    }
  }
  if (toast.value.type === 'success') {
    return {
      background: 'color-mix(in srgb, var(--success) 15%, var(--bg-elevated))',
      borderColor: 'color-mix(in srgb, var(--success) 40%, transparent)',
      color: 'var(--text-primary)',
    }
  }
  return {
    background: 'var(--bg-elevated)',
    borderColor: 'var(--border-strong)',
    color: 'var(--text-primary)',
  }
})

const toastDotColor = computed(() => {
  if (toast.value.type === 'error') return 'var(--danger)'
  if (toast.value.type === 'success') return 'var(--success)'
  return 'var(--accent)'
})
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.25s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
