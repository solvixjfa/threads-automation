from fastapi import APIRouter

router = APIRouter()

@router.post("/import")
async def import_history():
    return {"status": "success", "message": "History import started"}
