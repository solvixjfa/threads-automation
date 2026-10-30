# Ixiera - Threads Automation & Intelligence

Ixiera adalah platform SaaS all-in-one untuk kreator, agency, dan bisnis untuk mengelola akun Threads secara otomatis. Dibangun dengan arsitektur modern yang memisahkan antara Frontend, Backend AI, dan Database.

## 🚀 Fitur Utama
- **AI Content Planner**: Membuat rencana konten 3 hari ke depan berdasarkan histori dan RAG.
- **Auto-Reply Cerdas**: Membalas komentar menggunakan AI (HITL / Full Auto) dengan persona brand.
- **Repurpose Engine**: Mengubah postingan lama menjadi 3 angle baru yang segar.
- **Deep Analytics**: Analisis Best Time, Hook, Length, dan Topic Clustering (menggunakan ML).
- **BYOK (Bring Your Own Key)**: Dukungan API Key Groq/Gemini milik user sendiri untuk menghemat biaya server.
- **Multi-Bahasa**: Dukungan penuh Bahasa Indonesia (ID) dan Inggris (EN).

## 🛠️ Tech Stack
- **Frontend**: Vue 3, Vite, TailwindCSS, Pinia, Vue Router, Vue-i18n. Di-deploy di **Vercel**.
- **Backend (API & AI)**: Python, FastAPI, Scikit-Learn (untuk ML), Groq SDK, Google GenAI. Di-deploy di **Railway**.
- **Database & Auth**: Supabase (PostgreSQL), pgvector (untuk RAG).
- **Edge Functions**: Deno (TypeScript) untuk Webhook, OAuth, dan task ringan. Di-deploy di **Supabase**.
- **Email**: Resend API.

## 📁 Struktur Direktori
- `/backend` - Python FastAPI, Logic AI, Worker background (Queue, Metrics, Replies).
- `/web` - Vue 3 Frontend.
- `/supabase` - Migrations SQL, Edge Functions (OAuth, Webhook, Worker ringan).
- `/docs` - Dokumentasi teknis & arsitektur.

## ⚙️ Environment Variables

### Backend (`/backend/.env`)
- `SUPABASE_URL`: URL project Supabase.
- `SUPABASE_SERVICE_ROLE_KEY`: Secret key (Bypass RLS).
- `GEMINI_API_KEY`: API Key Google Gemini.
- `GROQ_API_KEY`: API Key Groq (untuk fallback/primary text generation).
- `DISCORD_WEBHOOK_URL`: Notifikasi error/health.

### Frontend (`/web/.env`)
- `VITE_SUPABASE_URL`: URL project Supabase.
- `VITE_SUPABASE_ANON_KEY`: Public anon key.

## 🚀 Cara Deploy
1. **Database**: Jalankan semua file di `supabase/migrations` ke Supabase SQL Editor.
2. **Backend**: Hubungkan repo ke Railway, set Root Directory ke `/backend`, dan masukkan env vars.
3. **Frontend**: Hubungkan repo ke Vercel, set Root Directory ke `/web`, masukkan env vars.
4. **Edge Functions**: Push ke branch `main`, GitHub Actions akan otomatis deploy fungsi ke Supabase.
