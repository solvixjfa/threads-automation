<template>
  <div class="min-h-screen bg-black text-white font-sans selection:bg-white selection:text-black flex">
    
    <!-- Mobile Sidebar Overlay -->
    <div 
      v-if="isSidebarOpen" 
      @click="isSidebarOpen = false"
      class="fixed inset-0 bg-black/70 backdrop-blur-md z-40 md:hidden"
    ></div>

    <!-- Sidebar (Glossy Black/White Minimalist) -->
    <aside 
      :class="[
        isSidebarOpen ? 'translate-x-0' : '-translate-x-full',
        'fixed inset-y-0 left-0 z-50 w-64 bg-black/80 backdrop-blur-xl border-r border-white/10 transition-transform duration-300 ease-in-out md:relative md:translate-x-0 flex flex-col'
      ]"
    >
      <!-- Brand Logo Area -->
      <div class="flex items-center h-20 px-6 border-b border-white/10">
        <div class="w-8 h-8 bg-white text-black font-extrabold flex items-center justify-center rounded text-sm tracking-wider mr-3">IX</div>
        <span class="font-bold tracking-tight text-lg text-white">ixiera.id</span>
      </div>

      <!-- Navigation Links -->
      <nav class="flex-1 px-4 py-6 space-y-1.5 overflow-y-auto">
        <RouterLink 
          v-for="item in navigation" 
          :key="item.name" 
          :to="item.path"
          @click="isSidebarOpen = false"
          :class="[
            route.path === item.path ? 'bg-white text-black font-semibold shadow-[0_0_20px_rgba(255,255,255,0.2)]' : 'text-zinc-400 hover:bg-white/10 hover:text-white',
            'flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 text-sm'
          ]"
        >
          <component :is="item.icon" class="w-4 h-4 shrink-0" />
          <span>{{ item.name }}</span>
        </RouterLink>
      </nav>

      <!-- Footer Info -->
      <div class="p-4 border-t border-white/10 text-xs text-zinc-500">
        <span>Threads System v1.0</span>
      </div>
    </aside>

    <!-- Main Content Area -->
    <main class="flex-1 flex flex-col min-w-0 h-screen overflow-hidden">
      <!-- Mobile Top Header -->
      <header class="md:hidden flex items-center justify-between h-16 px-4 bg-black/80 backdrop-blur-md border-b border-white/10 z-30">
        <div class="flex items-center gap-2">
          <div class="w-6 h-6 bg-white text-black font-extrabold flex items-center justify-center rounded text-xs">IX</div>
          <span class="font-bold text-sm tracking-tight">ixiera.id</span>
        </div>
        <button @click="isSidebarOpen = !isSidebarOpen" class="p-2 bg-white/5 hover:bg-white/10 rounded-md text-white border border-white/10 transition">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
          </svg>
        </button>
      </header>

      <!-- View Router Container -->
      <div class="flex-1 overflow-y-auto p-6 md:p-10 bg-black">
        <RouterView />
      </div>
    </main>

  </div>
</template>

<script setup lang="ts">
import { ref, h } from 'vue'
import { RouterView, RouterLink, useRoute } from 'vue-router'

const route = useRoute()
const isSidebarOpen = ref(false)

// SVG Icons (Tanpa Emoticon)
const LayoutDashboardIcon = () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z' })
])

const EditIcon = () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z' })
])

const InboxIcon = () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4' })
])

const SettingsIcon = () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z' }),
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M15 12a3 3 0 11-6 0 3 3 0 016 0z' })
])

const navigation = [
  { name: 'Dashboard', path: '/', icon: LayoutDashboardIcon },
  { name: 'Composer', path: '/composer', icon: EditIcon },
  { name: 'Inbox & Auto-Reply', path: '/inbox', icon: InboxIcon },
  { name: 'Settings', path: '/settings', icon: SettingsIcon },
]
</script>
