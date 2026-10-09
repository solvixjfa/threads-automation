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
