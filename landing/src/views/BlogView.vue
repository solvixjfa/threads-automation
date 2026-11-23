<template>
  <div class="min-h-screen bg-[var(--bg)] text-[var(--text)] font-sans">
    <AppNavbar />
    <main class="pt-32 pb-24 px-6 max-w-[1120px] mx-auto">
      <div class="max-w-2xl mb-12">
        <div class="inline-flex items-center px-3 py-1 rounded-full border border-[var(--line)] text-xs font-bold tracking-widest text-[var(--muted)] uppercase mb-4">
          {{ locale === 'id' ? 'PLAYBOOK & RESOURCES' : 'PLAYBOOK & RESOURCES' }}
        </div>
        <h1 class="font-display text-5xl md:text-6xl mb-4">
          {{ locale === 'id' ? 'Panduan & template ' : 'Guides & templates ' }}
          <span class="italic">{{ locale === 'id' ? 'siap pakai.' : 'ready to deploy.' }}</span>
        </h1>
        <p class="text-lg text-[var(--muted)] leading-relaxed">
          {{ locale === 'id'
            ? 'Strategi pertumbuhan organik, framework copywriting, dan kumpulan prompt yang bisa langsung kamu tempel ke Ixiera.'
            : 'Organic growth playbooks, copywriting frameworks, and prompt templates ready to paste directly into Ixiera.' }}
        </p>
      </div>

      <!-- Filter Tabs -->
      <div class="flex flex-wrap gap-2 mb-10 pb-6 border-b border-[var(--line)]">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          @click="activeTab = tab.key"
          class="px-4 py-2 rounded-full text-xs font-bold uppercase tracking-wider border transition"
          :class="activeTab === tab.key
            ? 'bg-[var(--text)] text-[var(--bg)] border-[var(--text)]'
            : 'border-[var(--line)] text-[var(--muted)] hover:text-[var(--text)] hover:bg-[var(--surface-2)]'"
        >
          {{ locale === 'id' ? tab.id : tab.en }}
        </button>
      </div>

      <!-- Grid Articles -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <RouterLink
          v-for="post in filteredPosts"
          :key="post.slug"
          :to="`/blog/${post.slug}`"
          class="border rounded-2xl p-8 bg-[var(--surface)] hover:border-[var(--text)] transition flex flex-col justify-between group"
          :class="post.isResource ? 'border-[var(--text)]' : 'border-[var(--line)]'"
        >
          <div>
            <div class="flex items-center justify-between gap-2 text-xs mb-5">
              <span
                class="font-mono font-bold uppercase tracking-wider px-2.5 py-1 rounded"
                :class="post.isResource ? 'bg-[var(--text)] text-[var(--bg)]' : 'bg-[var(--surface-2)] text-[var(--muted)]'"
              >
                {{ locale === 'id' ? post.category.id : post.category.en }}
              </span>
              <span class="text-[var(--muted)]">{{ locale === 'id' ? post.readTime.id : post.readTime.en }}</span>
            </div>

            <h2 class="text-2xl font-bold leading-snug mb-3 group-hover:underline underline-offset-4">
              {{ locale === 'id' ? post.title.id : post.title.en }}
            </h2>

            <p class="text-sm text-[var(--muted)] leading-relaxed">
              {{ locale === 'id' ? post.excerpt.id : post.excerpt.en }}
            </p>
          </div>

          <div class="mt-8 pt-4 border-t border-[var(--line)] flex items-center justify-between text-xs font-bold">
            <span>{{ post.isResource ? (locale === 'id' ? 'Buka & Salin Template' : 'Open & Copy Templates') : (locale === 'id' ? 'Baca Panduan Lengkap' : 'Read Full Guide') }}</span>
            <span>&rarr;</span>
          </div>
        </RouterLink>
      </div>
    </main>
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useI18n } from 'vue-i18n'
import AppNavbar from '../components/layouts/AppNavbar.vue'
import AppFooter from '../components/layouts/AppFooter.vue'
import { blogPosts } from '../data/blogPosts'

const { locale } = useI18n({ useScope: 'global' })
const activeTab = ref<'all' | 'growth' | 'copywriting' | 'resource'>('all')

const tabs = [
  { key: 'all' as const, id: 'Semua', en: 'All' },
  { key: 'growth' as const, id: 'Algoritma & Growth', en: 'Algorithm & Growth' },
  { key: 'copywriting' as const, id: 'Copywriting & Jualan', en: 'Copywriting & Sales' },
  { key: 'resource' as const, id: 'Free Resource & Prompt', en: 'Free Resources & Prompts' }
]

const filteredPosts = computed(() => {
  if (activeTab.value === 'all') return blogPosts
  return blogPosts.filter(p => p.tag === activeTab.value)
})
</script>
