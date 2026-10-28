<template>
  <Card>
    <template #header>
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-sm font-bold">Reply Strategy</h2>
          <p class="text-xs theme-text-muted mt-0.5">Control how the AI handles each comment category.</p>
        </div>
        <Button @click="save" :disabled="saving" :loading="saving" size="sm">
          {{ saving ? 'Saving...' : 'Save Settings' }}
        </Button>
      </div>
    </template>

    <div v-if="loading" class="space-y-3">
      <div v-for="i in 5" :key="i" class="h-20 skeleton"></div>
    </div>

    <div v-else class="space-y-4">
      <div v-for="cat in categories" :key="cat.value" class="p-4 rounded-xl theme-bg-sec border theme-border space-y-3">
        <!-- HEADER KATEGORI & DROPDOWN AKSI -->
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-3">
          <div class="min-w-0 flex-1">
            <div class="flex items-center gap-2 flex-wrap">
              <span class="text-sm font-bold">{{ cat.label }}</span>
              <Badge v-if="!state[cat.value].enabled" variant="danger">Disabled</Badge>
            </div>
            <p class="text-xs theme-text-muted mt-0.5">{{ cat.description }}</p>
          </div>
          
          <div class="flex items-center gap-3 shrink-0">
            <div class="w-40">
              <Select 
                v-model="state[cat.value].action" 
                :options="[
                  { label: 'Auto AI', value: 'llm' },
                  { label: 'Use Template', value: 'template' },
                  { label: 'Ignore / Skip', value: 'skip' }
                ]" 
                :disabled="!state[cat.value].enabled"
              />
            </div>
            
            <!-- TOGGLE ENABLE/DISABLE -->
            <button
              type="button"
              @click="state[cat.value].enabled = !state[cat.value].enabled"
              class="relative inline-flex h-6 w-11 shrink-0 items-center rounded-full transition"
              :style="{ background: state[cat.value].enabled ? 'var(--accent)' : 'var(--bg-hover)' }"
            >
              <span
                class="inline-block h-5 w-5 rounded-full transition-transform"
                :style="{
                  background: state[cat.value].enabled ? 'var(--accent-text)' : 'var(--text-muted)',
                  transform: state[cat.value].enabled ? 'translateX(22px)' : 'translateX(2px)'
                }"
              ></span>
            </button>
          </div>
        </div>

        <!-- TEMPLATE EDITOR (Hanya muncul kalau milih 'Use Template') -->
        <div v-if="state[cat.value].enabled && state[cat.value].action === 'template'" class="space-y-2 pt-3 border-t theme-border">
          <div v-if="state[cat.value].templates.length === 0" class="text-[11px] theme-text-muted italic">
            Using default system templates. Add custom below to override.
          </div>
          <div
            v-for="(tpl, idx) in state[cat.value].templates"
            :key="idx"
            class="flex items-center gap-2 p-2 rounded-lg theme-bg border theme-border text-xs"
          >
            <span class="flex-1 whitespace-pre-wrap">{{ tpl }}</span>
            <button @click="removeTemplate(cat.value, idx)" class="text-xs font-bold shrink-0 hover:underline" style="color: var(--danger);">Remove</button>
          </div>

          <div class="flex items-start gap-2">
            <input
              v-model="newTemplate[cat.value]"
              type="text"
              placeholder="Write new template..."
              class="input flex-1"
              @keydown.enter.prevent="addTemplate(cat.value)"
            />
            <Button variant="secondary" size="sm" :disabled="!newTemplate[cat.value]?.trim()" @click="addTemplate(cat.value)">Add</Button>
          </div>
        </div>

        <div v-if="state[cat.value].enabled && state[cat.value].action === 'llm'" class="text-[11px] theme-text-muted pt-2 border-t theme-border">
          This category will generate replies using AI (costs 1 credit per reply, unless using your own API key).
        </div>
      </div>
    </div>
  </Card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { supabase } from '../lib/supabase'
import { useNotify } from '../composables/useNotify'
import { Card, Button, Badge, Select } from './ui'

const { showToast } = useNotify()
const loading = ref(true)
const saving = ref(false)
const accountId = ref<string | null>(null)

const categories = [
  { value: 'question', label: 'Questions', description: 'Asking about price, info, etc.' },
  { value: 'praise', label: 'Praise', description: 'Compliments like "keren", "mantap"' },
  { value: 'neutral', label: 'Neutral', description: 'Greetings or general comments' },
  { value: 'spam', label: 'Spam', description: 'Promotions or suspicious links' },
  { value: 'toxic', label: 'Toxic', description: 'Insults or negative attacks' },
]

const state = ref<Record<string, { enabled: boolean; action: string; templates: string[] }>>({})
const newTemplate = ref<Record<string, string>>({})

function initState(rules: any = {}) {
  const s: Record<string, any> = {}
  for (const cat of categories) {
    const r = rules[cat.value] || {}
    
    // Default action kalau belum pernah disetting
    let defaultAction = 'llm'
    if (cat.value === 'praise' || cat.value === 'neutral') defaultAction = 'template'
    if (cat.value === 'spam' || cat.value === 'toxic') defaultAction = 'skip'

    s[cat.value] = {
      enabled: r.enabled !== undefined ? r.enabled : true,
      action: r.action || defaultAction,
      templates: Array.isArray(r.templates) ? [...r.templates] : [],
    }
    newTemplate.value[cat.value] = ''
  }
  state.value = s
}

async function load() {
  loading.value = true
  try {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) return
    const { data: account } = await supabase
      .schema('threads')
      .from('threads_accounts')
      .select('id')
      .eq('user_id', user.id)
      .maybeSingle()
    if (!account) return
    accountId.value = account.id

    const { data: settings } = await supabase
      .schema('threads')
      .from('auto_reply_settings')
      .select('rules')
      .eq('account_id', account.id)
      .maybeSingle()

    initState(settings?.rules || {})
  } finally {
    loading.value = false
  }
}

function addTemplate(cat: string) {
  const tpl = (newTemplate.value[cat] || '').trim()
  if (!tpl) return
  state.value[cat].templates.push(tpl)
  newTemplate.value[cat] = ''
}

function removeTemplate(cat: string, idx: number) {
  state.value[cat].templates.splice(idx, 1)
}

async function save() {
  if (!accountId.value) return
  saving.value = true
  try {
    const { error } = await supabase
      .schema('threads')
      .from('auto_reply_settings')
      .update({ rules: state.value })
      .eq('account_id', accountId.value)
    if (error) throw error
    showToast('Reply strategy saved.', 'success')
  } catch (err: any) {
    showToast('Failed to save: ' + err.message, 'error')
  } finally {
    saving.value = false
  }
}

onMounted(load)
</script>
