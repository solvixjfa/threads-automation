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


class SyncAccountRequest(BaseModel):
    account_id: str


@router.post("/sync-account")
async def sync_account_full(req: SyncAccountRequest):
    from datetime import datetime, timezone
    db = get_supabase()
    acc_res = (
        db.schema("threads")
        .from_("threads_accounts")
        .select("id, user_id, threads_user_id, username, settings, connection_status")
        .eq("id", req.account_id)
        .limit(1)
        .execute()
    )
    if not acc_res.data:
        raise HTTPException(status_code=404, detail="Account not found")

    acc = acc_res.data[0]
    token = (acc.get("settings") or {}).get("access_token")
    if not token:
        raise HTTPException(status_code=400, detail="Access token not found")

    now_iso = datetime.now(timezone.utc).isoformat()
    today_str = datetime.now(timezone.utc).date().isoformat()
    profile_pic = None
    followers_count = None
    discovered = 0
    synced_metrics = 0

    async with httpx.AsyncClient(timeout=20.0) as client:
        # 1. Sync profil & foto profil terbaru
        try:
            me_res = await client.get(
                "https://graph.threads.net/v1.0/me",
                params={"fields": "id,username,threads_profile_picture_url,followers_count", "access_token": token},
            )
            if me_res.status_code == 200:
                me_data = me_res.json()
                profile_pic = me_data.get("threads_profile_picture_url")
                followers_count = me_data.get("followers_count")
                upd = {"last_refresh_at": now_iso}
                if me_data.get("username"):
                    upd["username"] = me_data["username"]
                if profile_pic:
                    upd["profile_picture_url"] = profile_pic
                db.schema("threads").from_("threads_accounts").update(upd).eq("id", req.account_id).execute()
        except Exception as e:
            logging.warning(f"[SyncAccount] Profile fetch warning: {e}")

        # 2. Tarik daftar post dari /me/threads dan simpan teks + timestamp asli
        try:
            media_res = await client.get(
                "https://graph.threads.net/v1.0/me/threads",
                params={
                    "fields": "id,text,permalink,timestamp,media_type",
                    "limit": "50",
                    "access_token": token,
                },
            )
            if media_res.status_code == 200:
                items = media_res.json().get("data") or []
                for item in items:
                    media_id = str(item.get("id") or "")
                    if not media_id:
                        continue
                    post_text = item.get("text") or ""
                    permalink = item.get("permalink") or f"https://www.threads.com/post/{media_id}"
                    posted_at = item.get("timestamp") or now_iso
                    media_type = item.get("media_type") or "TEXT"

                    existing_post = (
                        db.schema("threads")
                        .from_("posts")
                        .select("id, text")
                        .eq("account_id", req.account_id)
                        .eq("threads_media_id", media_id)
                        .limit(1)
                        .execute()
                    )
                    if not existing_post.data:
                        db.schema("threads").from_("posts").insert({
                            "account_id": req.account_id,
                            "threads_media_id": media_id,
                            "text": post_text or None,
                            "media_type": media_type,
                            "permalink": permalink,
                            "posted_at": posted_at,
                            "source": "imported",
                        }).execute()
                        discovered += 1
                    else:
                        db.schema("threads").from_("posts").update({
                            "text": post_text or existing_post.data[0].get("text"),
                            "media_type": media_type,
                            "permalink": permalink,
                            "posted_at": posted_at,
                        }).eq("id", existing_post.data[0]["id"]).execute()

                    # Sinkronkan juga ke scheduled_posts dengan idempotency_key wajib
                    existing_sp = (
                        db.schema("threads")
                        .from_("scheduled_posts")
                        .select("id, text")
                        .eq("account_id", req.account_id)
                        .eq("published_media_id", media_id)
                        .limit(1)
                        .execute()
                    )
                    fallback_label = "[Media Post]" if media_type in ("IMAGE", "VIDEO", "CAROUSEL_ALBUM") else "[Post]"
                    safe_text = (post_text or fallback_label)[:500]
                    if not existing_sp.data:
                        try:
                            db.schema("threads").from_("scheduled_posts").insert({
                                "account_id": req.account_id,
                                "text": safe_text,
                                "scheduled_for": posted_at,
                                "status": "published",
                                "published_media_id": media_id,
                                "idempotency_key": f"meta_{req.account_id}_{media_id}",
                            }).execute()
                        except Exception as sp_err:
                            logging.warning(f"[SyncAccount] scheduled_posts insert skip: {sp_err}")
                    elif post_text and (not existing_sp.data[0].get("text") or existing_sp.data[0].get("text") == "Postingan Tanpa Teks"):
                        db.schema("threads").from_("scheduled_posts").update({
                            "text": safe_text,
                            "scheduled_for": posted_at,
                        }).eq("id", existing_sp.data[0]["id"]).execute()

                    # Simpan ke post_history untuk RAG
                    if post_text and len(post_text.strip()) >= 5:
                        try:
                            from app.services.rag import save_post_to_history_sync
                            save_post_to_history_sync(
                                account_id=req.account_id,
                                threads_media_id=media_id,
                                text=post_text,
                                posted_at=posted_at,
                            )
                        except Exception:
                            pass
        except Exception as e:
            logging.warning(f"[SyncAccount] Media list warning: {e}")

        # 3. Tarik metrik views/likes/replies/reposts/quotes untuk 30 post terbaru
        posts_rows = (
            db.schema("threads")
            .from_("posts")
            .select("id, threads_media_id")
            .eq("account_id", req.account_id)
            .order("posted_at", desc=True)
            .limit(30)
            .execute()
        ).data or []

        daily_views = daily_likes = daily_replies = daily_reposts = daily_quotes = 0
        for p in posts_rows:
            media_id = p.get("threads_media_id")
            if not media_id:
                continue
            try:
                ins_res = await client.get(
                    f"https://graph.threads.net/v1.0/{media_id}/insights",
                    params={
                        "metric": "views,likes,replies,reposts,quotes",
                        "access_token": token,
                    },
                )
                if ins_res.status_code == 200:
                    ins_data = ins_res.json().get("data") or []
                    metrics = {
                        item["name"]: item["values"][0]["value"]
                        for item in ins_data
                        if item.get("name") and item.get("values")
                    }
                    v = metrics.get("views", 0)
                    l = metrics.get("likes", 0)
                    r = metrics.get("replies", 0)
                    rp = metrics.get("reposts", 0)
                    q = metrics.get("quotes", 0)

                    daily_views += v
                    daily_likes += l
                    daily_replies += r
                    daily_reposts += rp
                    daily_quotes += q

                    db.schema("threads").from_("post_metrics").delete().eq("post_id", p["id"]).eq("snapshot_label", "latest").execute()
                    db.schema("threads").from_("post_metrics").insert({
                        "post_id": p["id"],
                        "snapshot_label": "latest",
                        "views": v,
                        "likes": l,
                        "replies": r,
                        "reposts": rp,
                        "quotes": q,
                        "captured_at": now_iso,
                    }).execute()
                    synced_metrics += 1
            except Exception as m_err:
                logging.warning(f"[SyncAccount] Metrics skip {media_id}: {m_err}")

        if posts_rows:
            try:
                db.schema("threads").from_("account_insights_daily").upsert(
                    {
                        "account_id": req.account_id,
                        "date": today_str,
                        "views": daily_views,
                        "likes": daily_likes,
                        "replies": daily_replies,
                        "reposts": daily_reposts,
                        "quotes": daily_quotes,
                        **({"followers_count": followers_count} if followers_count is not None else {}),
                    },
                    on_conflict="account_id,date",
                ).execute()
            except Exception as d_err:
                logging.warning(f"[SyncAccount] Daily insights upsert skip: {d_err}")

    return {
        "success": True,
        "discovered": discovered,
        "synced": synced_metrics,
        "profile_picture_url": profile_pic,
        "last_refresh_at": now_iso,
    }
