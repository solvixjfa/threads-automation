-- ============================================================================
-- MIGRATION: MULTI-ACCOUNT SHARED PLAN, CREDITS & BYOK SYNCHRONIZATION
-- ============================================================================

-- 1. Tambah kolom terpusat di threads.profiles sebagai cadangan jika user bayar sebelum connect akun
ALTER TABLE threads.profiles
  ADD COLUMN IF NOT EXISTS plan_started_at TIMESTAMPTZ,
  ADD COLUMN IF NOT EXISTS plan_expires_at TIMESTAMPTZ,
  ADD COLUMN IF NOT EXISTS credit_balance INT DEFAULT 0 NOT NULL,
  ADD COLUMN IF NOT EXISTS pending_plan TEXT,
  ADD COLUMN IF NOT EXISTS custom_gemini_key TEXT,
  ADD COLUMN IF NOT EXISTS custom_groq_key TEXT;

-- 2. Helper function untuk batas maksimal akun per paket
CREATE OR REPLACE FUNCTION threads.get_max_accounts(p_plan TEXT, p_role TEXT DEFAULT 'user')
RETURNS INT AS $$
BEGIN
  IF p_role = 'admin' THEN
    RETURN 50;
  ELSIF p_plan = 'paid_credit' THEN
    RETURN 10;
  ELSIF p_plan = 'paid_byok' THEN
    RETURN 3;
  ELSE
    RETURN 1;
  END IF;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- 3. Trigger BEFORE INSERT pada threads_accounts:
--    Otomatis mewarisi plan, kredit, BYOK keys, dan role dari akun lain milik user_id yang sama (atau dari profiles)
CREATE OR REPLACE FUNCTION threads.inherit_user_plan_on_insert()
RETURNS TRIGGER AS $$
DECLARE
  v_sibling RECORD;
  v_profile RECORD;
BEGIN
  SELECT plan, plan_started_at, plan_expires_at, credit_balance, pending_plan,
         custom_gemini_key, custom_groq_key, role
  INTO v_sibling
  FROM threads.threads_accounts
  WHERE user_id = NEW.user_id
  ORDER BY
    CASE plan
      WHEN 'paid_credit' THEN 4
      WHEN 'paid_byok' THEN 3
      WHEN 'trial' THEN 2
      ELSE 1
    END DESC,
    created_at ASC
  LIMIT 1;

  IF FOUND THEN
    NEW.plan := COALESCE(v_sibling.plan, 'none');
    NEW.plan_started_at := v_sibling.plan_started_at;
    NEW.plan_expires_at := v_sibling.plan_expires_at;
    NEW.credit_balance := COALESCE(v_sibling.credit_balance, 0);
    NEW.pending_plan := v_sibling.pending_plan;
    NEW.custom_gemini_key := v_sibling.custom_gemini_key;
    NEW.custom_groq_key := v_sibling.custom_groq_key;
    NEW.role := COALESCE(v_sibling.role, 'user');
  ELSE
    SELECT plan, plan_started_at, plan_expires_at, credit_balance, pending_plan,
           custom_gemini_key, custom_groq_key, role::text AS role_text
    INTO v_profile
    FROM threads.profiles
    WHERE id = NEW.user_id;

    IF FOUND THEN
      IF v_profile.plan IS NOT NULL AND v_profile.plan <> 'free' THEN
        NEW.plan := v_profile.plan;
      END IF;
      IF v_profile.plan_started_at IS NOT NULL THEN
        NEW.plan_started_at := v_profile.plan_started_at;
      END IF;
      IF v_profile.plan_expires_at IS NOT NULL THEN
        NEW.plan_expires_at := v_profile.plan_expires_at;
      END IF;
      IF COALESCE(v_profile.credit_balance, 0) > 0 THEN
        NEW.credit_balance := v_profile.credit_balance;
      END IF;
      NEW.pending_plan := COALESCE(v_profile.pending_plan, NEW.pending_plan);
      NEW.custom_gemini_key := COALESCE(v_profile.custom_gemini_key, NEW.custom_gemini_key);
      NEW.custom_groq_key := COALESCE(v_profile.custom_groq_key, NEW.custom_groq_key);
      IF v_profile.role_text = 'admin' THEN
        NEW.role := 'admin';
      END IF;
    END IF;
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS trg_inherit_user_plan_on_insert ON threads.threads_accounts;
CREATE TRIGGER trg_inherit_user_plan_on_insert
  BEFORE INSERT ON threads.threads_accounts
  FOR EACH ROW
  EXECUTE FUNCTION threads.inherit_user_plan_on_insert();

-- 4. Trigger AFTER UPDATE pada threads_accounts:
--    Menyinkronkan perubahan plan, kredit, dan BYOK keys ke semua akun lain milik user_id yang sama + profiles
CREATE OR REPLACE FUNCTION threads.sync_user_plan_across_accounts()
RETURNS TRIGGER AS $$
BEGIN
  -- Cegah recursive trigger loop saat mengupdate baris saudara milik user yang sama
  IF pg_trigger_depth() > 1 THEN
    RETURN NEW;
  END IF;

  UPDATE threads.threads_accounts
  SET
    plan = NEW.plan,
    plan_started_at = NEW.plan_started_at,
    plan_expires_at = NEW.plan_expires_at,
    credit_balance = NEW.credit_balance,
    pending_plan = NEW.pending_plan,
    custom_gemini_key = NEW.custom_gemini_key,
    custom_groq_key = NEW.custom_groq_key
  WHERE user_id = NEW.user_id
    AND id <> NEW.id;

  UPDATE threads.profiles
  SET
    plan = COALESCE(NEW.plan, 'free'),
    plan_started_at = NEW.plan_started_at,
    plan_expires_at = NEW.plan_expires_at,
    credit_balance = COALESCE(NEW.credit_balance, 0),
    pending_plan = NEW.pending_plan,
    custom_gemini_key = NEW.custom_gemini_key,
    custom_groq_key = NEW.custom_groq_key
  WHERE id = NEW.user_id;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS trg_sync_user_plan_across_accounts ON threads.threads_accounts;
CREATE TRIGGER trg_sync_user_plan_across_accounts
  AFTER UPDATE OF plan, plan_started_at, plan_expires_at, credit_balance, pending_plan, custom_gemini_key, custom_groq_key
  ON threads.threads_accounts
  FOR EACH ROW
  EXECUTE FUNCTION threads.sync_user_plan_across_accounts();

-- 5. Backfill data existing agar semua akun milik user yang sama langsung sinkron
WITH ranked_accounts AS (
  SELECT DISTINCT ON (user_id)
    user_id,
    plan,
    plan_started_at,
    plan_expires_at,
    credit_balance,
    pending_plan,
    custom_gemini_key,
    custom_groq_key
  FROM threads.threads_accounts
  ORDER BY
    user_id,
    CASE plan
      WHEN 'paid_credit' THEN 4
      WHEN 'paid_byok' THEN 3
      WHEN 'trial' THEN 2
      ELSE 1
    END DESC,
    credit_balance DESC,
    created_at ASC
)
UPDATE threads.threads_accounts ta
SET
  plan = ra.plan,
  plan_started_at = ra.plan_started_at,
  plan_expires_at = ra.plan_expires_at,
  credit_balance = ra.credit_balance,
  pending_plan = ra.pending_plan,
  custom_gemini_key = COALESCE(ta.custom_gemini_key, ra.custom_gemini_key),
  custom_groq_key = COALESCE(ta.custom_groq_key, ra.custom_groq_key)
FROM ranked_accounts ra
WHERE ta.user_id = ra.user_id;
