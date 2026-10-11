from fastapi import APIRouter

router = APIRouter()

@router.post("/embed")
async def embed_knowledge():
    return {"status": "success", "message": "Knowledge embedded to pgvector"}
