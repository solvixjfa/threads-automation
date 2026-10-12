<template>
  <div class="space-y-6 max-w-4xl">
    <div>
      <h1 class="text-2xl font-bold tracking-tight text-white">Content Repurpose AI</h1>
      <p class="text-zinc-400 text-sm mt-1">Daur ulang postingan lama atau teks panjang jadi 3 variasi angle Threads yang fresh.</p>
    </div>

    <!-- Input Box -->
    <div class="bg-white/5 border border-white/10 rounded-xl p-6 space-y-4">
      <div class="space-y-2">
        <label class="text-xs font-semibold text-zinc-300 uppercase tracking-wider">Teks Asli / Postingan Lama</label>
        <textarea 
          v-model="sourceText" 
          rows="4" 
          placeholder="Paste postingan lama, artikel, atau cuitan yang ingin didaur ulang di sini..."
          class="w-full bg-black border border-white/20 rounded-lg p-4 text-sm text-white placeholder:text-zinc-600 focus:outline-none focus:border-white transition resize-none"
        ></textarea>
      </div>

      <div class="space-y-2">
        <label class="text-xs font-semibold text-zinc-300 uppercase tracking-wider">Pilih Angle Daur Ulang</label>
        <select 
          v-model="repurposeAngle"
          class="w-full bg-black border border-white/20 rounded-lg p-3 text-sm text-white focus:outline-none focus:border-white transition"
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
          class="bg-white text-black hover:bg-zinc-200 text-sm font-bold py-2.5 px-6 rounded-lg transition disabled:opacity-50 flex items-center gap-2"
        >
          <span v-if="isGenerating" class="w-4 h-4 border-2 border-black border-t-transparent rounded-full animate-spin"></span>
          <span>{{ isGenerating ? 'Mendaur Ulang...' : 'Daur Ulang Teks' }}</span>
        </button>
      </div>
    </div>

    <!-- Hasil Repurpose -->
    <div v-if="results.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div v-for="(item, idx) in results" :key="idx" class="bg-black border border-white/10 p-5 rounded-xl space-y-3 relative group">
        <div class="flex justify-between items-center border-b border-white/10 pb-2">
          <span class="text-xs font-bold text-zinc-400">Variasi {{ idx + 1 }}</span>
          <button @click="copyText(item.content)" class="text-xs text-zinc-500 hover:text-white transition flex items-center gap-1">
            Salin Teks
          </button>
        </div>
        <p class="text-sm text-zinc-300 whitespace-pre-wrap leading-relaxed">{{ item.content }}</p>
        <div class="absolute inset-0 bg-black/80 flex items-center justify-center opacity-0 group-hover:opacity-100 transition backdrop-blur-sm rounded-xl">
           <button @click="sendToComposer(item.content)" class="bg-white text-black px-4 py-2 rounded-lg font-bold text-sm hover:scale-105 transition transform">
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

const router = useRouter()
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
    if (!user) throw new Error("Not auth")

    const { data: acc } = await supabase.schema('threads').from('threads_accounts').select('id').eq('user_id', user.id).maybeSingle()
    if (!acc) throw new Error("No account")

    // Kita pakai endpoint generate-post yang udah ada, cuma prompt-nya kita modif sedikit via payload
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
  } catch (err: any) {
    alert("Gagal: " + err.message)
  } finally {
    isGenerating.value = false
  }
}

function copyText(text: string) {
  navigator.clipboard.writeText(text)
  alert('Tersalin ke clipboard!')
}

function sendToComposer(text: string) {
  // Simpan ke local storage buat diambil composer
  localStorage.setItem('draft_repurpose', text)
  router.push('/composer')
}
</script>
