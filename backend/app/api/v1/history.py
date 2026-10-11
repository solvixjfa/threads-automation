from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.importer import import_threads_history

router = APIRouter()

class HistoryImportRequest(BaseModel):
    account_id: str
    access_token: str
    max_pages: int = 5

@router.post("/import")
async def import_history(payload: HistoryImportRequest):
    try:
        result = await import_threads_history(payload.account_id, payload.access_token, payload.max_pages)
        return {"status": "success", "summary": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
