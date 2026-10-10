<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-2xl font-bold text-slate-900 tracking-tight">Inbox & Auto-Reply</h1>
      <p class="text-slate-500 text-sm mt-1">Pantau balasan masuk dari Threads dan kelola respons otomatis.</p>
    </div>

    <div class="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden flex flex-col items-center justify-center p-12 space-y-4">
      <div class="w-16 h-16 bg-indigo-50 text-indigo-500 rounded-full flex items-center justify-center mb-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
        </svg>
      </div>
      <h2 class="text-lg font-bold text-slate-800">Inbox Kosong</h2>
      <p class="text-sm text-slate-500 text-center max-w-sm">Belum ada balasan yang ditarik dari Threads. Pastikan webhook aktif atau tunggu interaksi audiens.</p>
      
      <button class="mt-4 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold py-2.5 px-6 rounded-lg transition shadow-md">
        Refresh Inbox
      </button>
    </div>
  </div>
</template>
