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
