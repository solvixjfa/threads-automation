<template>
  <div class="space-y-8 relative">
    <NotifyOverlay />
    <div>
      <h1 class="text-2xl font-bold text-slate-900 tracking-tight">Content Repurpose AI</h1>
      <p class="text-slate-500 text-sm mt-1">Daur ulang postingan lama atau teks panjang jadi 3 variasi angle Threads yang fresh.</p>
    </div>

    <!-- Input Box -->
    <div class="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-4">
      <div class="space-y-2">
        <label class="text-xs font-bold text-slate-700 uppercase tracking-wide">Teks Asli / Postingan Lama</label>
        <textarea 
          v-model="sourceText" 
          rows="4" 
          placeholder="Paste postingan lama, artikel, atau cuitan yang ingin didaur ulang di sini..."
          class="w-full bg-slate-50 border border-slate-200 rounded-xl p-4 text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition resize-none"
        ></textarea>
      </div>

      <div class="space-y-2">
        <label class="text-xs font-bold text-slate-700 uppercase tracking-wide">Pilih Angle Daur Ulang</label>
        <select 
          v-model="repurposeAngle"
          class="w-full bg-white border border-slate-200 rounded-xl p-3 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition"
        >
          <option value="Format Listicle (Poin-poin praktis)">Ubah jadi Listicle (Poin-poin)</option>
          <option value="Kontroversial / Hot Take (Lebih memancing opini)">Ubah jadi Kontroversial / Hot Take</option>
          <option value="Storytelling (Bercerita pengalaman pribadi)">Ubah jadi Storytelling</option>
          <option value="Utasan Panjang (Edukasi mendalam)">Ubah jadi Thread Panjang Edukatif</option>
        </select>
      </div>

      <div class="flex justify-end pt-2">
        <button 
          @click="generateRepurpose" 
          :disabled="isGenerating || !sourceText"
          class="bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold py-2.5 px-6 rounded-xl transition shadow-sm disabled:opacity-50 flex items-center gap-2"
        >
          <span v-if="isGenerating" class="w-3 h-3 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
          <span>{{ isGenerating ? 'Mendaur Ulang...' : 'Daur Ulang Teks' }}</span>
        </button>
      </div>
    </div>

    <!-- Hasil Repurpose -->
    <div v-if="results.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div v-for="(item, idx) in results" :key="idx" class="bg-white border border-slate-200 p-5 rounded-2xl space-y-3 relative group overflow-hidden shadow-sm">
        <div class="flex justify-between items-center border-b border-slate-100 pb-2">
          <span class="text-xs font-bold text-indigo-600 uppercase">Variasi {{ idx + 1 }}</span>
          <button @click="copyText(item.content)" class="text-xs font-bold text-slate-500 hover:text-indigo-600 transition flex items-center gap-1">
            Salin Teks
          </button>
        </div>
        <p class="text-sm text-slate-800 whitespace-pre-wrap leading-relaxed">{{ item.content }}</p>
        
        <div class="absolute inset-0 bg-white/90 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity backdrop-blur-sm">
           <button @click="sendToComposer(item.content)" class="bg-indigo-600 text-white px-5 py-2.5 rounded-xl font-bold text-sm hover:scale-105 transition transform shadow-lg">
             Kirim ke Composer
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
import NotifyOverlay from '../components/NotifyOverlay.vue'

const router = useRouter()
const { showToast } = useNotify()
const sourceText = ref('')
const repurposeAngle = ref('Format Listicle (Poin-poin praktis)')
const isGenerating = ref(false)
const results = ref<any[]>([])

async function generateRepurpose() {
  if (!sourceText.value) return
  isGenerating.value = true
  results.value = []

  try {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) throw new Error("Not authenticated")

    const { data: acc } = await supabase.schema('threads').from('threads_accounts').select('id').eq('user_id', user.id).maybeSingle()
    if (!acc) throw new Error("No account linked")

    const res = await fetch('https://threads-automation-production-53ad.up.railway.app/api/v1/rag/generate-post', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        account_id: acc.id,
        topic: `Teks Asli:\n"${sourceText.value}"`,
        tone: 'Custom Prompt',
        custom_prompt: `Tugas lu MENGUBAH / MENDAUR ULANG teks asli di atas menjadi 3 variasi berbeda. \nAngle yang diminta: ${repurposeAngle.value}.\nJangan mengarang informasi baru, cukup ubah format, gaya bahasa, dan strukturnya agar cocok diposting ulang di Threads.`
      })
    })

    const data = await res.json()
    if (!res.ok) throw new Error(data.detail)
    
    results.value = data.options || []
    showToast('Berhasil mendaur ulang konten!', 'success')
  } catch (err: any) {
    showToast("Gagal: " + err.message, 'error')
  } finally {
    isGenerating.value = false
  }
}

function copyText(text: string) {
  navigator.clipboard.writeText(text)
  showToast('Tersalin ke clipboard!', 'info')
}

function sendToComposer(text: string) {
  localStorage.setItem('draft_repurpose', text)
  router.push('/composer')
}
</script>
