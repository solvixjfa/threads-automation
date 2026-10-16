<template>
  <Card>
    <template #header>
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-sm font-bold">Reply templates</h2>
          <p class="text-xs theme-text-muted mt-0.5">Control auto replies per comment category.</p>
        </div>
        <Button @click="save" :disabled="saving" :loading="saving" size="sm">
          {{ saving ? 'Saving...' : 'Save' }}
        </Button>
      </div>
    </template>

    <div v-if="loading" class="space-y-3">
      <div v-for="i in 3" :key="i" class="h-16 skeleton"></div>
    </div>

    <div v-else class="space-y-4">
      <div v-for="cat in categories" :key="cat.value" class="p-4 rounded-xl theme-bg-sec border theme-border space-y-3">
        <div class="flex items-start justify-between gap-3">
          <div class="min-w-0 flex-1">
            <div class="flex items-center gap-2 flex-wrap">
              <span class="text-sm font-bold">{{ cat.label }}</span>
              <Badge :variant="cat.llmOnly ? 'accent' : 'default'">
                {{ cat.llmOnly ? 'AI only' : 'Template' }}
              </Badge>
            </div>
            <p class="text-xs theme-text-muted mt-0.5">{{ cat.description }}</p>
          </div>
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

        <div v-if="!cat.llmOnly && state[cat.value].enabled" class="space-y-2 pt-2 divider">
          <div v-if="state[cat.value].templates.length === 0" class="text-xs theme-text-muted italic">
            Using system templates. Add custom below to override.
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

        <div v-if="cat.llmOnly && state[cat.value].enabled" class="text-xs theme-text-muted pt-2 divider">
          This category always uses AI with your knowledge base. Cannot use templates.
        </div>
        <div v-if="!state[cat.value].enabled" class="text-xs theme-text-muted pt-2 divider">
          Disabled. Comments in this category will not receive auto replies.
        </div>
      </div>
    </div>
  </Card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { supabase } from '../lib/supabase'
import { useNotify } from '../composables/useNotify'
import { Card, Button, Badge } from './ui'

const { showToast } = useNotify()
const loading = ref(true)
const saving = ref(false)
const accountId = ref<string | null>(null)

const categories = [
  { value: 'praise', label: 'Praise', description: 'Comments like keren, mantap, thanks', llmOnly: false },
  { value: 'neutral', label: 'Neutral', description: 'Greetings or general comments', llmOnly: false },
  { value: 'question', label: 'Question', description: 'Needs answer with brand context', llmOnly: true },
  { value: 'spam', label: 'Spam', description: 'Promotions or suspicious links', llmOnly: true },
  { value: 'toxic', label: 'Toxic', description: 'Insults or attacks', llmOnly: true },
]

const state = ref<Record<string, { enabled: boolean; templates: string[] }>>({})
const newTemplate = ref<Record<string, string>>({})

function initState(rules: any = {}) {
  const s: Record<string, any> = {}
  for (const cat of categories) {
    const r = rules[cat.value] || {}
    s[cat.value] = {
      enabled: r.enabled !== undefined ? r.enabled : true,
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
    showToast('Templates saved.', 'success')
  } catch (err: any) {
    showToast('Failed to save: ' + err.message, 'error')
  } finally {
    saving.value = false
  }
}

onMounted(load)
</script>
