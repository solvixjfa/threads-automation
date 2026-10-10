<template>
  <Teleport to="body">
    <!-- Toast Notification -->
    <Transition name="fade">
      <div 
        v-if="toast.show" 
        class="fixed bottom-6 right-6 z-[999] px-5 py-3.5 rounded-xl shadow-2xl flex items-center gap-3 border text-xs font-bold transition-all"
        :class="{
          'bg-rose-900 text-rose-100 border-rose-700': toast.type === 'error',
          'bg-emerald-900 text-emerald-100 border-emerald-700': toast.type === 'success',
          'bg-slate-900 text-slate-100 border-slate-700': toast.type === 'info'
        }"
      >
        <span 
          class="w-2.5 h-2.5 rounded-full shrink-0" 
          :class="{
            'bg-rose-400 animate-pulse': toast.type === 'error',
            'bg-emerald-400': toast.type === 'success',
            'bg-indigo-400': toast.type === 'info'
          }"
        ></span>
        <span>{{ toast.message }}</span>
      </div>
    </Transition>

    <!-- Confirm Modal Overlay -->
    <Transition name="fade">
      <div v-if="confirmModal.show" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-[999] flex items-center justify-center p-4">
        <div class="bg-white border border-slate-200 rounded-2xl max-w-sm w-full p-6 space-y-4 shadow-2xl">
          <div class="space-y-1">
            <h3 class="text-sm font-bold text-slate-900 uppercase tracking-wide">{{ confirmModal.title }}</h3>
            <p class="text-xs text-slate-600 leading-relaxed">{{ confirmModal.message }}</p>
          </div>
          <div class="flex justify-end gap-3 pt-2">
            <button 
              @click="closeConfirm" 
              class="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-xl transition"
            >
              {{ confirmModal.cancelText }}
            </button>
            <button 
              @click="handleConfirm" 
              class="px-5 py-2 bg-rose-600 hover:bg-rose-700 text-white text-xs font-bold rounded-xl transition shadow-sm"
            >
              {{ confirmModal.confirmText }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { useNotify } from '../composables/useNotify'
const { toast, confirmModal, closeConfirm, handleConfirm } = useNotify()
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.25s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
