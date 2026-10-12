import { createRouter, createWebHistory } from 'vue-router'
import { supabase } from '../lib/supabase'
import DashboardLayout from '../components/DashboardLayout.vue'
import DashboardView from '../views/DashboardView.vue'
import ComposerView from '../views/ComposerView.vue'
import InboxView from '../views/InboxView.vue'
import SettingsView from '../views/SettingsView.vue'
import LoginView from '../views/LoginView.vue'
import RepurposeView from '../views/RepurposeView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/login', name: 'login', component: LoginView },
    { 
      path: '/', 
      component: DashboardLayout,
      meta: { requiresAuth: true },
      children: [
        { path: '', redirect: '/dashboard' },
        { path: 'dashboard', name: 'dashboard', component: DashboardView },
        { path: 'composer', name: 'composer', component: ComposerView },
        { path: 'inbox', name: 'inbox', component: InboxView },
        { path: 'repurpose', name: 'repurpose', component: RepurposeView },
        { path: 'settings', name: 'settings', component: SettingsView },
      ]
    }
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
