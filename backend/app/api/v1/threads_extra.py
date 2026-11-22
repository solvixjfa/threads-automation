import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
import httpx
from app.services.rag import get_supabase
from app.services.auto_reply import generate_rag_reply, publish_reply_to_threads

router = APIRouter()


def _get_account_credentials(account_id: str) -> dict:
    db = get_supabase()
    res = (
        db.schema("threads")
        .from_("threads_accounts")
        .select("id, threads_user_id, username, settings, connection_status, kill_switch, ai_provider")
        .eq("id", account_id)
        .limit(1)
        .execute()
    )
    if not res.data:
        raise ValueError("Account not found")
    acc = res.data[0]
    if acc.get("connection_status") != "connected":
        raise ValueError("Threads account is not connected")
    token = (acc.get("settings") or {}).get("access_token")
    if not token:
        raise ValueError("Threads access token not found")
    acc["_token"] = token
    return acc


class MentionGenerateRequest(BaseModel):
    account_id: str
    mention_text: str
    author_username: str = "creator"
    provider: Optional[str] = None
    model_name: Optional[str] = None


class MentionReplyRequest(BaseModel):
    account_id: str
    mention_media_id: str
    reply_text: str


@router.get("/locations/search")
async def search_threads_locations(
    account_id: str = Query(...),
    q: str = Query(..., min_length=1),
    latitude: Optional[float] = Query(None),
    longitude: Optional[float] = Query(None),
):
    try:
        acc = _get_account_credentials(account_id)
        params = {
            "q": q.strip(),
            "access_token": acc["_token"],
        }
        if latitude is not None and longitude is not None:
            params["latitude"] = str(latitude)
            params["longitude"] = str(longitude)

        async with httpx.AsyncClient(timeout=15.0) as client:
            res = await client.get("https://graph.threads.net/v1.0/location_search", params=params)
            data = res.json()
            if res.status_code != 200 or "error" in data:
                err_msg = (data.get("error") or {}).get("message") or res.text[:200]
                raise HTTPException(status_code=400, detail=f"Threads Location Search error: {err_msg}")

            locations = []
            for item in data.get("data") or []:
                locations.append({
                    "id": str(item.get("id") or ""),
                    "name": item.get("name") or "",
                    "address": item.get("address") or "",
                    "city": item.get("city") or "",
                    "country": item.get("country") or "",
                })
            return {"locations": [loc for loc in locations if loc["id"]]}
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.error(f"[Location Search] Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/mentions")
async def get_threads_mentions(
    account_id: str = Query(...),
    limit: int = Query(25, ge=1, le=50),
):
    try:
        acc = _get_account_credentials(account_id)
        threads_uid = acc.get("threads_user_id") or "me"
        params = {
            "fields": "id,text,username,timestamp,permalink,media_type,media_url",
            "limit": str(limit),
            "access_token": acc["_token"],
        }
        async with httpx.AsyncClient(timeout=15.0) as client:
            res = await client.get(f"https://graph.threads.net/v1.0/{threads_uid}/mentions", params=params)
            data = res.json()
            if res.status_code != 200 or "error" in data:
                err_msg = (data.get("error") or {}).get("message") or res.text[:200]
                raise HTTPException(status_code=400, detail=f"Threads Mentions error: {err_msg}")

            mentions = []
            for item in data.get("data") or []:
                mentions.append({
                    "id": str(item.get("id") or ""),
                    "text": item.get("text") or "",
                    "username": item.get("username") or "user",
                    "timestamp": item.get("timestamp") or "",
                    "permalink": item.get("permalink") or "",
                    "media_type": item.get("media_type") or "TEXT",
                    "media_url": item.get("media_url") or "",
                })
            return {"mentions": mentions}
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.error(f"[Mentions Fetch] Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/mentions/generate-reply")
async def generate_mention_reply(req: MentionGenerateRequest):
    try:
        acc = _get_account_credentials(req.account_id)
        if acc.get("kill_switch"):
            raise ValueError("Kill Switch is active for this account")
        chosen_provider = req.provider or acc.get("ai_provider") or "groq"
        draft = await generate_rag_reply(
            account_id=req.account_id,
            user_comment=req.mention_text or "Thanks for mentioning us!",
            post_text=req.mention_text or "",
            author_username=req.author_username or "user",
            provider=chosen_provider,
            model_name=req.model_name,
            tone_prompt="Reply naturally and appreciatively to a user who mentioned our account on Threads. Keep it concise (1-2 sentences).",
        )
        if not draft:
            raise ValueError("Unable to generate AI reply")
        return {"reply_text": draft.strip()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/mentions/reply")
async def reply_to_mention(req: MentionReplyRequest):
    try:
        acc = _get_account_credentials(req.account_id)
        if acc.get("kill_switch"):
            raise ValueError("Kill Switch is active for this account")
        clean_text = (req.reply_text or "").strip()
        if not req.mention_media_id or not clean_text:
            raise ValueError("mention_media_id and reply_text are required")
        published_id = await publish_reply_to_threads(req.account_id, req.mention_media_id, clean_text)
        return {"success": True, "reply_threads_id": published_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.error(f"[Mention Reply] Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
