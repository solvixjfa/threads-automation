import uuid
import logging
from app.core.config import CREDIT_COSTS
from app.services.rag import get_supabase
from fastapi import HTTPException
from datetime import datetime, timezone

class BillingError(Exception):
    def __init__(self, message, code):
        self.message = message
        self.code = code
        super().__init__(self.message)

def check_and_spend(account_id: str, action_type: str) -> str:
    """Mengecek plan dan memotong kredit. Return ref_id untuk refund."""
    db = get_supabase()
    
    # FIX: Ganti maybeSingle() jadi limit(1).execute()
    acc = db.schema("threads").from_("threads_accounts").select("plan, plan_expires_at, credit_balance, custom_gemini_key, custom_groq_key").eq("id", account_id).limit(1).execute()
    
    if not acc.data:
        raise BillingError("Account not found", "NOT_FOUND")

    # FIX: Ambil index [0] karena data berupa list
    acc_data = acc.data[0]
    plan = acc_data.get("plan", "none")
    expires_at = acc_data.get("plan_expires_at")
    balance = acc_data.get("credit_balance", 0)
    
    if plan == "none":
        raise BillingError("Plan kamu sudah berakhir. Perpanjang untuk memakai fitur AI.", "PLAN_EXPIRED")

    # Cek expiry (Supabase returns ISO string)
    if expires_at:
        try:
            exp_dt = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
            if exp_dt < datetime.now(timezone.utc):
                raise BillingError("Plan kamu sudah berakhir. Perpanjang untuk memakai fitur AI.", "PLAN_EXPIRED")
        except ValueError:
            pass 

    # 2. Dapatkan Cost
    cost = CREDIT_COSTS.get(action_type, 1)
    if cost == 0:
        return str(uuid.uuid4()) # No cost

    # 3. Eksekusi RPC Atomik
    ref_id = str(uuid.uuid4())
    try:
        db.rpc("spend_credits", {
            "p_account_id": account_id,
            "p_amount": cost,
            "p_action_type": action_type,
            "p_ref_id": ref_id
        }).execute()
    except Exception as e:
        err_str = str(e)
        if "INSUFFICIENT_CREDITS" in err_str:
            raise BillingError("Kredit bulan ini habis. Reply otomatis memakai template sampai periode berikutnya.", "INSUFFICIENT_CREDITS")
        elif "PLAN_EXPIRED" in err_str:
            raise BillingError("Plan kamu sudah berakhir. Perpanjang untuk memakai fitur AI.", "PLAN_EXPIRED")
        else:
            logging.error(f"Billing RPC Error: {err_str}")
            raise HTTPException(status_code=500, detail="Internal billing error")

    return ref_id

def refund_credits(account_id: str, action_type: str, ref_id: str):
    """Mengembalikan kredit jika LLM gagal."""
    db = get_supabase()
    cost = CREDIT_COSTS.get(action_type, 1)
    if cost == 0:
        return

    try:
        db.rpc("refund_credits", {
            "p_account_id": account_id,
            "p_amount": cost,
            "p_action_type": action_type,
            "p_ref_id": ref_id
        }).execute()
        logging.info(f"[Billing] Refunded {cost} credits for {action_type} ({ref_id})")
    except Exception as e:
        logging.error(f"[Billing] Failed to refund: {str(e)}")
