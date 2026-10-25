<template>
  <div class="space-y-8 relative">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Composer</h1>
      <p class="text-sm theme-text-muted mt-1">Write or auto-generate drafts with AI, split threads, and schedule posts.</p>
    </div>

    <Card>
      <template #header>
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full animate-pulse" style="background: var(--accent);"></span>
            <h2 class="text-xs font-bold uppercase tracking-wide">AI Content Planner</h2>
          </div>
          <button @click="showAiPanel = !showAiPanel" class="text-xs font-bold theme-text hover:underline">
            {{ showAiPanel ? 'Hide Panel' : 'Auto-Generate Drafts' }}
          </button>
        </div>
      </template>

      <div v-if="showAiPanel" class="space-y-4">
        <!-- ROW 1: TOPIC & TONE -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <Input v-model="aiTopic" label="Topic / Short Idea" placeholder="Enter a short topic..." />
          <Select 
            v-model="aiTone" 
            label="Tone / Style" 
            :options="[
              { label: 'Educational & Insight', value: 'Educational & Casual Insight' },
              { label: 'Storytelling', value: 'Personal Storytelling' },
              { label: 'Hot Take / Opinion', value: 'Hot Take & Discussion' },
              { label: 'Q&A / Spark Discussion', value: 'Question / Q&A' },
              { label: 'Custom / Free Instruction', value: 'Custom Prompt' }
            ]" 
          />
        </div>

        <!-- ROW 2: PROVIDER & MODEL (DROPDOWN REUSABLE) -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 p-3 rounded-lg border theme-border" style="background: var(--bg-sec);">
          <Select 
            v-model="aiProvider" 
            label="AI Provider" 
            :options="[
              { label: 'Groq (Llama) - Fast', value: 'groq' },
              { label: 'Gemini (Google) - Smart', value: 'gemini' }
            ]" 
            @update:model-value="handleProviderChange"
          />
          
          <Select 
            v-model="aiModel" 
            label="Specific Model" 
            :options="availableModels"
            :disabled="isLoadingModels || availableModels.length === 0"
            :placeholder="isLoadingModels ? 'Loading models...' : 'Select a model'"
          />
        </div>

        <!-- CUSTOM PROMPT -->
        <div v-if="aiTone === 'Custom Prompt'">
          <Textarea v-model="customPrompt" label="Custom Instruction" :rows="3" placeholder="Example: Write in casual English..." />
        </div>

        <!-- ACTION BUTTONS -->
        <div class="flex justify-end items-center gap-4 mt-2">
          <div class="flex items-center gap-2 px-3 py-1.5 rounded-lg border text-xs font-bold transition-colors"
            :style="hasCustomKey ? 'border-color: var(--success); color: var(--success);' : (aiCredits > 0 ? 'border-color: var(--accent); color: var(--accent);' : 'border-color: var(--danger); color: var(--danger);')">
            <span class="w-2 h-2 rounded-full" :style="hasCustomKey ? 'background: var(--success);' : (aiCredits > 0 ? 'background: var(--accent);' : 'background: var(--danger);')"></span>
            <span v-if="hasCustomKey">Unlimited (Own Key)</span>
            <span v-else-if="aiCredits > 0">{{ aiCredits }} Credits Left</span>
            <span v-else>Out of Credits</span>
          </div>

          <Button @click="generateAiIdeas" :disabled="isGenerating || !aiTopic || (aiTone === 'Custom Prompt' && !customPrompt) || (!hasCustomKey && aiCredits <= 0) || !aiModel" :loading="isGenerating">
            {{ isGenerating ? 'Planning Content...' : 'Generate 3-Day Plan' }}
          </Button>
        </div>

        <div v-if="aiResults.length > 0" class="grid grid-cols-1 md:grid-cols-3 gap-3 pt-3 divider">
          <div v-for="item in aiResults" :key="item.id" class="card card-hover p-4 flex flex-col justify-between space-y-3">
            <div class="space-y-1.5">
              <Badge variant="accent">{{ item.title }}</Badge>
              <p class="text-xs whitespace-pre-wrap leading-relaxed">{{ item.content }}</p>
            </div>
            <Button variant="secondary" size="sm" @click="applyAiDraft(item.content)">Use This Draft</Button>
          </div>
        </div>
      </div>
    </Card>

    <Card>
      <div class="flex justify-between items-center mb-4">
        <span class="text-xs font-bold uppercase tracking-wide">Main Post Text</span>
        <div class="flex items-center gap-2">
          <Badge v-if="postText.length > 500" variant="accent">Auto-Split ({{ threadParts.length }} Parts)</Badge>
          <span class="text-xs font-medium" :class="postText.length > 500 ? 'theme-text font-bold' : 'theme-text-muted'">{{ postText.length }} Chars</span>
        </div>
      </div>

      <Textarea v-model="postText" :rows="6" placeholder="Write your draft here..." />

      <div v-if="threadParts.length > 1" class="space-y-3 pt-3 divider mt-4">
        <span class="text-xs font-bold uppercase tracking-wide">Thread Preview ({{ threadParts.length }} Parts)</span>
        <div v-for="(part, idx) in threadParts" :key="idx" class="p-3 rounded-xl theme-bg-sec border theme-border space-y-1.5">
          <div class="flex justify-between items-center text-[11px] font-bold theme-text-muted">
            <span>Part {{ idx + 1 }} of {{ threadParts.length }}</span>
            <span :class="part.length > 500 ? 'font-bold' : ''" :style="part.length > 500 ? 'color: var(--danger);' : ''">{{ part.length }} / 500</span>
          </div>
          <textarea v-model="threadParts[idx]" rows="3" class="textarea text-xs"></textarea>
        </div>
      </div>

      <div class="flex flex-wrap items-center gap-3 mt-4">
        <Button variant="secondary" @click="checkScore" :disabled="isChecking || !postText" :loading="isChecking">
          {{ isChecking ? 'Analyzing...' : 'Check AI Score' }}
        </Button>                                                  
        <div class="flex-1 flex justify-end items-center gap-3 flex-wrap">
          <BestTimeChip @apply="(val) => scheduledDate = val" />
          <input v-model="scheduledDate" type="datetime-local" class="input" style="width: auto;" />
          <Button @click="schedulePost" :disabled="isSaving" :loading="isSaving">
            {{ isSaving ? 'Processing...' : (threadParts.length > 1 ? 'Schedule ' + threadParts.length + ' Threads' : 'Schedule Post') }}
          </Button>
        </div>
      </div>
    </Card>                                                        
    
    <Teleport to="body">                                                 
      <div v-if="scoreResult" class="fixed inset-0 backdrop-blur-sm z-[100] flex items-center justify-center p-4" style="background: rgba(0,0,0,0.6);">                                                          
        <div class="card max-w-md w-full p-6 space-y-4">
          <div class="flex justify-between items-center pb-3 divider">
            <h3 class="text-sm font-bold uppercase tracking-wide">AI Score Analysis</h3>
            <Badge variant="accent">{{ scoreResult.score }} / 100</Badge>
          </div>
          <div class="space-y-1">
            <label class="label">Feedback Notes</label>
            <p class="text-xs leading-relaxed theme-bg-sec p-3.5 rounded-xl border theme-border">{{ scoreResult.feedback }}</p>
          </div>
          <div class="flex justify-end pt-2"><Button @click="scoreResult = null">Close</Button></div>                                                           
        </div>
      </div>                                                           
    </Teleport>
  </div>
</template>

<script setup lang="ts">                                           
import { ref, watch, onMounted } from 'vue'
import { supabase } from '../lib/supabase'                         
import { useNotify } from '../composables/useNotify'
import BestTimeChip from '../components/BestTimeChip.vue'
import { Card, Button, Input, Textarea, Badge, Select } from '../components/ui'
                                                                  
const { showToast } = useNotify()
                                                                  
const postText = ref('')
const threadParts = ref<string[]>([])
const scheduledDate = ref('')
const isSaving = ref(false)
const isChecking = ref(false)                                      
const showAiPanel = ref(true)
const aiTopic = ref('')
const aiTone = ref('Educational & Casual Insight')
const customPrompt = ref('')
const isGenerating = ref(false)
const aiResults = ref<any[]>([])
const scoreResult = ref<any>(null)                                 
const aiCredits = ref(20)
const hasCustomKey = ref(false)
const currentAccountId = ref<string | null>(null)

const aiProvider = ref('groq')
const aiModel = ref('')
const availableModels = ref<{id: string, name: string}[]>([])
const isLoadingModels = ref(false)

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
      // Format data dari backend biar sesuai sama props options di komponen Select
      availableModels.value = data.models.map((m: any) => ({ label: m.name, value: m.id }))
      aiModel.value = data.models[0].id
    } else {
      availableModels.value = []
      aiModel.value = ''
    }
  } catch (err) {
    console.error('Failed to load models', err)
    showToast('Failed to load models for this provider.', 'error')
  } finally {
    isLoadingModels.value = false
  }
}

function handleProviderChange() {
  fetchModels()
}

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
      throw new Error(errData.detail || 'Failed to process draft on backend')
    }
                                                                       
    const resData = await response.json()
    if (resData?.options) {                                              
      aiResults.value = resData.options
      if (!hasCustomKey.value) aiCredits.value = Math.max(0, aiCredits.value - 1)
      showToast('3-Day Content Plan generated successfully!', 'success')
    }                                                                
  } catch (err: any) {
    if (err.name === 'AbortError') {
      showToast('Request timed out. Please try again.', 'error')
    } else {
      showToast('AI Generator failed: ' + err.message, 'error')
    }
  } finally {
    isGenerating.value = false                                       
  }
}

function applyAiDraft(content: string) {
  postText.value = content
  showToast('AI Draft applied to Composer.', 'info')
}
                                                                   
async function checkScore() {
  isChecking.value = true
  try {
    const { data, error } = await supabase.functions.invoke('score-draft', { body: { text: postText.value } })
    if (error) throw error
    if (data?.error) throw new Error(data.error)
    scoreResult.value = { score: data?.score ?? 80, feedback: data?.feedback ?? 'Text looks good.' }
  } catch (err: any) {
    showToast('AI Analysis failed: ' + err.message, 'error')           
  } finally { isChecking.value = false }
}

async function schedulePost() {
  if (!postText.value.trim()) {
    showToast('Please write a post first.', 'error')
    return
  }
  if (!scheduledDate.value) {
    showToast('Please select a schedule time.', 'error')
    return
  }
  
  const scheduleTime = new Date(scheduledDate.value).getTime()
  if (isNaN(scheduleTime)) {
    showToast('Invalid date format. Please pick a valid date.', 'error')
    return
  }
  if (scheduleTime <= Date.now()) { 
    showToast('Schedule time must be in the future.', 'error')
    return 
  }

  isSaving.value = true

  try {
    let targetAccountId = currentAccountId.value
    if (!targetAccountId) {
      const { data: { user } } = await supabase.auth.getUser()
      if (!user) throw new Error('User not authenticated')    
      const { data: account } = await supabase.schema('threads').from('threads_accounts').select('id').eq('user_id', user.id).maybeSingle()
      if (!account) throw new Error('Threads account not connected')
      targetAccountId = account.id
      currentAccountId.value = targetAccountId
    }

    const partsToSchedule = threadParts.value.length > 0 ? threadParts.value : [postText.value]

    let parentId = null
    for (let i = 0; i < partsToSchedule.length; i++) {                 
      const { data: insertedPart, error: insertError } = await supabase.schema('threads').from('scheduled_posts').insert({
        account_id: targetAccountId, 
        text: partsToSchedule[i], 
        scheduled_for: new Date(scheduledDate.value).toISOString(),
        status: 'scheduled', 
        parent_id: parentId, 
        sequence_number: i + 1, 
        idempotency_key: crypto.randomUUID()                             
      }).select().single()                                                  
      
      if (insertError) throw insertError                                 
      if (i === 0) { parentId = insertedPart.id }
    }                                                              
    
    showToast(`Successfully scheduled ${partsToSchedule.length} thread(s)!`, 'success')
    postText.value = ''
    localStorage.removeItem('ixiera_draft_text')                   
    
    const d = new Date()                                               
    d.setHours(d.getHours() + 1); d.setMinutes(d.getMinutes() - d.getTimezoneOffset())
    scheduledDate.value = d.toISOString().slice(0, 16)
    localStorage.setItem('ixiera_draft_time', scheduledDate.value)
  } catch (err: any) {
    showToast('Failed to schedule: ' + err.message, 'error')
  } finally { 
    isSaving.value = false 
  }
}

onMounted(async () => {
  const { data: { user } } = await supabase.auth.getUser()
  if (user) {
    const { data: acc } = await supabase.schema('threads').from('threads_accounts').select('id, ai_credits, custom_gemini_key, custom_groq_key, ai_provider').eq('user_id', user.id).maybeSingle()
    if (acc) {
      currentAccountId.value = acc.id
      aiCredits.value = acc.ai_credits ?? 20
      hasCustomKey.value = !!(acc.custom_gemini_key || acc.custom_groq_key)
      if (acc.ai_provider) aiProvider.value = acc.ai_provider
      
      await fetchModels()
    }
  }

  const savedRepurpose = localStorage.getItem('draft_repurpose')
  if (savedRepurpose) {
    postText.value = savedRepurpose
    localStorage.removeItem('draft_repurpose')
  } else {
    const localDraftText = localStorage.getItem('ixiera_draft_text')
    if (localDraftText) { postText.value = localDraftText }
  }

  const localDraftTime = localStorage.getItem('ixiera_draft_time')
  if (localDraftTime) {
    scheduledDate.value = localDraftTime
  } else {
    const d = new Date()
    d.setHours(d.getHours() + 1)
    d.setMinutes(d.getMinutes() - d.getTimezoneOffset())
    scheduledDate.value = d.toISOString().slice(0, 16)
  }
})
</script>
