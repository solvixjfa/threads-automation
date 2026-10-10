import { ref } from 'vue'

export interface ToastState {
  show: boolean
  message: string
  type: 'success' | 'error' | 'info'
}

export interface ConfirmState {
  show: boolean
  title: string
  message: string
  confirmText: string
  cancelText: string
  onConfirm: () => void | Promise<void>
}

const toast = ref<ToastState>({ show: false, message: '', type: 'info' })
const confirmModal = ref<ConfirmState>({
  show: false,
  title: '',
  message: '',
  confirmText: 'Ya, Lanjutkan',
  cancelText: 'Batal',
  onConfirm: () => {}
})

export function useNotify() {
  function showToast(message: string, type: 'success' | 'error' | 'info' = 'info') {
    toast.value = { show: true, message, type }
    setTimeout(() => { toast.value.show = false }, 3500)
  }

  function askConfirm(options: {
    title?: string
    message: string
    confirmText?: string
    cancelText?: string
    onConfirm: () => void | Promise<void>
  }) {
    confirmModal.value = {
      show: true,
      title: options.title || 'Konfirmasi Tindakan',
      message: options.message,
      confirmText: options.confirmText || 'Ya, Lanjutkan',
      cancelText: options.cancelText || 'Batal',
      onConfirm: options.onConfirm
    }
  }

  function closeConfirm() {
    confirmModal.value.show = false
  }

  async function handleConfirm() {
    const action = confirmModal.value.onConfirm
    closeConfirm()
    if (action) await action()
  }

  return {
    toast,
    confirmModal,
    showToast,
    askConfirm,
    closeConfirm,
    handleConfirm
  }
}
