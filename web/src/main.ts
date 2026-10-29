import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createI18n } from 'vue-i18n'
import App from './App.vue'
import router from './router'
import './assets/main.css'
import './styles/theme.css'

import en from './locales/en.json'
import id from './locales/id.json'

// FUNGSI BUAT NAMPILIN ERROR DI LAYAR HP
function showErrorOnScreen(errorMsg: string) {
  document.body.innerHTML = `
    <div style="padding: 20px; font-family: monospace; background: #000; color: #ff5555; min-height: 100vh; display: flex; flex-direction: column;">
      <h1 style="color: #fff; font-size: 20px; margin-bottom: 10px;">🚨 APP CRASHED 🚨</h1>
      <p style="color: #aaa; font-size: 12px; margin-bottom: 10px;">Screenshot layar ini dan kirim ke developer:</p>
      <pre style="white-space: pre-wrap; word-wrap: break-word; background: #222; padding: 15px; border-radius: 8px; font-size: 11px; color: #ff9999;">${errorMsg}</pre>
    </div>
  `;
}

try {
  const savedLang = localStorage.getItem('app_lang') || 'en'

  const i18n = createI18n({
    legacy: false,
    locale: savedLang,
    fallbackLocale: 'en',
    messages: { en, id }
  })

  const app = createApp(App)

  // Nangkep error di dalam komponen Vue
  app.config.errorHandler = (err: any, instance, info) => {
    console.error(err)
    showErrorOnScreen(`Vue Component Error:\n${err}\n\nInfo: ${info}`)
  }

  app.use(createPinia())
  app.use(router)
  app.use(i18n)
  app.mount('#app')

} catch (err: any) {
  // Nangkep error saat inisialisasi (misal i18n gagal load)
  console.error(err)
  showErrorOnScreen(`Init Error:\n${err.message || err}\n\nStack:\n${err.stack || ''}`)
}
