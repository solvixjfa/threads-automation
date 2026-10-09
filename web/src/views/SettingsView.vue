<template>
  <div class="max-w-4xl mx-auto space-y-8">
    <div>
      <h1 class="text-2xl font-bold text-slate-100">Settings & Configuration</h1>
      <p class="text-slate-400 text-sm mt-1">Atur koneksi akun Threads, prompt AI Gemini, serta batas keamanan otomatisasi.</p>
    </div>

    <!-- SECTION 1: ACCOUNT CONNECTION & EMERGENCY KILL SWITCH -->
    <div class="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-6 shadow-xl">
      <div class="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h2 class="text-base font-semibold text-slate-200">Koneksi Akun Threads</h2>
          <p class="text-xs text-slate-400">Status tautan OAuth Meta Threads API.</p>
        </div>
        
        <button
          @click="connectThreads"
          class="bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-medium px-4 py-2 rounded-lg transition"
        >
          {{ settingsStore.account ? 'Re-connect Account' : 'Connect Threads Account' }}
        </button>
      </div>

      <div v-if="settingsStore.account" class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
        <div class="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-1">
          <span class="text-slate-500">Username Terhubung</span>
          <p class="text-slate-200 font-bold text-sm">@{{ settingsStore.account.username || 'Unlinked' }}</p>
        </div>

        <div class="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-1">
          <span class="text-slate-500">Status Koneksi</span>
          <p class="text-emerald-400 font-bold text-sm uppercase">{{ settingsStore.account.connection_status }}</p>
        </div>
      </div>

      <!-- Emergency Kill Switch -->
      <div v-if="settingsStore.account" class="p-4 bg-rose-950/20 border border-rose-900/40 rounded-lg flex items-center justify-between">
        <div>
          <h3 class="text-xs font-bold text-rose-300">Emergency Kill Switch</h3>
          <p class="text-[11px] text-rose-400/80">Hentikan secara paksa semua jadwal publish dan auto-reply AI.</p>
        </div>
        <button
          @click="settingsStore.toggleKillSwitch(!settingsStore.account.kill_switch)"
          :class="['px-4 py-1.5 text-xs font-bold rounded-lg transition', settingsStore.account.kill_switch ? 'bg-rose-600 text-white' : 'bg-slate-800 text-slate-300 hover:bg-slate-700']"
        >
          {{ settingsStore.account.kill_switch ? 'KILL SWITCH ACTIVE' : 'Enable Kill Switch' }}
        </button>
      </div>
    </div>

    <!-- SECTION 2: GEMINI AI AUTO-REPLY CONFIGURATION -->
    <div class="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-6 shadow-xl">
      <h2 class="text-base font-semibold text-slate-200 border-b border-slate-800 pb-4">Pengaturan Gemini AI Auto-Reply</h2>

      <div class="space-y-4 text-xs">
        <div class="flex items-center justify-between">
          <label class="font-medium text-slate-300">Aktifkan Auto-Reply Engine</label>
          <input
            type="checkbox"
            v-model="form.enabled"
            class="w-4 h-4 accent-indigo-600 rounded"
          />
        </div>

        <div class="space-y-1">
          <label class="font-medium text-slate-300">Mode Operasi</label>
          <select v-model="form.mode" class="w-full bg-slate-950 border border-slate-800 text-slate-200 rounded-lg p-2.5 focus:outline-none">
            <option value="review">Review Queue (Setujui manual sebelum terkirim)</option>
            <option value="auto">Fully Automatic (Kirim otomatis via Gemini)</option>
          </select>
        </div>

        <div class="space-y-1">
          <label class="font-medium text-slate-300">Tone & Instruksi AI (Tone Prompt)</label>
          <textarea
            v-model="form.tone_prompt"
            rows="3"
            placeholder="Balas dengan ramah, suportif, dan sertakan gaya santai khas Threads..."
            class="w-full bg-slate-950 border border-slate-800 text-slate-200 rounded-lg p-3 focus:outline-none"
          ></textarea>
        </div>

        <div class="space-y-1">
          <label class="font-medium text-slate-300">Knowledge Base (Fakta & Referensi AI)</label>
          <textarea
            v-model="form.knowledge_base"
            rows="4"
            placeholder="Tuliskan FAQ, harga produk, atau detail layanan bisnis kamu di sini agar AI tidak berhalusinasi..."
            class="w-full bg-slate-950 border border-slate-800 text-slate-200 rounded-lg p-3 focus:outline-none"
          ></textarea>
        </div>

        <div class="pt-4 flex justify-end">
          <button
            @click="handleSave"
            :disabled="settingsStore.loading"
            class="bg-indigo-600 hover:bg-indigo-500 text-white font-medium px-5 py-2.5 rounded-lg transition disabled:opacity-50"
          >
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
  const res = await settingsStore.saveSettings(form.value)
  if (res.success) {
    alert('Pengaturan AI berhasil disimpan!')
  }
}

onMounted(async () => {
  await settingsStore.fetchAccountAndSettings()
  if (settingsStore.settings) {
    form.value.enabled = settingsStore.settings.enabled
    form.value.mode = settingsStore.settings.mode
    form.value.tone_prompt = settingsStore.settings.tone_prompt
    form.value.knowledge_base = settingsStore.settings.knowledge_base
  }
})
</script>
