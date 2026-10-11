import os
import asyncio
import logging
import httpx
from datetime import datetime, timezone
from supabase import create_client, Client
from app.services.leads import analyze_and_notify_lead
from app.services.auto_reply import generate_rag_reply

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

def get_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

async def fetch_and_process_replies():
    db = get_supabase()
    
    accounts_res = db.schema("threads").from_("threads_accounts").select("id, settings").eq("connection_status", "connected").execute()
    accounts = accounts_res.data or []

    async with httpx.AsyncClient() as client:
        for acc in accounts:
            acc_id = acc["id"]
            token = acc.get("settings", {}).get("access_token")
            if not token:
                continue

            # Ambil Pengaturan Auto Reply
            settings_res = db.schema("threads").from_("auto_reply_settings").select("*").eq("account_id", acc_id).maybeSingle().execute()
            auto_settings = settings_res.data or {}
            is_enabled = auto_settings.get("enabled", True)
            reply_mode = auto_settings.get("mode", "review")

            posts_res = db.schema("threads").from_("posts").select("id, threads_media_id").eq("account_id", acc_id).order("created_at", desc=True).limit(20).execute()
            posts = posts_res.data or []

            for post in posts:
                media_id = post["threads_media_id"]
                post_db_id = post["id"]
                if not media_id:
                    continue

                url = f"https://graph.threads.net/v1.0/{media_id}/replies?fields=id,text,username,timestamp&access_token={token}"
                try:
                    res = await client.get(url, timeout=10.0)
                    if res.status_code != 200:
                        continue
                    
                    data = res.json().get("data", [])

                    for reply in data:
                        reply_id = reply.get("id")
                        text = reply.get("text", "")
                        author_username = reply.get("username", "unknown")
                        timestamp = reply.get("timestamp")

                        exist_res = db.schema("threads").from_("replies").select("id").eq("threads_reply_id", reply_id).execute()
                        
                        if not exist_res.data:
                            # 1. Analisa Lead (Berjalan terpisah)
                            analysis = await analyze_and_notify_lead(acc_id, author_username, text)
                            is_lead = analysis.get("is_lead", False)

                            # 2. Simpan ke tabel replies utama
                            db.schema("threads").from_("replies").insert({
                                "account_id": acc_id,
                                "post_id": post_db_id,
                                "threads_reply_id": reply_id,
                                "author_username": author_username,
                                "text": text,
                                "is_lead": is_lead,
                                "replied_at": timestamp,
                                "raw": reply,
                                "processed_at": datetime.now(timezone.utc).isoformat()
                            }).execute()

                            # 3. Generate Draf AI & Masukkan ke Review Queue jika aktif
                            if is_enabled:
                                try:
                                    draft_text = await generate_rag_reply(
                                        account_id=acc_id, 
                                        user_comment=text, 
                                        author_username=author_username
                                    )
                                    
                                    db.schema("threads").from_("auto_reply_logs").insert({
                                        "account_id": acc_id,
                                        "status": "unprocessed" if reply_mode == "review" else "approved",
                                        "final_text": draft_text,
                                        "llm_meta": {
                                            "incoming_comment": text, 
                                            "username": author_username, 
                                            "reply_id": reply_id
                                        }
                                    }).execute()
                                except Exception as ai_err:
                                    logging.error(f"[AI Draft Error]: {str(ai_err)}")
                            
                except Exception as e:
                    logging.error(f"[Worker Replies] Error: {str(e)}")

async def reply_worker_loop():
    while True:
        try:
            await fetch_and_process_replies()
        except Exception as e:
            logging.error(f"[Worker Replies Loop] Error: {str(e)}")
        await asyncio.sleep(600)
