import os
os.system("git checkout HEAD~1 backend/app/workers/replies.py backend/app/api/v1/admin.py")
with open('backend/app/api/v1/admin.py', 'r') as f:
    admin_c = f.read()
old_admin = '''    now = datetime.now(timezone.utc)
    current_exp = acc.data[0].get("plan_expires_at")
    target_user_id = acc.data[0].get("user_id")'''
new_admin = '''    if payload.plan_type == 'trial':
        days = 7
        credits = 20
    else:
        days = PAID_DAYS
        credits = PAID_CREDITS if payload.plan_type == 'paid_credit' else 0

    now = datetime.now(timezone.utc)
    current_exp = acc.data[0].get("plan_expires_at")
    target_user_id = acc.data[0].get("user_id")'''
if old_admin in admin_c: admin_c = admin_c.replace(old_admin, new_admin)
old_credits = '''    if payload.plan_type == 'trial':
        days = 7
        credits = 20
    else:
        days = PAID_DAYS
        credits = PAID_CREDITS if payload.plan_type == 'paid_credit' else 0

    db.schema'''
new_credits = '''    db.schema'''
if old_credits in admin_c: admin_c = admin_c.replace(old_credits, new_credits)
with open('backend/app/api/v1/admin.py', 'w', newline='\n') as f: f.write(admin_c)
with open('backend/app/workers/replies.py', 'r') as f: rep_c = f.read()
trial_block = '''
    # --- AUTO TRIAL LOGIC ---
    from app.core.config import TRIAL_DAYS, TRIAL_CREDITS
    plan = acc.get("plan")
    if (plan is None or plan == "none") and not acc.get("plan_started_at"):
        from datetime import datetime, timezone, timedelta
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
                "account_id": acc_id,
                "delta": TRIAL_CREDITS,
                "reason": "trial_start",
                "note": "Auto granted trial upon first connection"
            }).execute()
        except Exception as e:
            logging.warning(f"[Auto Trial] Gagal insert ledger: {e}")

        logging.info(f"[Auto Trial] Granted {TRIAL_CREDITS} credits to {acc_id}")
    # ------------------------
'''
target = '    token = acc.get("settings", {}).get("access_token")\n'
if target in rep_c and 'AUTO TRIAL LOGIC' not in rep_c:
    rep_c = rep_c.replace(target, target + trial_block)
with open('backend/app/workers/replies.py', 'w', newline='\n') as f: f.write(rep_c)
print('✅ FIX SUCCESS')
