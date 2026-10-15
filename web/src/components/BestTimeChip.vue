<template>
  <div v-if="loading" class="animate-pulse h-8 w-48 rounded-full theme-bg-sec border theme-border"></div>
  
  <div v-else-if="bestTimeToday" class="inline-flex items-center gap-2.5 p-1 pr-3 theme-bg-sec border theme-border rounded-full text-[11px] md:text-xs shadow-sm transition-all hover:border-[var(--accent)]">
    <div class="flex items-center justify-center w-6 h-6 rounded-full" style="background: var(--accent); color: var(--accent-text);">
      <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
    </div>
    
    <div class="flex items-center gap-1">
      <span class="theme-text-muted font-medium">Best time <span class="font-bold theme-text">{{ dayLabel }}</span>:</span>
      <span class="font-extrabold" style="color: var(--accent);">{{ bestTimeToday }}</span>
    </div>
    
    <div class="h-3 w-px bg-gray-500/30"></div>
    
    <!-- Tambah type="button" agar stabil -->
    <button type="button" @click="applyTime" class="font-bold theme-text hover:underline focus:outline-none flex items-center gap-1">
      <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
      Pakai
    </button>
    
    <div class="h-3 w-px bg-gray-500/30 hidden sm:block"></div>
    
    <router-link to="/analytics" class="hover:underline theme-text-muted hidden sm:inline-block">Insight</router-link>
  </div>

  <div v-else class="inline-flex items-center gap-2 px-3 py-1.5 theme-bg-sec border theme-border rounded-full text-[11px] md:text-xs opacity-80">
    <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="theme-text-muted"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
    <span class="theme-text-muted">Data insight belum cukup</span>
    <span class="theme-text-muted">·</span>
    <router-link to="/analytics" class="hover:underline theme-text-muted">Lihat Detail</router-link>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { supabase } from '../lib/supabase'
import { useNotify } from '../composables/useNotify'

const emit = defineEmits(['apply'])
const { showToast } = useNotify() // Import composable Toast
const loading = ref(true)
const bestTimeToday = ref<string | null>(null)
const dayLabel = ref('hari ini')
const fallbackDayOffset = ref(0)

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

    const { data, error } = await supabase.functions.invoke('get-best-time', {
      body: { account_id: account.id }
    })

    if (!error && data) {
      const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
      const todayIdx = new Date().getDay()
      const todayName = days[todayIdx].toLowerCase()
      
      let list = []
      if (Array.isArray(data)) list = data
      else if (data?.data) list = data.data
      else if (data?.top_slots) list = data.top_slots
      else if (data?.heatmap) list = data.heatmap
      
      if (list.length > 0) {
        let todaySlots = list.filter((item: any) => 
          (item.day && item.day.toLowerCase() === todayName) || 
          (item.weekday && item.weekday.toLowerCase() === todayName)
        )
        
        if (todaySlots.length > 0) {
          // Filter slot yang masih belum lewat hari ini
          const nowMs = Date.now()
          const futureSlots = todaySlots.filter((slot: any) => {
            const foundHour = slot.hour
            const parts = foundHour.split(':')
            if (parts.length < 2) return false
            const slotTime = new Date()
            slotTime.setHours(parseInt(parts[0]), parseInt(parts[1]) || 0, 0, 0)
            return slotTime.getTime() > nowMs
          })

          const pool = futureSlots.length > 0 ? futureSlots : todaySlots
          pool.sort((a: any, b: any) => (b.er_pct || 0) - (a.er_pct || 0))

          const foundHour = pool[0].hour
          const parts = foundHour.split(':')
          if (parts.length >= 2) {
            bestTimeToday.value = `${parts[0].padStart(2, '0')}:${parts[1].padStart(2, '0')}`
            dayLabel.value = futureSlots.length > 0 ? 'hari ini' : 'besok'
          }
        } else {
          list.sort((a: any, b: any) => (b.er_pct || 0) - (a.er_pct || 0))
          const globalBest = list[0]
          const targetDayRaw = globalBest.day || globalBest.weekday
          
          if (targetDayRaw) {
            const targetDay = targetDayRaw.charAt(0).toUpperCase() + targetDayRaw.slice(1).toLowerCase()
            const targetIdx = days.indexOf(targetDay)
            
            let diff = targetIdx - todayIdx
            if (diff <= 0) diff += 7 
            fallbackDayOffset.value = diff
            
            const dayMap: Record<string, string> = { Sunday: 'Minggu', Monday: 'Senin', Tuesday: 'Selasa', Wednesday: 'Rabu', Thursday: 'Kamis', Friday: 'Jumat', Saturday: 'Sabtu' }
            
            const foundHour = globalBest.hour
            const parts = foundHour.split(':')
            if (parts.length >= 2) {
              bestTimeToday.value = `${parts[0].padStart(2, '0')}:${parts[1].padStart(2, '0')}`
              dayLabel.value = `terdekat (${dayMap[targetDay] || targetDay})`
            }
          }
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
  
  if (fallbackDayOffset.value > 0) {
    d.setDate(d.getDate() + fallbackDayOffset.value)
  }
  
  d.setHours(parseInt(hh), parseInt(mm) || 0, 0, 0)
  
  if (d.getTime() <= Date.now()) {
    d.setDate(d.getDate() + 1)
  }
  
  const tzOffset = d.getTimezoneOffset() * 60000
  const localISOTime = new Date(d.getTime() - tzOffset).toISOString().slice(0, 16)
  
  emit('apply', localISOTime)
  showToast('Waktu terbaik berhasil diterapkan!', 'success') // <--- INI FEEDBACKNYA
}
</script>
