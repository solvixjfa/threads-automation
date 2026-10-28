<template>
  <div class="min-h-screen flex items-center justify-center p-4 theme-bg">
    <div class="w-full max-w-sm space-y-6">
      <div class="text-center space-y-2">
        <div class="w-12 h-12 mx-auto flex items-center justify-center rounded-lg text-sm font-black theme-accent">IX</div>
        <h1 class="text-2xl font-bold theme-text">{{ isSignUp ? $t('login.sign_up_title') : $t('login.welcome') }}</h1>
        <p class="text-xs theme-text-muted">{{ isSignUp ? $t('login.sign_up_subtitle') : $t('login.subtitle') }}</p>
      </div>

      <Card>
        <div class="space-y-4">
          <div class="space-y-1">
            <label class="label">{{ $t('login.email') }}</label>
            <input v-model="email" type="email" :placeholder="$t('login.email_placeholder')" class="input w-full" />
          </div>
          <div class="space-y-1">
            <label class="label">{{ $t('login.password') }}</label>
            <input v-model="password" type="password" :placeholder="$t('login.password_placeholder')" class="input w-full" @keydown.enter="handleSubmit" />
          </div>

          <Button @click="handleSubmit" :disabled="loading" :loading="loading" class="w-full">
            {{ loading ? $t('common.processing') : (isSignUp ? $t('login.sign_up') : $t('login.sign_in')) }}
          </Button>

          <button @click="isSignUp = !isSignUp" class="w-full text-center text-xs theme-text-muted hover:theme-text transition">
            {{ isSignUp ? $t('login.toggle_to_login') : $t('login.toggle_to_signup') }}
          </button>
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

const isSignUp = ref(false)
const email = ref('')
const password = ref('')
const loading = ref(false)

async function handleSubmit() {
  if (!email.value || !password.value) {
    showToast(t('login.error_empty'), 'error')
    return
  }
  if (isSignUp.value && password.value.length < 6) {
    showToast(t('login.error_short_password'), 'error')
    return
  }

  loading.value = true
  try {
    let result
    if (isSignUp.value) {
      result = await supabase.auth.signUp({ email: email.value, password: password.value })
    } else {
      result = await supabase.auth.signInWithPassword({ email: email.value, password: password.value })
    }

    if (result.error) throw result.error

    if (isSignUp.value) {
      showToast('Account created! Check your email to confirm.', 'success')
    } else {
      router.push('/dashboard')
    }
  } catch (err: any) {
    showToast(t('login.error_invalid') + ' (' + err.message + ')', 'error')
  } finally {
    loading.value = false
  }
}
</script>
