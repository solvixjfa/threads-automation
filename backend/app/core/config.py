import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# BILLING CONFIG
TRIAL_DAYS = int(os.getenv("TRIAL_DAYS", "7"))
TRIAL_CREDITS = int(os.getenv("TRIAL_CREDITS", "20"))
PAID_DAYS = int(os.getenv("PAID_DAYS", "30"))
PAID_CREDITS = int(os.getenv("PAID_CREDITS", "100"))
REPLY_MAX_PER_HOUR = int(os.getenv("REPLY_MAX_PER_HOUR", "5"))
REMINDER_DAYS_BEFORE_EXPIRY = int(os.getenv("REMINDER_DAYS_BEFORE_EXPIRY", "3"))

# COST MAP
CREDIT_COSTS = {
    "generate": 1,
    "reply_ai": 1,
    "repurpose": 1,
    "advanced_analytics": 1,
    "deep_scoring": 1
}

def _validate():
    missing = [k for k, v in {
        "SUPABASE_URL": SUPABASE_URL,
        "SUPABASE_SERVICE_ROLE_KEY": SUPABASE_SERVICE_ROLE_KEY,
    }.items() if not v]
    if missing:
        raise RuntimeError(f"Missing required env vars: {', '.join(missing)}")

_validate()
