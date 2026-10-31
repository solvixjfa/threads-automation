<template>
  <div class="min-h-[100dvh] flex bg-[var(--bg-sec)] theme-text">
    
    <!-- ADMIN SIDEBAR (Bisa disembunyiin di mobile) -->
    <aside class="w-64 border-r theme-border bg-[var(--bg)] flex-col hidden md:flex shrink-0 h-[100dvh] sticky top-0">
      <div class="h-16 flex items-center px-6 border-b theme-border">
        <span class="font-black text-lg tracking-widest uppercase">Admin<span class="text-[var(--accent)]">.</span></span>
      </div>
      
      <nav class="flex-1 p-4 space-y-2">
        <RouterLink to="/admin" exact-active-class="bg-[var(--bg-sec)] font-bold" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm theme-text-muted hover:theme-text transition-colors">
          <BarChart3 class="w-4 h-4" /> Overview
        </RouterLink>
        <RouterLink to="/admin/users" active-class="bg-[var(--bg-sec)] font-bold" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm theme-text-muted hover:theme-text transition-colors">
          <Users class="w-4 h-4" /> Users
        </RouterLink>
      </nav>

      <div class="p-4 border-t theme-border space-y-2">
        <RouterLink to="/dashboard" class="flex items-center gap-3 px-3 py-2 text-xs font-bold theme-text-muted hover:theme-text">
          <ArrowLeft class="w-4 h-4" /> Balik ke App
        </RouterLink>
      </div>
    </aside>

    <!-- MAIN CONTENT ADMIN -->
    <main class="flex-1 h-[100dvh] overflow-y-auto">
      <!-- Header Mobile -->
      <header class="md:hidden h-16 flex items-center justify-between px-4 border-b theme-border bg-[var(--bg)] sticky top-0 z-20">
        <span class="font-black tracking-widest uppercase">Admin Panel</span>
        <RouterLink to="/dashboard" class="text-xs font-bold underline text-[var(--accent)]">Back to App</RouterLink>
      </header>
      
      <div class="p-4 md:p-8 max-w-6xl mx-auto pb-20">
        <RouterView />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { RouterView, RouterLink } from 'vue-router'
import { BarChart3, Users, ArrowLeft } from 'lucide-vue-next'
</script>
