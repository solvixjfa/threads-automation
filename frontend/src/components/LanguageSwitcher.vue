<template>
  <div class="inline-flex rounded-lg overflow-hidden border theme-border">
    <button
      v-for="l in langs"
      :key="l.code"
      type="button"
      @click="changeLang(l.code)"
      class="px-3 py-1.5 text-xs font-bold transition"
      :class="locale === l.code ? 'bg-[var(--text)] text-[var(--bg)]' : 'theme-text-muted hover:theme-text'"
    >
      {{ l.label }}
    </button>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { locale } = useI18n()
const langs = [
  { code: 'en', label: 'EN' },
  { code: 'id', label: 'ID' },
]

function changeLang(code: string) {
  locale.value = code
  localStorage.setItem('app_lang', code)
}
</script>
