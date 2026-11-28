import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# BILLING CONFIG (1 Credit = 1 Token)
TRIAL_DAYS = int(os.getenv("TRIAL_DAYS", "7"))
TRIAL_CREDITS = int(os.getenv("TRIAL_CREDITS", "15000"))
PAID_DAYS = int(os.getenv("PAID_DAYS", "30"))
PAID_CREDITS = int(os.getenv("PAID_CREDITS", "100000"))
REPLY_MAX_PER_HOUR = int(os.getenv("REPLY_MAX_PER_HOUR", "5"))
REMINDER_DAYS_BEFORE_EXPIRY = int(os.getenv("REMINDER_DAYS_BEFORE_EXPIRY", "3"))

PLAN_CREDITS = {
    "trial": TRIAL_CREDITS,
    "starter": 100000,
    "pro": 300000,
    "business": 750000,
    "agency": 0,
    # Legacy beta plans (grandfathered until expiry)
    "paid_credit": 100000,
    "paid_byok": 0,
}

BYOK_PLANS = ("agency", "paid_byok")

# Validasi hanya dilakukan di awal (pemotongan mengikuti jumlah token aktual)
CREDIT_COSTS = {
    "generate": 1,
    "reply_ai": 1,
    "repurpose": 1,
    "advanced_analytics": 1,
    "deep_scoring": 1,
    "improve_draft": 1,
    "label_topics": 1,
}

def _validate():
    missing = [k for k, v in {
        "SUPABASE_URL": SUPABASE_URL,
        "SUPABASE_SERVICE_ROLE_KEY": SUPABASE_SERVICE_ROLE_KEY,
    }.items() if not v]
    if missing:
        raise RuntimeError(f"Missing required env vars: {', '.join(missing)}")

_validate()
