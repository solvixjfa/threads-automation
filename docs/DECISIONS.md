# Technical Decisions Log

Dokumen ini mencatat alasan di balik pemilihan teknologi dan arsitektur pada project Ixiera.

## 1. Mengapa memisahkan Backend (FastAPI) dan Supabase Edge Functions?
- **Edge Functions (Deno/TS)**: Digunakan untuk tugas-tugas ringan yang butuh eksekusi cepat dan respons instan (seperti menerima Webhook dari Threads API, OAuth, dsb).
- **FastAPI (Python)**: Digunakan untuk proses berat seperti *polling* antrean, klasifikasi teks, dan pemrosesan AI. Python memiliki ekosistem AI dan *library* yang jauh lebih kaya dibandingkan Deno.

## 2. Mengapa menggunakan RAG (Retrieval-Augmented Generation)?
- AI (Gemini) secara bawaan tidak mengetahui data internal brand. RAG dengan pgvector di Supabase memungkinkan AI menjawab pertanyaan pelanggan berdasarkan dokumen/fakta yang di-upload oleh user, mengurangi halusinasi AI.

## 3. Mengapa Vue 3 + Vite + Vercel?
- Vite memberikan *build time* yang sangat cepat.
- Vercel menawarkan *deployment* gratis (hobby tier) yang sangat mudah untuk SPA (Single Page Application) tanpa perlu konfigurasi server yang rumit.

## 4. Mengapa Railway untuk Backend?
- Railway mendukung *deployment* berbasis Docker (mudah untuk menjalankan Python worker jangka panjang), dan tidak membatasi waktu eksekusi (timeout) selama proses AI berjalan, dibandingkan serverless function biasa.
