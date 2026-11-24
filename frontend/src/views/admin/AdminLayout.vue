<template>
  <div class="min-h-[100dvh] flex bg-[var(--bg-sec)] theme-text">

    <!-- DESKTOP SIDEBAR -->
    <aside class="w-64 border-r theme-border bg-[var(--bg)] hidden md:flex flex-col shrink-0 h-[100dvh] sticky top-0">
      <div class="h-16 flex items-center justify-between px-6 border-b theme-border">
        <div>
          <span class="font-black text-base tracking-widest uppercase block leading-none">Ixiera<span class="text-[var(--accent)]">.</span></span>
          <span class="text-[10px] font-bold uppercase tracking-wider theme-text-muted mt-1 block">Admin & CRM</span>
        </div>
      </div>

      <nav class="flex-1 p-4 space-y-6 overflow-y-auto">
        <!-- GROUP 1: PLATFORM -->
        <div class="space-y-1">
          <div class="px-3 pb-1.5 text-[10px] font-bold uppercase tracking-widest theme-text-muted">
            Platform
          </div>
          <RouterLink
            to="/admin"
            exact-active-class="bg-[var(--bg-sec)] font-bold theme-text border theme-border"
            class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm theme-text-muted hover:theme-text hover:bg-[var(--bg-sec)] transition-colors"
          >
            <BarChart3 class="w-4 h-4 shrink-0" />
            <span>Overview</span>
          </RouterLink>
          <RouterLink
            to="/admin/users"
            active-class="bg-[var(--bg-sec)] font-bold theme-text border theme-border"
            class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm theme-text-muted hover:theme-text hover:bg-[var(--bg-sec)] transition-colors"
          >
            <Users class="w-4 h-4 shrink-0" />
            <span>Users & Plans</span>
          </RouterLink>
        </div>

        <!-- GROUP 2: SALES & CRM -->
        <div class="space-y-1">
          <div class="px-3 pb-1.5 text-[10px] font-bold uppercase tracking-widest theme-text-muted">
            Sales & Outreach CRM
          </div>
          <RouterLink
            to="/admin/crm"
            exact-active-class="bg-[var(--bg-sec)] font-bold theme-text border theme-border"
            class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm theme-text-muted hover:theme-text hover:bg-[var(--bg-sec)] transition-colors"
          >
            <MessageSquare class="w-4 h-4 shrink-0" />
            <span>Pipeline Leads</span>
          </RouterLink>
          <RouterLink
            to="/admin/templates"
            active-class="bg-[var(--bg-sec)] font-bold theme-text border theme-border"
            class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm theme-text-muted hover:theme-text hover:bg-[var(--bg-sec)] transition-colors"
          >
            <FileText class="w-4 h-4 shrink-0" />
            <span>Outreach Templates</span>
          </RouterLink>
          <RouterLink
            to="/admin/analytics"
            active-class="bg-[var(--bg-sec)] font-bold theme-text border theme-border"
            class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm theme-text-muted hover:theme-text hover:bg-[var(--bg-sec)] transition-colors"
          >
            <TrendingUp class="w-4 h-4 shrink-0" />
            <span>Sales Analytics</span>
          </RouterLink>
        </div>
      </nav>

      <div class="p-4 border-t theme-border">
        <RouterLink
          to="/dashboard"
          class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-bold theme-text-muted hover:theme-text hover:bg-[var(--bg-sec)] transition-colors"
        >
          <ArrowLeft class="w-4 h-4 shrink-0" />
          <span>Kembali ke App</span>
        </RouterLink>
      </div>
    </aside>

    <!-- MOBILE DRAWER SIDEBAR -->
    <Teleport to="body">
      <div v-if="drawerOpen" class="fixed inset-0 z-[90] md:hidden flex">
        <!-- Backdrop -->
        <div
          @click="drawerOpen = false"
          class="fixed inset-0 bg-black/60 backdrop-blur-xs transition-opacity"
        ></div>

        <!-- Drawer Panel -->
        <aside class="relative w-72 max-w-[82vw] bg-[var(--bg)] border-r theme-border h-[100dvh] flex flex-col z-10 shadow-2xl">
          <div class="h-14 flex items-center justify-between px-5 border-b theme-border shrink-0">
            <div>
              <span class="font-black text-base tracking-widest uppercase block leading-none">Ixiera<span class="text-[var(--accent)]">.</span></span>
              <span class="text-[10px] font-bold uppercase tracking-wider theme-text-muted mt-0.5 block">Admin & CRM</span>
            </div>
            <button
              @click="drawerOpen = false"
              class="p-2 rounded-lg theme-text-muted hover:theme-text hover:bg-[var(--bg-sec)]"
              aria-label="Tutup menu"
            >
              <X class="w-5 h-5" />
            </button>
          </div>

          <nav class="flex-1 p-4 space-y-6 overflow-y-auto">
            <!-- GROUP 1: PLATFORM -->
            <div class="space-y-1.5">
              <div class="px-3 pb-1 text-[10px] font-bold uppercase tracking-widest theme-text-muted">
                Platform
              </div>
              <RouterLink
                to="/admin"
                @click="drawerOpen = false"
                exact-active-class="bg-[var(--bg-sec)] font-bold theme-text border theme-border"
                class="flex items-center gap-3 px-3.5 py-3 rounded-xl text-sm theme-text-muted hover:theme-text transition-colors"
              >
                <BarChart3 class="w-4 h-4 shrink-0" />
                <span>Overview</span>
              </RouterLink>
              <RouterLink
                to="/admin/users"
                @click="drawerOpen = false"
                active-class="bg-[var(--bg-sec)] font-bold theme-text border theme-border"
                class="flex items-center gap-3 px-3.5 py-3 rounded-xl text-sm theme-text-muted hover:theme-text transition-colors"
              >
                <Users class="w-4 h-4 shrink-0" />
                <span>Users & Plans</span>
              </RouterLink>
            </div>

            <!-- GROUP 2: SALES & CRM -->
            <div class="space-y-1.5">
              <div class="px-3 pb-1 text-[10px] font-bold uppercase tracking-widest theme-text-muted">
                Sales & Outreach CRM
              </div>
              <RouterLink
                to="/admin/crm"
                @click="drawerOpen = false"
                exact-active-class="bg-[var(--bg-sec)] font-bold theme-text border theme-border"
                class="flex items-center gap-3 px-3.5 py-3 rounded-xl text-sm theme-text-muted hover:theme-text transition-colors"
              >
                <MessageSquare class="w-4 h-4 shrink-0" />
                <span>Pipeline Leads</span>
              </RouterLink>
              <RouterLink
                to="/admin/templates"
                @click="drawerOpen = false"
                active-class="bg-[var(--bg-sec)] font-bold theme-text border theme-border"
                class="flex items-center gap-3 px-3.5 py-3 rounded-xl text-sm theme-text-muted hover:theme-text transition-colors"
              >
                <FileText class="w-4 h-4 shrink-0" />
                <span>Outreach Templates</span>
              </RouterLink>
              <RouterLink
                to="/admin/analytics"
                @click="drawerOpen = false"
                active-class="bg-[var(--bg-sec)] font-bold theme-text border theme-border"
                class="flex items-center gap-3 px-3.5 py-3 rounded-xl text-sm theme-text-muted hover:theme-text transition-colors"
              >
                <TrendingUp class="w-4 h-4 shrink-0" />
                <span>Sales Analytics</span>
              </RouterLink>
            </div>
          </nav>

          <div class="p-4 border-t theme-border shrink-0">
            <RouterLink
              to="/dashboard"
              @click="drawerOpen = false"
              class="flex items-center gap-3 px-3.5 py-3 rounded-xl text-xs font-bold theme-text-muted hover:theme-text bg-[var(--bg-sec)]"
            >
              <ArrowLeft class="w-4 h-4 shrink-0" />
              <span>Kembali ke App Utama</span>
            </RouterLink>
          </div>
        </aside>
      </div>
    </Teleport>

    <!-- MAIN CONTENT AREA -->
    <main class="flex-1 min-w-0 h-[100dvh] overflow-y-auto flex flex-col">

      <!-- MOBILE TOP BAR -->
      <header class="md:hidden h-14 border-b theme-border bg-[var(--bg)] sticky top-0 z-20 shrink-0 px-4 flex items-center justify-between gap-3">
        <div class="flex items-center gap-3 min-w-0">
          <button
            @click="drawerOpen = true"
            class="p-2 -ml-2 rounded-lg border theme-border bg-[var(--bg-sec)] theme-text active:scale-95 transition-transform"
            aria-label="Buka sidebar"
          >
            <Menu class="w-5 h-5" />
          </button>
          <div class="min-w-0">
            <div class="text-[10px] font-bold uppercase tracking-wider theme-text-muted leading-none">
              {{ currentGroupLabel }}
            </div>
            <div class="text-sm font-black truncate mt-0.5">
              {{ currentPageTitle }}
            </div>
          </div>
        </div>

        <RouterLink
          to="/dashboard"
          class="text-xs font-bold px-2.5 py-1.5 rounded-lg border theme-border theme-text-muted hover:theme-text shrink-0"
        >
          App
        </RouterLink>
      </header>

      <div class="p-4 md:p-8 max-w-5xl w-full mx-auto pb-24 flex-1">
        <RouterView />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { RouterView, RouterLink, useRoute } from 'vue-router'
import {
  BarChart3, Users, MessageSquare, FileText,
  TrendingUp, ArrowLeft, Menu, X
} from 'lucide-vue-next'

const route = useRoute()
const drawerOpen = ref(false)

watch(() => route.fullPath, () => {
  drawerOpen.value = false
})

const currentGroupLabel = computed(() => {
  if (route.path.startsWith('/admin/crm') || route.path.startsWith('/admin/templates') || route.path.startsWith('/admin/analytics')) {
    return 'Sales & CRM'
  }
  return 'Admin Platform'
})

const currentPageTitle = computed(() => {
  if (route.path === '/admin/users') return 'Users & Plans'
  if (route.path === '/admin/crm') return 'Pipeline Leads'
  if (route.path === '/admin/templates') return 'Outreach Templates'
  if (route.path === '/admin/analytics') return 'Sales Analytics'
  return 'Overview'
})
</script>
