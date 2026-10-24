# Arsitektur & Alur Data Ixiera

## 1. Alur Auto-Reply (Backend Python)
1. Komentar baru masuk dari Webhook Threads (via Supabase Edge Function).
2. Data masuk ke tabel antrean `reply_queue` di database Supabase.
3. `reply_worker_loop` (berjalan di FastAPI) melakukan *polling* data dari antrean.
4. `comment_classifier.py` mengklasifikasi komentar (Spam/Toxic di-skip, Question/Lead diproses).
5. `rag.py` melakukan pencarian vektor ke tabel `brand_knowledge` untuk mendapatkan konteks.
6. `auto_reply.py` merangkai prompt dan memanggil Gemini API.
7. `publish_reply_to_threads` mengirim balasan ke Meta Graph API.
8. Status antrean di database diperbarui (Sukses/Gagal).

## 2. Alur Content Composer (Frontend)
1. User mengisi topik dan tone di `ComposerView.vue`.
2. Frontend memanggil Edge Function `generate-post` (Supabase).
3. Edge Function memanggil Gemini API dengan prompt RAG.
4. AI mengembalikan 3 draf (JSON). User memilih dan menjadwalkan post.
