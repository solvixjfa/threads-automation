<template>
  <footer class="border-t border-[var(--line)] bg-[var(--bg)] py-12 md:py-16">
    <div class="max-w-[1120px] mx-auto px-6">
      
      <!-- Grid 4 Kolom -->
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-10 md:gap-8">
        
        <!-- 1. Brand & Copyright -->
        <div class="space-y-4">
          <a href="/" class="flex items-center gap-2">
            <div class="w-8 h-8 flex items-center justify-center rounded-md text-sm font-bold bg-[var(--text)] text-[var(--bg)]">IX</div>
            <span class="font-bold text-xl tracking-tight">Ixiera</span>
          </a>
          <p class="text-sm text-[var(--muted)] leading-relaxed pr-4">
            Platform all-in-one untuk mengelola dan mengotomatisasi akun Threads kamu.
          </p>
          <p class="text-xs text-[var(--muted)] pt-4">
            &copy; 2026 Ixiera.<br>All rights reserved.
          </p>
        </div>

        <!-- 2. Produk -->
        <div>
          <h4 class="font-bold text-sm mb-4">Produk</h4>
          <ul class="space-y-3 text-sm text-[var(--muted)]">
            <li><a href="/#fitur" class="hover:text-[var(--text)] transition">Fitur</a></li>
            <li><a href="/pricing" class="hover:text-[var(--text)] transition">Harga</a></li>
            <li><a href="/#cara-kerja" class="hover:text-[var(--text)] transition">Cara Kerja</a></li>
            <li><a href="/#faq" class="hover:text-[var(--text)] transition">FAQ</a></li>
          </ul>
        </div>

        <!-- 3. Legal -->
        <div>
          <h4 class="font-bold text-sm mb-4">Legal</h4>
          <ul class="space-y-3 text-sm text-[var(--muted)]">
            <li><a href="/privacy" class="hover:text-[var(--text)] transition">Kebijakan Privasi</a></li>
            <li><a href="/terms" class="hover:text-[var(--text)] transition">Syarat & Ketentuan</a></li>
            <li><a href="/data-deletion" class="hover:text-[var(--text)] transition">Hapus Data</a></li>
          </ul>
        </div>

        <!-- 4. Hubungi Kami -->
        <div>
          <h4 class="font-bold text-sm mb-4">Hubungi Kami</h4>
          <ul class="space-y-3 text-sm text-[var(--muted)]">
            <li>
              <a href="https://instagram.com/ixiera.id" target="_blank" rel="noopener" class="flex items-center gap-3 hover:text-[var(--text)] transition">
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
                <span>@ixiera.id</span>
              </a>
            </li>
            <li>
              <a href="https://threads.net/@ixiera.id" target="_blank" rel="noopener" class="flex items-center gap-3 hover:text-[var(--text)] transition">
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm1.537 18.764c-1.385.354-2.849.231-4.019-.373-1.586-.819-2.518-2.464-2.518-4.465 0-3.051 2.31-5.196 5.42-5.196 2.465 0 4.136 1.044 4.892 2.902.254.619.231 1.243.231 1.243s-1.457-.253-2.637-.253c-1.827 0-3.077.86-3.077 2.274 0 1.526 1.352 2.328 2.827 2.328.923 0 1.842-.346 2.496-1.035.653-.688.996-1.751.996-3.076 0-3.442-2.24-5.644-5.624-5.644-3.383 0-5.623 2.202-5.623 5.644 0 3.642 2.722 5.904 6.436 5.904 1.533 0 2.934-.312 4.018-.842l.596 2.294c-1.458.681-3.134.996-4.915.996-4.734 0-8.112-3.025-8.112-8.352 0-5.324 3.378-8.353 8.113-8.353 4.735 0 8.113 3.029 8.113 8.353 0 1.976-.629 3.648-1.743 4.823-1.11 1.171-2.635 1.792-4.446 1.792-1.705 0-3.071-.585-3.071-1.854 0-.62.28-1.151.739-1.44.46-.289 1.101-.424 1.845-.424.543 0 1.078.059 1.582.177z"/></svg>
                <span>@ixiera.id</span>
              </a>
            </li>
            <li>
              <a href="https://wa.me/6285702373412" target="_blank" rel="noopener" class="flex items-center gap-3 hover:text-[var(--text)] transition">
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
                <span>0857-0237-3412</span>
              </a>
            </li>
            <li>
              <a href="mailto:contact@ixiera.id" class="flex items-center gap-3 hover:text-[var(--text)] transition">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
                <span>contact@ixiera.id</span>
              </a>
            </li>
          </ul>
        </div>
      </div>
      
      <!-- Disclaimer Meta -->
      <div class="mt-12 pt-6 border-t border-[var(--line)]">
        <p class="text-[11px] text-[var(--muted)] text-center leading-relaxed">
          Ixiera adalah produk independen dan tidak berafiliasi dengan Meta Platforms.<br class="hidden md:block">
          Threads adalah merek dagang Meta.
        </p>
      </div>
    </div>
  </footer>
</template>
