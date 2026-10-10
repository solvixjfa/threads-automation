<template>
  <div class="max-w-4xl mx-auto space-y-8">
    <div>
      <h1 class="text-2xl font-bold text-white tracking-tight">Settings & Configuration</h1>
      <p class="text-zinc-400 text-sm mt-1">Atur koneksi akun Threads, prompt AI Gemini, serta batas keamanan otomatisasi.</p>
    </div>

    <!-- SECTION 1: ACCOUNT CONNECTION -->
    <div class="bg-zinc-950/80 backdrop-blur-xl border border-white/10 rounded-xl p-6 space-y-6 shadow-2xl">
      <div class="flex items-center justify-between border-b border-white/10 pb-4">
        <div>
          <h2 class="text-base font-semibold text-white">Koneksi Akun Threads</h2>
          <p class="text-xs text-zinc-400">Status tautan OAuth Meta Threads API.</p>
        </div>
        <button
          @click="connectThreads"
          class="bg-white hover:bg-zinc-200 text-black text-xs font-bold px-4 py-2 rounded-lg transition"
        >
          {{ settingsStore.account?.connection_status === 'connected' ? 'Re-connect Account' : 'Connect Account' }}
        </button>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
        <div class="p-4 bg-black border border-white/10 rounded-lg space-y-1">
          <span class="text-zinc-500">Username Terhubung</span>
          <p class="text-white font-bold text-sm">@{{ settingsStore.account?.username || 'Belum Terhubung' }}</p>
        </div>
        <div class="p-4 bg-black border border-white/10 rounded-lg space-y-1">
          <span class="text-zinc-500">Status Koneksi</span>
          <p :class="['font-bold text-sm uppercase tracking-wider', settingsStore.account?.connection_status === 'connected' ? 'text-emerald-400' : 'text-amber-400']">
            {{ settingsStore.account?.connection_status || 'Disconnected' }}
          </p>
        </div>
      </div>

      <!-- Emergency Kill Switch -->
      <div v-if="settingsStore.account?.id" class="p-5 bg-black border border-white/10 rounded-lg flex items-center justify-between mt-4">
        <div>
          <h3 class="text-xs font-bold text-rose-500 uppercase tracking-wider">Emergency Kill Switch</h3>
          <p class="text-[11px] text-zinc-400 mt-1">Hentikan paksa semua jadwal publish & auto-reply.</p>
        </div>
        <button
          @click="settingsStore.toggleKillSwitch(!settingsStore.account.kill_switch)"
          :class="['px-5 py-2 text-xs font-bold rounded-lg transition uppercase tracking-wider', settingsStore.account.kill_switch ? 'bg-rose-600 text-white' : 'bg-zinc-900 border border-white/10 text-white hover:bg-zinc-800']"
        >
          {{ settingsStore.account.kill_switch ? 'Kill Switch Active' : 'Enable Kill Switch' }}
        </button>
      </div>
    </div>

    <!-- SECTION 2: GEMINI AI CONFIGURATION -->
    <div class="bg-zinc-950/80 backdrop-blur-xl border border-white/10 rounded-xl p-6 space-y-6 shadow-2xl">
      <h2 class="text-base font-semibold text-white border-b border-white/10 pb-4">Pengaturan Gemini AI Auto-Reply</h2>

      <div class="space-y-5 text-sm">
        <div class="flex items-center justify-between">
          <label class="font-medium text-zinc-300">Aktifkan Auto-Reply Engine</label>
          <input type="checkbox" v-model="form.enabled" class="w-4 h-4 rounded bg-black border-white/10" />
        </div>

        <div class="space-y-2">
          <label class="font-medium text-zinc-300">Mode Operasi</label>
          <select v-model="form.mode" class="w-full bg-black border border-white/10 text-white rounded-lg p-3 focus:outline-none focus:border-white transition">
            <option value="review">Review Queue (Setujui manual sebelum terkirim)</option>
            <option value="auto">Fully Automatic (Kirim otomatis via Gemini)</option>
          </select>
        </div>

        <div class="space-y-2">
          <label class="font-medium text-zinc-300">Tone & Instruksi AI (Prompt)</label>
          <textarea v-model="form.tone_prompt" rows="3" class="w-full bg-black border border-white/10 text-white rounded-lg p-3 focus:outline-none focus:border-white transition resize-none"></textarea>
        </div>

        <div class="space-y-2">
          <label class="font-medium text-zinc-300">Knowledge Base (Fakta Bisnis)</label>
          <textarea v-model="form.knowledge_base" rows="4" placeholder="Tuliskan FAQ, detail layanan, atau fakta bisnis..." class="w-full bg-black border border-white/10 text-white rounded-lg p-3 focus:outline-none focus:border-white transition resize-none"></textarea>
        </div>

        <div class="pt-4 flex justify-end">
          <button @click="handleSave" :disabled="settingsStore.loading" class="bg-white hover:bg-zinc-200 text-black font-bold px-6 py-2.5 rounded-lg transition disabled:opacity-50">
            {{ settingsStore.loading ? 'Menyimpan...' : 'Simpan Pengaturan' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useSettingsStore } from '../stores/settings'

const settingsStore = useSettingsStore()
const form = ref({
  enabled: false,
  mode: 'review' as 'review' | 'auto',
  tone_prompt: 'Balas dengan ramah, profesional, dan ringkas.',
  knowledge_base: ''
})

function connectThreads() {
  const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || 'https://xtarsaurwclktwhhryas.supabase.co'
  window.location.href = `${supabaseUrl}/functions/v1/threads-oauth-start`
}

async function handleSave() {
  await settingsStore.saveSettings(form.value)
}

onMounted(async () => {
  await settingsStore.fetchAccountAndSettings()
  if (settingsStore.settings) {
    form.value.enabled = settingsStore.settings.enabled
    form.value.mode = settingsStore.settings.mode
    form.value.tone_prompt = settingsStore.settings.tone_prompt || 'Balas dengan ramah, profesional, dan ringkas.'
    form.value.knowledge_base = settingsStore.settings.knowledge_base || ''
  }
})
</script>
