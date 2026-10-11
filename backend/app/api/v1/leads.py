from fastapi import APIRouter

router = APIRouter()

@router.post("/analyze")
async def analyze_lead():
    return {"status": "success", "message": "Lead analyzed"}
