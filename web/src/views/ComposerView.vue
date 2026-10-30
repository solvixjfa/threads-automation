<template>
  <div class="space-y-8 relative">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">{{ $t('content.composer.title') }}</h1>
      <p class="text-sm theme-text-muted mt-1">{{ $t('content.composer.subtitle') }}</p>
    </div>

    <Card>
      <template #header>
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full animate-pulse" style="background: var(--accent);"></span>
            <h2 class="text-xs font-bold uppercase tracking-wide">{{ $t('content.composer.ai_planner') }}</h2>
          </div>
          <button @click="showAiPanel = !showAiPanel" class="text-xs font-bold theme-text hover:underline">
            {{ showAiPanel ? $t('content.composer.hide_panel') : $t('content.composer.auto_generate') }}
          </button>
        </div>
      </template>

      <div v-if="showAiPanel" class="space-y-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <Input v-model="aiTopic" :label="$t('content.composer.topic')" :placeholder="$t('content.composer.topic_ph')" />
          <Select 
            v-model="aiTone" 
            :label="$t('content.composer.tone')" 
            :options="toneOptions" 
          />
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 p-3 rounded-lg border theme-border" style="background: var(--bg-sec);">
          <Select 
            v-model="aiProvider" 
            :label="$t('content.composer.provider')" 
            :options="[{label: 'Groq (Fast)', value: 'groq'}, {label: 'Gemini (Smart)', value: 'gemini'}]" 
            @update:model-value="handleProviderChange"
          />
          <Select 
            v-model="aiModel" 
            :label="$t('content.composer.model')" 
            :options="availableModels"
            :disabled="isLoadingModels || availableModels.length === 0"
            :placeholder="isLoadingModels ? 'Loading...' : 'Select a model'"
          />
        </div>

        <div v-if="aiTone === 'Custom Prompt'">
          <Textarea v-model="customPrompt" :label="$t('content.composer.custom_instruction')" :rows="3" :placeholder="$t('content.composer.custom_ph')" />
        </div>

        <div class="flex justify-end items-center gap-4 mt-2">
          <div class="flex items-center gap-2 px-3 py-1.5 rounded-lg border text-xs font-bold transition-colors"
            :style="isUsingOwnKey ? 'border-color: var(--success); color: var(--success);' : (aiCredits > 0 ? 'border-color: var(--accent); color: var(--accent);' : 'border-color: var(--danger); color: var(--danger);')">
            <span class="w-2 h-2 rounded-full" :style="isUsingOwnKey ? 'background: var(--success);' : (aiCredits > 0 ? 'background: var(--accent);' : 'background: var(--danger);')"></span>
            <span v-if="isUsingOwnKey">Unlimited (Own Key)</span>
            <span v-else-if="aiCredits > 0">{{ aiCredits }} Credits</span>
            <span v-else>Out of Credits</span>
          </div>

          <Button @click="generateAiIdeas" :disabled="isGenerating || !aiTopic || (aiTone === 'Custom Prompt' && !customPrompt) || (!isUsingOwnKey && aiCredits <= 0) || !aiModel" :loading="isGenerating">
            {{ isGenerating ? $t('content.composer.generating') : $t('content.composer.generate_plan') }}
          </Button>
        </div>

        <div v-if="aiResults.length > 0" class="grid grid-cols-1 md:grid-cols-3 gap-3 pt-3 divider">
          <!-- FIX: Tambahin min-w-0 biar grid gak jebol -->
          <div v-for="item in aiResults" :key="item.id" class="card card-hover p-4 flex flex-col justify-between space-y-3 min-w-0">
            <div class="space-y-2 min-w-0">
              <!-- FIX: Ganti Badge jadi div dengan break-words -->
              <div class="inline-block px-2.5 py-1 rounded-md text-[10px] font-bold uppercase tracking-wider bg-[var(--accent)] text-white leading-tight break-words whitespace-normal">
                {{ item.title }}
              </div>
              <!-- FIX: Tambahin break-words di paragraf -->
              <p class="text-xs whitespace-pre-wrap leading-relaxed break-words">{{ item.content }}</p>
            </div>
            <Button variant="secondary" size="sm" @click="applyAiDraft(item.content)">Use This Draft</Button>
          </div>
        </div>
      </div>
    </Card>

    <Card>
      <div class="flex justify-between items-center mb-4">
        <span class="text-xs font-bold uppercase tracking-wide">{{ $t('content.composer.main_text') }}</span>
        <div class="flex items-center gap-2">
          <Badge v-if="postText.length > 500" variant="accent">Auto-Split ({{ threadParts.length }})</Badge>
          <span class="text-xs font-medium" :class="postText.length > 500 ? 'theme-text font-bold' : 'theme-text-muted'">{{ postText.length }} {{ $t('content.composer.chars') }}</span>
        </div>
      </div>

      <Textarea v-model="postText" :rows="6" :placeholder="$t('content.composer.draft_ph')" />

      <div v-if="threadParts.length > 1" class="space-y-3 pt-3 divider mt-4">
        <span class="text-xs font-bold uppercase tracking-wide">{{ $t('content.composer.split_preview') }} ({{ threadParts.length }})</span>
        <div v-for="(part, idx) in threadParts" :key="idx" class="p-3 rounded-xl theme-bg-sec border theme-border space-y-1.5">
          <div class="flex justify-between items-center text-[11px] font-bold theme-text-muted">
            <span>Part {{ idx + 1 }} / {{ threadParts.length }}</span>
            <span :class="part.length > 500 ? 'font-bold' : ''" :style="part.length > 500 ? 'color: var(--danger);' : ''">{{ part.length }} / 500</span>
          </div>
          <textarea v-model="threadParts[idx]" rows="3" class="textarea text-xs"></textarea>
        </div>
      </div>

      <div class="flex flex-wrap items-center gap-3 mt-4">
        <Button variant="secondary" @click="checkScore" :disabled="isChecking || !postText">
          {{ isChecking ? $t('content.composer.checking') : $t('content.composer.check_score') }}
        </Button>                                                  
        <div class="flex-1 flex justify-end items-center gap-3 flex-wrap">
          <BestTimeChip @apply="(val) => scheduledDate = val" />
          <input v-model="scheduledDate" type="datetime-local" class="input" style="width: auto;" />
          <Button @click="schedulePost" :disabled="isSaving" :loading="isSaving">
            {{ isSaving ? $t('content.composer.saving') : (threadParts.length > 1 ? $t('content.composer.schedule_threads', { n: threadParts.length }) : $t('content.composer.schedule')) }}
          </Button>
        </div>
      </div>
    </Card>                                                        
    
    <Teleport to="body">                                                 
      <div v-if="scoreResult" class="fixed inset-0 backdrop-blur-sm z-[100] flex items-center justify-center p-4" style="background: rgba(0,0,0,0.6);">                                                          
        <div class="card max-w-md w-full p-6 space-y-4 shadow-2xl" style="background: var(--bg);">
          <div class="flex justify-between items-center pb-3 divider">
            <h3 class="text-sm font-bold uppercase tracking-wide theme-text">{{ $t('content.composer.modal_title') }}</h3>
            <Badge :variant="scoreResult.score >= 80 ? 'accent' : (scoreResult.score >= 60 ? 'default' : 'danger')">
              {{ scoreResult.score }} / 100
            </Badge>
          </div>
          
          <div class="space-y-2">
            <label class="label theme-text-muted">{{ scoreResult.isAi ? 'Deep AI Feedback' : 'Quick Feedback' }}</label>
            <ul class="text-xs leading-relaxed theme-bg-sec p-3.5 rounded-xl border theme-border space-y-1.5 list-disc pl-6 theme-text">
              <li v-for="(fb, i) in scoreResult.feedback" :key="i">{{ fb }}</li>
            </ul>
          </div>

          <div v-if="!scoreResult.isAi" class="pt-2 border-t theme-border flex justify-between items-center">
            <span class="text-[10px] theme-text-muted">Want deeper analysis?</span>
            <Button 
              @click="deepAiScore" 
              :disabled="isDeepScoring || (!isUsingOwnKey && aiCredits <= 0)" 
              :loading="isDeepScoring"
              size="sm"
            >
              {{ isDeepScoring ? $t('content.composer.modal_deep_ai_loading') : $t('content.composer.modal_deep_ai') }}
            </Button>
          </div>

          <div class="flex justify-end pt-2">
            <Button variant="secondary" @click="scoreResult = null">{{ $t('content.composer.modal_close') }}</Button>
          </div>                                                           
        </div>
      </div>                                                           
    </Teleport>
  </div>
</template>

<script setup lang="ts">                                           
import { ref, watch, onMounted, computed } from 'vue'
import { supabase } from '../lib/supabase'                         
import { useNotify } from '../composables/useNotify'
import { useI18n } from 'vue-i18n'
import BestTimeChip from '../components/BestTimeChip.vue'
import { Card, Button, Input, Textarea, Badge, Select } from '../components/ui'
                                                                  
const { showToast } = useNotify()
const { t } = useI18n()
                                                                  
const postText = ref('')
const threadParts = ref<string[]>([])
const scheduledDate = ref('')
const isSaving = ref(false)
const isChecking = ref(false)   
const isDeepScoring = ref(false)                                   
const showAiPanel = ref(true)
const aiTopic = ref('')
const aiTone = ref('Educational & Casual Insight')
const customPrompt = ref('')
const isGenerating = ref(false)
const aiResults = ref<any[]>([])
const scoreResult = ref<any>(null)                                 
const aiCredits = ref(20)
const currentAccountId = ref<string | null>(null)

const aiProvider = ref('groq')
const aiModel = ref('')
const availableModels = ref<{id: string, name: string}[]>([])
const isLoadingModels = ref(false)

const customGeminiKey = ref('')
const customGroqKey = ref('')

const toneOptions = computed(() => [
  { label: t('content.composer.tones.edu'), value: 'Educational & Casual Insight' },
  { label: t('content.composer.tones.story'), value: 'Personal Storytelling' },
  { label: t('content.composer.tones.hot_take'), value: 'Hot Take & Discussion' },
  { label: t('content.composer.tones.qa'), value: 'Question / Q&A' },
  { label: t('content.composer.tones.custom'), value: 'Custom Prompt' },
])

const isUsingOwnKey = computed(() => {
  if (aiProvider.value === 'groq') return !!customGroqKey.value
  return !!customGeminiKey.value
})

function splitTextIntoParts(text: string, maxLen = 480): string[] {  
  if (text.length <= maxLen) return [text]
  const paragraphs = text.split(/\n+/)
  const parts: string[] = []
  let current = ''                                                   
  for (const p of paragraphs) {
    if ((current + '\n\n' + p).trim().length <= maxLen) {                
      current = current ? current + '\n\n' + p : p
    } else {
      if (current) parts.push(current.trim())
      if (p.length <= maxLen) { current = p } 
      else {                                                             
        const sentences = p.match(/[^.!?]+[.!?]+/g) || [p]
        for (const s of sentences) {
          if ((current + ' ' + s).trim().length <= maxLen) { current = current ? current + ' ' + s : s } 
          else {
            if (current) parts.push(current.trim())                            
            current = s
          }
        }
      }
    }
  }                                                                  
  if (current) parts.push(current.trim())
  return parts
}                                                                  

function handleTextChange() { threadParts.value = splitTextIntoParts(postText.value) }
                                                                   
watch(postText, (newVal) => {
  handleTextChange()
  localStorage.setItem('ixiera_draft_text', newVal)                
})

watch(scheduledDate, (newVal) => { localStorage.setItem('ixiera_draft_time', newVal) })                                                                 

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
  } catch (err) { console.error(err) } finally { isLoadingModels.value = false }
}

function handleProviderChange() { fetchModels() }

async function generateAiIdeas() {
  if (!aiTopic.value || !aiModel.value) return
  isGenerating.value = true
  aiResults.value = []                                             
  
  const controller = new AbortController()
  const timeoutId = setTimeout(() => controller.abort(), 45000)

  try {
    const response = await fetch('https://threads-automation-production-53ad.up.railway.app/api/v1/rag/generate-post', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      signal: controller.signal,
      body: JSON.stringify({ 
        account_id: currentAccountId.value, 
        topic: aiTopic.value, 
        tone: aiTone.value, 
        provider: aiProvider.value,
        model_name: aiModel.value,
        custom_prompt: aiTone.value === 'Custom Prompt' ? customPrompt.value : undefined 
      })
    })

    clearTimeout(timeoutId)

    if (!response.ok) {
      const errData = await response.json()
      throw new Error(errData.detail || 'Failed to process draft')
    }
                                                                       
    const resData = await response.json()
    if (resData?.options) {                                              
      aiResults.value = resData.options
      if (!isUsingOwnKey.value) aiCredits.value = Math.max(0, aiCredits.value - 1)
      showToast('Content Plan generated!', 'success')
    }                                                                
  } catch (err: any) {
    if (err.name === 'AbortError') showToast('Request timed out.', 'error')
    else showToast('AI Generator failed: ' + err.message, 'error')
  } finally { isGenerating.value = false }
}

function applyAiDraft(content: string) {
  postText.value = content
  showToast('AI Draft applied.', 'info')
}

function checkScore() {
  if (!postText.value.trim()) return
  isChecking.value = true
  setTimeout(() => {
    const text = postText.value.trim()
    let score = 50
    let feedback: string[] = []

    if (text.length < 50) feedback.push("Post is too short. Add more context.")
    else if (text.length > 500) { score += 10; feedback.push("Post is long. It will be split into a thread.") }
    else { score += 20; feedback.push("Optimal character length.") }

    const hookWords = ['?', 'gimana', 'menurut', 'setuju', 'pendapat', 'how', 'what', 'agree', 'think']
    if (hookWords.some(w => text.toLowerCase().includes(w))) {
      score += 15; feedback.push("Great hook! Inviting readers to reply.")
    } else feedback.push("Consider adding a question to spark discussion.")

    if (text.includes('\n')) {
      score += 10; feedback.push("Good use of line breaks.")
    } else feedback.push("Add line breaks to make it easier to read.")

    const hashtags = text.match(/#[\w]+/g) || []
    if (hashtags.length > 3) { score -= 10; feedback.push(`Too many hashtags (${hashtags.length}). Max 3.`) }

    score = Math.max(0, Math.min(100, score))
    if (score >= 80) feedback.unshift("This post looks solid!")
    scoreResult.value = { score, feedback, isAi: false }
    isChecking.value = false
  }, 600)
}

async function deepAiScore() {
  if (!postText.value.trim() || !aiModel.value) return
  isDeepScoring.value = true
  try {
    const res = await fetch('https://threads-automation-production-53ad.up.railway.app/api/v1/rag/score-draft', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ account_id: currentAccountId.value, text: postText.value, provider: aiProvider.value, model_name: aiModel.value })
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.detail)

    scoreResult.value = { score: data.data.score, feedback: data.data.feedback, isAi: true }
    if (!isUsingOwnKey.value) aiCredits.value = Math.max(0, aiCredits.value - 1)
    showToast('Deep AI Analysis complete!', 'success')
  } catch (err: any) {
    showToast('Deep AI failed: ' + err.message, 'error')
  } finally { isDeepScoring.value = false }
}

async function schedulePost() {
  if (!postText.value.trim()) { showToast('Write a post first.', 'error'); return }
  if (!scheduledDate.value) { showToast('Select a schedule time.', 'error'); return }
  
  const localDate = new Date(scheduledDate.value)
  if (isNaN(localDate.getTime())) { showToast('Invalid date format.', 'error'); return }
  if (localDate.getTime() <= Date.now()) { showToast('Schedule must be in the future.', 'error'); return }

  isSaving.value = true
  try {
    let targetAccountId = currentAccountId.value
    if (!targetAccountId) {
      const { data: { user } } = await supabase.auth.getUser()
      if (!user) throw new Error('Not authenticated')    
      const { data: account } = await supabase.schema('threads').from('threads_accounts').select('id').eq('user_id', user.id).maybeSingle()
      if (!account) throw new Error('Threads account not connected')
      targetAccountId = account.id
      currentAccountId.value = targetAccountId
    }

    const partsToSchedule = threadParts.value.length > 0 ? threadParts.value : [postText.value]
    let parentId = null
    for (let i = 0; i < partsToSchedule.length; i++) {                 
      const { data: insertedPart, error: insertError } = await supabase.schema('threads').from('scheduled_posts').insert({
        account_id: targetAccountId, text: partsToSchedule[i], scheduled_for: localDate.toISOString(),
        status: 'scheduled', parent_id: parentId, sequence_number: i + 1, idempotency_key: crypto.randomUUID()                             
      }).select().single()                                                  
      if (insertError) throw insertError                                 
      if (i === 0) parentId = insertedPart.id
    }                                                              
    
    showToast(`Scheduled ${partsToSchedule.length} thread(s)!`, 'success')
    postText.value = ''
    localStorage.removeItem('ixiera_draft_text')                   
    
    const nextHour = new Date()
    nextHour.setHours(nextHour.getHours() + 1)
    nextHour.setMinutes(0)
    const tzOffset = nextHour.getTimezoneOffset() * 60000
    scheduledDate.value = (new Date(nextHour.getTime() - tzOffset)).toISOString().slice(0, 16)
    localStorage.setItem('ixiera_draft_time', scheduledDate.value)
  } catch (err: any) {
    showToast('Failed to schedule: ' + err.message, 'error')
  } finally { isSaving.value = false }
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
      await fetchModels()
    }
  }

  const savedRepurpose = localStorage.getItem('draft_repurpose')
  if (savedRepurpose) { postText.value = savedRepurpose; localStorage.removeItem('draft_repurpose') }
  else { const localDraftText = localStorage.getItem('ixiera_draft_text'); if (localDraftText) postText.value = localDraftText }

  const localDraftTime = localStorage.getItem('ixiera_draft_time')
  if (localDraftTime) scheduledDate.value = localDraftTime
  else {
    const d = new Date()
    d.setHours(d.getHours() + 1); d.setMinutes(0)
    const tzOffset = d.getTimezoneOffset() * 60000
    scheduledDate.value = (new Date(d.getTime() - tzOffset)).toISOString().slice(0, 16)
  }
})
</script>
