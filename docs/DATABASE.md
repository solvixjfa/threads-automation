# Skema Database (Supabase)

Semua tabel berada di dalam schema `threads`.

## Tabel Core
- **`threads_accounts`**: Menyimpan data user, access token Meta, kredit AI, provider AI aktif.
- **`posts`**: Menyimpan postingan yang ditarik dari Meta.
- **`scheduled_posts`**: Antrean postingan (Terjadwal / Published / Gagal).
- **`replies`**: Menyimpan semua komentar yang masuk dari Meta.
- **`auto_reply_logs`**: Log balasan AI (status: pending, sent, skipped).
- **`auto_reply_settings`**: Pengaturan worker (mode HITL/Auto, tone_prompt, max_per_hour).

## Tabel AI & RAG
- **`brand_knowledge`**: Menyimpan dokumen brand. Memiliki kolom `embedding` (pgvector) untuk pencarian semantik.
- **`content_scores`**: Menyimpan skor kualitas draf postingan.

## Tabel Analytics
- **`post_metrics`**: Menyimpan snapshot views/likes per postingan.
- **`account_insights_daily`**: Akumulasi metrik harian (followers, views, dll).

## Tabel Pendukung
- **`keyword_watches`** & **`keyword_results`**: Untuk fitur pemantauan keyword.
- **`notifications`**: Notifikasi in-app.
- **`oauth_states`**: State sementara untuk alur OAuth Meta.
- **`api_call_logs`** & **`audit_logs`**: Log sistem.
