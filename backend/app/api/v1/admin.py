from fastapi import APIRouter, HTTPException, Header, Depends
from pydantic import BaseModel
from app.services.rag import get_supabase
from app.core.config import TRIAL_DAYS, TRIAL_CREDITS, PAID_DAYS, PLAN_CREDITS
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

        uid = user_res.user.id
        prof = db.schema("threads").from_("profiles").select("role").eq("id", uid).limit(1).execute()
        is_prof_admin = bool(prof.data and prof.data[0].get("role") == "admin")

        acc = (
            db.schema("threads")
            .from_("threads_accounts")
            .select("role")
            .eq("user_id", uid)
            .eq("role", "admin")
            .limit(1)
            .execute()
        )
        is_acc_admin = bool(acc.data)

        if not is_prof_admin and not is_acc_admin:
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
        logger.error("RESEND_API_KEY tidak ditemukan di env server")
        return
    html_content = f"""
    <div style="font-family: sans-serif; color: #111; max-width: 500px; margin: 0 auto; padding: 20px; border: 1px solid #eee; border-radius: 10px;">
        <h2 style="color: #000;">Pembayaran Berhasil!</h2>
        <p>Halo Kreator,</p>
        <p>Kabar baik! Akun Ixiera kamu sudah berhasil di-upgrade ke paket <strong>{plan_name}</strong>.</p>
        <p>Sekarang kamu bisa menikmati semua fitur AI (Generate, Repurpose, Auto-Reply) di seluruh akun Threads yang terhubung.</p>
        <br/>
        <a href="https://app.ixiera.online/dashboard" style="background: #000; color: #fff; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">Buka Dashboard</a>
        <br/><br/>
        <p style="font-size: 12px; color: #666;">Jika ada kendala, balas email ini atau hubungi WhatsApp Admin.</p>
    </div>
    """
    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(
                "https://api.resend.com/emails",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={"from": f"Ixiera <{from_email}>", "to": [email], "subject": "Upgrade Berhasil! Akun Ixiera Kamu Sudah Aktif", "html": html_content},
                timeout=10.0
            )
            if res.status_code == 200:
                logger.info(f"Email sukses terkirim ke {email}")
            else:
                logger.error(f"Gagal kirim email via Resend: {res.text}")
    except Exception as e:
        logger.error(f"Error saat kirim email: {str(e)}")

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

    accounts_data = accs.data or []
    account_counts = {}
    for acc in accounts_data:
        uid = acc["user_id"]
        account_counts[uid] = account_counts.get(uid, 0) + 1

    results = []
    for acc in accounts_data:
        uid = acc["user_id"]
        results.append({
            "id": acc["id"],
            "user_id": uid,
            "email": user_map.get(uid, "Unknown"),
            "username": acc.get("username", "-"),
            "role": acc.get("role", "user"),
            "connection_status": acc.get("connection_status", "-"),
            "plan": acc.get("plan", "none"),
            "pending_plan": acc.get("pending_plan"),
            "plan_expires_at": acc.get("plan_expires_at"),
            "credit_balance": acc.get("credit_balance", 0),
            "account_count": account_counts.get(uid, 1),
            "last_error": acc.get("last_error"),
            "created_at": acc.get("created_at")
        })
    results.sort(key=lambda x: x["created_at"] or "", reverse=True)
    return {"success": True, "users": results}

@router.post("/extend")
async def extend_plan(payload: AdminActionRequest, user = Depends(verify_admin)):
    db = get_supabase()
    acc = db.schema("threads").from_("threads_accounts").select("plan_expires_at, user_id").eq("id", payload.account_id).limit(1).execute()
    if not acc.data:
        raise HTTPException(404, "Account not found")

    if payload.plan_type == 'trial':
        days = TRIAL_DAYS
        credits = TRIAL_CREDITS
    else:
        days = PAID_DAYS
        credits = PLAN_CREDITS.get(payload.plan_type, 0)

    now = datetime.now(timezone.utc)
    target_user_id = acc.data[0].get("user_id")

    # Cek masa aktif tertinggi di semua akun milik user ini
    siblings = db.schema("threads").from_("threads_accounts").select("plan_expires_at").eq("user_id", target_user_id).execute()
    latest_exp = None
    for row in (siblings.data or []):
        exp_str = row.get("plan_expires_at")
        if not exp_str:
            continue
        try:
            dt = datetime.fromisoformat(exp_str.replace("Z", "+00:00"))
            if latest_exp is None or dt > latest_exp:
                latest_exp = dt
        except ValueError:
            continue

    if latest_exp and latest_exp > now:
        new_exp = latest_exp + timedelta(days=days)
    else:
        new_exp = now + timedelta(days=days)

    # Trigger database trg_sync_user_plan_across_accounts otomatis menyinkronkan ke seluruh akun milik user_id & profiles
    db.schema("threads").from_("threads_accounts").update({
        "plan": payload.plan_type,
        "plan_started_at": now.isoformat(),
        "plan_expires_at": new_exp.isoformat(),
        "credit_balance": credits,
        "pending_plan": None
    }).eq("id", payload.account_id).execute()

    db.schema("threads").from_("credit_ledger").insert({
        "account_id": payload.account_id,
        "delta": credits,
        "reason": "renewal_reset",
        "note": f"Admin extended to {payload.plan_type}"
    }).execute()

    try:
        user_res = db.auth.admin.get_user_by_id(target_user_id)
        if user_res and user_res.user and user_res.user.email:
            plan_labels = {
                "starter": "Starter",
                "pro": "Pro",
                "business": "Business",
                "agency": "Agency (BYOK)",
                "paid_credit": "Pro Credit",
                "paid_byok": "Pro BYOK",
                "trial": "Trial",
            }
            plan_name = plan_labels.get(payload.plan_type, payload.plan_type)
            await send_approval_email(user_res.user.email, plan_name)
    except Exception as e:
        logger.error(f"Gagal ambil data user untuk email: {str(e)}")

    return {"success": True, "new_expires": new_exp.isoformat(), "credits": credits}

@router.post("/adjust-credits")
async def adjust_credits(payload: AdjustCreditRequest, user = Depends(verify_admin)):
    db = get_supabase()
    acc = db.schema("threads").from_("threads_accounts").select("credit_balance").eq("id", payload.account_id).limit(1).execute()
    if not acc.data:
        raise HTTPException(404, "Account not found")

    current = acc.data[0].get("credit_balance", 0)
    new_bal = max(0, current + payload.delta)

    # Trigger database otomatis menyinkronkan saldo kredit baru ke semua akun milik user_id
    db.schema("threads").from_("threads_accounts").update({"credit_balance": new_bal}).eq("id", payload.account_id).execute()
    db.schema("threads").from_("credit_ledger").insert({
        "account_id": payload.account_id,
        "delta": payload.delta,
        "reason": "manual_adjust",
        "note": payload.note
    }).execute()

    return {"success": True, "new_balance": new_bal}

@router.get("/ledger/{account_id}")
async def get_ledger(account_id: str, user = Depends(verify_admin)):
    db = get_supabase()
    res = db.schema("threads").from_("credit_ledger").select("*").eq("account_id", account_id).order("created_at", desc=True).execute()
    return {"success": True, "ledger": res.data or []}

@router.post("/downgrade")
async def downgrade_plan(payload: AdminActionRequest, user = Depends(verify_admin)):
    db = get_supabase()
    db.schema("threads").from_("threads_accounts").update({
        "plan": "none",
        "plan_expires_at": None,
        "credit_balance": 0,
        "pending_plan": None
    }).eq("id", payload.account_id).execute()
    return {"success": True, "message": "Downgraded to free"}

@router.post("/force-sync")
async def force_sync_user(payload: AdminActionRequest, user = Depends(verify_admin)):
    db = get_supabase()
    acc_res = db.schema('threads').from_('threads_accounts').select('settings, id').eq('id', payload.account_id).maybe_single().execute()
    if not acc_res.data:
        raise HTTPException(404, "Account not found")
    token = (acc_res.data.get('settings') or {}).get('access_token')
    if not token:
        raise HTTPException(400, "No access token")
    from app.workers.replies import sync_profile_and_metrics
    async with httpx.AsyncClient() as client:
        await sync_profile_and_metrics(db, client, payload.account_id, token)
    return {"success": True, "message": "Profile & Metrics synced manually"}

@router.get("/stats")
async def get_admin_stats(user = Depends(verify_admin)):
    db = get_supabase()
    accs = db.schema("threads").from_("threads_accounts").select("user_id, plan, pending_plan, credit_balance").execute()
    rows = accs.data or []
    total_accounts = len(rows)

    plan_rank = {"agency": 7, "business": 6, "pro": 5, "starter": 4, "paid_credit": 4, "paid_byok": 3, "trial": 2, "none": 1}
    plan_price = {"starter": 59000, "pro": 99000, "business": 179000, "agency": 249000, "paid_credit": 29000, "paid_byok": 19000}
    user_plans = {}
    pending_users = set()
    for acc in rows:
        uid = acc.get("user_id")
        if not uid:
            continue
        p = acc.get("plan") or "none"
        if plan_rank.get(p, 1) > plan_rank.get(user_plans.get(uid, "none"), 0):
            user_plans[uid] = p

        if acc.get("pending_plan"):
            pending_users.add(uid)

    total_users = len(user_plans)
    total_pro_credit = sum(1 for p in user_plans.values() if p in ("starter", "pro", "business", "paid_credit"))
    total_pro_byok = sum(1 for p in user_plans.values() if p in ("agency", "paid_byok"))
    total_pending = len(pending_users)
    mrr_est = sum(plan_price.get(p, 0) for p in user_plans.values())

    return {
        "success": True,
        "stats": {
            "total_users": total_users,
            "total_accounts": total_accounts,
            "pro_credit": total_pro_credit,
            "pro_byok": total_pro_byok,
            "pending_requests": total_pending,
            "mrr_estimate": mrr_est
        }
    }

@router.get("/token-stats")
async def get_token_stats(user = Depends(verify_admin)):
    db = get_supabase()
    thirty_days_ago = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()

    res_logs = (
        db.schema("threads")
        .from_("api_call_logs")
        .select("account_id, prompt_tokens, completion_tokens")
        .eq("endpoint", "generate_post")
        .gte("created_at", thirty_days_ago)
        .execute()
    )
    logs = res_logs.data or []

    res_users = db.schema("threads").from_("threads_accounts").select("id, username").execute()
    users = {u['id']: u.get('username', 'Unknown') for u in (res_users.data or [])}

    per_user_dict = {}
    total_prompt = 0
    total_comp = 0

    for l in logs:
        acc_id = l.get('account_id')
        pt = l.get('prompt_tokens', 0) or 0
        ct = l.get('completion_tokens', 0) or 0

        total_prompt += pt
        total_comp += ct

        if acc_id not in per_user_dict:
            per_user_dict[acc_id] = {
                "account_id": acc_id,
                "username": users.get(acc_id, 'Unknown'),
                "generates": 0,
                "prompt": 0,
                "completion": 0
            }

        per_user_dict[acc_id]["generates"] += 1
        per_user_dict[acc_id]["prompt"] += pt
        per_user_dict[acc_id]["completion"] += ct

    per_user_list = list(per_user_dict.values())
    per_user_list.sort(key=lambda x: x["prompt"] + x["completion"], reverse=True)

    return {
        "success": True,
        "stats": {
            "total_prompt": total_prompt,
            "total_completion": total_comp,
            "total_tokens": total_prompt + total_comp,
            "total_generates": len(logs)
        },
        "per_user": per_user_list
    }
