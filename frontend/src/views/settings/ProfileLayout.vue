<template>
  <div>
    <!-- ROOT: Vertical menu -->
    <div v-if="isRoot">
      <div class="mb-6">
        <h1 class="text-2xl font-bold tracking-tight">{{ $t('menu.profile') }}</h1>
        <p class="text-sm theme-text-muted mt-1">{{ $t('settings.subtitle') }}</p>
      </div>

      <div class="space-y-2">
        <RouterLink
          v-for="item in menuItems"
          :key="item.path"
          :to="item.path"
          class="card p-4 flex items-center justify-between hover:border-[var(--border-strong)] transition group"
        >
          <div class="flex items-center gap-3">
            <div class="w-9 h-9 rounded-lg flex items-center justify-center theme-bg-sec border theme-border">
              <component :is="item.icon" class="w-4 h-4 theme-text-muted" />
            </div>
            <div>
              <p class="text-sm font-bold">{{ $t(item.labelKey) }}</p>
              <p class="text-[11px] theme-text-muted">{{ $t(item.descKey) }}</p>
            </div>
          </div>
          <ChevronRight class="w-4 h-4 theme-text-muted opacity-50 group-hover:opacity-100 transition" />
        </RouterLink>
      </div>

      <button
        @click="handleLogout"
        type="button"
        class="w-full mt-6 py-3 px-4 rounded-lg border border-red-500/40 text-red-500 hover:bg-red-500/10 transition font-bold text-sm flex items-center justify-center gap-2"
      >
        <LogOut class="w-4 h-4" />
        Logout
      </button>
    </div>

    <!-- SUB-ROUTE: Back button + content -->
    <div v-else>
      <button
        @click="goBack"
        type="button"
        class="mb-4 -ml-2 flex items-center gap-1 px-2 py-1.5 rounded-md hover:theme-bg-hover transition theme-text-muted hover:theme-text text-sm font-medium"
      >
        <ChevronLeft class="w-4 h-4" />
        {{ $t('menu.profile') }}
      </button>
      <RouterView />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter, RouterView, RouterLink } from 'vue-router'
import { User, MessageSquare, LayoutTemplate, BookOpen, Bot, LogOut, ChevronRight, ChevronLeft } from 'lucide-vue-next'
import { supabase } from '../../lib/supabase'

const route = useRoute()
const router = useRouter()

const isRoot = computed(() => route.path === '/profile' || route.path === '/profile/')

const menuItems = [
  { path: '/profile/account', icon: User, labelKey: 'settings.tabs.account', descKey: 'profile.desc_account' },
  { path: '/profile/auto-reply', icon: MessageSquare, labelKey: 'settings.tabs.auto_reply', descKey: 'profile.desc_auto_reply' },
  { path: '/profile/templates', icon: LayoutTemplate, labelKey: 'settings.tabs.templates', descKey: 'profile.desc_templates' },
  { path: '/profile/knowledge', icon: BookOpen, labelKey: 'settings.tabs.knowledge', descKey: 'profile.desc_knowledge' },
  { path: '/profile/ai', icon: Bot, labelKey: 'settings.tabs.ai', descKey: 'profile.desc_ai' },
]

function goBack() {
  router.push('/profile')
}

async function handleLogout() {
  await supabase.auth.signOut()
  window.location.href = '/login'
}
</script>
