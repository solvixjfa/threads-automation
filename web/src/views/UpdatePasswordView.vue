<template>
  <div class="min-h-screen flex items-center justify-center p-4 theme-bg">
    <div class="w-full max-w-sm space-y-6">
      <div class="text-center space-y-2">
        <div class="w-12 h-12 mx-auto flex items-center justify-center rounded-lg text-sm font-black theme-accent">IX</div>
        <h1 class="text-2xl font-bold theme-text">Update Password</h1>
        <p class="text-xs theme-text-muted">Masukkan password baru Anda.</p>
      </div>

      <div class="card p-6 space-y-4">
        <!-- Kalau lagi loading validasi token -->
        <div v-if="checking" class="text-center py-4 text-xs theme-text-muted animate-pulse">
          Memvalidasi link...
        </div>

        <!-- Kalau link invalid/expired -->
        <div v-else-if="errorMsg" class="text-center py-4 space-y-3">
          <div class="p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-500 text-xs">
            {{ errorMsg }}
          </div>
          <RouterLink to="/login" class="btn btn-secondary w-full">Kembali ke Login</RouterLink>
        </div>

        <!-- Form Update Password -->
        <div v-else class="space-y-4">
          <div class="space-y-1">
            <label class="label">Password Baru</label>
            <input v-model="newPassword" type="password" placeholder="Minimal 6 karakter" class="input w-full" />
          </div>
          <div class="space-y-1">
            <label class="label">Konfirmasi Password</label>
            <input v-model="confirmPassword" type="password" placeholder="Ulangi password baru" class="input w-full" />
          </div>

          <button @click="handleUpdate" :disabled="loading" class="btn btn-primary w-full flex justify-center items-center h-10">
            <span v-if="loading" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></span>
            {{ loading ? 'Menyimpan...' : 'Simpan Password' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { supabase } from '../lib/supabase'
import { useNotify } from '../composables/useNotify'

const router = useRouter()
const { showToast } = useNotify()

const newPassword = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const checking = ref(true)
const errorMsg = ref('')

onMounted(async () => {
  // Supabase otomatis ngasih session "recovery" pas URL punya #access_token...
  const { data: { session }, error } = await supabase.auth.getSession()
  
  if (error || !session) {
    errorMsg.value = 'Link reset password tidak valid atau sudah kedaluwarsa. Silakan minta link baru.'
  }
  checking.value = false
})

async function handleUpdate() {
  if (!newPassword.value || !confirmPassword.value) {
    showToast('Isi semua kolom password.', 'error')
    return
  }
  if (newPassword.value.length < 6) {
    showToast('Password minimal 6 karakter.', 'error')
    return
  }
  if (newPassword.value !== confirmPassword.value) {
    showToast('Konfirmasi password tidak cocok.', 'error')
    return
  }

  loading.value = true
  try {
    const { error } = await supabase.auth.updateUser({ password: newPassword.value })
    if (error) throw error
    
    showToast('Password berhasil diubah! Silakan login ulang.', 'success')
    await supabase.auth.signOut()
    
    setTimeout(() => {
      router.push('/login')
    }, 1500)
  } catch (err: any) {
    showToast('Gagal update password: ' + err.message, 'error')
  } finally {
    loading.value = false
  }
}
</script>
