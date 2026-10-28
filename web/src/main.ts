import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createI18n } from 'vue-i18n'
import App from './App.vue'
import router from './router'
import './assets/main.css'
import './styles/theme.css'

// Import kamus bahasa
import en from './locales/en.json'
import id from './locales/id.json'

// Ambil bahasa dari localStorage, atau default ke 'en'
const savedLang = localStorage.getItem('app_lang') || 'en'

const i18n = createI18n({
  legacy: false, // Wajib false buat Vue 3 Composition API
  locale: savedLang,
  fallbackLocale: 'en',
  messages: { en, id }
})

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(i18n)
app.mount('#app')
