import { defineStore } from 'pinia'
import { ref } from 'vue'
import { supabase } from '../lib/supabase'

export interface ScheduledPost {
  id?: string
  account_id: string
  text: string
  scheduled_for: string
  status?: string
}

export interface ScoreResult {
  score: number
  breakdown: Record<string, any>
  suggestions: string[]
}

export const useComposerStore = defineStore('composer', () => {
  const loading = ref(false)
  const scoring = ref(false)
  const lastScore = ref<ScoreResult | null>(null)
  const scheduledPosts = ref<ScheduledPost[]>([])

  async function scoreDraft(text: string, accountId: string) {
    if (!text.trim()) return
    scoring.value = true
    lastScore.value = null

    try {
      const { data, error } = await supabase.functions.invoke('score-draft', {
        body: { text, account_id: accountId }
      })

      if (error) throw error
      if (data?.result) {
        lastScore.value = {
          score: data.result.score,
          breakdown: data.result.breakdown || {},
          suggestions: data.result.suggestions || []
        }
      }
    } catch (err: any) {
      console.error('Error scoring draft:', err)
    } finally {
      scoring.value = false
    }
  }

  async function createScheduledPost(post: ScheduledPost) {
    loading.value = true
    try {
      const { data, error } = await supabase
        .schema('threads')
        .from('scheduled_posts')
        .insert({
          account_id: post.account_id,
          text: post.text,
          scheduled_for: post.scheduled_for,
          status: 'scheduled'
        })
        .select('*')
        .single()

      if (error) throw error
      if (data) {
        scheduledPosts.value.unshift(data)
      }
      return { success: true }
    } catch (err: any) {
      console.error('Error scheduling post:', err)
      return { success: false, error: err.message }
    } finally {
      loading.value = false
    }
  }

  async function fetchScheduledPosts(accountId: string) {
    loading.value = true
    try {
      const { data, error } = await supabase
        .schema('threads')
        .from('scheduled_posts')
        .select('*')
        .eq('account_id', accountId)
        .order('scheduled_for', { ascending: true })

      if (error) throw error
      if (data) {
        scheduledPosts.value = data
      }
    } catch (err: any) {
      console.error('Error fetching posts:', err)
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    scoring,
    lastScore,
    scheduledPosts,
    scoreDraft,
    createScheduledPost,
    fetchScheduledPosts
  }
})
