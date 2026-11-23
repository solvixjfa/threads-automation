# IXIERA — MASTER PROJECT AUDIT & AI HANDOFF

## 1. IDENTITAS & INFRASTRUKTUR PRODUK
- **Nama Produk:** Ixiera (SaaS Asisten AI & Otomatisasi Threads)
- **Domain:**
  - Marketing / Landing Page: `https://ixiera.online` (`./landing`)
  - Web Application: `https://app.ixiera.online`
- **DNS & Email:** Cloudflare DNS, Resend (`send.ixiera.online` - region `ap-northeast-1`), Lark Suite (`support@ixiera.online`)
- **AI Stack (Dual-AI):**
  - **Google Gemini:** 3-Day AI Content Planner, Quick Score, Knowledge Base (Style/Persona RAG).
  - **Groq:** Klasifikasi komentar Smart Inbox & generasi draf balasan cepat.
- **Integrasi Utama:** Meta Threads API (OAuth, Publish, Reply, Mentions, Insights, Location Tagging, Share to Instagram, Keyword Search, Profile Discovery, Trending Topics).

## 2. ATURAN KERAS CODEBASE & UI (WAJIB DIPATUHI AI BERIKUTNYA)
1. **Strict Monochrome Theme (Dark & Light Mode):**
   - Seluruh UI menggunakan CSS variables: `--bg`, `--surface`, `--surface-2`, `--line`, `--text`, `--muted`, `--faint`, `--bar-dim`.
   - Mode gelap aktif via class `.dark` pada `<html>`, mode terang via `html:not(.dark)`.
   - **DILARANG** menimpa atau merusak variabel tema dark/light mode yang sudah berjalan.
   - **Pengecualian Warna:** Hanya logo sponsor marquee (**Google Gemini** gradient SVG dan badge **Groq** `#F55036`) yang memakai warna asli brand.
2. **Bilingual Localization (`vue-i18n`):**
   - Landing page wajib mendukung penuh bahasa Indonesia (`id`) dan Inggris (`en`) secara sinkron di seluruh komponen (`LandingView.vue`, `FeaturesView.vue`, `PricingView.vue`, `BlogView.vue`, `AppNavbar.vue`, `AppFooter.vue`).
3. **Meta App Review & Policy Guardrails:**
   - **DILARANG** menulis klaim *"Official Meta API"* atau *"API Resmi Meta"* di copywriting publik. Gunakan *"Threads API"* atau *"Login aman via Meta"*.
   - **Auto-Reply strictly INBOUND:** Hanya membalas komentar di postingan sendiri dan `@mentions` publik (dilengkapi mode Review Manual, batas per jam, dan Kill Switch).
   - **Trending Topics & Keyword Search:** Hanya digunakan untuk riset ide dan pembuatan konten orisinal pengguna, **bukan** untuk outbound auto-comment ke postingan orang lain.

## 3. STATUS PENGERJAAN TERAKHIR
- **Landing Page (`ixiera.online`):**
  - Hero section, mockup dashboard, infinite moving marquee (Gemini & Groq berwarna), 3 showcase fitur utama, pricing matrix (Trial 7 Hari Rp 0, Pro 30 Hari Rp 29.000, BYOK 30 Hari Rp 19.000), section Blog & Free Playbook, FAQ 9 item, dan Footer bilingual (`ID/EN`) sudah selesai dan live di branch `main`.
- **Meta App Review:**
  - Seluruh scope sudah diajukan dan sedang menunggu hasil peninjauan Meta.

---

## 4. HASIL AUDIT OTOMATIS REPOSITORY
### Git Branch & 10 Commit Terakhir
```text

```

### Struktur Direktori (Maksimal Depth 4)
```text
.
./AI_HANDOFF.md
./ARCHITECTURE_AUTO.md
./Common
./Exited
./Instance
./README.md
./audit.sh
./audit_report.txt
./audit_structure.txt
./backend
./backend/Dockerfile
./backend/app
./backend/app/api
./backend/app/api/v1
./backend/app/core
./backend/app/core/config.py
./backend/app/services
./backend/app/services/__pycache__
./backend/app/services/auto_reply.py
./backend/app/services/billing.py
./backend/app/services/comment_classifier.py
./backend/app/services/comment_templates.py
./backend/app/services/importer.py
./backend/app/services/leads.py
./backend/app/services/rag.py
./backend/app/services/trending_outreach.py
./backend/app/workers
./backend/app/workers/__pycache__
./backend/app/workers/replies.py
./backend/main.py
./backend/railway.json
./backend/requirements.txt
./docs
./docs/ARCHITECTURE.md
./docs/DATABASE.md
./docs/DECISIONS.md
./frontend
./frontend/index.html
./frontend/package.json
./frontend/postcss.config.js
./frontend/public
./frontend/public/apple-touch-icon.png
./frontend/public/manifest.json
./frontend/public/pwa-192x192.png
./frontend/public/pwa-512x512.png
./frontend/src
./frontend/src/App.vue
./frontend/src/assets
./frontend/src/assets/main.css
./frontend/src/components
./frontend/src/components/AppSidebar.vue
./frontend/src/components/BestTimeChart.vue
./frontend/src/components/BestTimeChip.vue
./frontend/src/components/BestTimeHeatmap.vue
./frontend/src/components/BestTimeLineChart.vue
./frontend/src/components/BottomNav.vue
./frontend/src/components/DoughnutChart.vue
./frontend/src/components/GrowthChart.vue
./frontend/src/components/LanguageSwitcher.vue
./frontend/src/components/NotifyOverlay.vue
./frontend/src/components/PasswordInput.vue
./frontend/src/components/TemplateSettingsCard.vue
./frontend/src/components/WorkerStatusCard.vue
./frontend/src/components/ui
./frontend/src/composables
./frontend/src/composables/useNotify.ts
./frontend/src/composables/useTheme.ts
./frontend/src/config
./frontend/src/config/pricing.ts
./frontend/src/lib
./frontend/src/lib/supabase.ts
./frontend/src/locales
./frontend/src/locales/en.json
./frontend/src/locales/id.json
./frontend/src/main.ts
./frontend/src/router
./frontend/src/router/index.ts
./frontend/src/stores
./frontend/src/stores/composer.ts
./frontend/src/stores/inbox.ts
./frontend/src/stores/settings.ts
./frontend/src/styles
./frontend/src/styles/theme.css
./frontend/src/views
./frontend/src/views/ComposerView.vue
./frontend/src/views/DashboardView.vue
./frontend/src/views/DataDeletionView.vue
./frontend/src/views/InboxView.vue
./frontend/src/views/LandingView.vue
./frontend/src/views/LoginView.vue
./frontend/src/views/PricingView.vue
./frontend/src/views/PrivacyView.vue
./frontend/src/views/RepurposeView.vue
./frontend/src/views/TermsView.vue
./frontend/src/views/TutorialView.vue
./frontend/src/views/UpdatePasswordView.vue
./frontend/src/views/admin
./frontend/src/views/analytics
./frontend/src/views/content
./frontend/src/views/settings
./frontend/tailwind.config.js
./frontend/tsconfig.json
./frontend/vercel.json
./frontend/vite.config.ts
./generate_handoff.sh
./landing
./landing/index.html
./landing/package.json
./landing/postcss.config.js
./landing/public
./landing/public/ixiera-og-image.png
./landing/public/llms.txt
./landing/public/og-image.svg
./landing/public/robots.txt
./landing/public/sitemap.xml
./landing/src
./landing/src/App.vue
./landing/src/App.vue.bak
./landing/src/assets
./landing/src/assets/main.css
./landing/src/assets/main.css.bak
./landing/src/components
./landing/src/components/BestTimeChip.vue
./landing/src/components/BestTimeHeatmap.vue
./landing/src/components/LanguageSwitcher.vue
./landing/src/components/NotifyOverlay.vue
./landing/src/components/PasswordInput.vue
./landing/src/components/TemplateSettingsCard.vue
./landing/src/components/WorkerStatusCard.vue
./landing/src/components/layouts
./landing/src/components/ui
./landing/src/composables
./landing/src/composables/useNotify.ts
./landing/src/composables/useTheme.ts
./landing/src/config
./landing/src/config/pricing.ts
./landing/src/data
./landing/src/data/blogPosts.ts
./landing/src/lib
./landing/src/lib/supabase.ts
./landing/src/locales
./landing/src/locales/en.json
./landing/src/locales/id.json
./landing/src/main.ts
./landing/src/router
./landing/src/router/index.ts
./landing/src/router/index.ts.bak
./landing/src/styles
./landing/src/styles/theme.css
./landing/src/views
./landing/src/views/BlogPostView.vue
./landing/src/views/BlogView.vue
./landing/src/views/ComposerView.vue
./landing/src/views/DashboardView.vue
./landing/src/views/DataDeletionView.vue
./landing/src/views/FaqView.vue
./landing/src/views/FeatureDetailView.vue
./landing/src/views/FeaturesView.vue
./landing/src/views/HowItWorksView.vue
./landing/src/views/InboxView.vue
./landing/src/views/LandingView.vue
./landing/src/views/LandingView.vue.bak
./landing/src/views/LoginView.vue
./landing/src/views/PricingView.vue
./landing/src/views/PricingView.vue.bak
./landing/src/views/PrivacyView.vue
./landing/src/views/RepurposeView.vue
./landing/src/views/TermsView.vue
./landing/src/views/UpdatePasswordView.vue
./landing/tailwind.config.js
./landing/tsconfig.json
./landing/vercel.json
./landing/vite.config.ts
./openapi.json
./supabase
./supabase/config.toml
./supabase/functions
./supabase/functions/_shared
./supabase/functions/_shared/cors.ts
./supabase/functions/_shared/llm.ts
./supabase/functions/_shared/quota.ts
./supabase/functions/admin-health
./supabase/functions/admin-health/index.ts
./supabase/functions/admin-manage-queue
./supabase/functions/admin-manage-queue/index.ts
./supabase/functions/auto-reply-engine
./supabase/functions/auto-reply-engine/index.ts
./supabase/functions/cleanup-storage
./supabase/functions/cleanup-storage/index.ts
./supabase/functions/generate-post
./supabase/functions/generate-post/index.ts
./supabase/functions/get-analytics
./supabase/functions/get-analytics/index.ts
./supabase/functions/get-best-time
./supabase/functions/get-best-time/index.ts
./supabase/functions/get-worker-status
./supabase/functions/get-worker-status/index.ts
./supabase/functions/score-draft
./supabase/functions/score-draft/index.ts
./supabase/functions/threads-data-deletion
./supabase/functions/threads-data-deletion/index.ts
./supabase/functions/threads-oauth-callback
./supabase/functions/threads-oauth-callback/index.ts
./supabase/functions/threads-oauth-start
./supabase/functions/threads-oauth-start/index.ts
./supabase/functions/threads-webhook
./supabase/functions/threads-webhook/index.ts
./supabase/functions/worker-metrics
./supabase/functions/worker-metrics/index.ts
./supabase/functions/worker-publish
./supabase/functions/worker-publish/index.ts
./supabase/functions/worker-token-refresh
./supabase/functions/worker-token-refresh/index.ts
./supabase/migrations
./supabase/migrations/20261009000000_p0_initial_schema.sql
./supabase/migrations/20261009000001_p2_metrics_and_import.sql
./supabase/migrations/20261009000002_p3_quota_tracker.sql
./supabase/migrations/20261009000003_p4_replies_and_inbox.sql
./supabase/migrations/20261009000004_p5_auto_reply.sql
./supabase/migrations/20261009000005_p6_content_scoring.sql
./supabase/migrations/20261009000006_p8_keyword_watch.sql
./supabase/migrations/20261009000007_p9_notifications_and_health.sql
./temp_func.txt
```

### Daftar Package.json & Dependencies
#### `./landing/package.json`
```json
{
  "name": "threads-automation-web",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "@supabase/supabase-js": "^2.39.0",
    "lucide-vue-next": "^0.300.0",
    "pinia": "^2.1.7",
    "vue": "^3.4.0",
    "vue-router": "^4.2.5",
    "vue-i18n": "^9.14.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.0",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32",
    "tailwindcss": "^3.4.0",
    "typescript": "^5.3.0",
    "vite": "^5.0.0",
    "vue-tsc": "^2.0.0"
  }
}```

#### `./frontend/package.json`
```json
{
  "name": "threads-automation-web",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "@supabase/supabase-js": "^2.39.0",
    "lucide-vue-next": "^0.300.0",
    "pinia": "^2.1.7",
    "vue": "^3.4.0",
    "vue-router": "^4.2.5",
    "vue-i18n": "^9.14.0",
    "chart.js": "^4.4.7",
    "vue-chartjs": "^5.3.2"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.0",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32",
    "tailwindcss": "^3.4.0",
    "typescript": "^5.3.0",
    "vite": "^5.0.0",
    "vue-tsc": "^2.0.0",
    "vite-plugin-pwa": "^0.20.5"
  }
}
```

### Daftar Environment Variable Keys (Tanpa Value)
```text
--- ./landing/.env ---
SUPABASE_URL
SUPABASE_ANON_KEY
--- ./backend/.env ---
SUPABASE_URL
SUPABASE_SERVICE_ROLE_KEY
GEMINI_API_KEY
GEMINI_MODEL
DISCORD_WEBHOOK_URL
--- ./frontend/.env ---
SUPABASE_URL
SUPABASE_ANON_KEY
```

### Daftar Views, Components & API Routes
```text
./backend/app/api/v1
./backend/app/api/v1/__pycache__
./backend/app/api/v1/admin.py
./backend/app/api/v1/analytics.py
./backend/app/api/v1/history.py
./backend/app/api/v1/leads.py
./backend/app/api/v1/payment.py
./backend/app/api/v1/queue.py
./backend/app/api/v1/rag.py
./backend/app/api/v1/threads_extra.py
./backend/app/api/v1/trending.py
./backend/app/services/__pycache__
./backend/app/services/__pycache__/auto_reply.cpython-312.pyc
./backend/app/services/__pycache__/importer.cpython-312.pyc
./backend/app/services/__pycache__/rag.cpython-312.pyc
./backend/app/services/auto_reply.py
./backend/app/services/billing.py
./backend/app/services/comment_classifier.py
./backend/app/services/comment_templates.py
./backend/app/services/importer.py
./backend/app/services/leads.py
./backend/app/services/rag.py
./backend/app/services/trending_outreach.py
./frontend/src/components/AppSidebar.vue
./frontend/src/components/BestTimeChart.vue
./frontend/src/components/BestTimeChip.vue
./frontend/src/components/BestTimeHeatmap.vue
./frontend/src/components/BestTimeLineChart.vue
./frontend/src/components/BottomNav.vue
./frontend/src/components/DoughnutChart.vue
./frontend/src/components/GrowthChart.vue
./frontend/src/components/LanguageSwitcher.vue
./frontend/src/components/NotifyOverlay.vue
./frontend/src/components/PasswordInput.vue
./frontend/src/components/TemplateSettingsCard.vue
./frontend/src/components/WorkerStatusCard.vue
./frontend/src/components/ui
./frontend/src/components/ui/Badge.vue
./frontend/src/components/ui/Button.vue
./frontend/src/components/ui/Card.vue
./frontend/src/components/ui/EmptyState.vue
./frontend/src/components/ui/Input.vue
./frontend/src/components/ui/Select.vue
./frontend/src/components/ui/Spinner.vue
./frontend/src/components/ui/Textarea.vue
./frontend/src/components/ui/index.ts
./frontend/src/views/ComposerView.vue
./frontend/src/views/DashboardView.vue
./frontend/src/views/DataDeletionView.vue
./frontend/src/views/InboxView.vue
./frontend/src/views/LandingView.vue
./frontend/src/views/LoginView.vue
./frontend/src/views/PricingView.vue
./frontend/src/views/PrivacyView.vue
./frontend/src/views/RepurposeView.vue
./frontend/src/views/TermsView.vue
./frontend/src/views/TutorialView.vue
./frontend/src/views/UpdatePasswordView.vue
./frontend/src/views/admin
./frontend/src/views/admin/AdminLayout.vue
./frontend/src/views/admin/AdminOverview.vue
./frontend/src/views/admin/AdminUsers.vue
./frontend/src/views/analytics
./frontend/src/views/analytics/AnalyticsLayout.vue
./frontend/src/views/analytics/BestTimeView.vue
./frontend/src/views/analytics/HookView.vue
./frontend/src/views/analytics/LengthView.vue
./frontend/src/views/analytics/SentimentView.vue
./frontend/src/views/analytics/TopicView.vue
./frontend/src/views/content
./frontend/src/views/content/ContentLayout.vue
./frontend/src/views/content/QueueView.vue
./frontend/src/views/content/TrendingView.vue
./frontend/src/views/settings
./frontend/src/views/settings/AccountView.vue
./frontend/src/views/settings/AiView.vue
./frontend/src/views/settings/AutoReplyView.vue
./frontend/src/views/settings/KnowledgeView.vue
./frontend/src/views/settings/ProfileLayout.vue
./frontend/src/views/settings/SettingsLayout.vue
./frontend/src/views/settings/TemplateView.vue
./landing/src/components/BestTimeChip.vue
./landing/src/components/BestTimeHeatmap.vue
./landing/src/components/LanguageSwitcher.vue
./landing/src/components/NotifyOverlay.vue
./landing/src/components/PasswordInput.vue
./landing/src/components/TemplateSettingsCard.vue
./landing/src/components/WorkerStatusCard.vue
./landing/src/components/layouts
./landing/src/components/layouts/AppFooter.vue
./landing/src/components/layouts/AppNavbar.vue
./landing/src/components/ui
./landing/src/components/ui/Badge.vue
./landing/src/components/ui/Button.vue
./landing/src/components/ui/Card.vue
./landing/src/components/ui/EmptyState.vue
./landing/src/components/ui/Input.vue
./landing/src/components/ui/Select.vue
./landing/src/components/ui/Spinner.vue
./landing/src/components/ui/Textarea.vue
./landing/src/components/ui/index.ts
./landing/src/views/BlogPostView.vue
./landing/src/views/BlogView.vue
./landing/src/views/ComposerView.vue
./landing/src/views/DashboardView.vue
./landing/src/views/DataDeletionView.vue
./landing/src/views/FaqView.vue
./landing/src/views/FeatureDetailView.vue
./landing/src/views/FeaturesView.vue
./landing/src/views/HowItWorksView.vue
./landing/src/views/InboxView.vue
./landing/src/views/LandingView.vue
./landing/src/views/LandingView.vue.bak
./landing/src/views/LoginView.vue
./landing/src/views/PricingView.vue
./landing/src/views/PricingView.vue.bak
./landing/src/views/PrivacyView.vue
./landing/src/views/RepurposeView.vue
./landing/src/views/TermsView.vue
./landing/src/views/UpdatePasswordView.vue
```

---

## 5. TECH STACK LENGKAP & KONFIGURASI DEPLOYMENT

### Backend Dependencies (Python)
#### `./backend/requirements.txt`
```text
fastapi
uvicorn
supabase
google-genai
pydantic
httpx
python-dotenv
groq
scikit-learn
python-multipart>=0.0.9
```

### Konfigurasi Deploy / CI-CD / Docker
#### `./landing/vercel.json`
```text
{
  "version": 2,
  "redirects": [
    {
      "source": "/(.*)",
      "has": [
        {
          "type": "host",
          "value": "ixiera.online"
        }
      ],
      "destination": "https://ixiera.online/$1",
      "permanent": true
    },
    {
      "source": "/(.*)",
      "has": [
        {
          "type": "host",
          "value": "www.ixiera.online"
        }
      ],
      "destination": "https://ixiera.online/$1",
      "permanent": true
    }
  ],
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

#### `./.github/workflows/deploy-functions.yml`
```text
name: Deploy Supabase Edge Functions

on:
  push:
    branches:
      - main
    paths:
      - 'supabase/functions/**'
      - '.github/workflows/deploy-functions.yml'
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - uses: supabase/setup-cli@v1
        with:
          version: latest

      - name: Deploy All Functions
        run: |
          supabase functions deploy --project-ref xtarsaurwclktwhhryas --yes
        env:
          SUPABASE_ACCESS_TOKEN: ${{ secrets.SUPABASE_ACCESS_TOKEN }}
```

#### `./backend/Dockerfile`
```text
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
```

#### `./backend/railway.json`
```text
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  },
  "deploy": {
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

#### `./frontend/vercel.json`
```text
{
  "version": 2,
  "redirects": [
    {
      "source": "/(.*)",
      "has": [
        {
          "type": "host",
          "value": "app.ixiera.online"
        }
      ],
      "destination": "https://app.ixiera.online/$1",
      "permanent": true
    }
  ],
  "rewrites": [
    {
      "source": "/((?!manifest\\.json|sw\\.js|workbox-.*\\.js|pwa-.*\\.png|apple-touch-icon\\.png|assets/|vite\\.svg).*)",
      "destination": "/index.html"
    }
  ]
}
```

---

## 6. ARSITEKTUR & SYSTEM WORKFLOW END-TO-END

1. **Auth & Workspace Binding (Meta Threads OAuth):**
   - User login via Meta OAuth -> callback menukar short-lived token ke long-lived token -> sistem mengecek `threads_user_id` lintas workspace (jika sudah pernah terhubung, otomatis melakukan *re-bind* ke workspace aktif agar tidak duplikat akun).
2. **AI Content Planner & Composer (`app.ixiera.online`):**
   - Input topik/niche -> **Google Gemini** mengambil konteks gaya bahasa user dari **Knowledge Base (RAG)** -> menghasilkan draf 3-hari + skor evaluasi (**Quick Score**).
   - Mendukung pencarian lokasi (*Location Autocomplete*) dan toggle **Share to Instagram** sebelum publish langsung atau masuk antrean jadwal.
3. **Trending Topics & Riset Konten:**
   - Mengambil data tren Meta Threads (cache terpisah antara *topic chips* dan hasil *post search*) -> digunakan murni untuk inspirasi pembuatan konten baru pengguna.
4. **Smart Inbox & Inbound Auto-Reply:**
   - Sinkronisasi komentar postingan user dan `@mentions` publik -> **Groq** mengklasifikasikan intent (Pertanyaan, Pujian, Spam) dan menyusun draf balasan cepat sesuai gaya bahasa user -> dikirim manual 1-klik atau otomatis sesuai batas aman per jam (*rate limit* & *kill switch*).
5. **Sistem Kredit & Paket Akses:**
   - **7-Day Trial:** Rp 0 (20 kredit AI gratis).
   - **Pro (30 Hari):** Rp 29.000 (100 kredit AI memakai API key sistem).
   - **BYOK (30 Hari):** Rp 19.000 (kuota unlimited memakai API key Gemini/Groq milik user sendiri).

---

## 7. SKEMA SQL & DATABASE MODELS
### File SQL & Migrasi
#### `./supabase/migrations/20261009000000_p0_initial_schema.sql`
```sql
-- 1. SCHEMA ISOLASI KHUSUS THREADS AUTOMATION
CREATE SCHEMA IF NOT EXISTS threads;

-- 2. EXTENSIONS
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 3. ENUMS DI DALAM SCHEMA THREADS
CREATE TYPE threads.connection_status_type AS ENUM (
  'waitlist', 'invited', 'accepted_claimed', 'connected', 
  'token_expiring', 'needs_reconnect', 'disconnected', 'suspended'
);

CREATE TYPE threads.user_role_type AS ENUM ('admin', 'user');

CREATE TYPE threads.post_status_type AS ENUM (
  'draft', 'scheduled', 'publishing', 'published', 'failed', 'cancelled'
);

CREATE TYPE threads.reply_log_status_type AS ENUM (
  'pending_review', 'approved', 'sent', 'skipped', 'failed', 'rejected'
);

-- 4. PROFILES TABLE (threads.profiles)
CREATE TABLE threads.profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email TEXT NOT NULL,
  role threads.user_role_type DEFAULT 'user' NOT NULL,
  plan TEXT DEFAULT 'free' NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- Helper function untuk cek admin (RLS)
CREATE OR REPLACE FUNCTION threads.is_admin()
RETURNS BOOLEAN AS $$
BEGIN
  RETURN EXISTS (
    SELECT 1 FROM threads.profiles 
    WHERE id = auth.uid() AND role = 'admin'
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger buat bikin profile otomatis saat user signup di Supabase Auth
CREATE OR REPLACE FUNCTION threads.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO threads.profiles (id, email)
  VALUES (new.id, new.email);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE TRIGGER on_auth_user_created_threads
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION threads.handle_new_user();

-- 5. THREADS ACCOUNTS TABLE
CREATE TABLE threads.threads_accounts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES threads.profiles(id) ON DELETE CASCADE,
  threads_user_id TEXT UNIQUE,
  username TEXT,
  connection_status threads.connection_status_type DEFAULT 'waitlist' NOT NULL,
  invited_at TIMESTAMPTZ,
  accepted_claimed_at TIMESTAMPTZ,
  connected_at TIMESTAMPTZ,
  token_secret_id UUID,
  token_expires_at TIMESTAMPTZ,
  last_refresh_at TIMESTAMPTZ,
  last_error TEXT,
  kill_switch BOOLEAN DEFAULT FALSE NOT NULL,
  settings JSONB DEFAULT '{}'::jsonb NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- 6. OAUTH STATES TABLE
CREATE TABLE threads.oauth_states (
  state TEXT PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES threads.profiles(id) ON DELETE CASCADE,
  expires_at TIMESTAMPTZ NOT NULL,
  used BOOLEAN DEFAULT FALSE NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- 7. SCHEDULED POSTS TABLE
CREATE TABLE threads.scheduled_posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  account_id UUID NOT NULL REFERENCES threads.threads_accounts(id) ON DELETE CASCADE,
  text TEXT CHECK (char_length(text) <= 500),
  media JSONB DEFAULT '[]'::jsonb,
  reply_control TEXT DEFAULT 'everyone',
  scheduled_for TIMESTAMPTZ NOT NULL,
  status threads.post_status_type DEFAULT 'scheduled' NOT NULL,
  attempts INT DEFAULT 0 NOT NULL,
  last_error TEXT,
  creation_id TEXT,
  published_media_id TEXT,
  idempotency_key TEXT UNIQUE NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- 8. POSTS TABLE
CREATE TABLE threads.posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  account_id UUID NOT NULL REFERENCES threads.threads_accounts(id) ON DELETE CASCADE,
  threads_media_id TEXT UNIQUE NOT NULL,
  text TEXT,
  media_type TEXT,
  permalink TEXT,
  posted_at TIMESTAMPTZ NOT NULL,
  source TEXT DEFAULT 'imported' NOT NULL,
  topic_tag TEXT,
  raw JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- 9. AUDIT LOGS TABLE
CREATE TABLE threads.audit_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  actor_id UUID REFERENCES threads.profiles(id),
  action TEXT NOT NULL,
  target TEXT,
  meta JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- 10. ENABLE RLS ON ALL TABLES IN THREADS SCHEMA
ALTER TABLE threads.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE threads.threads_accounts ENABLE ROW LEVEL SECURITY;
ALTER TABLE threads.oauth_states ENABLE ROW LEVEL SECURITY;
ALTER TABLE threads.scheduled_posts ENABLE ROW LEVEL SECURITY;
ALTER TABLE threads.posts ENABLE ROW LEVEL SECURITY;
ALTER TABLE threads.audit_logs ENABLE ROW LEVEL SECURITY;

-- 11. RLS POLICIES
CREATE POLICY "User can view own profile" ON threads.profiles FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Admin full access profiles" ON threads.profiles FOR ALL USING (threads.is_admin());

CREATE POLICY "User can view own threads_account" ON threads.threads_accounts FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "User can update own threads_account" ON threads.threads_accounts FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Admin full access threads_accounts" ON threads.threads_accounts FOR ALL USING (threads.is_admin());

CREATE POLICY "User manage own scheduled_posts" ON threads.scheduled_posts FOR ALL 
  USING (account_id IN (SELECT id FROM threads.threads_accounts WHERE user_id = auth.uid()));

CREATE POLICY "User view own posts" ON threads.posts FOR SELECT 
  USING (account_id IN (SELECT id FROM threads.threads_accounts WHERE user_id = auth.uid()));

CREATE POLICY "Admin view audit logs" ON threads.audit_logs FOR SELECT USING (threads.is_admin());
```

#### `./supabase/migrations/20261009000001_p2_metrics_and_import.sql`
```sql
-- 1. TABEL POST METRICS (SNAPSHOTS)
CREATE TABLE IF NOT EXISTS threads.post_metrics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  post_id UUID NOT NULL REFERENCES threads.posts(id) ON DELETE CASCADE,
  snapshot_label TEXT NOT NULL CHECK (snapshot_label IN ('1h', '24h', '72h', '7d', 'latest')),
  views INT DEFAULT 0 NOT NULL,
  likes INT DEFAULT 0 NOT NULL,
  replies INT DEFAULT 0 NOT NULL,
  reposts INT DEFAULT 0 NOT NULL,
  quotes INT DEFAULT 0 NOT NULL,
  shares INT DEFAULT 0 NOT NULL,
  clicks INT DEFAULT 0 NOT NULL,
  captured_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
  CONSTRAINT unique_post_snapshot UNIQUE(post_id, snapshot_label)
);

-- 2. TABEL ACCOUNT INSIGHTS DAILY
CREATE TABLE IF NOT EXISTS threads.account_insights_daily (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  account_id UUID NOT NULL REFERENCES threads.threads_accounts(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  views INT DEFAULT 0 NOT NULL,
  likes INT DEFAULT 0 NOT NULL,
  replies INT DEFAULT 0 NOT NULL,
  reposts INT DEFAULT 0 NOT NULL,
  quotes INT DEFAULT 0 NOT NULL,
  followers_count INT DEFAULT 0 NOT NULL,
  demographics JSONB DEFAULT '{}'::jsonb NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
  CONSTRAINT unique_account_date UNIQUE(account_id, date)
);

-- 3. ENABLE RLS
ALTER TABLE threads.post_metrics ENABLE ROW LEVEL SECURITY;
ALTER TABLE threads.account_insights_daily ENABLE ROW LEVEL SECURITY;

-- 4. RLS POLICIES
CREATE POLICY "User view own post metrics" ON threads.post_metrics FOR SELECT
  USING (post_id IN (
    SELECT p.id FROM threads.posts p 
    JOIN threads.threads_accounts ta ON p.account_id = ta.id 
    WHERE ta.user_id = auth.uid()
  ));

CREATE POLICY "User view own account insights" ON threads.account_insights_daily FOR SELECT
  USING (account_id IN (
    SELECT id FROM threads.threads_accounts WHERE user_id = auth.uid()
  ));
```

#### `./supabase/migrations/20261009000002_p3_quota_tracker.sql`
```sql
-- 1. TABEL QUOTA USAGE
CREATE TABLE IF NOT EXISTS threads.quota_usage (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  account_id UUID NOT NULL REFERENCES threads.threads_accounts(id) ON DELETE CASCADE,
  kind TEXT NOT NULL CHECK (kind IN ('publish', 'reply', 'keyword')),
  window_start TIMESTAMPTZ NOT NULL,
  used INT DEFAULT 0 NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
  CONSTRAINT unique_account_kind_window UNIQUE(account_id, kind, window_start)
);

-- 2. ENABLE RLS
ALTER TABLE threads.quota_usage ENABLE ROW LEVEL SECURITY;

-- 3. DROP POLICY DULU JIKA SUDAH ADA
DROP POLICY IF EXISTS "User view own quota usage" ON threads.quota_usage;

-- 4. BUAT POLICY BARU
CREATE POLICY "User view own quota usage" ON threads.quota_usage FOR SELECT
  USING (account_id IN (
    SELECT id FROM threads.threads_accounts WHERE user_id = auth.uid()
  ));
```

#### `./supabase/migrations/20261009000003_p4_replies_and_inbox.sql`
```sql
-- 1. TABEL REPLIES
CREATE TABLE IF NOT EXISTS threads.replies (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  account_id UUID NOT NULL REFERENCES threads.threads_accounts(id) ON DELETE CASCADE,
  post_id UUID REFERENCES threads.posts(id) ON DELETE SET NULL,
  threads_reply_id TEXT UNIQUE NOT NULL,
  parent_reply_id TEXT,
  author_username TEXT NOT NULL,
  text TEXT NOT NULL,
  replied_at TIMESTAMPTZ NOT NULL,
  hide_status TEXT DEFAULT 'visible' NOT NULL CHECK (hide_status IN ('visible', 'hidden')),
  is_own BOOLEAN DEFAULT FALSE NOT NULL,
  classification TEXT DEFAULT 'unclassified' CHECK (classification IN ('unclassified', 'question', 'praise', 'spam', 'toxic', 'neutral')),
  processed_at TIMESTAMPTZ,
  raw JSONB DEFAULT '{}'::jsonb NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- 2. ENABLE RLS
ALTER TABLE threads.replies ENABLE ROW LEVEL SECURITY;

-- 3. DROP POLICY IF EXISTS
DROP POLICY IF EXISTS "User view own replies" ON threads.replies;
DROP POLICY IF EXISTS "User update own replies" ON threads.replies;

-- 4. RLS POLICIES
CREATE POLICY "User view own replies" ON threads.replies FOR SELECT
  USING (account_id IN (
    SELECT id FROM threads.threads_accounts WHERE user_id = auth.uid()
  ));

CREATE POLICY "User update own replies" ON threads.replies FOR UPDATE
  USING (account_id IN (
    SELECT id FROM threads.threads_accounts WHERE user_id = auth.uid()
  ));
```

#### `./supabase/migrations/20261009000004_p5_auto_reply.sql`
```sql
-- 1. TABEL AUTO REPLY SETTINGS
CREATE TABLE IF NOT EXISTS threads.auto_reply_settings (
  account_id UUID PRIMARY KEY REFERENCES threads.threads_accounts(id) ON DELETE CASCADE,
  enabled BOOLEAN DEFAULT FALSE NOT NULL,
  mode TEXT DEFAULT 'review' CHECK (mode IN ('review', 'auto')),
  tone_prompt TEXT DEFAULT 'Balas dengan ramah, profesional, dan ringkas.',
  knowledge_base TEXT DEFAULT '',
  rules JSONB DEFAULT '{"blocklist": [], "skip_usernames": [], "only_questions": false}'::jsonb NOT NULL,
  max_per_hour INT DEFAULT 10 NOT NULL,
  max_per_day INT DEFAULT 50 NOT NULL,
  cooldown_per_user_minutes INT DEFAULT 60 NOT NULL,
  hide_toxic BOOLEAN DEFAULT TRUE NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- 2. TABEL AUTO REPLY LOGS
CREATE TABLE IF NOT EXISTS threads.auto_reply_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  account_id UUID NOT NULL REFERENCES threads.threads_accounts(id) ON DELETE CASCADE,
  reply_id UUID UNIQUE NOT NULL REFERENCES threads.replies(id) ON DELETE CASCADE,
  status threads.reply_log_status_type DEFAULT 'pending_review' NOT NULL,
  generated_text TEXT,
  final_text TEXT,
  skip_reason TEXT,
  llm_meta JSONB DEFAULT '{}'::jsonb,
  sent_media_id TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- 3. ENABLE RLS
ALTER TABLE threads.auto_reply_settings ENABLE ROW LEVEL SECURITY;
ALTER TABLE threads.auto_reply_logs ENABLE ROW LEVEL SECURITY;

-- 4. DROP POLICY IF EXISTS
DROP POLICY IF EXISTS "User manage own auto_reply_settings" ON threads.auto_reply_settings;
DROP POLICY IF EXISTS "User manage own auto_reply_logs" ON threads.auto_reply_logs;

-- 5. RLS POLICIES
CREATE POLICY "User manage own auto_reply_settings" ON threads.auto_reply_settings FOR ALL
  USING (account_id IN (SELECT id FROM threads.threads_accounts WHERE user_id = auth.uid()));

CREATE POLICY "User manage own auto_reply_logs" ON threads.auto_reply_logs FOR ALL
  USING (account_id IN (SELECT id FROM threads.threads_accounts WHERE user_id = auth.uid()));
```

#### `./supabase/migrations/20261009000005_p6_content_scoring.sql`
```sql
-- 1. TABEL CONTENT SCORES
CREATE TABLE IF NOT EXISTS threads.content_scores (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  account_id UUID NOT NULL REFERENCES threads.threads_accounts(id) ON DELETE CASCADE,
  scheduled_post_id UUID REFERENCES threads.scheduled_posts(id) ON DELETE CASCADE,
  score INT NOT NULL CHECK (score >= 0 AND score <= 100),
  breakdown JSONB DEFAULT '{}'::jsonb NOT NULL,
  suggestions JSONB DEFAULT '[]'::jsonb NOT NULL,
  model_version TEXT DEFAULT 'v1.0' NOT NULL,
  actual_engagement NUMERIC,
  created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- 2. ENABLE RLS
ALTER TABLE threads.content_scores ENABLE ROW LEVEL SECURITY;

-- 3. DROP POLICY IF EXISTS
DROP POLICY IF EXISTS "User view own content_scores" ON threads.content_scores;

-- 4. RLS POLICIES
CREATE POLICY "User view own content_scores" ON threads.content_scores FOR SELECT
  USING (account_id IN (
    SELECT id FROM threads.threads_accounts WHERE user_id = auth.uid()
  ));
```

#### `./supabase/migrations/20261009000006_p8_keyword_watch.sql`
```sql
-- 1. TABEL KEYWORD WATCHES
CREATE TABLE IF NOT EXISTS threads.keyword_watches (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  account_id UUID NOT NULL REFERENCES threads.threads_accounts(id) ON DELETE CASCADE,
  query TEXT NOT NULL,
  search_type TEXT DEFAULT 'TOP' CHECK (search_type IN ('TOP', 'RECENT')),
  is_active BOOLEAN DEFAULT TRUE NOT NULL,
  last_run_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- 2. TABEL KEYWORD RESULTS
CREATE TABLE IF NOT EXISTS threads.keyword_results (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  watch_id UUID NOT NULL REFERENCES threads.keyword_watches(id) ON DELETE CASCADE,
  threads_media_id TEXT NOT NULL,
  username TEXT NOT NULL,
  text TEXT,
  posted_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
  CONSTRAINT unique_watch_media UNIQUE(watch_id, threads_media_id)
);

-- 3. ENABLE RLS
ALTER TABLE threads.keyword_watches ENABLE ROW LEVEL SECURITY;
ALTER TABLE threads.keyword_results ENABLE ROW LEVEL SECURITY;

-- 4. DROP POLICY IF EXISTS
DROP POLICY IF EXISTS "User manage own keyword_watches" ON threads.keyword_watches;
DROP POLICY IF EXISTS "User view own keyword_results" ON threads.keyword_results;

-- 5. RLS POLICIES
CREATE POLICY "User manage own keyword_watches" ON threads.keyword_watches FOR ALL
  USING (account_id IN (SELECT id FROM threads.threads_accounts WHERE user_id = auth.uid()));

CREATE POLICY "User view own keyword_results" ON threads.keyword_results FOR SELECT
  USING (watch_id IN (
    SELECT kw.id FROM threads.keyword_watches kw
    JOIN threads.threads_accounts ta ON kw.account_id = ta.id
    WHERE ta.user_id = auth.uid()
  ));
```

#### `./supabase/migrations/20261009000007_p9_notifications_and_health.sql`
```sql
-- 1. TABEL NOTIFICATIONS
CREATE TABLE IF NOT EXISTS threads.notifications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES threads.profiles(id) ON DELETE CASCADE,
  type TEXT NOT NULL,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  read_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- 2. TABEL API CALL LOGS (OBSERVABILITY)
CREATE TABLE IF NOT EXISTS threads.api_call_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  account_id UUID REFERENCES threads.threads_accounts(id) ON DELETE CASCADE,
  endpoint TEXT NOT NULL,
  status INT NOT NULL,
  error TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- 3. ENABLE RLS
ALTER TABLE threads.notifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE threads.api_call_logs ENABLE ROW LEVEL SECURITY;

-- 4. DROP POLICY IF EXISTS
DROP POLICY IF EXISTS "User view own notifications" ON threads.notifications;
DROP POLICY IF EXISTS "User update own notifications" ON threads.notifications;
DROP POLICY IF EXISTS "Admin view api_call_logs" ON threads.api_call_logs;

-- 5. RLS POLICIES
CREATE POLICY "User view own notifications" ON threads.notifications FOR SELECT
  USING (user_id = auth.uid());

CREATE POLICY "User update own notifications" ON threads.notifications FOR UPDATE
  USING (user_id = auth.uid());

CREATE POLICY "Admin view api_call_logs" ON threads.api_call_logs FOR SELECT
  USING (threads.is_admin());
```

### Backend Database Models / Schemas
_Tidak ditemukan file models Python._
