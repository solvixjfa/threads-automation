// Stub function. Tidak dipakai di production.
// Auto-reply dijalankan di backend Python Railway, bukan edge function.
// File ini untuk memenuhi validasi bundling CI.

Deno.serve(() => {
  return new Response(JSON.stringify({ status: "ok", note: "not used" }), {
    headers: { "Content-Type": "application/json" },
  });
});
