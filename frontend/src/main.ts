import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createI18n } from 'vue-i18n'
import App from './App.vue'
import router from './router'
import './assets/main.css'
import './styles/theme.css'

import en from './locales/en.json'
import id from './locales/id.json'

try {
  const savedLang = localStorage.getItem('app_lang') || 'en'

  const i18n = createI18n({
    legacy: false,
    locale: savedLang,
    fallbackLocale: 'en',
    messages: { en, id },
    missingWarn: false,
    fallbackWarn: false,
    silentTranslationWarn: true,
    silentFallbackWarn: true
  })

  const app = createApp(App)

  // Nangkep error di dalam komponen Vue
  app.config.errorHandler = (err: any, instance, info) => {
    document.body.innerHTML = `
      <div style="padding: 20px; font-family: monospace; background: #000; color: #ff5555; min-height: 100vh;">
        <h1 style="color: #fff;">🚨 VUE COMPONENT CRASH 🚨</h1>
        <pre style="white-space: pre-wrap;">${err}\n\nInfo: ${info}</pre>
      </div>
    `
  }

  app.use(createPinia())
  app.use(router)
  app.use(i18n)
  app.mount('#app')

} catch (err: any) {
  // Nangkep error saat inisialisasi (misal i18n atau router gagal load)
  document.body.innerHTML = `
    <div style="padding: 20px; font-family: monospace; background: #000; color: #ff5555; min-height: 100vh;">
      <h1 style="color: #fff;">🚨 INIT CRASH 🚨</h1>
      <pre style="white-space: pre-wrap;">${err.message}\n\n${err.stack}</pre>
    </div>
  `
}
