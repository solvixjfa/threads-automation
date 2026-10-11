from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.rag import store_knowledge, get_available_embedding_models
from app.services.auto_reply import generate_rag_reply

router = APIRouter()

class KnowledgeRequest(BaseModel):
    account_id: str
    title: str
    content: str
    category: Optional[str] = "general"

class AutoReplyRequest(BaseModel):
    account_id: str
    user_comment: str
    author_username: Optional[str] = ""

@router.get("/list-models")
async def list_embedding_models():
    try:
        models = get_available_embedding_models()
        return {"status": "success", "embedding_models_found": models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/embed")
async def embed_knowledge(payload: KnowledgeRequest):
    try:
        result = await store_knowledge(
            account_id=payload.account_id,
            title=payload.title,
            content=payload.content,
            category=payload.category or "general"
        )
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-reply")
async def generate_reply(payload: AutoReplyRequest):
    try:
        reply = await generate_rag_reply(
            account_id=payload.account_id,
            user_comment=payload.user_comment,
            author_username=payload.author_username or ""
        )
        return {"status": "success", "reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
