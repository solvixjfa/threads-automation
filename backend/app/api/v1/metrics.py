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

def get_token_from_db(db, account_id):
    # KUNCI PERBAIKAN: Ambil dari kolom 'settings'
    res = db.schema('threads').from_('threads_accounts').select('settings').eq('id', f'"{account_id}"').maybe_single().execute()
    
    if not res.data:
        return None
        
    settings = res.data.get('settings') or {}
    return settings.get('access_token')

@router.post("/sync")
async def sync_metrics(payload: SyncRequest):
    account_id = payload.account_id
    db = get_supabase()

    try:
        token = get_token_from_db(db, account_id)
        if not token:
            raise HTTPException(status_code=400, detail="Access token tidak ditemukan di settings akun ini.")

        # Ambil post
        posts_res = db.schema('threads').from_('posts').select('id, threads_media_id').eq('account_id', f'"{account_id}"').execute()
        
        if not posts_res.data:
            return {"status": "success", "message": "Belum ada post"}

        updated_count = 0
        
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
                
                await asyncio.sleep(0.5)

        return {"status": "success", "message": f"Berhasil update {updated_count} post"}
        
    except Exception as e:
        print(f"[Metrics Sync] Fatal Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sync-profile")
async def sync_profile(payload: SyncRequest):
    account_id = payload.account_id
    db = get_supabase()

    try:
        token = get_token_from_db(db, account_id)
        if not token:
            raise HTTPException(status_code=400, detail="Access token tidak ditemukan di settings akun ini.")

        url = f"https://graph.threads.net/v1.0/me?fields=id,username,threads_profile_picture_url,threads_biography&access_token={token}"
        
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, timeout=15.0)
            if resp.status_code != 200:
                err_detail = resp.json().get('error', {}).get('message', 'Gagal dari Meta')
                raise HTTPException(status_code=resp.status_code, detail=err_detail)

            data = resp.json()
            
            db.schema('threads').from_('threads_accounts').update({
                "username": data.get("username"),
                "profile_picture_url": data.get("threads_profile_picture_url"),
                "biography": data.get("threads_biography")
            }).eq("id", f'"{account_id}"').execute()

        return {"status": "success", "message": "Profile berhasil disinkronkan"}
    except Exception as e:
        print(f"[Profile Sync] Fatal Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
