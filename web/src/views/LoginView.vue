<template>
  <div class="min-h-[70vh] flex items-center justify-center p-4">
    <div class="w-full max-w-md bg-zinc-950/90 backdrop-blur-xl border border-white/10 rounded-2xl p-8 space-y-6 shadow-2xl">
      <div class="text-center space-y-2">
        <h1 class="text-2xl font-bold text-white tracking-tight">Ixiera Automation</h1>
        <p class="text-xs text-zinc-400">Masuk ke akun kamu untuk mengelola otomatisasi Threads.</p>
      </div>

      <form @submit.prevent="handleAuth" class="space-y-4">
        <div class="space-y-1">
          <label class="text-xs font-semibold text-zinc-300">Email</label>
          <input
            v-model="email"
            type="email"
            required
            placeholder="nama@email.com"
            class="w-full bg-black border border-white/10 rounded-lg p-3 text-sm text-white focus:outline-none focus:border-white transition"
          />
        </div>

        <div class="space-y-1">
          <label class="text-xs font-semibold text-zinc-300">Password</label>
          <input
            v-model="password"
            type="password"
            required
            placeholder="••••••••"
            class="w-full bg-black border border-white/10 rounded-lg p-3 text-sm text-white focus:outline-none focus:border-white transition"
          />
        </div>

        <div v-if="errorMsg" class="p-3 bg-rose-950/80 border border-rose-500/30 rounded-lg text-rose-300 text-xs">
          {{ errorMsg }}
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-white hover:bg-zinc-200 text-black font-bold text-xs py-3 rounded-lg transition disabled:opacity-50"
        >
          {{ loading ? 'Memproses...' : (isSignUp ? 'Daftar Akun Baru' : 'Masuk') }}
        </button>
      </form>

      <div class="text-center pt-2">
        <button
          @click="isSignUp = !isSignUp; errorMsg = ''"
          class="text-xs text-zinc-400 hover:text-white underline transition"
        >
          {{ isSignUp ? 'Sudah punya akun? Login' : 'Belum punya akun? Daftar' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { supabase } from '../lib/supabase'

const router = useRouter()
const email = ref('')
const password = ref('')
const isSignUp = ref(false)
const loading = ref(false)
const errorMsg = ref('')

async function handleAuth() {
  loading.value = true
  errorMsg.value = ''

  try {
    if (isSignUp.value) {
      const { error } = await supabase.auth.signUp({
        email: email.value,
        password: password.value
      })
      if (error) throw error
      alert('Pendaftaran berhasil! Silakan login.')
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
    errorMsg.value = err.message || 'Gagal autentikasi'
  } finally {
    loading.value = false
  }
}
</script>
