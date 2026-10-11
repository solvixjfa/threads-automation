import os
import httpx
import logging
import re
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

# Daftar kata kunci yang sering dipakai orang saat mau beli/tanya layanan
BUYING_KEYWORDS = [
    r"\bberapa\b", r"\bharga\b", r"\bminat\b", r"\bpesan\b", 
    r"\border\b", r"\bpricelist\b", r"\bdm\b", r"\bcara beli\b", 
    r"\bmau\b", r"\btertarik\b", r"\bfee\b", r"\bkerjasama\b",
    r"\bkerja sama\b", r"\bbuatkan\b", r"\bbikinin\b"
]

def get_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def detect_buying_intent(comment: str) -> bool:
    comment_lower = comment.lower()
    for pattern in BUYING_KEYWORDS:
        if re.search(pattern, comment_lower):
            return True
    return False

async def analyze_and_notify_lead(account_id: str, username: str, comment: str) -> dict:
    is_lead = detect_buying_intent(comment)
    
    result = {
        "is_lead": is_lead,
        "method": "rule-based",
        "comment": comment
    }

    # Jika bukan lead, langsung return tanpa memproses webhook
    if not is_lead:
        return result

    # Jika Lead, ambil setting user untuk nembak webhook (Make.com / Discord)
    db = get_supabase()
    res = db.schema("threads").from_("threads_accounts").select("username, settings").eq("id", account_id).maybeSingle().execute()
    account = res.data

    if account:
        settings = account.get("settings") or {}
        webhook_url = settings.get("lead_webhook_url")

        if webhook_url:
            payload = {
                "content": f"🚨 **Hot Lead Detected for @{account.get('username')}!**",
                "embeds": [{
                    "title": "Ada prospek baru di Threads!",
                    "color": 5814783,
                    "fields": [
                        {"name": "Username", "value": f"@{username}", "inline": True},
                        {"name": "Komentar", "value": f"_{comment}_", "inline": False}
                    ]
                }]
            }
            
            try:
                async with httpx.AsyncClient() as http_client:
                    await http_client.post(webhook_url, json=payload, timeout=5.0)
            except Exception as e:
                logging.error(f"Gagal memicu webhook untuk akun {account_id}: {str(e)}")

    return result
