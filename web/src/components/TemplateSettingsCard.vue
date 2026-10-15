<template>
  <Card>
    <template #header>
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-sm font-bold uppercase tracking-wide">Template Balasan</h2>
          <p class="text-xs theme-text-muted mt-0.5">Atur balasan otomatis per kategori komentar</p>
        </div>
        <Button @click="save" :disabled="saving" :loading="saving" size="sm">
          {{ saving ? 'Menyimpan...' : 'Simpan' }}
        </Button>
      </div>
    </template>

    <div v-if="loading" class="space-y-3">
      <div v-for="i in 3" :key="i" class="h-16 skeleton"></div>
    </div>

    <div v-else class="space-y-4">
      <div
        v-for="cat in categories"
        :key="cat.value"
        class="p-4 rounded-xl theme-bg-sec border theme-border space-y-3"
      >
        <div class="flex items-start justify-between gap-3">
          <div class="min-w-0 flex-1">
            <div class="flex items-center gap-2 flex-wrap">
              <span class="text-sm font-bold">{{ cat.label }}</span>
              <Badge :variant="cat.llmOnly ? 'accent' : 'default'">
                {{ cat.llmOnly ? 'Otomatis AI' : 'Template' }}
              </Badge>
            </div>
            <p class="text-xs theme-text-muted mt-0.5">{{ cat.description }}</p>
          </div>
          <label class="relative inline-flex items-center cursor-pointer shrink-0">
            <input
              type="checkbox"
              v-model="state[cat.value].enabled"
              class="sr-only peer"
            />
            <div class="w-11 h-6 rounded-full transition theme-bg-hover peer-checked:theme-accent after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:rounded-full after:h-5 after:w-5 after:transition-all after:theme-bg peer-checked:after:translate-x-full"></div>
          </label>
        </div>

        <div v-if="!cat.llmOnly && state[cat.value].enabled" class="space-y-2 pt-2 divider">
          <div v-if="state[cat.value].templates.length === 0" class="text-xs theme-text-muted italic">
            Pakai template sistem (belum ada custom). Tambah di bawah kalau mau ganti.
          </div>
          <div
            v-for="(tpl, idx) in state[cat.value].templates"
            :key="idx"
            class="flex items-center gap-2 p-2 rounded-lg theme-bg border theme-border text-xs"
          >
            <span class="flex-1 whitespace-pre-wrap">{{ tpl }}</span>
            <button
              @click="removeTemplate(cat.value, idx)"
              class="text-xs font-bold shrink-0 hover:underline"
              style="color: var(--danger);"
            >
              Hapus
            </button>
          </div>

          <div class="flex items-start gap-2">
            <input
              v-model="newTemplate[cat.value]"
              type="text"
              placeholder="Tulis template baru..."
              class="input flex-1"
              @keydown.enter.prevent="addTemplate(cat.value)"
            />
            <Button
              variant="secondary"
              size="sm"
              :disabled="!newTemplate[cat.value]?.trim()"
              @click="addTemplate(cat.value)"
            >
              Tambah
            </Button>
          </div>
        </div>

        <div v-if="cat.llmOnly && state[cat.value].enabled" class="text-xs theme-text-muted pt-2 divider">
          Kategori ini selalu pakai AI (RAG) karena butuh konteks brand. Tidak bisa pakai template.
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
  { value: 'praise', label: 'Pujian', description: 'Komentar seperti keren, mantap, thanks', llmOnly: false },
  { value: 'neutral', label: 'Netral', description: 'Sapaan atau komentar umum', llmOnly: false },
  { value: 'question', label: 'Pertanyaan', description: 'Butuh balasan dengan konteks brand', llmOnly: true },
  { value: 'spam', label: 'Spam', description: 'Komentar promosi atau link aneh', llmOnly: true },
  { value: 'toxic', label: 'Toxic', description: 'Komentar kasar atau menyerang', llmOnly: true },
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
  } catch (err) {
    console.error(err)
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
    showToast('Template berhasil disimpan!', 'success')
  } catch (err: any) {
    showToast('Gagal menyimpan: ' + err.message, 'error')
  } finally {
    saving.value = false
  }
}

onMounted(load)
</script>
