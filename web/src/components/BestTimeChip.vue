<template>
  <div v-if="loading" class="animate-pulse h-8 w-48 rounded-full theme-bg-sec border theme-border"></div>
  <div v-else-if="bestTimeToday" class="inline-flex items-center gap-2 px-3 py-1.5 theme-bg-sec border theme-border rounded-full text-[11px] md:text-xs">
    <span class="theme-text-muted">Best time {{ dayLabel }}:</span>
    <span class="font-bold theme-text">{{ bestTimeToday }}</span>
    <button @click="applyTime" class="font-bold theme-text hover:underline focus:outline-none">Pakai</button>
    <span class="theme-text-muted">·</span>
    <router-link to="/analytics" class="hover:underline theme-text-muted">Lihat Insight</router-link>
  </div>
  <div v-else class="inline-flex items-center gap-2 px-3 py-1.5 theme-bg-sec border theme-border rounded-full text-[11px] md:text-xs">
    <span class="theme-text-muted">Belum ada data Best Time</span>
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
      const todayName = days[todayIdx]
      
      const list = Array.isArray(data) ? data : (data.data || data.top_slots || data.heatmap || [])
      
      // 1. Coba cari slot khusus hari ini
      let todaySlots = list.filter((item: any) => item.day === todayName || item.weekday === todayName)
      
      if (todaySlots.length > 0) {
        todaySlots.sort((a: any, b: any) => (b.er_pct || 0) - (a.er_pct || 0))
        const foundHour = todaySlots[0].hour
        const parts = foundHour.split(':')
        if (parts.length >= 2) {
          bestTimeToday.value = `${parts[0].padStart(2, '0')}:${parts[1].padStart(2, '0')}`
          dayLabel.value = 'hari ini'
        }
      } else if (list.length > 0) {
        // 2. Fallback: Cari best time tertinggi secara keseluruhan jika hari ini kosong
        list.sort((a: any, b: any) => (b.er_pct || 0) - (a.er_pct || 0))
        const globalBest = list[0]
        const targetDay = globalBest.day || globalBest.weekday
        const targetIdx = days.indexOf(targetDay)
        
        let diff = targetIdx - todayIdx
        if (diff <= 0) diff += 7 // Hitung maju ke hari tersebut di minggu depan
        fallbackDayOffset.value = diff
        
        const dayMap: Record<string, string> = { Sunday: 'Minggu', Monday: 'Senin', Tuesday: 'Selasa', Wednesday: 'Rabu', Thursday: 'Kamis', Friday: 'Jumat', Saturday: 'Sabtu' }
        
        const foundHour = globalBest.hour
        const parts = foundHour.split(':')
        if (parts.length >= 2) {
          bestTimeToday.value = `${parts[0].padStart(2, '0')}:${parts[1].padStart(2, '0')}`
          dayLabel.value = `terdekat (${dayMap[targetDay]})`
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
  
  // Jika menggunakan fallback hari lain, majukan tanggal kalendernya
  if (fallbackDayOffset.value > 0) {
    d.setDate(d.getDate() + fallbackDayOffset.value)
  }
  
  d.setHours(parseInt(hh), parseInt(mm) || 0, 0, 0)
  
  // Validasi: Cegah set waktu di masa lalu
  if (d.getTime() <= Date.now()) {
    d.setDate(d.getDate() + 1)
  }
  
  const tzOffset = d.getTimezoneOffset() * 60000
  const localISOTime = new Date(d.getTime() - tzOffset).toISOString().slice(0, 16)
  
  emit('apply', localISOTime)
}
</script>
