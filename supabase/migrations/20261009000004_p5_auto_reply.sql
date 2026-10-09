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
