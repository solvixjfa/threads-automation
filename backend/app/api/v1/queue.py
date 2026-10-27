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
