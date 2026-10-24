# Ixiera — Threads Automation & Intelligence

Sistem full-stack untuk otomasi dan analitik platform Threads (Meta). Aplikasi ini mencakup auto-reply cerdas berbasis RAG (Retrieval-Augmented Generation), penjadwalan posting, analitik performa, dan deteksi *lead*.

## 🏗️ Arsitektur Sistem

1. **Frontend (`/web`)**: Vue 3 + Vite + Tailwind + Pinia. Di-deploy otomatis via **Vercel**.
2. **Backend Core (`/backend`)**: Python + FastAPI. Menangani background worker untuk antrean balasan, klasifikasi teks, dan AI. Di-deploy via **Railway**.
3. **Supabase Edge Functions (`/supabase/functions`)**: Deno + TypeScript. Menangani webhook Meta dan OAuth. Di-deploy via **Supabase CLI**.

## 📁 Struktur Direktori
- `backend/` — FastAPI Engine, Services (RAG, AI, Classifier), Worker.
- `web/` — Frontend Vue 3.
- `supabase/` — Edge Functions & Migrations SQL.
- `docs/` — Dokumentasi arsitektur.

## 🚀 Panduan Deployment (Production)

### 1. Frontend (Vercel)
- Hubungkan repository GitHub ini ke Vercel.
- Set Root Directory ke `web`.
- Tambahkan Environment Variables di dashboard Vercel:
  - `VITE_SUPABASE_URL`
  - `VITE_SUPABASE_ANON_KEY`
- Deploy otomatis setiap ada push ke branch `main`.

### 2. Backend (Railway)
- Hubungkan repository ke Railway.
- Set Root Directory ke `backend`.
- Railway akan otomatis mendeteksi `Dockerfile` dan melakukan build.
- Tambahkan Environment Variables di dashboard Railway:
  - `SUPABASE_URL`
  - `SUPABASE_SERVICE_ROLE_KEY`
  - `GEMINI_API_KEY`
  - `GEMINI_MODEL`
  - `DISCORD_WEBHOOK_URL`

### 3. Supabase (Edge Functions)
- Deploy otomatis berjalan via GitHub Actions (`.github/workflows/deploy-functions.yml`).
- Pastikan `SUPABASE_ACCESS_TOKEN` sudah diset di GitHub Secrets.
