import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.services.rag import get_supabase

router = APIRouter()

class EditQueueRequest(BaseModel):
    post_id: str
    text: str
    scheduled_for: str

class ActionQueueRequest(BaseModel):
    post_id: str

class BulkDeleteRequest(BaseModel):
    post_ids: List[str]

@router.put("/edit")
async def edit_queue(payload: EditQueueRequest):
    try:
        db = get_supabase()
        dt = datetime.fromisoformat(payload.scheduled_for.replace("Z", "+00:00"))
        db.schema("threads").from_("scheduled_posts").update({
            "text": payload.text,
            "scheduled_for": dt.isoformat()
        }).eq("id", payload.post_id).execute()
        return {"status": "success", "message": "Post updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{post_id}")
async def delete_queue(post_id: str):
    try:
        db = get_supabase()
        db.schema("threads").from_("scheduled_posts").delete().eq("id", post_id).execute()
        return {"status": "success", "message": "Post deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/bulk-delete")
async def bulk_delete_queue(payload: BulkDeleteRequest):
    try:
        db = get_supabase()
        if not payload.post_ids:
            return {"status": "success", "message": "No posts to delete"}
        db.schema("threads").from_("scheduled_posts").delete().in_("id", payload.post_ids).execute()
        return {"status": "success", "message": f"{len(payload.post_ids)} posts deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/retry")
async def retry_queue(payload: ActionQueueRequest):
    try:
        db = get_supabase()
        db.schema("threads").from_("scheduled_posts").update({
            "status": "scheduled", "attempts": 0, "last_error": None
        }).eq("id", payload.post_id).execute()
        return {"status": "success", "message": "Post queued for retry"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{post_id}/threads")
async def delete_from_threads(post_id: str):
    try:
        db = get_supabase()
        post_res = (
            db.schema("threads")
            .from_("scheduled_posts")
            .select("id, account_id, published_media_id")
            .eq("id", post_id)
            .maybe_single()
            .execute()
        )
        post = post_res.data
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        media_id = post.get("published_media_id")
        if not media_id:
            raise HTTPException(status_code=400, detail="Post has no published_media_id")

        acc_res = (
            db.schema("threads")
            .from_("threads_accounts")
            .select("settings, token_secret_id")
            .eq("id", post["account_id"])
            .limit(1)
            .execute()
        )
        acc_data = acc_res.data[0] if acc_res.data else {}
        token = (acc_data.get("settings") or {}).get("access_token")

        if not token and acc_data.get("token_secret_id"):
            vault_res = (
                db.schema("vault")
                .from_("decrypted_secrets")
                .select("decrypted_secret")
                .eq("id", acc_data["token_secret_id"])
                .maybe_single()
                .execute()
            )
            token = (vault_res.data or {}).get("decrypted_secret")

        if not token:
            raise HTTPException(status_code=400, detail="Threads access token missing")

        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.delete(
                f"https://graph.threads.net/v1.0/{media_id}",
                params={"access_token": token}
            )
            data = resp.json() if resp.content else {}
            if resp.status_code >= 400 or not data.get("success", False):
                err_msg = (data.get("error") or {}).get("message") or resp.text or "Threads API delete failed"
                raise HTTPException(status_code=resp.status_code or 400, detail=err_msg)

        db.schema("threads").from_("scheduled_posts").delete().eq("id", post_id).execute()
        return {"status": "success", "message": "Deleted from Threads"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
