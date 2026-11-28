-- ============================================================================
-- MIGRATION: 4-TIER PRICING (STARTER, PRO, BUSINESS, AGENCY) & ACCOUNT LIMITS
-- ============================================================================

-- 1. Update batas maksimal akun per paket (pertahankan paid_credit & paid_byok untuk user beta lama)
CREATE OR REPLACE FUNCTION threads.get_max_accounts(p_plan TEXT, p_role TEXT DEFAULT 'user')
RETURNS INT AS $$
BEGIN
  IF p_role = 'admin' THEN
    RETURN 50;
  ELSIF p_plan = 'agency' THEN
    RETURN 50;
  ELSIF p_plan = 'business' THEN
    RETURN 20;
  ELSIF p_plan = 'pro' THEN
    RETURN 5;
  ELSIF p_plan = 'starter' THEN
    RETURN 2;
  ELSIF p_plan = 'paid_credit' THEN
    RETURN 10;
  ELSIF p_plan = 'paid_byok' THEN
    RETURN 3;
  ELSE
    RETURN 1;
  END IF;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- 2. Update urutan prioritas warisan paket saat connect akun Threads baru
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
      WHEN 'agency' THEN 7
      WHEN 'business' THEN 6
      WHEN 'pro' THEN 5
      WHEN 'starter' THEN 4
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
