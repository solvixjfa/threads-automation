from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.leads import analyze_and_notify_lead

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
