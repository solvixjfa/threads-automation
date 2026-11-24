DROP TRIGGER IF EXISTS trg_sync_user_plan_across_accounts ON threads.threads_accounts;
DROP FUNCTION IF EXISTS threads.sync_user_plan_across_accounts();
DROP TRIGGER IF EXISTS trg_inherit_user_plan_on_insert ON threads.threads_accounts;
DROP FUNCTION IF EXISTS threads.inherit_user_plan_on_insert();
DROP FUNCTION IF EXISTS threads.get_max_accounts(TEXT, TEXT);

ALTER TABLE threads.profiles
  DROP COLUMN IF EXISTS plan_started_at,
  DROP COLUMN IF EXISTS plan_expires_at,
  DROP COLUMN IF EXISTS credit_balance,
  DROP COLUMN IF EXISTS pending_plan,
  DROP COLUMN IF EXISTS custom_gemini_key,
  DROP COLUMN IF EXISTS custom_groq_key;
