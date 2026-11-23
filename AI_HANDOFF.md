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
