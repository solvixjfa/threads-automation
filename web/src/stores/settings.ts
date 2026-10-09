import { defineStore } from 'pinia'
import { ref } from 'vue'
import { supabase } from '../lib/supabase'

export interface ThreadsAccount {
  id: string
  threads_user_id: string
  username: string
  connection_status: string
  kill_switch: boolean
}

export interface AutoReplySettings {
  account_id: string
  enabled: boolean
  mode: 'review' | 'auto'
  tone_prompt: string
  knowledge_base: string
  max_per_day: number
  hide_toxic: boolean
}

export const useSettingsStore = defineStore('settings', () => {
  const loading = ref(false)
  const account = ref<ThreadsAccount | null>(null)
  const settings = ref<AutoReplySettings | null>(null)

  async function fetchAccountAndSettings() {
    loading.value = true
    try {
      const { data: accData } = await supabase
        .schema('threads')
        .from('threads_accounts')
        .select('*')
        .maybeSingle()

      if (accData) {
        account.value = accData

        const { data: setData } = await supabase
          .schema('threads')
          .from('auto_reply_settings')
          .select('*')
          .eq('account_id', accData.id')
          .maybeSingle()

        if (setData) settings.value = setData
      }
    } catch (err: any) {
      console.error('Error fetching settings:', err)
    } finally {
      loading.value = false
    }
  }

  async function saveSettings(newSettings: Partial<AutoReplySettings>) {
    if (!account.value) return { success: false, error: 'No account connected' }
    loading.value = true
    try {
      const { error } = await supabase
        .schema('threads')
        .from('auto_reply_settings')
        .upsert({
          account_id: account.value.id,
          ...newSettings
        }, { onConflict: 'account_id' })

      if (error) throw error
      return { success: true }
    } catch (err: any) {
      console.error('Error saving settings:', err)
      return { success: false, error: err.message }
    } finally {
      loading.value = false
    }
  }

  async function toggleKillSwitch(enabled: boolean) {
    if (!account.value) return
    try {
      const { error } = await supabase
        .schema('threads')
        .from('threads_accounts')
        .update({ kill_switch: enabled })
        .eq('id', account.value.id)

      if (error) throw error
      account.value.kill_switch = enabled
    } catch (err: any) {
      console.error('Error toggling kill switch:', err)
    }
  }

  return {
    loading,
    account,
    settings,
    fetchAccountAndSettings,
    saveSettings,
    toggleKillSwitch
  }
})
