<template>
  <div class="flex items-center gap-2">
    <select v-model="currentLang" @change="changeLang" class="input text-xs py-1 px-2">
      <option value="en">English</option>
      <option value="id">Indonesia</option>
    </select>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'

const { locale } = useI18n()
const currentLang = ref(locale.value)

function changeLang() {
  locale.value = currentLang.value
  localStorage.setItem('app_lang', currentLang.value)
}
</script>
