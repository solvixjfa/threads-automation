import { ref } from 'vue'

type Theme = 'light' | 'dark'
const theme = ref<Theme>('light')
let initialized = false

function applyTheme(t: Theme) {
  const root = document.documentElement
  if (t === 'dark') root.classList.add('dark')
  else root.classList.remove('dark')
}

function initTheme() {
  if (initialized) return
  initialized = true
  const saved = localStorage.getItem('ixiera-theme') as Theme | null
  if (saved === 'dark' || saved === 'light') {
    theme.value = saved
  } else {
    theme.value = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
  }
  applyTheme(theme.value)
}

export function useTheme() {
  function toggle() {
    theme.value = theme.value === 'dark' ? 'light' : 'dark'
    localStorage.setItem('ixiera-theme', theme.value)
    applyTheme(theme.value)
  }
  return { theme, toggle, initTheme }
}
