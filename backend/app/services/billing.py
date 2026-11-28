import uuid
import logging
from app.core.config import BYOK_PLANS
from app.services.rag import get_supabase
from fastapi import HTTPException
from datetime import datetime, timezone

class BillingError(Exception):
    def __init__(self, message, code):
        self.message = message
        self.code = code
        super().__init__(self.message)

def check_and_spend(account_id: str, action_type: str) -> str:
    """Validasi plan aktif & saldo > 0 di awal. Pemotongan dilakukan setelah token AI diketahui."""
    db = get_supabase()

    acc = db.schema("threads").from_("threads_accounts").select(
        "plan, plan_expires_at, credit_balance, custom_gemini_key, custom_groq_key"
    ).eq("id", account_id).limit(1).execute()

    if not acc.data:
        raise BillingError("Account not found", "NOT_FOUND")

    acc_data = acc.data[0]
    plan = acc_data.get("plan", "none")
    expires_at = acc_data.get("plan_expires_at")
    balance = acc_data.get("credit_balance", 0)

    if plan == "none":
        raise BillingError("Plan kamu sudah berakhir. Perpanjang untuk memakai fitur AI.", "PLAN_EXPIRED")

    if expires_at:
        try:
            exp_dt = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
            if exp_dt < datetime.now(timezone.utc):
                raise BillingError("Plan kamu sudah berakhir. Perpanjang untuk memakai fitur AI.", "PLAN_EXPIRED")
        except ValueError:
            pass

    # Bypass pengecekan kredit untuk paket BYOK (Agency / legacy Pro BYOK)
    if plan in BYOK_PLANS:
        return str(uuid.uuid4())

    if balance <= 0:
        raise BillingError("Kredit token bulan ini habis. Upgrade atau tunggu periode berikutnya.", "INSUFFICIENT_CREDITS")

    return str(uuid.uuid4())

def spend_token_credits(account_id: str, action_type: str, total_tokens: int, ref_id: str = None):
    """Memotong credit_balance sesuai total token (prompt + completion) setelah AI selesai."""
    tokens = int(total_tokens or 0)
    if tokens <= 0:
        return

    db = get_supabase()
    acc = db.schema("threads").from_("threads_accounts").select("plan, credit_balance").eq("id", account_id).limit(1).execute()
    if not acc.data:
        return

    plan = acc.data[0].get("plan", "none")
    balance = int(acc.data[0].get("credit_balance") or 0)

    if plan in BYOK_PLANS or balance <= 0:
        return

    # Batasi maksimal sebesar sisa saldo agar generasi terakhir tidak gagal RPC
    deduct_amount = min(balance, tokens)
    tx_ref = ref_id or str(uuid.uuid4())

    try:
        db.schema("threads").rpc("spend_credits", {
            "p_account_id": account_id,
            "p_amount": deduct_amount,
            "p_action_type": action_type,
            "p_ref_id": tx_ref
        }).execute()
        logging.info(f"[Billing] Deducted {deduct_amount} token-credits for {action_type} (acc={account_id})")
    except Exception as e:
        logging.error(f"[Billing] Failed to deduct {deduct_amount} token-credits: {str(e)}")

def refund_credits(account_id: str, action_type: str, ref_id: str):
    """No-op karena pemotongan dilakukan setelah generasi sukses."""
    return
