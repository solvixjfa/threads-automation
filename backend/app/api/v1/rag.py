from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.rag import store_knowledge, backfill_unembedded_knowledge, generate_rag_post, get_all_raw_models, get_available_models, repurpose_content
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

class BackfillRequest(BaseModel):
    account_id: str

class GeneratePostRequest(BaseModel):
    account_id: str
    topic: str
    tone: Optional[str] = "Edukasi & Insight Kasual"
    custom_prompt: Optional[str] = None
    provider: Optional[str] = "gemini"
    model_name: Optional[str] = None

class RepurposeRequest(BaseModel):
    account_id: str
    source_text: str
    angle: str
    provider: Optional[str] = "gemini"
    model_name: Optional[str] = None

@router.get("/list-models")
async def list_embedding_models():
    try:
        models = get_all_raw_models()
        return {"status": "success", "raw_models_in_api_key": models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models/{provider}")
async def list_ai_models(provider: str, account_id: str):
    try:
        models = await get_available_models(account_id, provider)
        return {"status": "success", "models": models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/embed")
async def embed_knowledge(payload: KnowledgeRequest):
    try:
        result = await store_knowledge(
            account_id=payload.account_id, title=payload.title, content=payload.content,
            category=payload.category or "general"
        )
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/backfill")
async def backfill_knowledge(payload: BackfillRequest):
    try:
        result = await backfill_unembedded_knowledge(payload.account_id)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-reply")
async def generate_reply(payload: AutoReplyRequest):
    try:
        reply = await generate_rag_reply(
            account_id=payload.account_id, user_comment=payload.user_comment, author_username=payload.author_username or ""
        )
        return {"status": "success", "reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-post")
async def generate_post(payload: GeneratePostRequest):
    try:
        options = await generate_rag_post(
            account_id=payload.account_id, topic=payload.topic,
            tone=payload.tone or "Edukasi & Insight Kasual",
            custom_prompt=payload.custom_prompt,
            provider=payload.provider or "gemini",
            model_name=payload.model_name
        )
        return {"status": "success", "options": options}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/repurpose")
async def repurpose(payload: RepurposeRequest):
    try:
        options = await repurpose_content(
            account_id=payload.account_id,
            source_text=payload.source_text,
            angle=payload.angle,
            provider=payload.provider or "gemini",
            model_name=payload.model_name
        )
        return {"status": "success", "options": options}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
