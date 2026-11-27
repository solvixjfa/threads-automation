<template>
  <div class="space-y-6">
    <!-- HEADER -->
    <div class="flex flex-wrap justify-between items-center gap-3">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Outreach Templates</h1>
        <p class="text-xs theme-text-muted mt-0.5">Library pesan siap salin untuk prospecting, komentar kontekstual, follow-up, dan onboarding.</p>
      </div>
      <button @click="openCreateModal" class="btn btn-primary btn-sm flex items-center gap-1.5">
        <Plus class="w-4 h-4" />
        Template Baru
      </button>
    </div>

    <!-- CATEGORY TABS & SEARCH -->
    <div class="space-y-3">
      <div class="flex gap-1.5 overflow-x-auto pb-1">
        <button
          v-for="cat in CATEGORY_TABS"
          :key="cat"
          @click="selectedCategory = cat"
          class="px-3 py-1.5 rounded-lg text-xs font-bold whitespace-nowrap border transition-colors"
          :class="selectedCategory === cat
            ? 'bg-[var(--accent)] text-[var(--accent-text)] border-[var(--accent)]'
            : 'theme-bg theme-border theme-text-muted hover:theme-text'"
        >
          {{ cat }}
        </button>
      </div>

      <div class="relative">
        <Search class="w-4 h-4 theme-text-muted absolute left-3 top-1/2 -translate-y-1/2" />
        <input
          v-model.trim="searchQuery"
          type="text"
          placeholder="Cari nama template atau isi pesan..."
          class="input w-full pl-9 text-sm"
        />
      </div>
    </div>

    <!-- LOADING / EMPTY -->
    <div v-if="loading" class="p-10 text-center text-sm theme-text-muted animate-pulse">
      Memuat library template...
    </div>
    <div v-else-if="filteredTemplates.length === 0" class="card p-10 text-center text-sm theme-text-muted">
      Belum ada template di kategori ini.
    </div>

    <!-- TEMPLATE CARDS -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div
        v-for="tpl in filteredTemplates"
        :key="tpl.id"
        class="card p-4 flex flex-col justify-between gap-4"
      >
        <div class="space-y-2.5">
          <div class="flex items-start justify-between gap-2">
            <div>
              <span class="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded theme-bg-sec theme-text-muted">
                {{ tpl.category }}
              </span>
              <h3 class="font-bold text-sm mt-1.5">{{ tpl.name }}</h3>
            </div>
          </div>

          <div class="p-3 rounded-lg theme-bg-sec border theme-border text-xs leading-relaxed whitespace-pre-line select-all">
            {{ tpl.content }}
          </div>
        </div>

        <div class="flex items-center justify-between gap-2 pt-2 border-t theme-border">
          <button
            @click="copyTemplate(tpl)"
            class="btn btn-primary btn-sm flex-1 flex items-center justify-center gap-1.5 py-2"
          >
            <Check v-if="copiedId === tpl.id" class="w-3.5 h-3.5" />
            <Copy v-else class="w-3.5 h-3.5" />
            <span>{{ copiedId === tpl.id ? 'Tersalin!' : 'Copy Pesan' }}</span>
          </button>

          <button
            @click="openEditModal(tpl)"
            class="btn btn-secondary btn-sm px-3 py-2 flex items-center gap-1"
            title="Edit template"
          >
            <Edit3 class="w-3.5 h-3.5" />
            <span class="text-xs">Edit</span>
          </button>

          <button
            @click="deleteTemplate(tpl)"
            class="p-2 rounded-lg border theme-border theme-text-muted hover:text-red-500 transition-colors"
            title="Hapus template"
          >
            <Trash2 class="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </div>

    <!-- MODAL CREATE / EDIT TEMPLATE -->
    <Teleport to="body">
      <div v-if="showModal" class="fixed inset-0 z-[100] flex items-end sm:items-center justify-center p-0 sm:p-4 bg-black/60 backdrop-blur-sm">
        <div class="card w-full sm:max-w-lg rounded-t-2xl sm:rounded-2xl p-5 space-y-4 theme-bg max-h-[90dvh] overflow-y-auto">
          <div class="flex items-center justify-between">
            <h3 class="text-base font-bold">{{ editingId ? 'Edit Template' : 'Tambah Template Baru' }}</h3>
            <button @click="showModal = false" class="p-1 theme-text-muted hover:theme-text">
              <X class="w-5 h-5" />
            </button>
          </div>

          <form @submit.prevent="saveTemplate" class="space-y-3">
            <div>
              <label class="block text-xs font-bold mb-1">Kategori</label>
              <select v-model="form.category" class="input w-full text-sm" required>
                <option v-for="c in CATEGORIES" :key="c" :value="c">{{ c }}</option>
              </select>
            </div>

            <div>
              <label class="block text-xs font-bold mb-1">Nama Template</label>
              <input
                v-model.trim="form.name"
                type="text"
                placeholder="Misal: Follow-up Kreator Niche Edukasi"
                class="input w-full text-sm"
                required
              />
            </div>

            <div>
              <label class="block text-xs font-bold mb-1">Isi Pesan</label>
              <textarea
                v-model="form.content"
                rows="6"
                placeholder="Tulis pesan natural, singkat, dan tidak kaku..."
                class="input w-full text-sm leading-relaxed"
                required
              ></textarea>
            </div>

            <div class="flex justify-end gap-2 pt-2">
              <button type="button" @click="showModal = false" class="btn btn-secondary btn-sm">Batal</button>
              <button type="submit" :disabled="saving" class="btn btn-primary btn-sm">
                {{ saving ? 'Menyimpan...' : 'Simpan Template' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { supabase } from '../../lib/supabase'
import { useNotify } from '../../composables/useNotify'
import { Plus, Search, Copy, Check, Edit3, Trash2, X } from 'lucide-vue-next'

interface CrmTemplate {
  id: string
  category: string
  name: string
  content: string
  sort_order: number
}

const CATEGORIES = ['Cold Outreach', 'Contextual Outreach', 'Follow-up', 'Product & Trial']
const CATEGORY_TABS = ['Semua', ...CATEGORIES]

const { showToast } = useNotify()
const templates = ref<CrmTemplate[]>([])
const loading = ref(true)
const saving = ref(false)
const selectedCategory = ref('Semua')
const searchQuery = ref('')
const copiedId = ref<string | null>(null)

const showModal = ref(false)
const editingId = ref<string | null>(null)
const form = ref({
  category: 'Cold Outreach',
  name: '',
  content: '',
})

const filteredTemplates = computed(() => {
  return templates.value.filter(t => {
    if (selectedCategory.value !== 'Semua' && t.category !== selectedCategory.value) return false
    if (searchQuery.value) {
      const q = searchQuery.value.toLowerCase()
      if (!t.name.toLowerCase().includes(q) && !t.content.toLowerCase().includes(q)) return false
    }
    return true
  })
})

async function fetchTemplates() {
  loading.value = true
  try {
    const { data, error } = await supabase
      .from('crm_templates')
      .select('*')
      .order('sort_order', { ascending: true })
      .order('created_at', { ascending: true })

    if (error) throw error
    templates.value = (data || []) as CrmTemplate[]
  } catch (err: any) {
    showToast('Gagal memuat template: ' + err.message, 'error')
  } finally {
    loading.value = false
  }
}

async function copyTemplate(tpl: CrmTemplate) {
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(tpl.content)
    } else {
      const ta = document.createElement('textarea')
      ta.value = tpl.content
      ta.style.position = 'fixed'
      ta.style.opacity = '0'
      document.body.appendChild(ta)
      ta.focus()
      ta.select()
      document.execCommand('copy')
      document.body.removeChild(ta)
    }
    copiedId.value = tpl.id
    showToast(`Template "${tpl.name}" disalin`, 'success')
    setTimeout(() => {
      if (copiedId.value === tpl.id) copiedId.value = null
    }, 2000)
  } catch {
    showToast('Gagal menyalin teks', 'error')
  }
}

function openCreateModal() {
  editingId.value = null
  form.value = {
    category: selectedCategory.value !== 'Semua' ? selectedCategory.value : 'Cold Outreach',
    name: '',
    content: '',
  }
  showModal.value = true
}

function openEditModal(tpl: CrmTemplate) {
  editingId.value = tpl.id
  form.value = {
    category: tpl.category,
    name: tpl.name,
    content: tpl.content,
  }
  showModal.value = true
}

async function saveTemplate() {
  if (!form.value.name || !form.value.content.trim()) return
  saving.value = true
  try {
    if (editingId.value) {
      const { data, error } = await supabase
        .from('crm_templates')
        .update({
          category: form.value.category,
          name: form.value.name,
          content: form.value.content.trim(),
          updated_at: new Date().toISOString(),
        })
        .eq('id', editingId.value)
        .select()
        .single()

      if (error) throw error
      const idx = templates.value.findIndex(t => t.id === editingId.value)
      if (idx !== -1 && data) templates.value[idx] = data as CrmTemplate
      showToast('Template diperbarui', 'success')
    } else {
      const { data, error } = await supabase
        .from('crm_templates')
        .insert({
          category: form.value.category,
          name: form.value.name,
          content: form.value.content.trim(),
          sort_order: templates.value.length + 1,
        })
        .select()
        .single()

      if (error) throw error
      if (data) templates.value.push(data as CrmTemplate)
      showToast('Template ditambahkan', 'success')
    }
    showModal.value = false
  } catch (err: any) {
    showToast('Gagal menyimpan template: ' + err.message, 'error')
  } finally {
    saving.value = false
  }
}

async function deleteTemplate(tpl: CrmTemplate) {
  if (!confirm(`Hapus template "${tpl.name}"?`)) return
  try {
    const { error } = await supabase.from('crm_templates').delete().eq('id', tpl.id)
    if (error) throw error
    templates.value = templates.value.filter(t => t.id !== tpl.id)
    showToast('Template dihapus', 'success')
  } catch (err: any) {
    showToast('Gagal menghapus: ' + err.message, 'error')
  }
}

onMounted(fetchTemplates)
</script>
