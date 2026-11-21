from fastapi import APIRouter, HTTPException, Header, Form
from pydantic import BaseModel
from app.services.rag import get_supabase
from app.core.config import PAID_DAYS, PAID_CREDITS
from datetime import datetime, timedelta, timezone
from typing import Optional
import hashlib
import httpx
import os
import time
import logging

router = APIRouter()
logger = logging.getLogger("uvicorn.error")

PLANS = {
    "paid_credit": {"amount": 29000, "name": "Ixiera Pro Credit (1 Bulan)"},
    "paid_byok": {"amount": 19000, "name": "Ixiera Pro BYOK (1 Bulan)"},
}

class CreateInvoiceRequest(BaseModel):
    plan_type: str
    payment_method: str = "SP"

def _md5(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()

@router.post("/create-invoice")
async def create_invoice(payload: CreateInvoiceRequest, authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing auth token")

    token = authorization.replace("Bearer ", "").strip()
    db = get_supabase()
    try:
        user_res = db.auth.get_user(token)
        if not user_res or not user_res.user:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = user_res.user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Auth failed: {str(e)}")

    selected = PLANS.get(payload.plan_type)
    if not selected:
        raise HTTPException(status_code=400, detail="Paket tidak valid")

    merchant_code = os.getenv("DUITKU_MERCHANT_CODE", "").strip()
    api_key = os.getenv("DUITKU_API_KEY", "").strip()
    is_sandbox = os.getenv("DUITKU_ENV", "sandbox").strip().lower() == "sandbox"
    backend_url = os.getenv("PUBLIC_BACKEND_URL", "https://api.ixiera.online").rstrip("/")
    frontend_url = os.getenv("PUBLIC_FRONTEND_URL", "https://app.ixiera.online").rstrip("/")

    if not merchant_code or not api_key:
        raise HTTPException(status_code=500, detail="Konfigurasi Duitku belum diisi di server")

    # Format orderId: IX--<user_id>--<plan_type>--<timestamp>
    merchant_order_id = f"IX--{user.id}--{payload.plan_type}--{int(time.time())}"
    amount = selected["amount"]
    signature = _md5(f"{merchant_code}{merchant_order_id}{amount}{api_key}")

    inquiry_url = (
        "https://sandbox.duitku.com/webapi/api/merchant/v2/inquiry"
        if is_sandbox
        else "https://passport.duitku.com/webapi/api/merchant/v2/inquiry"
    )

    req_body = {
        "merchantCode": merchant_code,
        "paymentAmount": amount,
        "paymentMethod": payload.payment_method,
        "merchantOrderId": merchant_order_id,
        "productDetails": selected["name"],
        "email": user.email or "user@ixiera.online",
        "customerVaName": (user.email or "Ixiera User").split("@")[0],
        "callbackUrl": f"{backend_url}/api/v1/payment/callback",
        "returnUrl": f"{frontend_url}/pricing?payment=success",
        "signature": signature,
        "expiryPeriod": 60,
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        res = await client.post(inquiry_url, json=req_body)
        data = res.json()

    if res.status_code != 200 or data.get("statusCode") != "00":
        logger.error(f"Duitku Inquiry Error: {data}")
        raise HTTPException(status_code=400, detail=data.get("statusMessage", "Gagal membuat invoice Duitku"))

    return {
        "success": True,
        "paymentUrl": data.get("paymentUrl"),
        "reference": data.get("reference"),
        "merchantOrderId": merchant_order_id,
    }

@router.post("/callback")
async def duitku_callback(
    merchantCode: str = Form(...),
    amount: str = Form(...),
    merchantOrderId: str = Form(...),
    resultCode: str = Form(...),
    signature: str = Form(...),
):
    api_key = os.getenv("DUITKU_API_KEY", "").strip()
    expected_sig = _md5(f"{merchantCode}{amount}{merchantOrderId}{api_key}")

    if signature != expected_sig:
        logger.warning(f"Invalid Duitku signature for order {merchantOrderId}")
        raise HTTPException(status_code=400, detail="Invalid signature")

    if resultCode == "00":
        parts = merchantOrderId.split("--")
        if len(parts) >= 3:
            user_id = parts[1]
            plan_type = parts[2]
            db = get_supabase()
            now = datetime.now(timezone.utc)
            credits = PAID_CREDITS if plan_type == "paid_credit" else 0

            # 1. Update profiles
            db.schema("threads").from_("profiles").update({"plan": plan_type}).eq("id", user_id).execute()

            # 2. Update threads_accounts jika sudah terhubung
            acc = db.schema("threads").from_("threads_accounts").select("id, plan_expires_at").eq("user_id", user_id).limit(1).execute()
            if acc.data:
                acc_id = acc.data[0]["id"]
                current_exp = acc.data[0].get("plan_expires_at")
                if current_exp:
                    try:
                        exp_dt = datetime.fromisoformat(current_exp.replace("Z", "+00:00"))
                        new_exp = exp_dt + timedelta(days=PAID_DAYS) if exp_dt > now else now + timedelta(days=PAID_DAYS)
                    except ValueError:
                        new_exp = now + timedelta(days=PAID_DAYS)
                else:
                    new_exp = now + timedelta(days=PAID_DAYS)

                db.schema("threads").from_("threads_accounts").update({
                    "plan": plan_type,
                    "plan_started_at": now.isoformat(),
                    "plan_expires_at": new_exp.isoformat(),
                    "credit_balance": credits,
                    "pending_plan": None,
                }).eq("id", acc_id).execute()

                db.schema("threads").from_("credit_ledger").insert({
                    "account_id": acc_id,
                    "delta": credits,
                    "reason": "renewal_reset",
                    "note": f"Duitku paid {plan_type} ({merchantOrderId})",
                }).execute()

            logger.info(f"Duitku payment success: user={user_id}, plan={plan_type}, order={merchantOrderId}")

    return "OK"
