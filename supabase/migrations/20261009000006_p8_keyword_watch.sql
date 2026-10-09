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
