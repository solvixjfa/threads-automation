import { createRouter, createWebHistory } from 'vue-router'
import { supabase } from '../lib/supabase'

import LandingView from '../views/LandingView.vue'
import PrivacyView from '../views/PrivacyView.vue'
import TermsView from '../views/TermsView.vue'
import DataDeletionView from '../views/DataDeletionView.vue'
import DashboardView from '../views/DashboardView.vue'
import SettingsLayout from '../views/settings/SettingsLayout.vue'
import AccountView from '../views/settings/AccountView.vue'
import AutoReplyView from '../views/settings/AutoReplyView.vue'
import TemplateView from '../views/settings/TemplateView.vue'
import KnowledgeView from '../views/settings/KnowledgeView.vue'
import AiView from '../views/settings/AiView.vue'
import LoginView from '../views/LoginView.vue'
import UpdatePasswordView from '../views/UpdatePasswordView.vue'
import ComposerView from '../views/ComposerView.vue'
import RepurposeView from '../views/RepurposeView.vue'
import InboxView from '../views/InboxView.vue'

import ContentLayout from '../views/content/ContentLayout.vue'
import QueueView from '../views/content/QueueView.vue'

import AnalyticsLayout from '../views/analytics/AnalyticsLayout.vue'
import BestTimeView from '../views/analytics/BestTimeView.vue'
import HookView from '../views/analytics/HookView.vue'
import LengthView from '../views/analytics/LengthView.vue'
import TopicView from '../views/analytics/TopicView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    // LANDING PAGE DI ROOT
    { path: '/', name: 'landing', component: LandingView },
    { path: '/privacy', name: 'privacy', component: PrivacyView },
    { path: '/terms', name: 'terms', component: TermsView },
    { path: '/data-deletion', name: 'data-deletion', component: DataDeletionView },
    
    { path: '/login', name: 'login', component: LoginView },
    { path: '/update-password', name: 'update-password', component: UpdatePasswordView },

    { path: '/dashboard', name: 'dashboard', component: DashboardView, meta: { requiresAuth: true } },

    {
      path: '/content',
      component: ContentLayout,
      meta: { requiresAuth: true },
      children: [
        { path: '', redirect: '/content/create' },
        { path: 'create', name: 'content-create', component: ComposerView },
        { path: 'variant', name: 'content-variant', component: RepurposeView },
        { path: 'queue', name: 'content-queue', component: QueueView },
      ],
    },

    { path: '/comment', name: 'comment', component: InboxView, meta: { requiresAuth: true } },

    {
      path: '/analytics',
      component: AnalyticsLayout,
      meta: { requiresAuth: true },
      children: [
        { path: '', redirect: '/analytics/best-time' },
        { path: 'best-time', name: 'analytics-best-time', component: BestTimeView },
        { path: 'hook', name: 'analytics-hook', component: HookView },
        { path: 'length', name: 'analytics-length', component: LengthView },
        { path: 'topic', name: 'analytics-topic', component: TopicView },
      ],
    },

    {
      path: '/settings',
      component: SettingsLayout,
      meta: { requiresAuth: true },
      children: [
        { path: '', redirect: '/settings/account' },
        { path: 'account', name: 'settings-account', component: AccountView },
        { path: 'auto-reply', name: 'settings-auto-reply', component: AutoReplyView },
        { path: 'templates', name: 'settings-templates', component: TemplateView },
        { path: 'knowledge', name: 'settings-knowledge', component: KnowledgeView },
        { path: 'ai', name: 'settings-ai', component: AiView },
      ],
    },

    // Legacy redirects
    { path: '/composer', redirect: '/content/create' },
    { path: '/repurpose', redirect: '/content/variant' },
    { path: '/inbox', redirect: '/comment' },

    { path: '/:pathMatch(.*)*', redirect: '/' },
  ],
})

// ROUTER GUARD: Redirect user yang udah login dari landing/login ke dashboard
router.beforeEach(async (to, _from, next) => {
  const { data: { session } } = await supabase.auth.getSession()

  if (to.meta.requiresAuth && !session) {
    next('/login')
  } else if ((to.path === '/login' || to.path === '/') && session) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
