<template>
  <div class="space-y-8 relative">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Repurpose</h1>
      <p class="text-sm theme-text-muted mt-1">Recycle old posts or long text into 3 fresh Threads angles.</p>
    </div>

    <!-- RECOMMENDATIONS SECTION -->
    <div v-if="recommendations.length > 0" class="space-y-3">
      <div class="flex items-center justify-between">
        <h2 class="text-sm font-bold uppercase tracking-wide">Recommended Posts</h2>
        <span class="text-[10px] font-bold theme-text-muted">By Highest Views</span>
      </div>
      <div class="flex gap-4 overflow-x-auto pb-4 pt-1 snap-x">
        <div 
          v-for="rec in recommendations" 
          :key="rec.id" 
          class="card p-4 w-72 shrink-0 snap-start flex flex-col justify-between space-y-3 hover:border-current transition-colors cursor-pointer group"
          @click="applyRecommendation(rec)"
        >
          <p class="text-xs leading-relaxed line-clamp-3 group-hover:theme-text transition-colors">{{ rec.text }}</p>
          
          <div class="flex items-center gap-4 text-xs">
            <div class="text-center">
              <span class="block text-[9px] theme-text-muted uppercase font-bold">Views</span>
              <span class="font-bold">{{ rec.views }}</span>
            </div>
            <div class="text-center">
              <span class="block text-[9px] theme-text-muted uppercase font-bold">Likes</span>
              <span class="font-bold">{{ rec.likes }}</span>
            </div>
            <div class="text-center">
              <span class="block text-[9px] theme-text-muted uppercase font-bold">ER</span>
              <span class="font-black">{{ rec.er }}%</span>
            </div>
            <div class="ml-auto opacity-0 group-hover:opacity-100 transition-opacity">
               <Badge variant="accent">Use</Badge>
            </div>
          </div>
        </div>
      </div>
    </div>

    <Card>
      <div class="space-y-4">
        <Textarea
          v-model="sourceText"
          label="Original Text / Old Post"
          :rows="4"
          placeholder="Paste an old post, article, or tweet you want to repurpose here..."
        />

        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <Select 
            v-model="repurposeAngle" 
            label="Repurpose Angle" 
            :options="[
              { label: 'Listicle (Actionable points)', value: 'Format Listicle (Poin-poin praktis)' },
              { label: 'Hot Take / Controversial', value: 'Kontroversial / Hot Take (Lebih memancing opini)' },
              { label: 'Personal Storytelling', value: 'Storytelling (Bercerita pengalaman pribadi)' },
              { label: 'Long Educational Thread', value: 'Utasan Panjang (Edukasi mendalam)' }
            ]" 
          />
          
          <Select 
            v-model="aiProvider" 
            label="AI Provider" 
            :options="[
              { label: 'Groq (Llama) - Fast', value: 'groq' },
              { label: 'Gemini (Google) - Smart', value: 'gemini' }
            ]" 
            @update:model-value="handleProviderChange"
          />
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <Select 
            v-model="aiModel" 
            label="Specific Model" 
            :options="availableModels"
            :disabled="isLoadingModels || availableModels.length === 0"
            :placeholder="isLoadingModels ? 'Loading models...' : 'Select a model'"
          />
          <div class="flex items-end pb-2">
             <div class="flex items-center gap-2 px-3 py-1.5 rounded-lg border text-xs font-bold transition-colors"
              :style="isUsingOwnKey ? 'border-color: var(--success); color: var(--success);' : (aiCredits > 0 ? 'border-color: var(--accent); color: var(--accent);' : 'border-color: var(--danger); color: var(--danger);')">
              <span class="w-2 h-2 rounded-full" :style="isUsingOwnKey ? 'background: var(--success);' : (aiCredits > 0 ? 'background: var(--accent);' : 'background: var(--danger);')"></span>
              <span v-if="isUsingOwnKey">Unlimited (Own Key)</span>
              <span v-else-if="aiCredits > 0">{{ aiCredits }} Credits Left</span>
              <span v-else>Out of Credits</span>
            </div>
          </div>
        </div>

        <div class="flex justify-end pt-2">
          <Button
            @click="generateRepurpose"
            :disabled="isGenerating || !sourceText || !aiModel || (!isUsingOwnKey && aiCredits <= 0)"
            :loading="isGenerating"
          >
            {{ isGenerating ? 'Repurposing...' : 'Repurpose Text' }}
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
          <Badge variant="accent">Variation {{ idx + 1 }}</Badge>
          <button
            @click="copyText(item.content)"
            class="text-xs font-bold theme-text-muted hover:theme-text transition"
          >
            Copy Text
          </button>
        </div>
        <p class="text-sm whitespace-pre-wrap leading-relaxed">{{ item.content }}</p>

        <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity backdrop-blur-sm" style="background: color-mix(in srgb, var(--bg-primary) 90%, transparent);">
          <Button @click="sendToComposer(item.content)">Send to Composer</Button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { supabase } from '../lib/supabase'
import { useNotify } from '../composables/useNotify'
import { Card, Button, Textarea, Badge, Select } from '../components/ui'

const router = useRouter()
const { showToast } = useNotify()

const sourceText = ref('')
const repurposeAngle = ref('Format Listicle (Poin-poin praktis)')
const isGenerating = ref(false)
const results = ref<any[]>([])

const currentAccountId = ref<string | null>(null)
const aiCredits = ref(20)
const customGeminiKey = ref('')
const customGroqKey = ref('')

const aiProvider = ref('groq')
const aiModel = ref('')
const availableModels = ref<{id: string, name: string}[]>([])
const isLoadingModels = ref(false)

const recommendations = ref<any[]>([])

const isUsingOwnKey = computed(() => {
  if (aiProvider.value === 'groq') return !!customGroqKey.value
  return !!customGeminiKey.value
})

function applyRecommendation(rec: any) {
  sourceText.value = rec.text
  showToast('Post moved to text editor.', 'info')
  // Scroll ke form input
  window.scrollTo({ top: 400, behavior: 'smooth' })
}

async function fetchRecommendations() {
  if (!currentAccountId.value) return
  try {
    const res = await fetch(`https://threads-automation-production-53ad.up.railway.app/api/v1/rag/recommendations/${currentAccountId.value}`)
    const data = await res.json()
    if (data.recommendations) recommendations.value = data.recommendations
  } catch (err) {
    console.error('Failed to load recommendations', err)
  }
}

async function fetchModels() {
  if (!currentAccountId.value) return
  isLoadingModels.value = true
  try {
    const res = await fetch(`https://threads-automation-production-53ad.up.railway.app/api/v1/rag/models/${aiProvider.value}?account_id=${currentAccountId.value}`)
    const data = await res.json()
    if (data.models && data.models.length > 0) {
      availableModels.value = data.models.map((m: any) => ({ label: m.name, value: m.id }))
      aiModel.value = data.models[0].id
    } else {
      availableModels.value = []
      aiModel.value = ''
    }
  } catch (err) {
    console.error('Failed to load models', err)
  } finally {
    isLoadingModels.value = false
  }
}

function handleProviderChange() {
  fetchModels()
}

async function generateRepurpose() {
  if (!sourceText.value || !aiModel.value) return
  isGenerating.value = true
  results.value = []

  const controller = new AbortController()
  const timeoutId = setTimeout(() => controller.abort(), 45000)

  try {
    const res = await fetch('https://threads-automation-production-53ad.up.railway.app/api/v1/rag/repurpose', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      signal: controller.signal,
      body: JSON.stringify({
        account_id: currentAccountId.value,
        source_text: sourceText.value,
        angle: repurposeAngle.value,
        provider: aiProvider.value,
        model_name: aiModel.value
      })
    })

    clearTimeout(timeoutId)

    const data = await res.json()
    if (!res.ok) throw new Error(data.detail)

    results.value = data.options || []
    if (!isUsingOwnKey.value) aiCredits.value = Math.max(0, aiCredits.value - 1)
    showToast('Successfully repurposed content!', 'success')
  } catch (err: any) {
    if (err.name === 'AbortError') {
      showToast('Request timed out. Please try again.', 'error')
    } else {
      showToast('Failed: ' + err.message, 'error')
    }
  } finally {
    isGenerating.value = false
  }
}

function copyText(text: string) {
  navigator.clipboard.writeText(text)
  showToast('Copied to clipboard!', 'info')
}

function sendToComposer(text: string) {
  localStorage.setItem('draft_repurpose', text)
  router.push('/content/create')
}

onMounted(async () => {
  const { data: { user } } = await supabase.auth.getUser()
  if (user) {
    const { data: acc } = await supabase.schema('threads').from('threads_accounts').select('id, ai_credits, custom_gemini_key, custom_groq_key, ai_provider').eq('user_id', user.id).maybeSingle()
    if (acc) {
      currentAccountId.value = acc.id
      aiCredits.value = acc.ai_credits ?? 20
      customGeminiKey.value = acc.custom_gemini_key || ''
      customGroqKey.value = acc.custom_groq_key || ''
      if (acc.ai_provider) aiProvider.value = acc.ai_provider
      
      // Load model & rekomendasi secara paralel
      await Promise.all([fetchModels(), fetchRecommendations()])
    }
  }
})
</script>
