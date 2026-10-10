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
      // 1. Ambil akun terhubung dari skema threads
      const { data: accData } = await supabase
        .schema('threads')
        .from('threads_accounts')
        .select('id, username, connection_status, kill_switch')
        .limit(1)
        .maybeSingle()

      if (accData) {
        account.value = {
          id: accData.id,
          username: accData.username || 'tester_account',
          connection_status: accData.connection_status || 'connected',
          kill_switch: !!accData.kill_switch
        }
      } else {
        // Fallback akun lokal untuk testing jika belum pernah OAuth
        account.value = {
          id: '00000000-0000-0000-0000-000000000000',
          username: 'Unlinked / Tester',
          connection_status: 'disconnected',
          kill_switch: false
        }
      }

      // 2. Ambil settingan auto-reply jika ada
      if (account.value?.id) {
        const { data: settData } = await supabase
          .schema('threads')
          .from('auto_reply_settings')
          .select('*')
          .eq('account_id', account.value.id)
          .maybeSingle()

        if (settData) {
          settings.value = settData
        }
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
    loading.value = true
    try {
      // Pastikan ada account_id yang valid
      let targetAccountId = account.value?.id

      if (!targetAccountId || targetAccountId === '00000000-0000-0000-0000-000000000000') {
        // Buatkan account_id valid di threads_accounts
        const newId = crypto.randomUUID()
        const { data: createdAcc, error: createErr } = await supabase
          .schema('threads')
          .from('threads_accounts')
          .insert({
            id: newId,
            username: 'tester_account',
            connection_status: 'connected'
          })
          .select('id, username, connection_status')
          .single()

        if (createErr) throw createErr
        if (createdAcc) {
          targetAccountId = createdAcc.id
          account.value = {
            id: createdAcc.id,
            username: createdAcc.username,
            connection_status: createdAcc.connection_status,
            kill_switch: false
          }
        }
      }

      const payload = {
        account_id: targetAccountId,
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
      alert('Pengaturan AI berhasil disimpan ke database!')
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
      alert(`Kill switch ${status ? 'AKTIF' : 'NONAKTIF'}`)
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
