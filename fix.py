import re

file_path = 'backend/app/workers/replies.py'
with open(file_path, 'r') as f:
    content = f.read()

# 1. Bersihin karakter aneh \r kalau ada
content = content.replace('\r\n', '\n').replace('\r', '\n')

# 2. Blok fungsi baru yang 100% rapi (tanpa error indentasi)
clean_func = """async def process_account(db, client, acc: dict) -> dict:
    account_stats = {"new_posts": 0, **empty_stats()}

    acc_id = acc["id"]
    acc_username = acc.get("username", "")
    token = acc.get("settings", {}).get("access_token")

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

    if not token:"""

# 3. Ganti total dari awal fungsi sampai sebelum 'if not token:'
content = re.sub(r'async def process_account\(db, client, acc: dict\) -> dict:.*?if not token:', clean_func, content, flags=re.DOTALL)

# 4. Tulis ulang paksa format Linux
with open(file_path, 'w', newline='\n') as f:
    f.write(content)

print("✅ SUKSES: File replies.py berhasil di-fix total dengan indentasi yang rapi!")
