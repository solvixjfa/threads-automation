<template>
  <Card>
    <template #header>
      <h2 class="text-sm font-bold">Content Length</h2>
      <p class="text-xs theme-text-muted mt-0.5">Hubungan panjang teks dengan engagement rate</p>
    </template>
    <EmptyState title="Coming soon" description="Rekomendasi panjang teks optimal berdasarkan data historis." />
  </Card>
</template>

<script setup lang="ts">
import { Card, EmptyState } from '../../components/ui'
</script>
