import os
import asyncio
import httpx
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from supabase import create_client

router = APIRouter()

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

def get_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

class SyncRequest(BaseModel):
    account_id: str

@router.post("/sync")
async def sync_metrics(payload: SyncRequest):
    account_id = payload.account_id
    db = get_supabase()

    try:
        # 1. Ambil Token
        acc_res = db.schema('threads').from_('threads_accounts').select('access_token').eq('id', account_id).single().execute()
        if not acc_res.data:
            raise HTTPException(status_code=404, detail="Akun tidak ditemukan")
        
        token = acc_res.data['access_token']

        # 2. Ambil semua post yang ada di database
        posts_res = db.schema('threads').from_('posts').select('id, threads_media_id').eq('account_id', account_id).execute()
        
        if not posts_res.data:
            return {"status": "success", "message": "Belum ada post untuk disinkronkan"}

        updated_count = 0
        
        # 3. Looping tarik metrik dari Meta (pakai jeda biar gak kena rate limit)
        async with httpx.AsyncClient() as client:
            for post in posts_res.data:
                media_id = post['threads_media_id']
                insight_url = f"https://graph.threads.net/v1.0/{media_id}/insights?metric=views,likes,replies,reposts,quotes&access_token={token}"
                
                try:
                    resp = await client.get(insight_url, timeout=15.0)
                    if resp.status_code == 200:
                        ins_data = resp.json()
                        if "data" in ins_data:
                            metrics = {item["name"]: item["values"][0]["value"] for item in ins_data["data"] if "values" in item}
                            
                            # Hapus snapshot 'latest' yang lama, insert yang baru
                            db.schema("threads").from_("post_metrics").delete().eq("post_id", post['id']).eq("snapshot_label", "latest").execute()
                            
                            db.schema("threads").from_("post_metrics").insert({
                                "post_id": post['id'],
                                "snapshot_label": "latest",
                                "views": metrics.get("views", 0),
                                "likes": metrics.get("likes", 0),
                                "replies": metrics.get("replies", 0),
                                "reposts": metrics.get("reposts", 0),
                                "quotes": metrics.get("quotes", 0),
                                "captured_at": datetime.now(timezone.utc).isoformat()
                            }).execute()
                            
                            updated_count += 1
                except Exception as e:
                    print(f"[Metrics Sync] Error post {media_id}: {e}")
                
                # Jeda 0.5 detik per request biar aman dari banned Meta
                await asyncio.sleep(0.5)

        return {"status": "success", "message": f"Berhasil update {updated_count} post"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sync-profile")
async def sync_profile(payload: SyncRequest):
    account_id = payload.account_id
    db = get_supabase()

    try:
        acc_res = db.schema('threads').from_('threads_accounts').select('access_token').eq('id', account_id).single().execute()
        if not acc_res.data:
            raise HTTPException(status_code=404, detail="Akun tidak ditemukan")
        
        token = acc_res.data['access_token']

        # Panggil API Meta buat narik Profile & Avatar
        url = f"https://graph.threads.net/v1.0/me?fields=id,username,threads_profile_picture_url,threads_biography&access_token={token}"
        
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, timeout=15.0)
            if resp.status_code != 200:
                raise HTTPException(status_code=resp.status_code, detail="Gagal narik profile dari Meta")

            data = resp.json()
            
            # Update tabel threads_accounts
            db.schema('threads').from_('threads_accounts').update({
                "username": data.get("username"),
                "profile_picture_url": data.get("threads_profile_picture_url"),
                "biography": data.get("threads_biography")
            }).eq("id", account_id).execute()

        return {"status": "success", "message": "Profile berhasil disinkronkan"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
