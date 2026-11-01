<template>
  <div class="min-h-screen flex items-center justify-center p-4 theme-bg">
    <div class="w-full max-w-sm space-y-6">
      
      <!-- HEADER -->
      <div class="text-center space-y-2">
        <div class="w-12 h-12 mx-auto flex items-center justify-center rounded-lg text-sm font-black bg-black text-white dark:bg-white dark:text-black">IX</div>
        <h1 class="text-2xl font-bold theme-text">
          {{ mode === 'login' ? $t('login.welcome') : (mode === 'signup' ? $t('login.sign_up_title') : $t('login.reset_password_title')) }}
        </h1>
        <p class="text-xs theme-text-muted">
          {{ mode === 'login' ? $t('login.subtitle') : (mode === 'signup' ? $t('login.sign_up_subtitle') : $t('login.reset_password_subtitle')) }}
        </p>
      </div>

      <!-- FORM CARD -->
      <div class="card p-6 space-y-4">
        
        <!-- GOOGLE LOGIN -->
        <div v-if="mode !== 'forgot'">
          <button @click="loginWithGoogle" :disabled="isGoogleLoading" class="w-full flex items-center justify-center gap-2 py-2.5 rounded-lg border theme-border hover:bg-[var(--bg-sec)] transition font-medium text-sm theme-text">
            <span v-if="isGoogleLoading" class="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin"></span>
            <svg v-else class="w-5 h-5" viewBox="0 0 24 24">
              <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
              <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
              <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" />
              <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" />
            </svg>
            Continue with Google
          </button>
          
          <div class="relative py-4">
            <div class="absolute inset-0 flex items-center"><div class="w-full border-t theme-border"></div></div>
            <div class="relative flex justify-center text-[10px] uppercase font-bold theme-text-muted">
              <span class="bg-[var(--bg)] px-2">Or continue with email</span>
            </div>
          </div>
        </div>

        <!-- EMAIL INPUT -->
        <div class="space-y-1">
          <label class="label">{{ $t('login.email') }}</label>
          <input v-model="email" type="email" :placeholder="$t('login.email_placeholder')" class="input w-full" />
        </div>

        <!-- PASSWORD INPUT -->
        <div v-if="mode !== 'forgot'" class="space-y-1">
          <div class="flex justify-between items-center">
            <label class="label">{{ $t('login.password') }}</label>
            <button v-if="mode === 'login'" @click="mode = 'forgot'" class="text-[11px] font-bold theme-text-muted hover:theme-text transition">
              {{ $t('login.forgot_password') }}
            </button>
          </div>
          <input v-model="password" type="password" :placeholder="$t('login.password_placeholder')" class="input w-full" @keydown.enter="handleSubmit" />
        </div>

        <!-- SUBMIT BUTTON -->
        <button @click="handleSubmit" :disabled="loading" class="w-full flex justify-center items-center h-10 rounded-lg font-bold bg-black text-white hover:bg-gray-800 dark:bg-white dark:text-black dark:hover:bg-gray-200 transition mt-2">
          <span v-if="loading" class="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin mr-2"></span>
          {{ loading ? $t('common.processing') : (mode === 'login' ? $t('login.sign_in') : (mode === 'signup' ? $t('login.sign_up') : $t('login.send_reset_link'))) }}
        </button>

        <!-- FOOTER TOGGLE -->
        <div class="text-center pt-2">
          <button v-if="mode === 'forgot'" @click="mode = 'login'" class="text-xs font-bold theme-text-muted hover:theme-text transition">
            {{ $t('login.back_to_login') }}
          </button>
          <button v-else @click="mode = mode === 'login' ? 'signup' : 'login'" class="text-xs theme-text-muted hover:theme-text transition">
            {{ mode === 'login' ? $t('login.toggle_to_signup') : $t('login.toggle_to_login') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { supabase } from '../lib/supabase'
import { useNotify } from '../composables/useNotify'
import { useI18n } from 'vue-i18n'

const router = useRouter()
const { showToast } = useNotify()
const { t } = useI18n()

type Mode = 'login' | 'signup' | 'forgot'
const mode = ref<Mode>('login')

const email = ref('')
const password = ref('')
const loading = ref(false)
const isGoogleLoading = ref(false)

async function loginWithGoogle() {
  isGoogleLoading.value = true
  try {
    const { error } = await supabase.auth.signInWithOAuth({
      provider: 'google',
      options: {
        redirectTo: `${window.location.origin}/dashboard`
      }
    })
    if (error) throw error
  } catch (err: any) {
    showToast(err.message, 'error')
    isGoogleLoading.value = false
  }
}

async function handleSubmit() {
  if (!email.value) { showToast(t('login.error_empty'), 'error'); return }
  if (mode.value !== 'forgot' && !password.value) { showToast(t('login.error_empty'), 'error'); return }
  if (mode.value === 'signup' && password.value.length < 6) { showToast(t('login.error_short_password'), 'error'); return }

  loading.value = true
  try {
    if (mode.value === 'login') {
      const { error } = await supabase.auth.signInWithPassword({ email: email.value, password: password.value })
      if (error) throw error
      router.push('/dashboard')
    } else if (mode.value === 'signup') {
      const { error } = await supabase.auth.signUp({ email: email.value, password: password.value })
      if (error) throw error
      showToast('Pendaftaran berhasil! Silakan cek email Anda untuk verifikasi.', 'success')
      mode.value = 'login'
    } else if (mode.value === 'forgot') {
      const { error } = await supabase.auth.resetPasswordForEmail(email.value, { redirectTo: `${window.location.origin}/update-password` })
      if (error) throw error
      showToast(t('login.reset_link_sent'), 'success')
      mode.value = 'login'
    }
  } catch (err: any) {
    showToast(err.message, 'error')
  } finally {
    loading.value = false
  }
}
</script>
