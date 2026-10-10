import { defineStore } from 'pinia'
import { ref } from 'vue'
import { supabase } from '../lib/supabase'

export interface ReplyItem {
  id: string
  author_username: string
  text: string
  replied_at: string
  classification: string
}

export interface AutoReplyLog {
  id: string
  reply_id: string
  status: string
  final_text: string
  reply?: {
    author_username: string
    text: string
  }
}

export const useInboxStore = defineStore('inbox', () => {
  const loading = ref(false)
  const replies = ref<ReplyItem[]>([])
  const reviewLogs = ref<AutoReplyLog[]>([])

  async function fetchReplies(accountId: string) {
    if (!accountId) return
    loading.value = true
    try {
      const { data, error } = await supabase
        .schema('threads')
        .from('replies')
        .select('id, author_username, text, replied_at, classification')
        .eq('account_id', accountId)
        .order('replied_at', { ascending: false })

      if (error) throw error
      if (data) replies.value = data
    } catch (err: any) {
      console.error('Error fetching replies:', err)
    } finally {
      loading.value = false
    }
  }

  async function fetchPendingReviews(accountId: string) {
    if (!accountId) return
    loading.value = true
    try {
      const { data, error } = await supabase
        .schema('threads')
        .from('auto_reply_logs')
        .select('id, reply_id, status, final_text, replies(author_username, text)')
        .eq('account_id', accountId)
        .eq('status', 'pending_review')

      if (error) throw error
      if (data) {
        reviewLogs.value = data.map((item: any) => ({
          id: item.id,
          reply_id: item.reply_id,
          status: item.status,
          final_text: item.final_text || '',
          reply: item.replies
        }))
      }
    } catch (err: any) {
      console.error('Error fetching review logs:', err)
    } finally {
      loading.value = false
    }
  }

  async function approveAndSendReply(logId: string, finalText: string) {
    loading.value = true
    try {
      const { error } = await supabase
        .schema('threads')
        .from('auto_reply_logs')
        .update({
          status: 'approved',
          final_text: finalText
        })
        .eq('id', logId)

      if (error) throw error
      reviewLogs.value = reviewLogs.value.filter(l => l.id !== logId)
      return { success: true }
    } catch (err: any) {
      console.error('Error approving reply:', err)
      alert('Error Approving Reply: ' + err.message)
      return { success: false, error: err.message }
    } finally {
      loading.value = false
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
