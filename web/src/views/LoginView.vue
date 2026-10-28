<template>
  <div class="min-h-screen flex items-center justify-center p-4 theme-bg">
    <div class="w-full max-w-sm space-y-6">
      
      <!-- HEADER -->
      <div class="text-center space-y-2">
        <div class="w-12 h-12 mx-auto flex items-center justify-center rounded-lg text-sm font-black theme-accent">IX</div>
        <h1 class="text-2xl font-bold theme-text">
          {{ mode === 'login' ? $t('login.welcome') : (mode === 'signup' ? $t('login.sign_up_title') : $t('login.reset_password_title')) }}
        </h1>
        <p class="text-xs theme-text-muted">
          {{ mode === 'login' ? $t('login.subtitle') : (mode === 'signup' ? $t('login.sign_up_subtitle') : $t('login.reset_password_subtitle')) }}
        </p>
      </div>

      <Card>
        <div class="space-y-4">
          <!-- EMAIL INPUT -->
          <div class="space-y-1">
            <label class="label">{{ $t('login.email') }}</label>
            <input v-model="email" type="email" :placeholder="$t('login.email_placeholder')" class="input w-full" />
          </div>

          <!-- PASSWORD INPUT (Disembunyiin kalau mode Forgot Password) -->
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
          <Button @click="handleSubmit" :disabled="loading" :loading="loading" class="w-full">
            {{ loading ? $t('common.processing') : (
              mode === 'login' ? $t('login.sign_in') : 
              (mode === 'signup' ? $t('login.sign_up') : $t('login.send_reset_link'))
            ) }}
          </Button>

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
      </Card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { supabase } from '../lib/supabase'
import { useNotify } from '../composables/useNotify'
import { useI18n } from 'vue-i18n'
import { Card, Button } from '../components/ui'

const router = useRouter()
const { showToast } = useNotify()
const { t } = useI18n()

type Mode = 'login' | 'signup' | 'forgot'
const mode = ref<Mode>('login')

const email = ref('')
const password = ref('')
const loading = ref(false)

async function handleSubmit() {
  // Validasi basic
  if (!email.value) {
    showToast(t('login.error_empty'), 'error')
    return
  }
  if (mode.value !== 'forgot' && !password.value) {
    showToast(t('login.error_empty'), 'error')
    return
  }
  if (mode.value === 'signup' && password.value.length < 6) {
    showToast(t('login.error_short_password'), 'error')
    return
  }

  loading.value = true
  try {
    if (mode.value === 'login') {
      const { error } = await supabase.auth.signInWithPassword({ email: email.value, password: password.value })
      if (error) throw error
      router.push('/dashboard')
      
    } else if (mode.value === 'signup') {
      const { error } = await supabase.auth.signUp({ email: email.value, password: password.value })
      if (error) throw error
      showToast('Account created! Check your email to confirm.', 'success')
      mode.value = 'login' // Balikin ke mode login setelah signup
      
    } else if (mode.value === 'forgot') {
      const { error } = await supabase.auth.resetPasswordForEmail(email.value, {
        redirectTo: `${window.location.origin}/login` // Nanti lu perlu halaman update password
      })
      if (error) throw error
      showToast(t('login.reset_link_sent'), 'success')
      mode.value = 'login'
    }
  } catch (err: any) {
    showToast(err.message, 'error')
  } finally {
    loading.value = false // INI KUNCI BIAR GAK STUCK
  }
}
</script>
