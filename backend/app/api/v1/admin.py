from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.rag import get_supabase
from app.core.config import PAID_DAYS, PAID_CREDITS, TRIAL_DAYS, TRIAL_CREDITS
from datetime import datetime, timedelta, timezone
from typing import Optional

router = APIRouter()

class AdminActionRequest(BaseModel):
    account_id: str
    plan_type: str # 'paid_credit' or 'paid_byok'

class AdjustCreditRequest(BaseModel):
    account_id: str
    delta: int
    note: str

@router.get("/users")
async def get_users():
    db = get_supabase()
    
    # 1. Ambil data dari threads_accounts
    accs = db.schema("threads").from_("threads_accounts").select("*").execute()
    
    # 2. Ambil email dari auth.users (via service role)
    # Note: Dalam implementasi nyata, lo perlu bikin RPC atau join dengan tabel profiles
    # Karena auth.users tidak bisa di-query langsung lewat Supabase-py standard client
    # Kita akan coba pake supabase.auth.admin.list_users() (butuh service role)
    try:
        users_res = db.auth.admin.list_users()
        users_list = users_res if isinstance(users_res, list) else users_res.users if hasattr(users_res, 'users') else []
        user_map = {u.id: u.email for u in users_list}
    except Exception as e:
        user_map = {}

    results = []
    for acc in (accs.data or []):
        results.append({
            "id": acc["id"],
            "email": user_map.get(acc["user_id"], "Unknown Email"),
            "username": acc.get("username", "-"),
            "connection_status": acc.get("connection_status", "-"),
            "plan": acc.get("plan", "none"),
            "plan_expires_at": acc.get("plan_expires_at"),
            "credit_balance": acc.get("credit_balance", 0),
            "created_at": acc.get("created_at")
        })
    
    # Urutkan berdasarkan tanggal terbaru
    results.sort(key=lambda x: x["created_at"] or "", reverse=True)
    return {"success": True, "users": results}

@router.post("/extend")
async def extend_plan(payload: AdminActionRequest):
    db = get_supabase()
    acc = db.schema("threads").from_("threads_accounts").select("plan_expires_at").eq("id", payload.account_id).maybeSingle().execute()
    
    if not acc.data: raise HTTPException(404, "Account not found")
    
    now = datetime.now(timezone.utc)
    current_exp = acc.data.get("plan_expires_at")
    
    # Logika extend: jika belum expired, tambah dari tanggal expired. Jika udah, tambah dari sekarang.
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
        "credit_balance": credits
    }).eq("id", payload.account_id).execute()

    # Catat di ledger (reset)
    db.schema("threads").from_("credit_ledger").insert({
        "account_id": payload.account_id,
        "delta": credits,
        "reason": "renewal_reset",
        "note": f"Admin extended plan to {payload.plan_type}"
    }).execute()

    return {"success": True, "new_expires": new_exp.isoformat(), "credits": credits}

@router.post("/adjust-credits")
async def adjust_credits(payload: AdjustCreditRequest):
    db = get_supabase()
    
    acc = db.schema("threads").from_("threads_accounts").select("credit_balance").eq("id", payload.account_id).maybeSingle().execute()
    if not acc.data: raise HTTPException(404, "Account not found")

    current_bal = acc.data.get("credit_balance", 0)
    new_bal = current_bal + payload.delta
    if new_bal < 0:
        raise HTTPException(400, "Credit balance cannot be negative")

    db.schema("threads").from_("threads_accounts").update({
        "credit_balance": new_bal
    }).eq("id", payload.account_id).execute()

    db.schema("threads").from_("credit_ledger").insert({
        "account_id": payload.account_id,
        "delta": payload.delta,
        "reason": "admin_adjust",
        "note": payload.note
    }).execute()

    return {"success": True, "new_balance": new_bal}

@router.get("/ledger/{account_id}")
async def get_ledger(account_id: str):
    db = get_supabase()
    res = db.schema("threads").from_("credit_ledger").select("*").eq("account_id", account_id).order("created_at", desc=True).limit(50).execute()
    return {"success": True, "ledger": res.data or []}
