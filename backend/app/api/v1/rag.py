from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.rag import (
    store_knowledge, backfill_unembedded_knowledge, generate_rag_post, 
    get_all_raw_models, get_available_models, repurpose_content, get_repurpose_recommendations,
    score_draft_ai, improve_draft_ai, label_topics_ai
)
from app.services.auto_reply import generate_rag_reply
from app.services.billing import check_and_spend, refund_credits, BillingError

router = APIRouter()

@router.get("/knowledge")
async def list_knowledge_endpoint(account_id: str):
    from app.services.rag import list_knowledge_docs
    docs = await list_knowledge_docs(account_id)
    return {"knowledge": docs}


class KnowledgeRequest(BaseModel):
    account_id: str
    title: str
    content: str
    category: Optional[str] = "general"

class AutoReplyRequest(BaseModel):
    account_id: str
    user_comment: str
    author_username: Optional[str] = ""
    provider: Optional[str] = "gemini"
    model_name: Optional[str] = None
    post_text: Optional[str] = ""
    reply_id: Optional[str] = None

class BackfillRequest(BaseModel):
    account_id: str

class GeneratePostRequest(BaseModel):
    account_id: str
    topic: str
    tone: Optional[str] = "Edukasi & Insight Kasual"
    custom_prompt: Optional[str] = None
    provider: Optional[str] = "gemini"
    model_name: Optional[str] = None
    selected_knowledge_ids: Optional[list[str]] = None

class RepurposeRequest(BaseModel):
    account_id: str
    source_text: str
    angle: str
    provider: Optional[str] = "gemini"
    model_name: Optional[str] = None

class ScoreDraftRequest(BaseModel):
    account_id: str
    text: str
    provider: Optional[str] = "groq"
    model_name: Optional[str] = None

class ImproveDraftRequest(BaseModel):
    account_id: str
    text: str
    provider: Optional[str] = "groq"
    model_name: Optional[str] = None

class LabelTopicsRequest(BaseModel):
    account_id: str
    clusters: list
    provider: Optional[str] = "groq"
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

@router.get("/recommendations/{account_id}")
async def list_recommendations(account_id: str):
    try:
        recs = await get_repurpose_recommendations(account_id)
        return {"status": "success", "recommendations": recs}
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
        import logging
        import httpx
        final_post_text = payload.post_text or ""
        
        if not final_post_text and payload.reply_id:
            try:
                from app.services.rag import get_supabase
                db = get_supabase()
                media_id = None
                
                # 1. Cek ke tabel scheduled_posts lewat ID (langsung)
                sp_res = db.schema("threads").from_("scheduled_posts").select("text").eq("id", payload.reply_id).limit(1).execute()
                if sp_res.data:
                    final_post_text = sp_res.data[0].get("text", "")
                
                if not final_post_text:
                    # 2. Cek ke tabel replies -> posts -> threads_media_id
                    r_res = db.schema("threads").from_("replies").select("post_id").eq("id", payload.reply_id).limit(1).execute()
                    if r_res.data and r_res.data[0].get("post_id"):
                        post_ref = r_res.data[0]["post_id"]
                        p_res = db.schema("threads").from_("posts").select("threads_media_id").eq("id", post_ref).limit(1).execute()
                        if p_res.data:
                            media_id = p_res.data[0].get("threads_media_id")
                            
                            # Coba cari di scheduled_posts pakai media_id
                            if media_id:
                                sp2 = db.schema("threads").from_("scheduled_posts").select("text").eq("published_media_id", media_id).limit(1).execute()
                                if sp2.data:
                                    final_post_text = sp2.data[0].get("text", "")
                                    
                            # 3. JALUR TERAKHIR: Tembak API Threads (Meta)
                            if not final_post_text and media_id:
                                acc = db.schema("threads").from_("threads_accounts").select("settings").eq("id", payload.account_id).limit(1).execute()
                                token = acc.data[0].get("settings", {}).get("access_token") if acc.data else None
                                if token:
                                    async with httpx.AsyncClient() as client:
                                        m_res = await client.get(f"https://graph.threads.net/v1.0/{media_id}?fields=text&access_token={token}")
                                        if m_res.status_code == 200:
                                            final_post_text = m_res.json().get("text", "")
                                            
                logging.info(f"[generate-reply] reply_id={payload.reply_id} media_id={media_id} post_text_len={len(final_post_text)}")
            except Exception as lookup_err:
                logging.error(f"[generate-reply] Post text lookup failed: {lookup_err}")

        reply = await generate_rag_reply(
            account_id=payload.account_id, user_comment=payload.user_comment,
            post_text=final_post_text,
            author_username=payload.author_username or "",
            provider=payload.provider or "gemini", model_name=payload.model_name
        )
        return {"status": "success", "reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-post")
async def generate_post(payload: GeneratePostRequest):
    ref_id = None
    try:
        ref_id = check_and_spend(payload.account_id, "generate")
        options = await generate_rag_post(
            account_id=payload.account_id, topic=payload.topic,
            tone=payload.tone or "Edukasi & Insight Kasual",
            custom_prompt=payload.custom_prompt,
            provider=payload.provider or "gemini",
            model_name=payload.model_name,
            selected_knowledge_ids=payload.selected_knowledge_ids
        )
        return {"status": "success", "options": options}
    except asyncio.CancelledError:
        if ref_id: refund_credits(payload.account_id, "generate", ref_id)
        raise
    except Exception as e:
        if ref_id: refund_credits(payload.account_id, "generate", ref_id)
        if isinstance(e, BillingError): raise HTTPException(status_code=403, detail=e.message)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/repurpose")
async def repurpose(payload: RepurposeRequest):
    ref_id = None
    try:
        ref_id = check_and_spend(payload.account_id, "repurpose")
        options = await repurpose_content(
            account_id=payload.account_id,
            source_text=payload.source_text,
            angle=payload.angle,
            provider=payload.provider or "gemini",
            model_name=payload.model_name
        )
        return {"status": "success", "options": options}
    except asyncio.CancelledError:
        if ref_id: refund_credits(payload.account_id, "repurpose", ref_id)
        raise
    except Exception as e:
        if ref_id: refund_credits(payload.account_id, "repurpose", ref_id)
        if isinstance(e, BillingError): raise HTTPException(status_code=403, detail=e.message)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/score-draft")
async def score_draft(payload: ScoreDraftRequest):
    ref_id = None
    try:
        ref_id = check_and_spend(payload.account_id, "deep_scoring")
        result = await score_draft_ai(
            account_id=payload.account_id,
            text=payload.text,
            provider=payload.provider or "groq",
            model_name=payload.model_name
        )
        return {"status": "success", "data": result}
    except Exception as e:
        if ref_id: refund_credits(payload.account_id, "deep_scoring", ref_id)
        if isinstance(e, BillingError): raise HTTPException(status_code=403, detail=e.message)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/improve")
async def improve_draft(payload: ImproveDraftRequest):
    try:
        text = await improve_draft_ai(
            account_id=payload.account_id,
            text=payload.text,
            provider=payload.provider or "groq",
            model_name=payload.model_name
        )
        return {"status": "success", "improved_text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/label-topics")
async def label_topics(payload: LabelTopicsRequest):
    try:
        names = await label_topics_ai(
            account_id=payload.account_id,
            clusters=payload.clusters,
            provider=payload.provider or "groq",
            model_name=payload.model_name
        )
        return {"status": "success", "topics": names}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
