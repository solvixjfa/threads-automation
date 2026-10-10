<template>
  <div class="min-h-screen flex items-center justify-center p-4">
    <div class="w-full max-w-sm bg-white border border-zinc-200 rounded-2xl p-8 space-y-6 shadow-xl">
      <div class="text-center space-y-2">
        <div class="inline-block bg-black text-white px-3 py-1.5 rounded-lg text-xs font-black tracking-widest uppercase mb-2">IXIERA</div>
        <h1 class="text-2xl font-bold text-zinc-900 tracking-tight">Halo!</h1>
        <p class="text-xs text-zinc-500">Masuk untuk ngatur otomatisasi Threads lu.</p>
      </div>

      <form @submit.prevent="handleAuth" class="space-y-4">
        <div class="space-y-1.5">
          <label class="text-xs font-bold text-zinc-700">Email</label>
          <input
            v-model="email"
            type="email"
            required
            placeholder="nama@email.com"
            class="w-full bg-zinc-50 border border-zinc-300 rounded-lg p-3 text-sm text-zinc-900 focus:outline-none focus:ring-2 focus:ring-black transition"
          />
        </div>

        <div class="space-y-1.5">
          <label class="text-xs font-bold text-zinc-700">Password</label>
          <input
            v-model="password"
            type="password"
            required
            placeholder="••••••••"
            class="w-full bg-zinc-50 border border-zinc-300 rounded-lg p-3 text-sm text-zinc-900 focus:outline-none focus:ring-2 focus:ring-black transition"
          />
        </div>

        <div v-if="errorMsg" class="p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-xs text-center font-medium">
          {{ errorMsg }}
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-black hover:bg-zinc-800 text-white font-bold text-sm py-3.5 rounded-lg transition shadow-md disabled:opacity-50"
        >
          {{ loading ? 'Bentar...' : (isSignUp ? 'Daftar' : 'Masuk') }}
        </button>
      </form>

      <div class="text-center pt-2">
        <button
          @click="isSignUp = !isSignUp; errorMsg = ''"
          class="text-xs text-zinc-500 hover:text-black font-medium underline transition"
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
      const { error } = await supabase.auth.signUp({ email: email.value, password: password.value })
      if (error) throw error
      alert('Sip, akun udah dibikin! Langsung login aja.')
      isSignUp.value = false
    } else {
      const { error } = await supabase.auth.signInWithPassword({ email: email.value, password: password.value })
      if (error) throw error
      router.push('/dashboard')
    }
  } catch (err: any) {
    errorMsg.value = err.message || 'Gagal login, cek lagi yak.'
  } finally {
    loading.value = false
  }
}
</script>
