import { defineStore } from 'pinia'
import { ref } from 'vue'
import { supabase } from '../lib/supabase'

export interface ReplyItem {
  id: string
  threads_reply_id: string
  author_username: string
  text: string
  replied_at: string
  classification: string
  hide_status: string
}

export interface AutoReplyLog {
  id: string
  reply_id: string
  status: string
  generated_text: string
  final_text: string
  skip_reason?: string
  reply?: ReplyItem
}

export const useInboxStore = defineStore('inbox', () => {
  const loading = ref(false)
  const replies = ref<ReplyItem[]>([])
  const reviewLogs = ref<AutoReplyLog[]>([])

  async function fetchReplies(accountId: string) {
    loading.value = true
    try {
      const { data, error } = await supabase
        .schema('threads')
        .from('replies')
        .select('*')
        .eq('account_id', accountId)
        .order('replied_at', { ascending: false })
        .limit(50)

      if (error) throw error
      if (data) replies.value = data
    } catch (err: any) {
      console.error('Error fetching replies:', err)
    } finally {
      loading.value = false
    }
  }

  async function fetchPendingReviews(accountId: string) {
    loading.value = true
    try {
      const { data, error } = await supabase
        .schema('threads')
        .from('auto_reply_logs')
        .select('*, reply:replies(*)')
        .eq('account_id', accountId)
        .eq('status', 'pending_review')
        .order('created_at', { ascending: false })

      if (error) throw error
      if (data) reviewLogs.value = data
    } catch (err: any) {
      console.error('Error fetching reviews:', err)
    } finally {
      loading.value = false
    }
  }

  async function approveAndSendReply(logId: string, finalText: string) {
    try {
      const { error } = await supabase
        .schema('threads')
        .from('auto_reply_logs')
        .update({
          status: 'sent',
          final_text: finalText
        })
        .eq('id', logId)

      if (error) throw error
      reviewLogs.value = reviewLogs.value.filter(item => item.id !== logId)
      return { success: true }
    } catch (err: any) {
      console.error('Error approving reply:', err)
      return { success: false, error: err.message }
    }
  }

  return {
    loading,
    replies,
    reviewLogs,
    fetchReplies,
    fetchPendingReviews,
    approveAndSendReply
  }
})
