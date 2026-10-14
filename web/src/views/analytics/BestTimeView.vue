<template>
  <Card>
    <template #header>
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-sm font-bold">Best Time to Post</h2>
          <p class="text-xs theme-text-muted mt-0.5">Heatmap engagement rate per weekday dan hour</p>
        </div>
        <Badge variant="accent">Priority #1</Badge>
      </div>
    </template>
    <EmptyState title="Data belum tersedia" description="Heatmap akan muncul setelah backend endpoint /analytics/best-time siap." />
  </Card>
</template>

<script setup lang="ts">
import { Card, Badge, EmptyState } from '../../components/ui'
</script>
