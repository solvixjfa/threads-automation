import { createRouter, createWebHistory } from 'vue-router'
import { supabase } from '../lib/supabase'
import DashboardView from '../views/DashboardView.vue'
import ComposerView from '../views/ComposerView.vue'
import InboxView from '../views/InboxView.vue'
import SettingsView from '../views/SettingsView.vue'
import LoginView from '../views/LoginView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/login', name: 'login', component: LoginView },
    { path: '/', redirect: '/dashboard' },
    { path: '/dashboard', name: 'dashboard', component: DashboardView, meta: { requiresAuth: true } },
    { path: '/composer', name: 'composer', component: ComposerView, meta: { requiresAuth: true } },
    { path: '/inbox', name: 'inbox', component: InboxView, meta: { requiresAuth: true } },
    { path: '/settings', name: 'settings', component: SettingsView, meta: { requiresAuth: true } },
  ]
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
