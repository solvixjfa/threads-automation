from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.leads import analyze_and_notify_lead
from app.workers.replies import fetch_and_process_replies

router = APIRouter()

class LeadAnalyzeRequest(BaseModel):
    account_id: str
    username: str
    comment: str

@router.post("/analyze")
async def analyze_lead(payload: LeadAnalyzeRequest):
    try:
        result = await analyze_and_notify_lead(payload.account_id, payload.username, payload.comment)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# FIX: Mengembalikan endpoint yang hilang agar tombol "Sync" berfungsi
@router.get("/sync-replies")
async def sync_existing_replies():
    try:
        await fetch_and_process_replies()
        return {"status": "success", "message": "Berhasil sinkronisasi komentar dan membuat draf balasan AI."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
