<template>
  <div class="min-h-screen flex items-center justify-center p-4 theme-bg relative">
    <NotifyOverlay />

    <div class="w-full max-w-sm card p-8 space-y-6" style="box-shadow: 0 20px 40px -12px rgba(0,0,0,0.15);">
      <div class="text-center space-y-2">
        <div class="inline-flex w-10 h-10 items-center justify-center rounded-lg text-sm font-black tracking-widest theme-accent mb-2">IX</div>
        <h1 class="text-2xl font-bold tracking-tight">Halo!</h1>
        <p class="text-xs theme-text-muted">Masuk untuk ngatur otomatisasi Threads lu.</p>
      </div>

      <form @submit.prevent="handleAuth" class="space-y-4">
        <Input
          v-model="email"
          label="Email"
          type="email"
          placeholder="nama@email.com"
        />

        <Input
          v-model="password"
          label="Password"
          type="password"
          placeholder="Minimal 6 karakter"
        />

        <div v-if="errorMsg" class="p-3 rounded-lg text-xs text-center font-medium border" :style="{ background: 'rgba(220,38,38,0.08)', borderColor: 'rgba(220,38,38,0.3)', color: 'var(--danger)' }">
          {{ errorMsg }}
        </div>

        <Button
          type="submit"
          :disabled="loading"
          :loading="loading"
          class="w-full"
        >
          {{ loading ? 'Bentar...' : (isSignUp ? 'Daftar' : 'Masuk') }}
        </Button>
      </form>

      <div class="flex items-center gap-3">
        <div class="flex-1 divider"></div>
        <span class="text-[10px] font-bold uppercase tracking-wider theme-text-muted">Atau</span>
        <div class="flex-1 divider"></div>
      </div>

      <button
        type="button"
        @click="handleGoogleLogin"
        :disabled="loading || googleLoading"
        class="w-full flex items-center justify-center gap-3 py-3 px-4 rounded-lg font-bold text-sm transition theme-bg-sec border theme-border hover:theme-bg-hover disabled:opacity-50"
      >
        <span v-if="googleLoading" class="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin"></span>
        <svg v-else width="18" height="18" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
          <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
          <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
          <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
        </svg>
        <span>{{ googleLoading ? 'Menghubungkan...' : 'Lanjut dengan Google' }}</span>
      </button>

      <div class="text-center pt-2">
        <button
          type="button"
          @click="isSignUp = !isSignUp; errorMsg = ''"
          class="text-xs theme-text-muted hover:theme-text font-medium underline transition"
        >
          {{ isSignUp ? 'Udah punya akun? Masuk aja' : 'Belum punya akun? Daftar dulu' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { supabase } from '../lib/supabase'
import { useNotify } from '../composables/useNotify'
import NotifyOverlay from '../components/NotifyOverlay.vue'
import { Input, Button } from '../components/ui'

const router = useRouter()
const { showToast } = useNotify()

const email = ref('')
const password = ref('')
const isSignUp = ref(false)
const loading = ref(false)
const googleLoading = ref(false)
const errorMsg = ref('')

async function handleAuth() {
  loading.value = true
  errorMsg.value = ''

  try {
    if (isSignUp.value) {
      if (password.value.length < 6) {
        throw new Error('Password minimal 6 karakter')
      }
      const { error } = await supabase.auth.signUp({
        email: email.value,
        password: password.value
      })
      if (error) throw error
      showToast('Akun berhasil dibuat! Silakan masuk.', 'success')
      isSignUp.value = false
    } else {
      const { error } = await supabase.auth.signInWithPassword({
        email: email.value,
        password: password.value
      })
      if (error) throw error
      router.push('/dashboard')
    }
  } catch (err: any) {
    errorMsg.value = err.message || 'Gagal login, cek lagi yak.'
  } finally {
    loading.value = false
  }
}

async function handleGoogleLogin() {
  googleLoading.value = true
  errorMsg.value = ''

  try {
    const { error } = await supabase.auth.signInWithOAuth({
      provider: 'google',
      options: {
        redirectTo: window.location.origin + '/dashboard',
      },
    })
    if (error) throw error
    // Supabase akan redirect ke Google, gak perlu push router manual
  } catch (err: any) {
    errorMsg.value = err.message || 'Gagal login dengan Google.'
    googleLoading.value = false
  }
}
</script>
