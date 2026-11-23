import { createRouter, createWebHistory } from 'vue-router'
import LandingView from '../views/LandingView.vue'
import FeaturesView from '../views/FeaturesView.vue'
import HowItWorksView from '../views/HowItWorksView.vue'
import FaqView from '../views/FaqView.vue'
import PricingView from '../views/PricingView.vue'
import PrivacyView from '../views/PrivacyView.vue'
import TermsView from '../views/TermsView.vue'
import DataDeletionView from '../views/DataDeletionView.vue'
import FeatureDetailView from '../views/FeatureDetailView.vue'

const router = createRouter({
  history: createWebHistory(),
  scrollBehavior(to, from, savedPosition) {
    if (to.hash) return { el: to.hash, behavior: 'smooth' }
    return { top: 0 }
  },
  routes: [
    { path: '/', name: 'landing', component: LandingView },
    { path: '/features', name: 'features', component: FeaturesView },
    { path: '/features/:slug', name: 'feature-detail', component: FeatureDetailView },
    { path: '/how-it-works', name: 'how-it-works', component: HowItWorksView },
    { path: '/faq', name: 'faq', component: FaqView },
    { path: '/pricing', name: 'pricing', component: PricingView },
    { path: '/privacy', name: 'privacy', component: PrivacyView },
    { path: '/terms', name: 'terms', component: TermsView },
    { path: '/data-deletion', name: 'data-deletion', component: DataDeletionView },
  ]
})
export default router
