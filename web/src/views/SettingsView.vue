<template>
  <div class="max-w-4xl mx-auto space-y-8">
    <div>
      <h1 class="text-2xl font-bold text-slate-900 tracking-tight">Settings & Configuration</h1>
      <p class="text-slate-500 text-sm mt-1">Atur koneksi akun Threads dan konfigurasi otomatisasi lu.</p>
    </div>

    <!-- Notification Banners -->
    <div v-if="successMsg" class="p-4 bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs rounded-xl flex items-center justify-between font-medium">
      <span>{{ successMsg }}</span>
      <button @click="successMsg = ''" class="text-emerald-500 hover:text-emerald-800 font-bold">✕</button>
    </div>
    <div v-if="errorMsg" class="p-4 bg-rose-50 border border-rose-200 text-rose-700 text-xs rounded-xl flex items-center justify-between font-medium">
      <span>Error: {{ errorMsg }}</span>
      <button @click="errorMsg = ''" class="text-rose-500 hover:text-rose-800 font-bold">✕</button>
    </div>

    <!-- SECTION 1: ACCOUNT CONNECTION -->
    <div class="bg-white border border-slate-200 rounded-2xl p-6 space-y-6 shadow-sm">
      <div class="flex items-center justify-between border-b border-slate-100 pb-4">
        <div>
          <h2 class="text-base font-bold text-slate-800">Koneksi Akun Threads</h2>
          <p class="text-xs text-slate-500">Status sambungan aplikasi lu dengan Meta.</p>
        </div>
        <button
          @click="connectThreads"
          :disabled="connecting"
          class="bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold px-5 py-2.5 rounded-lg transition shadow-sm disabled:opacity-50"
        >
          {{ connecting ? 'Mengalihkan...' : (settingsStore.account?.connection_status === 'connected' ? 'Re-connect Akun' : 'Connect Akun') }}
        </button>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
        <div class="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-1">
          <span class="text-slate-500 font-medium">Username Terhubung</span>
          <p class="text-slate-900 font-bold text-sm">@{{ settingsStore.account?.username || 'Belum Terhubung' }}</p>
        </div>
        <div class="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-1">
          <span class="text-slate-500 font-medium">Status Koneksi</span>
          <p :class="['font-bold text-sm uppercase tracking-wider', settingsStore.account?.connection_status === 'connected' ? 'text-emerald-600' : 'text-slate-400']">
            {{ settingsStore.account?.connection_status || 'Disconnected' }}
          </p>
        </div>
      </div>
    </div>

    <!-- SECTION 2: GEMINI AI CONFIGURATION -->
    <div class="bg-white border border-slate-200 rounded-2xl p-6 space-y-6 shadow-sm">
      <h2 class="text-base font-bold text-slate-800 border-b border-slate-100 pb-4">Pengaturan Gemini AI Auto-Reply</h2>

      <div class="space-y-5 text-sm">
        <div class="flex items-center justify-between">
          <label class="font-bold text-slate-700">Aktifkan Auto-Reply Engine</label>
          <input type="checkbox" v-model="form.enabled" class="w-5 h-5 rounded border-slate-300 text-indigo-600 focus:ring-indigo-500" />
        </div>

        <div class="space-y-2">
          <label class="font-bold text-slate-700">Mode Operasi</label>
          <select v-model="form.mode" class="w-full bg-slate-50 border border-slate-200 text-slate-800 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition">
            <option value="review">Review Queue (Setujui manual dulu)</option>
            <option value="auto">Fully Automatic (Langsung dibalas AI)</option>
          </select>
        </div>

        <div class="space-y-2">
          <label class="font-bold text-slate-700">Tone & Instruksi AI (Prompt)</label>
          <textarea v-model="form.tone_prompt" rows="3" class="w-full bg-slate-50 border border-slate-200 text-slate-800 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition resize-none"></textarea>
        </div>

        <div class="space-y-2">
          <label class="font-bold text-slate-700">Knowledge Base (Fakta Bisnis)</label>
          <textarea v-model="form.knowledge_base" rows="4" placeholder="Tuliskan FAQ, detail layanan, atau list harga..." class="w-full bg-slate-50 border border-slate-200 text-slate-800 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition resize-none"></textarea>
        </div>

        <div class="pt-4 flex justify-end">
          <button @click="handleSave" :disabled="settingsStore.loading" class="bg-indigo-600 hover:bg-indigo-700 text-white font-bold px-6 py-2.5 rounded-lg transition shadow-sm disabled:opacity-50">
            {{ settingsStore.loading ? 'Menyimpan...' : 'Simpan Pengaturan' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useSettingsStore } from '../stores/settings'
import { supabase } from '../lib/supabase'

const route = useRoute()
const router = useRouter()
const settingsStore = useSettingsStore()

const connecting = ref(false)
const successMsg = ref('')
const errorMsg = ref('')

const form = ref({
  enabled: false,
  mode: 'review' as 'review' | 'auto',
  tone_prompt: 'Balas dengan ramah, profesional, dan ringkas.',
  knowledge_base: ''
})

async function connectThreads() {
  connecting.value = true
  try {
    const { data, error } = await supabase.functions.invoke('threads-oauth-start')
    if (error) throw error
    if (data?.url) {
      window.location.href = data.url
    } else {
      throw new Error('Gagal dapetin URL OAuth Meta')
    }
  } catch (err: any) {
    alert('Error Connect Threads: ' + err.message)
  } finally {
    connecting.value = false
  }
}

async function handleSave() {
  await settingsStore.saveSettings(form.value)
  alert('Pengaturan AI sukses disimpan!')
}

onMounted(async () => {
  if (route.query.connected === 'true') {
    const username = route.query.username as string
    successMsg.value = `Sip! Akun Threads @${username || ''} sukses nyambung ke sistem.`
    router.replace({ query: {} })
  } else if (route.query.error) {
    errorMsg.value = decodeURIComponent(route.query.error as string)
    router.replace({ query: {} })
  }

  await settingsStore.fetchAccountAndSettings()
  if (settingsStore.settings) {
    form.value.enabled = settingsStore.settings.enabled
    form.value.mode = settingsStore.settings.mode
    form.value.tone_prompt = settingsStore.settings.tone_prompt || 'Balas dengan ramah, santai, dan ringkas.'
    form.value.knowledge_base = settingsStore.settings.knowledge_base || ''
  }
})
</script>
