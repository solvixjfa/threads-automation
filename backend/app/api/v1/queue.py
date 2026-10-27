from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone
from app.services.rag import get_supabase

router = APIRouter()

class EditQueueRequest(BaseModel):
    post_id: str
    text: str
    scheduled_for: str

class ActionQueueRequest(BaseModel):
    post_id: str

@router.put("/edit")
async def edit_queue(payload: EditQueueRequest):
    try:
        db = get_supabase()
        # Pastikan format tanggal valid
        try:
            dt = datetime.fromisoformat(payload.scheduled_for.replace("Z", "+00:00"))
        except ValueError:
            raise Exception("Invalid date format")

        { "error": db.schema("threads").from_("scheduled_posts").update({
            "text": payload.text,
            "scheduled_for": dt.isoformat()
        }).eq("id", payload.post_id).execute() }
        
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

@router.post("/retry")
async def retry_queue(payload: ActionQueueRequest):
    try:
        db = get_supabase()
        # Ubah status jadi 'scheduled' dan reset attempts biar worker narik lagi
        db.schema("threads").from_("scheduled_posts").update({
            "status": "scheduled",
            "attempts": 0,
            "last_error": None
        }).eq("id", payload.post_id).execute()
        return {"status": "success", "message": "Post queued for retry"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
