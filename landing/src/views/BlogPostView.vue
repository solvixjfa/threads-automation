<template>
  <div class="min-h-screen bg-[var(--bg)] text-[var(--text)] font-sans">
    <AppNavbar />
    <main class="pt-32 pb-24 px-6 max-w-3xl mx-auto">
      <RouterLink to="/blog" class="inline-flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-[var(--muted)] hover:text-[var(--text)] mb-8 transition">
        &larr; {{ locale === 'id' ? 'Kembali ke Blog & Resources' : 'Back to Blog & Resources' }}
      </RouterLink>

      <article v-if="post" class="space-y-8">
        <header class="space-y-4 pb-8 border-b border-[var(--line)]">
          <div class="flex flex-wrap items-center gap-3 text-xs">
            <span class="font-mono font-bold uppercase px-2.5 py-1 rounded bg-[var(--surface-2)] text-[var(--text)]">
              {{ locale === 'id' ? post.category.id : post.category.en }}
            </span>
            <span class="text-[var(--muted)]">{{ locale === 'id' ? post.readTime.id : post.readTime.en }}</span>
            <span class="text-[var(--muted)]">• {{ post.date }}</span>
          </div>

          <h1 class="font-display text-4xl md:text-5xl leading-tight">
            {{ locale === 'id' ? post.title.id : post.title.en }}
          </h1>

          <p class="text-lg text-[var(--muted)] leading-relaxed">
            {{ locale === 'id' ? post.excerpt.id : post.excerpt.en }}
          </p>
        </header>

        <div class="space-y-10">
          <section v-for="(sec, idx) in post.sections" :key="idx" class="space-y-4">
            <h2 class="text-2xl font-bold tracking-tight">
              {{ locale === 'id' ? sec.heading.id : sec.heading.en }}
            </h2>

            <p
              v-for="(para, pIdx) in (locale === 'id' ? sec.body.id : sec.body.en)"
              :key="pIdx"
              class="text-base text-[var(--muted)] leading-relaxed"
            >
              {{ para }}
            </p>

            <!-- Copyable Template Box -->
            <div v-if="sec.copyBox" class="border border-[var(--line)] rounded-xl bg-[var(--surface)] overflow-hidden mt-4">
              <div class="flex items-center justify-between px-4 py-2.5 border-b border-[var(--line)] bg-[var(--surface-2)]">
                <span class="text-xs font-bold uppercase tracking-wider text-[var(--muted)]">
                  {{ locale === 'id' ? sec.copyBox.label.id : sec.copyBox.label.en }}
                </span>
                <button
                  @click="copySnippet(sec.copyBox.content, idx)"
                  type="button"
                  class="text-xs font-bold px-3 py-1 rounded-md bg-[var(--text)] text-[var(--bg)] hover:opacity-90 transition"
                >
                  {{ copiedIdx === idx ? (locale === 'id' ? 'Tersalin!' : 'Copied!') : (locale === 'id' ? 'Salin Teks' : 'Copy Text') }}
                </button>
              </div>
              <pre class="p-4 text-xs md:text-sm font-mono whitespace-pre-wrap leading-relaxed text-[var(--text)]">{{ sec.copyBox.content }}</pre>
            </div>
          </section>
        </div>

        <!-- Bottom CTA -->
        <div class="mt-14 p-8 rounded-2xl border border-[var(--text)] bg-[var(--surface)] flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div class="space-y-1">
            <h3 class="text-xl font-bold">
              {{ locale === 'id' ? 'Praktekin langsung di akun Threads kamu.' : 'Put this into action on your Threads account.' }}
            </h3>
            <p class="text-sm text-[var(--muted)]">
              {{ locale === 'id'
                ? 'Trial gratis 7 hari + 20 kredit AI (Gemini & Groq). Tanpa kartu kredit.'
                : '7-day free trial + 20 AI credits (Gemini & Groq). No credit card required.' }}
            </p>
          </div>
          <a href="https://app.ixiera.online/login" class="shrink-0 px-6 py-3 rounded-full text-sm font-bold bg-[var(--text)] text-[var(--bg)] hover:opacity-90 transition">
            {{ locale === 'id' ? 'Mulai Trial Gratis' : 'Start Free Trial' }}
          </a>
        </div>
      </article>

      <div v-else class="text-center py-20 space-y-4">
        <p class="text-xl font-bold">{{ locale === 'id' ? 'Artikel tidak ditemukan.' : 'Article not found.' }}</p>
        <RouterLink to="/blog" class="inline-block px-6 py-2.5 rounded-full text-sm font-bold bg-[var(--text)] text-[var(--bg)]">
          {{ locale === 'id' ? 'Lihat Semua Artikel' : 'Browse All Articles' }}
        </RouterLink>
      </div>
    </main>
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import AppNavbar from '../components/layouts/AppNavbar.vue'
import AppFooter from '../components/layouts/AppFooter.vue'
import { blogPosts } from '../data/blogPosts'

const route = useRoute()
const { locale } = useI18n({ useScope: 'global' })
const copiedIdx = ref<number | null>(null)

const post = computed(() => blogPosts.find(p => p.slug === route.params.slug))

async function copySnippet(text: string, idx: number) {
  try {
    await navigator.clipboard.writeText(text)
    copiedIdx.value = idx
    setTimeout(() => { copiedIdx.value = null }, 2000)
  } catch {
    // fallback ignore
  }
}
</script>
