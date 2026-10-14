<template>
  <Card>
    <template #header>
      <h2 class="text-sm font-bold">Queue</h2>
    </template>
    <EmptyState title="Queue is empty" description="Scheduled posts akan tampil di sini setelah kamu menjadwalkan konten." />
  </Card>
</template>

<script setup lang="ts">
import { Card, EmptyState } from '../../components/ui'
</script>
