<template>
  <div class="space-y-6">
    <!-- HEADER -->
    <div class="flex items-center justify-between gap-3">
      <div>
        <h1 class="text-xl md:text-2xl font-bold tracking-tight">Sales Analytics</h1>
        <p class="text-xs theme-text-muted mt-0.5">Performa outreach, response rate, konversi, dan perbandingan channel.</p>
      </div>
      <button
        @click="fetchAnalytics"
        :disabled="loading"
        class="btn btn-secondary btn-sm flex items-center gap-1.5"
      >
        <RefreshCw class="w-3.5 h-3.5" :class="{ 'animate-spin': loading }" />
        <span>Refresh</span>
      </button>
    </div>

    <div v-if="loading" class="p-10 text-center text-sm theme-text-muted animate-pulse">
      Menghitung data analitik...
    </div>

    <template v-else>
      <!-- TOP KPI CARDS -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <div class="card p-4">
          <div class="text-[11px] font-bold uppercase theme-text-muted">Total Outreach</div>
          <div class="text-2xl font-black mt-1">{{ stats.totalOutreach }}</div>
          <div class="text-[11px] theme-text-muted mt-0.5">dari {{ leads.length }} total leads</div>
        </div>

        <div class="card p-4">
          <div class="text-[11px] font-bold uppercase theme-text-muted">Response Rate</div>
          <div class="text-2xl font-black mt-1">{{ stats.responseRate }}%</div>
          <div class="text-[11px] theme-text-muted mt-0.5">{{ stats.repliedCount }} prospek membalas</div>
        </div>

        <div class="card p-4">
          <div class="text-[11px] font-bold uppercase theme-text-muted">Trial & Activated</div>
          <div class="text-2xl font-black mt-1">{{ stats.trialCount }} / {{ stats.activatedCount }}</div>
          <div class="text-[11px] theme-text-muted mt-0.5">Interested: {{ stats.interestedCount }}</div>
        </div>

        <div class="card p-4">
          <div class="text-[11px] font-bold uppercase theme-text-muted">Paying Customers</div>
          <div class="text-2xl font-black mt-1 text-emerald-500">{{ stats.paidCount }}</div>
          <div class="text-[11px] theme-text-muted mt-0.5">Conv. Rate: {{ stats.conversionRate }}%</div>
        </div>
      </div>

      <!-- CHANNEL EFFECTIVENESS -->
      <div class="card overflow-hidden">
        <div class="p-4 border-b theme-border">
          <h2 class="text-sm font-bold">Efektivitas Outreach Channel</h2>
          <p class="text-xs theme-text-muted mt-0.5">Bandingkan hasil Cold DM vs Contextual Comment/Reply.</p>
        </div>

        <!-- Mobile Cards -->
        <div class="md:hidden divide-y theme-border">
          <div v-for="row in channelBreakdown" :key="row.channel" class="p-4 space-y-2">
            <div class="flex items-center justify-between">
              <span class="font-bold text-sm">{{ row.channel }}</span>
              <span class="text-xs font-bold text-emerald-500">{{ row.paid }} Paid ({{ row.paidRate }}%)</span>
            </div>
            <div class="grid grid-cols-3 gap-2 text-xs theme-bg-sec p-2.5 rounded-lg">
              <div>
                <div class="text-[10px] theme-text-muted">Leads</div>
                <div class="font-bold">{{ row.total }}</div>
              </div>
              <div>
                <div class="text-[10px] theme-text-muted">Replied</div>
                <div class="font-bold">{{ row.replied }} ({{ row.replyRate }}%)</div>
              </div>
              <div>
                <div class="text-[10px] theme-text-muted">Trial / Act</div>
                <div class="font-bold">{{ row.trialOrActivated }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Desktop Table -->
        <div class="hidden md:block overflow-x-auto">
          <table class="w-full text-left text-sm">
            <thead class="theme-bg-sec border-b theme-border text-xs uppercase theme-text-muted">
              <tr>
                <th class="p-4 font-bold">Outreach Channel</th>
                <th class="p-4 font-bold text-right">Total Leads</th>
                <th class="p-4 font-bold text-right">Replied</th>
                <th class="p-4 font-bold text-right">Interested</th>
                <th class="p-4 font-bold text-right">Trial / Activated</th>
                <th class="p-4 font-bold text-right">Paying</th>
              </tr>
            </thead>
            <tbody class="divide-y theme-border">
              <tr v-for="row in channelBreakdown" :key="row.channel" class="hover:theme-bg-sec transition-colors">
                <td class="p-4 font-bold">{{ row.channel }}</td>
                <td class="p-4 text-right">{{ row.total }}</td>
                <td class="p-4 text-right">{{ row.replied }} ({{ row.replyRate }}%)</td>
                <td class="p-4 text-right">{{ row.interested }}</td>
                <td class="p-4 text-right">{{ row.trialOrActivated }}</td>
                <td class="p-4 text-right font-bold text-emerald-500">{{ row.paid }} ({{ row.paidRate }}%)</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- PIPELINE DISTRIBUTIONS -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="card p-4 space-y-3">
          <h3 class="text-sm font-bold">Status Komunikasi</h3>
          <div class="space-y-2.5">
            <div v-for="item in commBreakdown" :key="item.label" class="space-y-1">
              <div class="flex justify-between text-xs">
                <span class="font-medium">{{ item.label }}</span>
                <span class="font-bold">{{ item.count }} ({{ item.pct }}%)</span>
              </div>
              <div class="w-full h-2 rounded-full theme-bg-sec overflow-hidden">
                <div class="h-full bg-[var(--accent)] rounded-full" :style="{ width: item.pct + '%' }"></div>
              </div>
            </div>
          </div>
        </div>

        <div class="card p-4 space-y-3">
          <h3 class="text-sm font-bold">Status Konversi</h3>
          <div class="space-y-2.5">
            <div v-for="item in convBreakdown" :key="item.label" class="space-y-1">
              <div class="flex justify-between text-xs">
                <span class="font-medium">{{ item.label }}</span>
                <span class="font-bold">{{ item.count }} ({{ item.pct }}%)</span>
              </div>
              <div class="w-full h-2 rounded-full theme-bg-sec overflow-hidden">
                <div class="h-full bg-[var(--accent)] rounded-full" :style="{ width: item.pct + '%' }"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { supabase } from '../../lib/supabase'
import { useNotify } from '../../composables/useNotify'
import { RefreshCw } from 'lucide-vue-next'

interface CrmLead {
  id: string
  outreach_channel: string
  comm_status: string
  conversion_status: string
}

const CHANNEL_OPTIONS = ['Cold DM', 'Contextual Comment', 'Contextual Reply', 'Inbound', 'Referral', 'Other']
const COMM_STATUS_OPTIONS = ['Not Contacted', 'Contacted', 'Replied', 'Follow-up Needed', 'No Response', 'Not Interested']
const CONV_STATUS_OPTIONS = ['Potential', 'Interested', 'Trial Started', 'Activated', 'Paid', 'Not Proceeding']

const { showToast } = useNotify()
const leads = ref<CrmLead[]>([])
const loading = ref(true)

const stats = computed(() => {
  const contactedLeads = leads.value.filter(l => l.comm_status !== 'Not Contacted')
  const totalOutreach = contactedLeads.length
  const repliedCount = leads.value.filter(l => l.comm_status === 'Replied').length
  const interestedCount = leads.value.filter(l => l.conversion_status === 'Interested').length
  const trialCount = leads.value.filter(l => l.conversion_status === 'Trial Started').length
  const activatedCount = leads.value.filter(l => l.conversion_status === 'Activated').length
  const paidCount = leads.value.filter(l => l.conversion_status === 'Paid').length

  return {
    totalOutreach,
    repliedCount,
    responseRate: totalOutreach > 0 ? Math.round((repliedCount / totalOutreach) * 100) : 0,
    interestedCount,
    trialCount,
    activatedCount,
    paidCount,
    conversionRate: totalOutreach > 0 ? Math.round((paidCount / totalOutreach) * 100) : 0,
  }
})

const channelBreakdown = computed(() => {
  return CHANNEL_OPTIONS.map(ch => {
    const group = leads.value.filter(l => (l.outreach_channel || 'Cold DM') === ch)
    const total = group.length
    const replied = group.filter(l => l.comm_status === 'Replied').length
    const interested = group.filter(l => l.conversion_status === 'Interested').length
    const trialOrActivated = group.filter(l => ['Trial Started', 'Activated'].includes(l.conversion_status)).length
    const paid = group.filter(l => l.conversion_status === 'Paid').length
    return {
      channel: ch,
      total,
      replied,
      replyRate: total > 0 ? Math.round((replied / total) * 100) : 0,
      interested,
      trialOrActivated,
      paid,
      paidRate: total > 0 ? Math.round((paid / total) * 100) : 0,
    }
  })
})

const commBreakdown = computed(() => {
  const total = leads.value.length
  return COMM_STATUS_OPTIONS.map(label => {
    const count = leads.value.filter(l => l.comm_status === label).length
    return { label, count, pct: total > 0 ? Math.round((count / total) * 100) : 0 }
  })
})

const convBreakdown = computed(() => {
  const total = leads.value.length
  return CONV_STATUS_OPTIONS.map(label => {
    const count = leads.value.filter(l => l.conversion_status === label).length
    return { label, count, pct: total > 0 ? Math.round((count / total) * 100) : 0 }
  })
})

async function fetchAnalytics() {
  loading.value = true
  try {
    const { data, error } = await supabase
      .from('crm_leads')
      .select('id, outreach_channel, comm_status, conversion_status')

    if (error) throw error
    leads.value = (data || []) as CrmLead[]
  } catch (err: any) {
    showToast('Gagal memuat analitik: ' + err.message, 'error')
  } finally {
    loading.value = false
  }
}

onMounted(fetchAnalytics)
</script>
