from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.leads import analyze_and_notify_lead
from app.workers.replies import fetch_and_process_replies
from app.services.auto_reply import publish_reply_to_threads

router = APIRouter()

class LeadAnalyzeRequest(BaseModel):
    account_id: str
    username: str
    comment: str

class PublishReplyRequest(BaseModel):
    account_id: str
    threads_reply_id: str
    text: str
    log_id: Optional[str] = None

@router.post("/analyze")
async def analyze_lead(payload: LeadAnalyzeRequest):
    try:
        result = await analyze_and_notify_lead(payload.account_id, payload.username, payload.comment)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sync-replies")
async def sync_existing_replies():
    try:
        await fetch_and_process_replies()
        return {"status": "success", "message": "Berhasil sinkronisasi komentar murni."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/publish-reply")
async def publish_reply_endpoint(payload: PublishReplyRequest):
    try:
        # 1. Kirim beneran ke Threads
        published_media_id = await publish_reply_to_threads(
            account_id=payload.account_id,
            threads_reply_to_id=payload.threads_reply_id,
            text=payload.text
        )
        
        # 2. Jika sukses, ubah status antrean di database lu jadi 'sent'
        if payload.log_id:
            from app.services.auto_reply import get_supabase
            db = get_supabase()
            db.schema("threads").from_("auto_reply_logs").update({
                "status": "sent",
                "final_text": payload.text,
                "sent_media_id": published_media_id
            }).eq("id", payload.log_id).execute()
            
        return {"status": "success", "published_id": published_media_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
