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
