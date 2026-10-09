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
