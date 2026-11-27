from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone
from app.services.rag import get_supabase
import httpx
import os
import html
import logging

router = APIRouter()
logger = logging.getLogger("uvicorn.error")


class StartChatRequest(BaseModel):
    visitor_token: str = Field(..., min_length=8, max_length=128)
    visitor_name: str = Field(..., min_length=1, max_length=80)
    visitor_email: Optional[str] = Field(None, max_length=120)
    page_url: Optional[str] = Field(None, max_length=300)
    faq_topic: Optional[str] = Field(None, max_length=120)
    message: str = Field(..., min_length=1, max_length=2000)


class SendVisitorMessageRequest(BaseModel):
    session_id: str = Field(..., min_length=10, max_length=64)
    visitor_token: str = Field(..., min_length=8, max_length=128)
    message: str = Field(..., min_length=1, max_length=2000)


async def notify_support_email(visitor_name: str, visitor_email: Optional[str], message: str, page_url: Optional[str], is_followup: bool = False):
    api_key = os.getenv("RESEND_API_KEY")
    from_email = os.getenv("RESEND_FROM_EMAIL", "onboarding@resend.dev")
    to_email = os.getenv("SUPPORT_ADMIN_EMAIL", "support@ixiera.online")
    if not api_key:
        logger.warning("RESEND_API_KEY tidak tersedia, melewati notifikasi email live chat")
        return

    safe_name = html.escape(visitor_name)
    safe_email = html.escape(visitor_email or "-")
    safe_msg = html.escape(message).replace("\n", "<br/>")
    safe_url = html.escape(page_url or "https://ixiera.online")
    prefix = "Balasan Baru" if is_followup else "Live Chat Baru"

    html_content = f"""
    <div style="font-family: sans-serif; color: #111; max-width: 520px; margin: 0 auto; padding: 20px; border: 1px solid #e5e7eb; border-radius: 10px;">
        <h2 style="margin-top: 0; color: #000;">{prefix} dari Pengunjung Ixiera</h2>
        <p style="margin: 6px 0;"><strong>Nama:</strong> {safe_name}</p>
        <p style="margin: 6px 0;"><strong>Email:</strong> {safe_email}</p>
        <p style="margin: 6px 0;"><strong>Halaman:</strong> {safe_url}</p>
        <div style="margin: 16px 0; padding: 14px; background: #f4f4f5; border-radius: 8px; font-size: 14px; line-height: 1.5;">
            {safe_msg}
        </div>
        <a href="https://app.ixiera.online/admin/live-chat" style="display: inline-block; background: #000; color: #fff; padding: 11px 20px; text-decoration: none; border-radius: 6px; font-weight: bold;">
            Balas di Admin Live Chat
        </a>
    </div>
    """
    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(
                "https://api.resend.com/emails",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={
                    "from": f"Ixiera Support <{from_email}>",
                    "to": [to_email],
                    "subject": f"[{prefix}] {visitor_name} bertanya di Ixiera",
                    "html": html_content,
                },
                timeout=10.0,
            )
            if res.status_code not in (200, 201):
                logger.error(f"Resend live chat alert gagal: {res.text}")
    except Exception as e:
        logger.error(f"Error kirim notifikasi live chat: {str(e)}")


@router.post("/start")
async def start_chat(payload: StartChatRequest):
    db = get_supabase()
    now_iso = datetime.now(timezone.utc).isoformat()
    clean_name = payload.visitor_name.strip()
    clean_msg = payload.message.strip()
    clean_email = payload.visitor_email.strip() if payload.visitor_email else None

    existing = (
        db.schema("threads")
        .from_("chat_sessions")
        .select("*")
        .eq("visitor_token", payload.visitor_token)
        .eq("status", "open")
        .order("last_message_at", desc=True)
        .limit(1)
        .execute()
    )

    if existing.data:
        session = existing.data[0]
        session_id = session["id"]
        new_unread = int(session.get("unread_admin", 0)) + 1
        db.schema("threads").from_("chat_sessions").update({
            "visitor_name": clean_name,
            "visitor_email": clean_email or session.get("visitor_email"),
            "unread_admin": new_unread,
            "last_message_at": now_iso,
        }).eq("id", session_id).execute()
    else:
        created = (
            db.schema("threads")
            .from_("chat_sessions")
            .insert({
                "visitor_token": payload.visitor_token,
                "visitor_name": clean_name,
                "visitor_email": clean_email,
                "page_url": payload.page_url,
                "status": "open",
                "unread_admin": 1,
                "last_message_at": now_iso,
            })
            .execute()
        )
        if not created.data:
            raise HTTPException(status_code=500, detail="Gagal membuat sesi chat")
        session = created.data[0]
        session_id = session["id"]

        if payload.faq_topic:
            db.schema("threads").from_("chat_messages").insert({
                "session_id": session_id,
                "sender_role": "bot",
                "message": f"Topik sebelumnya: {payload.faq_topic.strip()}",
            }).execute()

    msg_res = (
        db.schema("threads")
        .from_("chat_messages")
        .insert({
            "session_id": session_id,
            "sender_role": "visitor",
            "message": clean_msg,
        })
        .execute()
    )

    await notify_support_email(clean_name, clean_email, clean_msg, payload.page_url, is_followup=False)
    return {"session": session, "message": msg_res.data[0] if msg_res.data else None}


@router.post("/message")
async def send_visitor_message(payload: SendVisitorMessageRequest):
    db = get_supabase()
    now_iso = datetime.now(timezone.utc).isoformat()
    clean_msg = payload.message.strip()

    sess_res = (
        db.schema("threads")
        .from_("chat_sessions")
        .select("*")
        .eq("id", payload.session_id)
        .eq("visitor_token", payload.visitor_token)
        .limit(1)
        .execute()
    )
    if not sess_res.data:
        raise HTTPException(status_code=404, detail="Sesi chat tidak ditemukan")

    session = sess_res.data[0]
    prev_unread = int(session.get("unread_admin", 0))

    msg_res = (
        db.schema("threads")
        .from_("chat_messages")
        .insert({
            "session_id": payload.session_id,
            "sender_role": "visitor",
            "message": clean_msg,
        })
        .execute()
    )

    db.schema("threads").from_("chat_sessions").update({
        "status": "open",
        "unread_admin": prev_unread + 1,
        "last_message_at": now_iso,
    }).eq("id", payload.session_id).execute()

    if prev_unread == 0:
        await notify_support_email(
            session.get("visitor_name", "Pengunjung"),
            session.get("visitor_email"),
            clean_msg,
            session.get("page_url"),
            is_followup=True,
        )

    return {"message": msg_res.data[0] if msg_res.data else None}
