import { defineStore } from 'pinia'
import { ref } from 'vue'
import { supabase } from '../lib/supabase'

export interface AccountInfo {
  id: string
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
}

export const useSettingsStore = defineStore('settings', () => {
  const loading = ref(false)
  const account = ref<AccountInfo | null>(null)
  const settings = ref<AutoReplySettings | null>(null)

  async function fetchAccountAndSettings() {
    loading.value = true
    try {
      const { data: accData } = await supabase
        .schema('threads')
        .from('threads_accounts')
        .select('id, username, connection_status, kill_switch')
        .order('created_at', { ascending: false })
        .limit(1)
        .maybeSingle()

      if (accData) {
        account.value = {
          id: accData.id,
          username: accData.username || 'Unlinked Account',
          connection_status: accData.connection_status || 'disconnected',
          kill_switch: !!accData.kill_switch
        }

        const { data: settData } = await supabase
          .schema('threads')
          .from('auto_reply_settings')
          .select('*')
          .eq('account_id', accData.id)
          .maybeSingle()

        if (settData) {
          settings.value = settData
        }
      } else {
        account.value = null
      }
    } catch (err: any) {
      console.error('Error fetching settings:', err)
    } finally {
      loading.value = false
    }
  }

  async function saveSettings(formData: {
    enabled: boolean
    mode: 'review' | 'auto'
    tone_prompt: string
    knowledge_base: string
  }) {
    if (!account.value?.id) {
      alert('Gagal menyimpan: Belum ada akun Threads terhubung.')
      return { success: false }
    }

    loading.value = true
    try {
      const payload = {
        account_id: account.value.id,
        enabled: formData.enabled,
        mode: formData.mode,
        tone_prompt: formData.tone_prompt,
        knowledge_base: formData.knowledge_base
      }

      const { data, error } = await supabase
        .schema('threads')
        .from('auto_reply_settings')
        .upsert(payload, { onConflict: 'account_id' })
        .select('*')
        .single()

      if (error) throw error

      settings.value = data
      alert('Pengaturan AI berhasil disimpan!')
      return { success: true }
    } catch (err: any) {
      console.error('Error saving settings:', err)
      alert('Error Simpan Pengaturan: ' + (err.message || 'Gagal menyimpan ke database'))
      return { success: false, error: err.message }
    } finally {
      loading.value = false
    }
  }

  async function toggleKillSwitch(status: boolean) {
    if (!account.value?.id) return
    try {
      const { error } = await supabase
        .schema('threads')
        .from('threads_accounts')
        .update({ kill_switch: status })
        .eq('id', account.value.id)

      if (error) throw error
      account.value.kill_switch = status
      alert(`Kill switch status updated to: ${status ? 'ACTIVE' : 'INACTIVE'}`)
    } catch (err: any) {
      alert('Error Kill Switch: ' + err.message)
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
