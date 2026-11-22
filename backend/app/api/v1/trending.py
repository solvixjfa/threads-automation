from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from app.services.rag import get_supabase
from app.services.trending_outreach import (
    discover_trending_posts,
    inspect_creator_profile,
    generate_outreach_reply_draft,
    send_outreach_comment,
    run_auto_comment_cycle,
)

router = APIRouter()


class ReplyDraftRequest(BaseModel):
    account_id: str
    target_text: str = Field(..., min_length=1)
    target_username: str = "creator"
    reply_style: str = "insight"
    provider: Optional[str] = None
    model_name: Optional[str] = None


class SendReplyRequest(BaseModel):
    account_id: str
    target_media_id: str = Field(..., min_length=1)
    reply_text: str = Field(..., min_length=1, max_length=500)
    target_username: str = ""
    target_text: str = ""
    target_permalink: str = ""
    campaign_id: Optional[str] = None
    mode: str = "manual"


class CampaignUpsertRequest(BaseModel):
    id: Optional[str] = None
    account_id: str
    name: str = "Auto Outreach"
    region: str = "ID"
    category: str = "all"
    keywords: List[str] = []
    reply_style: str = "insight"
    max_per_hour: int = Field(default=3, ge=1, le=10)
    is_active: bool = False


class RunCampaignRequest(BaseModel):
    account_id: str


@router.get("/discover")
async def get_trending_discover(
    account_id: str = Query(...),
    region: str = Query("ID"),
    category: str = Query("all"),
    q: str = Query(""),
    limit: int = Query(20, ge=5, le=50),
    refresh: bool = Query(False),
    cache_only: bool = Query(False),
):
    try:
        return await discover_trending_posts(
            account_id=account_id,
            region=region,
            category=category,
            query=q,
            limit=limit,
            force_refresh=refresh,
            cache_only=cache_only,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/profile/{username}")
async def get_creator_profile(username: str, account_id: str = Query(...)):
    try:
        profile = await inspect_creator_profile(account_id=account_id, username=username)
        return {"profile": profile}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-reply")
async def post_generate_reply(req: ReplyDraftRequest):
    try:
        reply = await generate_outreach_reply_draft(
            account_id=req.account_id,
            target_text=req.target_text,
            target_username=req.target_username,
            reply_style=req.reply_style,
            provider=req.provider,
            model_name=req.model_name,
        )
        return {"reply_text": reply}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reply")
async def post_send_reply(req: SendReplyRequest):
    try:
        return await send_outreach_comment(
            account_id=req.account_id,
            target_media_id=req.target_media_id,
            reply_text=req.reply_text,
            target_username=req.target_username,
            target_text=req.target_text,
            target_permalink=req.target_permalink,
            campaign_id=req.campaign_id,
            mode=req.mode,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/campaigns")
async def list_campaigns(account_id: str = Query(...)):
    db = get_supabase()
    res = (
        db.schema("threads")
        .from_("outreach_campaigns")
        .select("*")
        .eq("account_id", account_id)
        .order("created_at", desc=True)
        .execute()
    )
    return {"campaigns": res.data or []}


@router.post("/campaigns")
async def upsert_campaign(req: CampaignUpsertRequest):
    db = get_supabase()
    clean_keywords = [k.strip() for k in (req.keywords or []) if k and k.strip()]
    payload = {
        "account_id": req.account_id,
        "name": req.name.strip() or "Auto Outreach",
        "region": (req.region or "ID").upper(),
        "category": (req.category or "all").lower(),
        "keywords": clean_keywords,
        "reply_style": req.reply_style or "insight",
        "max_per_hour": req.max_per_hour,
        "is_active": req.is_active,
    }
    if req.id:
        res = (
            db.schema("threads")
            .from_("outreach_campaigns")
            .update(payload)
            .eq("id", req.id)
            .eq("account_id", req.account_id)
            .execute()
        )
    else:
        res = db.schema("threads").from_("outreach_campaigns").insert(payload).execute()
    return {"campaign": res.data[0] if res.data else payload}


@router.post("/campaigns/run")
async def run_campaign_now(req: RunCampaignRequest):
    try:
        return await run_auto_comment_cycle(account_id=req.account_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/logs")
async def get_outreach_logs(account_id: str = Query(...), limit: int = Query(30, ge=1, le=100)):
    db = get_supabase()
    res = (
        db.schema("threads")
        .from_("outreach_logs")
        .select("*")
        .eq("account_id", account_id)
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return {"logs": res.data or []}
