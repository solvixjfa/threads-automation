# Arsitektur Sistem Ixiera

Ixiera menggunakan arsitektur *hybrid* untuk memisahkan beban kerja berat dan ringan.

## 1. Frontend (Vue 3 di Vercel)
- Berkomunikasi langsung dengan Supabase (Auth & Query data ringan).
- Memanggil Edge Functions Supabase untuk tugas ringan (OAuth, Webhook).
- Memanggil Backend Python di Railway untuk tugas berat (AI Generation, ML Clustering).

## 2. Backend Python (FastAPI di Railway)
- **API**: Menyediakan endpoint untuk generate content, repurpose, scoring, dan embedding.
- **Worker Loop**: Berjalan di background (asyncio) untuk:
  - Menarik komentar baru dari Meta API.
  - Melakukan klasifikasi teks (Spam, Toxic, Question).
  - Memanggil AI (Groq/Gemini) untuk membuat draf balasan.
  - Mempublikasikan balasan secara otomatis (jika mode Auto).
- **Machine Learning**: Menggunakan `scikit-learn` (TF-IDF + KMeans) untuk clustering topik secara lokal tanpa membebani API LLM.

## 3. Supabase (Database, Auth, Edge Functions)
- **Database**: PostgreSQL dengan ekstensi `pgvector` untuk RAG (Retrieval-Augmented Generation).
- **Edge Functions (Deno)**:
  - `threads-oauth-*`: Menangani login/authorize akun Threads.
  - `worker-metrics` & `worker-publish`: Worker ringan untuk metrik harian dan publikasi post.
  - `generate-post`: Fallback logic jika Railway down.
  - `send-email`: Integrasi Resend API untuk verifikasi akun.

## 4. Alur AI (LLM & RAG)
1. User memberikan instruksi (misal: "Bikin plan konten soal AI").
2. Backend Python mencari data di tabel `brand_knowledge` menggunakan embedding Gemini.
3. Data konteks (RAG) + instruksi user dikirim ke Groq atau Gemini.
4. AI menghasilkan output JSON.
5. Backend memotong kredit user (jika tidak menggunakan BYOK).
6. Hasil dikembalikan ke Frontend.
