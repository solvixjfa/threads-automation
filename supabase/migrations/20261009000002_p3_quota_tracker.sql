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
