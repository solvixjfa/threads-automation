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
