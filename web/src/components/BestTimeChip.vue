<template>
  <div v-if="loading" class="animate-pulse h-8 w-48 rounded-full theme-bg-sec"></div>
  <div v-else-if="bestTimeToday" class="inline-flex items-center gap-2 px-3 py-1.5 theme-bg-sec border theme-border rounded-full text-[11px] md:text-xs">
    <span class="theme-text-muted">Best time hari ini:</span>
    <span class="font-bold theme-text">{{ bestTimeToday }}</span>
    <button @click="applyTime" class="font-bold theme-text hover:underline focus:outline-none">Pakai</button>
    <span class="theme-text-muted">·</span>
    <router-link to="/analytics" class="hover:underline theme-text-muted">Lihat Insight</router-link>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { supabase } from '../lib/supabase'

const emit = defineEmits(['apply'])
const loading = ref(true)
const bestTimeToday = ref<string | null>(null)

onMounted(async () => {
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

    // Hit edge function backend untuk Best Time
    const { data, error } = await supabase.functions.invoke('get-best-time', {
      body: { account_id: account.id }
    })

    if (!error && data) {
      const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
      const todayName = days[new Date().getDay()]
      
      let foundHour = null
      // Adaptasi terhadap berbagai kemungkinan struktur payload dari edge function
      const list = Array.isArray(data) ? data : (data.data || data.top_slots || data.heatmap || [])
      
      // Filter data sesuai hari ini
      const todaySlots = list.filter((item: any) => item.day === todayName || item.weekday === todayName)
      
      if (todaySlots.length > 0) {
        // Ambil slot dengan Engagement Rate tertinggi (jika ada er_pct)
        todaySlots.sort((a: any, b: any) => (b.er_pct || 0) - (a.er_pct || 0))
        foundHour = todaySlots[0].hour
      }

      if (foundHour) {
        // Format jam HH:MM
        const parts = foundHour.split(':')
        if (parts.length >= 2) {
          bestTimeToday.value = `${parts[0].padStart(2, '0')}:${parts[1].padStart(2, '0')}`
        }
      }
    }
  } catch (e) {
    console.error('Failed to fetch best time', e)
  } finally {
    loading.value = false
  }
})

function applyTime() {
  if (!bestTimeToday.value) return
  
  const d = new Date()
  const [hh, mm] = bestTimeToday.value.split(':')
  d.setHours(parseInt(hh), parseInt(mm) || 0, 0, 0)
  
  // Validasi: Jika "best time" hari ini sudah kelewat, otomatis set jam tersebut untuk besok
  if (d.getTime() <= Date.now()) {
    d.setDate(d.getDate() + 1)
  }
  
  // Konversi ke YYYY-MM-DDThh:mm untuk input datetime-local
  const tzOffset = d.getTimezoneOffset() * 60000
  const localISOTime = new Date(d.getTime() - tzOffset).toISOString().slice(0, 16)
  
  emit('apply', localISOTime)
}
</script>
