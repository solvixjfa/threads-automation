<template>
  <div class="space-y-8">
    <div>
      <h1 class="text-2xl font-bold text-zinc-900 tracking-tight">Analytics & Overview</h1>
      <p class="text-zinc-500 text-sm mt-1">Ringkasan performa postingan dan metrik akun Threads kamu.</p>
    </div>

    <!-- Metric Cards Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div class="p-5 bg-white border border-zinc-200 rounded-xl shadow-sm space-y-2">
        <span class="text-xs font-semibold uppercase tracking-wider text-zinc-500">Total Scheduled</span>
        <p class="text-3xl font-black text-zinc-900">0</p>
      </div>

      <div class="p-5 bg-white border border-zinc-200 rounded-xl shadow-sm space-y-2">
        <span class="text-xs font-semibold uppercase tracking-wider text-zinc-500">Total Published</span>
        <p class="text-3xl font-black text-zinc-900">0</p>
      </div>

      <div class="p-5 bg-white border border-zinc-200 rounded-xl shadow-sm space-y-2">
        <span class="text-xs font-semibold uppercase tracking-wider text-zinc-500">Replies Received</span>
        <p class="text-3xl font-black text-zinc-900">0</p>
      </div>

      <div class="p-5 bg-white border border-zinc-200 rounded-xl shadow-sm space-y-2">
        <span class="text-xs font-semibold uppercase tracking-wider text-zinc-500">Pending Auto-Reply</span>
        <p class="text-3xl font-black text-zinc-900">0</p>
      </div>
    </div>
  </div>
</template>
