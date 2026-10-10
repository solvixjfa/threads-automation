<template>
  <div class="space-y-8">
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-slate-900 tracking-tight">Auto Reply Inbox</h1>
        <p class="text-slate-500 text-sm mt-1">Review dan kelola balasan komentar otomatis buatan AI sebelum terbit.</p>
      </div>
      <button 
        @click="fetchLogs" 
        class="bg-indigo-50 hover:bg-indigo-100 text-indigo-700 text-xs font-bold py-2.5 px-4 rounded-xl border border-indigo-100 transition"
      >
        Refresh Inbox
      </button>
    </div>

    <!-- Filter Tab -->
    <div class="flex border-b border-slate-200 text-xs font-bold gap-6">
      <button 
        @click="activeTab = 'pending'"
        class="pb-3 border-b-2 transition"
        :class="activeTab === 'pending' ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-slate-400 hover:text-slate-600'"
      >
        Antrean Review ({{ pendingLogs.length }})
      </button>
      <button 
        @click="activeTab = 'history'"
        class="pb-3 border-b-2 transition"
        :class="activeTab === 'history' ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-slate-400 hover:text-slate-600'"
      >
        Riwayat Terkirim / Skipped ({{ historyLogs.length }})
      </button>
    </div>

    <div v-if="loading" class="p-12 text-center text-xs text-slate-400 animate-pulse font-medium">
      Memuat pesan dan balasan AI...
    </div>

    <!-- Tab 1: Antrean Pending Review -->
    <div v-else-if="activeTab === 'pending'" class="space-y-4">
      <div v-if="pendingLogs.length === 0" class="bg-white border border-slate-200 rounded-2xl p-12 text-center text-xs text-slate-400 font-medium">
        Belum ada balasan komentar yang menunggu review.
      </div>

      <div v-for="log in pendingLogs" :key="log.id" class="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-4">
        <div class="flex justify-between items-start">
          <span class="text-[10px] font-bold uppercase tracking-wider bg-amber-50 text-amber-600 border border-amber-100 px-2.5 py-1 rounded-md">
            Menunggu Review
          </span>
          <span class="text-xs text-slate-400">{{ formatDate(log.created_at) }}</span>
        </div>

        <div class="space-y-1.5 bg-slate-50 p-4 rounded-xl border border-slate-100">
          <span class="text-[10px] font-bold text-slate-500 uppercase">Draf Balasan AI</span>
          <textarea
            v-model="log.final_text"
            rows="3"
            class="w-full bg-white border border-slate-200 rounded-lg p-3 text-xs text-slate-800 focus:outline-none focus:ring-1 focus:ring-indigo-500 transition resize-none"
          ></textarea>
        </div>

        <div class="flex justify-end items-center gap-3 pt-1">
          <button
            @click="updateStatus(log.id, 'skipped', log.final_text)"
            class="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-lg transition"
          >
            Abaikan / Skip
          </button>
          <button
            @click="updateStatus(log.id, 'approved', log.final_text)"
            class="px-5 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold rounded-lg transition shadow-sm"
          >
            Approve & Kirim
          </button>
        </div>
      </div>
    </div>

    <!-- Tab 2: History -->
    <div v-else class="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">
      <div v-if="historyLogs.length === 0" class="p-12 text-center text-xs text-slate-400 font-medium">
        Belum ada riwayat balasan terkirim atau diabaikan.
      </div>
      <div v-else class="divide-y divide-slate-100">
        <div v-for="log in historyLogs" :key="log.id" class="p-5 hover:bg-slate-50 transition space-y-2">
          <div class="flex justify-between items-center">
            <span
              class="px-2.5 py-1 text-[10px] font-bold uppercase tracking-wider rounded-md"
              :class="{
                'bg-emerald-50 text-emerald-600 border border-emerald-100': ['sent', 'approved'].includes(log.status),
                'bg-slate-100 text-slate-600 border border-slate-200': log.status === 'skipped'
              }"
            >
              {{ log.status }}
            </span>
            <span class="text-xs text-slate-400">{{ formatDate(log.created_at) }}</span>
          </div>
          <p class="text-xs text-slate-800 font-medium bg-slate-50 p-3 rounded-lg border border-slate-100 whitespace-pre-wrap">
            {{ log.final_text || log.generated_text || 'Tidak ada isi balasan.' }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { supabase } from '../lib/supabase'

const loading = ref(true)
const activeTab = ref<'pending' | 'history'>('pending')
const logs = ref<any[]>([])

const pendingLogs = computed(() => logs.value.filter(l => l.status === 'pending' || l.status === 'generated'))
const historyLogs = computed(() => logs.value.filter(l => l.status !== 'pending' && l.status !== 'generated'))

function formatDate(isoString: string) {
  if (!isoString) return ''
  return new Date(isoString).toLocaleString('id-ID', { dateStyle: 'medium', timeStyle: 'short' })
}

async function fetchLogs() {
  loading.value = true
  const { data } = await supabase
    .schema('threads')
    .from('auto_reply_logs')
    .select('*')
    .order('created_at', { ascending: false })
    .limit(30)

  if (data) logs.value = data
  loading.value = false
}

async function updateStatus(id: string, newStatus: string, finalText: string) {
  try {
    const { error } = await supabase
      .schema('threads')
      .from('auto_reply_logs')
      .update({
        status: newStatus,
        final_text: finalText
      })
      .eq('id', id)

    if (error) throw error
    await fetchLogs()
  } catch (err: any) {
    alert('Gagal perbarui status: ' + err.message)
  }
}

onMounted(() => {
  fetchLogs()
})
</script>
