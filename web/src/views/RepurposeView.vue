<template>
  <div class="space-y-8 relative">

    <div>
      <h1 class="text-2xl font-bold tracking-tight">Repurpose</h1>
      <p class="text-sm theme-text-muted mt-1">Daur ulang postingan lama atau teks panjang jadi 3 variasi angle Threads yang fresh.</p>
    </div>

    <Card>
      <div class="space-y-4">
        <Textarea
          v-model="sourceText"
          label="Teks Asli / Postingan Lama"
          :rows="4"
          placeholder="Paste postingan lama, artikel, atau cuitan yang ingin didaur ulang di sini..."
        />

        <div class="space-y-1">
          <label class="label">Pilih Angle Daur Ulang</label>
          <select v-model="repurposeAngle" class="input">
            <option value="Format Listicle (Poin-poin praktis)">Ubah jadi Listicle (Poin-poin)</option>
            <option value="Kontroversial / Hot Take (Lebih memancing opini)">Ubah jadi Kontroversial / Hot Take</option>
            <option value="Storytelling (Bercerita pengalaman pribadi)">Ubah jadi Storytelling</option>
            <option value="Utasan Panjang (Edukasi mendalam)">Ubah jadi Thread Panjang Edukatif</option>
          </select>
        </div>

        <div class="flex justify-end pt-2">
          <Button
            @click="generateRepurpose"
            :disabled="isGenerating || !sourceText"
            :loading="isGenerating"
          >
            {{ isGenerating ? 'Mendaur Ulang...' : 'Daur Ulang Teks' }}
          </Button>
        </div>
      </div>
    </Card>

    <div v-if="results.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div
        v-for="(item, idx) in results"
        :key="idx"
        class="card p-5 space-y-3 relative group overflow-hidden"
      >
        <div class="flex justify-between items-center pb-2 divider">
          <Badge variant="accent">Variasi {{ idx + 1 }}</Badge>
          <button
            @click="copyText(item.content)"
            class="text-xs font-bold theme-text-muted hover:theme-text transition"
          >
            Salin Teks
          </button>
        </div>
        <p class="text-sm whitespace-pre-wrap leading-relaxed">{{ item.content }}</p>

        <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity backdrop-blur-sm" style="background: color-mix(in srgb, var(--bg-primary) 90%, transparent);">
          <Button @click="sendToComposer(item.content)">Kirim ke Composer</Button>
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
import { Card, Button, Textarea, Badge } from '../components/ui'

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
    if (!user) throw new Error('Not authenticated')

    const { data: acc } = await supabase
      .schema('threads')
      .from('threads_accounts')
      .select('id')
      .eq('user_id', user.id)
      .maybeSingle()

    if (!acc) throw new Error('No account linked')

    const res = await fetch('https://threads-automation-production-53ad.up.railway.app/api/v1/rag/generate-post', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        account_id: acc.id,
        topic: 'Teks Asli:\n"' + sourceText.value + '"',
        tone: 'Custom Prompt',
        custom_prompt: 'Tugas lu MENGUBAH / MENDAUR ULANG teks asli di atas menjadi 3 variasi berbeda. \nAngle yang diminta: ' + repurposeAngle.value + '.\nJangan mengarang informasi baru, cukup ubah format, gaya bahasa, dan strukturnya agar cocok diposting ulang di Threads.'
      })
    })

    const data = await res.json()
    if (!res.ok) throw new Error(data.detail)

    results.value = data.options || []
    showToast('Berhasil mendaur ulang konten!', 'success')
  } catch (err: any) {
    showToast('Gagal: ' + err.message, 'error')
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
  router.push('/content/create')
}
</script>
