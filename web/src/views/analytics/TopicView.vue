<template>
  <Card>
    <template #header>
      <h2 class="text-sm font-bold">Topic Clusters</h2>
      <p class="text-xs theme-text-muted mt-0.5">Klaster topik otomatis dari konten kamu</p>
    </template>
    <EmptyState title="Coming soon" description="Clustering topik menggunakan TF-IDF dan KMeans dari data posts." />
  </Card>
</template>

<script setup lang="ts">
import { Card, EmptyState } from '../../components/ui'
</script>
