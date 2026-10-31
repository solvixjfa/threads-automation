from fastapi import APIRouter, HTTPException, Header, Depends
from pydantic import BaseModel
from app.services.rag import get_supabase
from app.core.config import PAID_DAYS, PAID_CREDITS
from datetime import datetime, timedelta, timezone
from typing import Optional
import httpx
import os
import logging

router = APIRouter()
logger = logging.getLogger("uvicorn.error")

class AdminActionRequest(BaseModel):
    account_id: str
    plan_type: str

class AdjustCreditRequest(BaseModel):
    account_id: str
    delta: int
    note: str

def verify_admin(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing auth token")
    token = authorization.replace("Bearer ", "").strip()
    db = get_supabase()
    try:
        user_res = db.auth.get_user(token)
        if not user_res or not user_res.user:
            raise HTTPException(status_code=401, detail="Invalid token")
        acc = db.schema("threads").from_("threads_accounts").select("role").eq("user_id", user_res.user.id).limit(1).execute()
        if not acc.data or acc.data[0].get("role") != "admin":
            raise HTTPException(status_code=403, detail="Admin access required")
        return user_res.user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Auth failed: {str(e)}")

async def send_approval_email(email: str, plan_name: str):
    api_key = os.getenv("RESEND_API_KEY")
    from_email = os.getenv("RESEND_FROM_EMAIL", "onboarding@resend.dev")
    
    if not api_key:
        logger.error("❌ RESEND_API_KEY tidak ditemukan di env Railway!")
        return

    html_content = f"""
    <div style="font-family: sans-serif; color: #111; max-width: 500px; margin: 0 auto; padding: 20px; border: 1px solid #eee; border-radius: 10px;">
        <h2 style="color: #000;">Pembayaran Berhasil! 🎉</h2>
        <p>Halo Kreator,</p>
        <p>Kabar baik! Akun Ixiera kamu sudah berhasil di-upgrade ke paket <strong>{plan_name}</strong>.</p>
        <p>Sekarang kamu bisa menikmati semua fitur AI (Generate, Repurpose, Auto-Reply) tanpa batas.</p>
        <br/>
        <a href="https://meta.ixiera.id/dashboard" style="background: #000; color: #fff; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">Buka Dashboard</a>
        <br/><br/>
        <p style="font-size: 12px; color: #666;">Jika ada kendala, balas email ini atau hubungi WhatsApp Admin.</p>
    </div>
    """

    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(
                "https://api.resend.com/emails",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={
                    "from": f"Ixiera <{from_email}>",
                    "to": [email],
                    "subject": "Upgrade Berhasil! Akun Ixiera Kamu Sudah Aktif",
                    "html": html_content
                },
                timeout=10.0
            )
            if res.status_code == 200:
                logger.info(f"✅ Email sukses terkirim ke {email}")
            else:
                logger.error(f"❌ Gagal kirim email via Resend: {res.text}")
    except Exception as e:
        logger.error(f"❌ Error saat kirim email: {str(e)}")

@router.get("/users")
async def get_users(user = Depends(verify_admin)):
    db = get_supabase()
    accs = db.schema("threads").from_("threads_accounts").select("*").execute()
    try:
        users_res = db.auth.admin.list_users()
        users_list = users_res if isinstance(users_res, list) else users_res.users if hasattr(users_res, 'users') else []
        user_map = {u.id: u.email for u in users_list}
    except Exception:
        user_map = {}

    results = []
    for acc in (accs.data or []):
        results.append({
            "id": acc["id"],
            "user_id": acc["user_id"],
            "email": user_map.get(acc["user_id"], "Unknown"),
            "username": acc.get("username", "-"),
            "role": acc.get("role", "user"),
            "connection_status": acc.get("connection_status", "-"),
            "plan": acc.get("plan", "none"),
            "pending_plan": acc.get("pending_plan"),
            "plan_expires_at": acc.get("plan_expires_at"),
            "credit_balance": acc.get("credit_balance", 0),
            "created_at": acc.get("created_at")
        })
    results.sort(key=lambda x: x["created_at"] or "", reverse=True)
    return {"success": True, "users": results}

@router.post("/extend")
async def extend_plan(payload: AdminActionRequest, user = Depends(verify_admin)):
    db = get_supabase()
    acc = db.schema("threads").from_("threads_accounts").select("plan_expires_at, user_id").eq("id", payload.account_id).limit(1).execute()
    if not acc.data: raise HTTPException(404, "Account not found")
    
    now = datetime.now(timezone.utc)
    current_exp = acc.data[0].get("plan_expires_at")
    target_user_id = acc.data[0].get("user_id")
    
    if current_exp:
        try:
            exp_dt = datetime.fromisoformat(current_exp.replace("Z", "+00:00"))
            new_exp = exp_dt + timedelta(days=PAID_DAYS) if exp_dt > now else now + timedelta(days=PAID_DAYS)
        except ValueError:
            new_exp = now + timedelta(days=PAID_DAYS)
    else:
        new_exp = now + timedelta(days=PAID_DAYS)

    credits = PAID_CREDITS if payload.plan_type == 'paid_credit' else 0
    
    db.schema("threads").from_("threads_accounts").update({
        "plan": payload.plan_type,
        "plan_started_at": now.isoformat(),
        "plan_expires_at": new_exp.isoformat(),
        "credit_balance": credits,
        "pending_plan": None
    }).eq("id", payload.account_id).execute()

    db.schema("threads").from_("credit_ledger").insert({
        "account_id": payload.account_id, "delta": credits, "reason": "renewal_reset",
        "note": f"Admin extended to {payload.plan_type}"
    }).execute()

    # KIRIM EMAIL
    try:
        user_res = db.auth.admin.get_user_by_id(target_user_id)
        if user_res and user_res.user and user_res.user.email:
            plan_name = "Pro Credit" if payload.plan_type == 'paid_credit' else "Pro BYOK"
            await send_approval_email(user_res.user.email, plan_name)
        else:
            logger.warning(f"⚠️ Email user tidak ditemukan untuk ID {target_user_id}")
    except Exception as e:
        logger.error(f"❌ Gagal ambil data user untuk email: {str(e)}")

    return {"success": True, "new_expires": new_exp.isoformat(), "credits": credits}

@router.get("/stats")
async def get_admin_stats(user = Depends(verify_admin)):
    db = get_supabase()
    
    # Ambil semua data user
    accs = db.schema("threads").from_("threads_accounts").select("plan, pending_plan, credit_balance").execute()
    
    total_users = len(accs.data or [])
    total_pro_credit = 0
    total_pro_byok = 0
    total_pending = 0
    
    for acc in (accs.data or []):
        if acc.get("plan") == "paid_credit": total_pro_credit += 1
        if acc.get("plan") == "paid_byok": total_pro_byok += 1
        if acc.get("pending_plan"): total_pending += 1

    # Hitung Estimasi Pendapatan (MRR)
    mrr_est = (total_pro_credit * 49000) + (total_pro_byok * 29000)

    return {
        "success": True,
        "stats": {
            "total_users": total_users,
            "pro_credit": total_pro_credit,
            "pro_byok": total_pro_byok,
            "pending_requests": total_pending,
            "mrr_estimate": mrr_est
        }
    }
