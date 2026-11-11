import { createRouter, createWebHistory } from 'vue-router'
import LandingView from '../views/LandingView.vue'
import PricingView from '../views/PricingView.vue'
import FeaturesView from '../views/FeaturesView.vue'
import PrivacyView from '../views/PrivacyView.vue'
import TermsView from '../views/TermsView.vue'
import DataDeletionView from '../views/DataDeletionView.vue'

const router = createRouter({
  history: createWebHistory(),
  scrollBehavior(to, from, savedPosition) {
    if (to.hash) {
      return { el: to.hash, behavior: 'smooth' }
    }
    return { top: 0 }
  },
  routes: [
    { path: '/', name: 'landing', component: LandingView },
    { path: '/pricing', name: 'pricing', component: PricingView },
    { path: '/features', name: 'features', component: FeaturesView },
    { path: '/privacy', name: 'privacy', component: PrivacyView },
    { path: '/terms', name: 'terms', component: TermsView },
    { path: '/data-deletion', name: 'data-deletion', component: DataDeletionView },
  ]
})

export default router
