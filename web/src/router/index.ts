import { createRouter, createWebHistory } from 'vue-router'
import { supabase } from '../lib/supabase'

import LandingView from '../views/LandingView.vue'
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
import PrivacyView from '../views/PrivacyView.vue'
import TermsView from '../views/TermsView.vue'
import DataDeletionView from '../views/DataDeletionView.vue'

import PricingView from '../views/PricingView.vue'
import AdminLayout from '../views/admin/AdminLayout.vue'
import AdminOverview from '../views/admin/AdminOverview.vue'
import AdminUsers from '../views/admin/AdminUsers.vue'

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
    { path: '/', name: 'landing', component: LandingView },
    { path: '/login', name: 'login', component: LoginView },
    { path: '/update-password', name: 'update-password', component: UpdatePasswordView },
    { path: '/privacy', name: 'privacy', component: PrivacyView },
    { path: '/terms', name: 'terms', component: TermsView },
    { path: '/data-deletion', name: 'data-deletion', component: DataDeletionView },
    {
      path: '/admin',
      component: AdminLayout,
      meta: { requiresAuth: true, requiresAdmin: true },
      children: [
        { path: '', name: 'admin-overview', component: AdminOverview },
        { path: 'users', name: 'admin-users', component: AdminUsers },
      ]
    },
    { path: '/pricing', name: 'pricing', component: PricingView, meta: { requiresAuth: true } },

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
    { path: '/:pathMatch(.*)*', redirect: '/' },
  ],
})

router.beforeEach(async (to, _from, next) => {
  // 1. Cek apakah ini baru balik dari OAuth (ada token di URL)
  const isOAuthCallback = window.location.hash.includes('access_token') || window.location.search.includes('code=')

  if (isOAuthCallback) {
    // Kasih waktu Supabase JS buat nyedot token dari URL (0.5 detik)
    await new Promise(resolve => setTimeout(resolve, 500))
  }

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
