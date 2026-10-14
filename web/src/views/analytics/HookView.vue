<template>
  <Card>
    <template #header>
      <h2 class="text-sm font-bold">Hook Performance</h2>
      <p class="text-xs theme-text-muted mt-0.5">Analisis efektivitas tipe hook pada baris pertama post</p>
    </template>
    <EmptyState title="Coming soon" description="Analisis tipe hook: Number/How-To, Warning, Curiosity, Personal Story, Topic." />
  </Card>
</template>

<script setup lang="ts">
import { Card, EmptyState } from '../../components/ui'
</script>
