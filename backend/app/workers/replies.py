import os
import asyncio
import logging
import httpx
from datetime import datetime, timezone
from supabase import create_client, Client
from app.services.leads import analyze_and_notify_lead

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

def get_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

async def fetch_and_process_replies():
    db = get_supabase()
    
    # 1. Ambil semua akun SaaS yang terhubung
    accounts_res = db.schema("threads").from_("threads_accounts").select("id, settings").eq("connection_status", "connected").execute()
    accounts = accounts_res.data or []

    async with httpx.AsyncClient() as client:
        for acc in accounts:
            acc_id = acc["id"]
            token = acc.get("settings", {}).get("access_token")
            if not token:
                continue

            # 2. Ambil 20 postingan terakhir dari akun tersebut
            posts_res = db.schema("threads").from_("posts").select("id, threads_media_id").eq("account_id", acc_id).order("created_at", desc=True).limit(20).execute()
            posts = posts_res.data or []

            for post in posts:
                media_id = post["threads_media_id"]
                post_db_id = post["id"]
                if not media_id:
                    continue

                # 3. Panggil Meta API untuk mengambil daftar balasan
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

                        # 4. Cek apakah balasan ini sudah ada di database
                        exist_res = db.schema("threads").from_("replies").select("id").eq("threads_reply_id", reply_id).execute()
                        
                        if not exist_res.data:
                            # JIKA BARU: Analisa buying intent
                            analysis = await analyze_and_notify_lead(acc_id, author_username, text)
                            is_lead = analysis.get("is_lead", False)

                            # 5. Insert pakai nama kolom lu yang bener
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
                            
                except Exception as e:
                    logging.error(f"[Worker Replies] Gagal menarik data untuk media {media_id}: {str(e)}")

async def reply_worker_loop():
    """Loop yang berjalan di background FastAPI setiap 10 menit"""
    while True:
        try:
            logging.info("[Worker Replies] Memulai siklus penarikan komentar Threads...")
            await fetch_and_process_replies()
            logging.info("[Worker Replies] Siklus selesai. Menunggu 10 menit.")
        except Exception as e:
            logging.error(f"[Worker Replies] Error pada siklus: {str(e)}")
        
        # Jeda 600 detik (10 menit)
        await asyncio.sleep(600)
