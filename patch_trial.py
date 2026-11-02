p = "backend/app/workers/replies.py"
s = open(p).read()

old_block = '''    # --- AUTO TRIAL LOGIC ---
    from app.core.config import TRIAL_DAYS, TRIAL_CREDITS
    plan = acc.get("plan")
    if (plan is None or plan == "none") and not acc.get("plan_started_at"):
        now = datetime.now(timezone.utc)
        expires = now + timedelta(days=TRIAL_DAYS)
        db.schema("threads").from_("threads_accounts").update({
            "plan": "trial",
            "plan_started_at": now.isoformat(),
            "plan_expires_at": expires.isoformat(),
            "credit_balance": TRIAL_CREDITS
        }).eq("id", acc_id).execute()
        try:
            db.schema("threads").from_("credit_ledger").insert({
                "account_id": acc_id, "delta": TRIAL_CREDITS, "reason": "trial_start",
                "note": "Auto granted trial upon first connection"
            }).execute()
        except Exception as e:
            logging.warning(f"[Auto Trial] Gagal insert ledger: {e}")
        logging.info(f"[Auto Trial] Granted {TRIAL_CREDITS} credits to {acc_id}")
    # ------------------------'''

new_block = '''    # --- AUTO TRIAL LOGIC ---
    from app.core.config import TRIAL_DAYS, TRIAL_CREDITS
    plan = acc.get("plan")
    if plan is None or plan in ("none", "free", ""):
        already = (
            db.schema("threads").from_("credit_ledger")
            .select("id").eq("account_id", acc_id).eq("reason", "trial_start")
            .limit(1).execute()
        )
        if not (already.data or []):
            now = datetime.now(timezone.utc)
            expires = now + timedelta(days=TRIAL_DAYS)
            db.schema("threads").from_("threads_accounts").update({
                "plan": "trial",
                "plan_started_at": now.isoformat(),
                "plan_expires_at": expires.isoformat(),
                "credit_balance": TRIAL_CREDITS
            }).eq("id", acc_id).execute()
            try:
                db.schema("threads").from_("credit_ledger").insert({
                    "account_id": acc_id, "delta": TRIAL_CREDITS, "reason": "trial_start",
                    "note": "Auto granted trial upon first connection"
                }).execute()
            except Exception as e:
                logging.warning(f"[Auto Trial] Gagal insert ledger: {e}")
            logging.info(f"[Auto Trial] Granted {TRIAL_CREDITS} credits to {acc_id}")
    # ------------------------'''

if old_block not in s:
    print("[FAIL] old trial block not found"); raise SystemExit(1)
s = s.replace(old_block, new_block, 1)
open(p, "w").write(s)
print("[OK] trial block patched")
