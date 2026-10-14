import { createRouter, createWebHistory } from 'vue-router'
import { supabase } from '../lib/supabase'

import DashboardView from '../views/DashboardView.vue'
import SettingsView from '../views/SettingsView.vue'
import LoginView from '../views/LoginView.vue'
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
    { path: '/login', name: 'login', component: LoginView },
    { path: '/', redirect: '/dashboard' },

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

    { path: '/settings', name: 'settings', component: SettingsView, meta: { requiresAuth: true } },

    // Legacy redirects
    { path: '/composer', redirect: '/content/create' },
    { path: '/repurpose', redirect: '/content/variant' },
    { path: '/inbox', redirect: '/comment' },

    { path: '/:pathMatch(.*)*', redirect: '/dashboard' },
  ],
})

router.beforeEach(async (to, _from, next) => {
  const { data: { session } } = await supabase.auth.getSession()

  if (to.meta.requiresAuth && !session) {
    next('/login')
  } else if (to.path === '/login' && session) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
