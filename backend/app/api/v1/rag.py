from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.rag import store_knowledge, search_knowledge
from app.services.auto_reply import generate_rag_reply

router = APIRouter()

class KnowledgeRequest(BaseModel):
    account_id: str
    title: str
    content: str

class AutoReplyRequest(BaseModel):
    account_id: str
    user_comment: str
    author_username: str = ""

@router.post("/embed")
async def embed_knowledge(payload: KnowledgeRequest):
    try:
        result = await store_knowledge(payload.account_id, payload.title, payload.content)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-reply")
async def generate_reply(payload: AutoReplyRequest):
    try:
        reply = await generate_rag_reply(payload.account_id, payload.user_comment, payload.author_username)
        return {"status": "success", "reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
