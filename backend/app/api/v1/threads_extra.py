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
    import asyncio
    from datetime import datetime, timezone, timedelta

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

    now_dt = datetime.now(timezone.utc)
    now_iso = now_dt.isoformat()
    today_str = now_dt.date().isoformat()
    cutoff_90d = now_dt - timedelta(days=95)

    threads_uid = str(acc.get("threads_user_id") or "me")
    profile_pic = None
    followers_count = None
    discovered = 0
    synced_metrics = 0
    daily_views_map = {}
    insights_errors = []

    async with httpx.AsyncClient(timeout=20.0) as client:
        # 1. Tarik profil, followers_count, dan 90-day daily views (3x30d) secara paralel
        now_unix = int(now_dt.timestamp())

        async def fetch_profile():
            return await client.get(
                "https://graph.threads.net/v1.0/me",
                params={"fields": "id,username,threads_profile_picture_url", "access_token": token},
            )

        async def fetch_followers():
            return await client.get(
                f"https://graph.threads.net/v1.0/{threads_uid}/threads_insights",
                params={"metric": "followers_count", "access_token": token},
            )

        async def fetch_views_window(w: int):
            until_ts = now_unix - (w * 30 * 86400)
            since_ts = until_ts - (30 * 86400)
            res = await client.get(
                f"https://graph.threads.net/v1.0/{threads_uid}/threads_insights",
                params={
                    "metric": "views",
                    "since": str(since_ts),
                    "until": str(until_ts),
                    "access_token": token,
                },
            )
            if res.status_code != 200 and threads_uid != "me":
                res = await client.get(
                    "https://graph.threads.net/v1.0/me/threads_insights",
                    params={
                        "metric": "views",
                        "since": str(since_ts),
                        "until": str(until_ts),
                        "access_token": token,
                    },
                )
            return w, res

        top_results = await asyncio.gather(
            fetch_profile(),
            fetch_followers(),
            fetch_views_window(0),
            fetch_views_window(1),
            fetch_views_window(2),
            return_exceptions=True,
        )

        # Proses profil
        me_res = top_results[0]
        if not isinstance(me_res, Exception) and me_res.status_code == 200:
            me_data = me_res.json()
            profile_pic = me_data.get("threads_profile_picture_url")
            upd = {"last_refresh_at": now_iso, "last_synced_at": now_iso}
            if me_data.get("username"):
                upd["username"] = me_data["username"]
            if profile_pic:
                upd["profile_picture_url"] = profile_pic
            db.schema("threads").from_("threads_accounts").update(upd).eq("id", req.account_id).execute()

        # Proses followers_count
        f_res = top_results[1]
        if not isinstance(f_res, Exception) and f_res.status_code == 200:
            for item in (f_res.json().get("data") or []):
                if item.get("name") == "followers_count":
                    tv = item.get("total_value") or {}
                    if isinstance(tv, dict) and tv.get("value") is not None:
                        followers_count = int(tv["value"])
                    elif item.get("values"):
                        followers_count = int(item["values"][-1].get("value") or 0)

        # Proses 90-day daily views time series
        for win_res in top_results[2:]:
            if isinstance(win_res, Exception):
                insights_errors.append(str(win_res)[:160])
                continue
            w_idx, v_res = win_res
            if v_res.status_code == 200:
                for item in (v_res.json().get("data") or []):
                    if item.get("name") == "views":
                        for val_obj in (item.get("values") or []):
                            end_t = str(val_obj.get("end_time") or "")
                            if len(end_t) >= 10:
                                d_key = end_t[:10]
                                daily_views_map[d_key] = int(val_obj.get("value") or 0)
            else:
                insights_errors.append(f"w{w_idx}:{v_res.status_code}:{v_res.text[:140]}")

        # 2. Langsung simpan 90 hari ke account_insights_daily SEBELUM sync post agar anti-timeout
        existing_daily_map = {}
        try:
            ex_rows = (
                db.schema("threads")
                .from_("account_insights_daily")
                .select("date, views, likes, replies, reposts, quotes, followers_count, demographics")
                .eq("account_id", req.account_id)
                .execute()
            ).data or []
            for r in ex_rows:
                if r.get("date"):
                    existing_daily_map[str(r["date"])[:10]] = r
        except Exception:
            pass

        continuous_dates = {(now_dt.date() - timedelta(days=i)).isoformat() for i in range(90)}
        all_dates = sorted(continuous_dates | set(daily_views_map.keys()) | set(existing_daily_map.keys()))

        def build_daily_rows(post_agg_map: dict):
            rows = []
            for d_key in sorted(set(all_dates) | set(post_agg_map.keys())):
                p_agg = post_agg_map.get(d_key, {})
                prev = existing_daily_map.get(d_key, {})
                views_val = max(
                    int(daily_views_map.get(d_key) or 0),
                    int(p_agg.get("views") or 0),
                    int(prev.get("views") or 0),
                )
                f_val = prev.get("followers_count")
                if d_key == today_str and followers_count is not None:
                    f_val = int(followers_count)
                elif f_val is None:
                    f_val = 0

                rows.append({
                    "account_id": req.account_id,
                    "date": d_key,
                    "views": views_val,
                    "likes": max(int(p_agg.get("likes") or 0), int(prev.get("likes") or 0)),
                    "replies": max(int(p_agg.get("replies") or 0), int(prev.get("replies") or 0)),
                    "reposts": max(int(p_agg.get("reposts") or 0), int(prev.get("reposts") or 0)),
                    "quotes": max(int(p_agg.get("quotes") or 0), int(prev.get("quotes") or 0)),
                    "followers_count": int(f_val),
                    "demographics": prev.get("demographics") if isinstance(prev.get("demographics"), dict) else {},
                })
            return rows

        upsert_error = None
        initial_rows = build_daily_rows({})
        try:
            db.schema("threads").from_("account_insights_daily").upsert(
                initial_rows,
                on_conflict="account_id,date",
            ).execute()
        except Exception as d_err:
            upsert_error = str(d_err)[:300]
            logging.error(f"[SyncAccount] Initial 90d upsert error: {d_err}")

        # 3. Tarik daftar post dengan pagination (maks 4 halaman = 200 post) & bulk insert
        try:
            existing_posts_res = (
                db.schema("threads")
                .from_("posts")
                .select("id, threads_media_id, text")
                .eq("account_id", req.account_id)
                .execute()
            ).data or []
            existing_posts_map = {str(r["threads_media_id"]): r for r in existing_posts_res if r.get("threads_media_id")}

            existing_sp_res = (
                db.schema("threads")
                .from_("scheduled_posts")
                .select("id, published_media_id, text")
                .eq("account_id", req.account_id)
                .execute()
            ).data or []
            existing_sp_map = {str(r["published_media_id"]): r for r in existing_sp_res if r.get("published_media_id")}

            next_url = "https://graph.threads.net/v1.0/me/threads"
            next_params = {
                "fields": "id,text,permalink,timestamp,media_type",
                "limit": "50",
                "access_token": token,
            }
            pages = 0
            new_posts_batch = []
            new_sp_batch = []
            seen_media_ids = set()

            while next_url and pages < 4:
                media_res = await client.get(next_url, params=next_params)
                next_params = None
                if media_res.status_code != 200:
                    break
                payload_json = media_res.json()
                items = payload_json.get("data") or []
                if not items:
                    break

                reached_old = False
                for item in items:
                    media_id = str(item.get("id") or "")
                    if not media_id or media_id in seen_media_ids:
                        continue
                    seen_media_ids.add(media_id)

                    post_text = item.get("text") or ""
                    raw_perm = (item.get("permalink") or "").strip()
                    permalink = raw_perm.replace("://www.threads.net/", "://www.threads.com/") if ("/@" in raw_perm and "/post/" in raw_perm) else ""
                    posted_at = item.get("timestamp") or now_iso
                    media_type = item.get("media_type") or "TEXT"

                    try:
                        if datetime.fromisoformat(posted_at.replace("Z", "+00:00")) < cutoff_90d:
                            reached_old = True
                    except Exception:
                        pass

                    if media_id not in existing_posts_map:
                        new_posts_batch.append({
                            "account_id": req.account_id,
                            "threads_media_id": media_id,
                            "text": post_text or None,
                            "media_type": media_type,
                            "permalink": permalink,
                            "posted_at": posted_at,
                            "source": "imported",
                        })
                        discovered += 1

                    fallback_label = "[Media Post]" if media_type in ("IMAGE", "VIDEO", "CAROUSEL_ALBUM") else "[Post]"
                    safe_text = (post_text or fallback_label)[:500]
                    if media_id not in existing_sp_map:
                        new_sp_batch.append({
                            "account_id": req.account_id,
                            "text": safe_text,
                            "scheduled_for": posted_at,
                            "status": "published",
                            "published_media_id": media_id,
                            "idempotency_key": f"meta_{req.account_id}_{media_id}",
                        })

                pages += 1
                next_url = (payload_json.get("paging") or {}).get("next")
                if reached_old:
                    break

            if new_posts_batch:
                db.schema("threads").from_("posts").insert(new_posts_batch).execute()
            if new_sp_batch:
                try:
                    db.schema("threads").from_("scheduled_posts").insert(new_sp_batch).execute()
                except Exception:
                    pass
        except Exception as e:
            logging.warning(f"[SyncAccount] Media list warning: {e}")

        # 4. Tarik metrik hingga 100 post terbaru secara paralel (Semaphore 15) & bulk insert post_metrics
        posts_rows = (
            db.schema("threads")
            .from_("posts")
            .select("id, threads_media_id, posted_at")
            .eq("account_id", req.account_id)
            .order("posted_at", desc=True)
            .limit(100)
            .execute()
        ).data or []

        sem = asyncio.Semaphore(15)

        async def fetch_one_metric(p_row):
            media_id = p_row.get("threads_media_id")
            if not media_id:
                return None
            async with sem:
                try:
                    ins_res = await client.get(
                        f"https://graph.threads.net/v1.0/{media_id}/insights",
                        params={
                            "metric": "views,likes,replies,reposts,quotes",
                            "access_token": token,
                        },
                    )
                    if ins_res.status_code != 200:
                        return None
                    ins_data = ins_res.json().get("data") or []
                    metrics = {
                        item["name"]: item["values"][0]["value"]
                        for item in ins_data
                        if item.get("name") and item.get("values")
                    }
                    return (p_row, metrics)
                except Exception:
                    return None

        metric_results = await asyncio.gather(*(fetch_one_metric(p) for p in posts_rows))

        post_daily_agg = {}
        metrics_insert_batch = []
        synced_post_ids = []

        for item in metric_results:
            if not item:
                continue
            p_row, metrics = item
            v = int(metrics.get("views") or 0)
            l = int(metrics.get("likes") or 0)
            r = int(metrics.get("replies") or 0)
            rp = int(metrics.get("reposts") or 0)
            q = int(metrics.get("quotes") or 0)

            ts = str(p_row.get("posted_at") or today_str)
            d_key = ts[:10] if len(ts) >= 10 else today_str
            agg = post_daily_agg.setdefault(d_key, {"views": 0, "likes": 0, "replies": 0, "reposts": 0, "quotes": 0})
            agg["views"] += v
            agg["likes"] += l
            agg["replies"] += r
            agg["reposts"] += rp
            agg["quotes"] += q

            synced_post_ids.append(p_row["id"])
            metrics_insert_batch.append({
                "post_id": p_row["id"],
                "snapshot_label": "latest",
                "views": v,
                "likes": l,
                "replies": r,
                "reposts": rp,
                "quotes": q,
                "captured_at": now_iso,
            })
            synced_metrics += 1

        if synced_post_ids:
            try:
                db.schema("threads").from_("post_metrics").delete().in_("post_id", synced_post_ids).eq("snapshot_label", "latest").execute()
                db.schema("threads").from_("post_metrics").insert(metrics_insert_batch).execute()
            except Exception as m_err:
                logging.warning(f"[SyncAccount] Bulk post_metrics warning: {m_err}")

        # 5. Update ulang account_insights_daily dengan agregat likes/replies/reposts/quotes harian
        final_rows = build_daily_rows(post_daily_agg)
        try:
            db.schema("threads").from_("account_insights_daily").upsert(
                final_rows,
                on_conflict="account_id,date",
            ).execute()
        except Exception as d_err:
            upsert_error = str(d_err)[:300]

    return {
        "success": True,
        "discovered": discovered,
        "synced": synced_metrics,
        "followers_count": followers_count,
        "days_synced": len(daily_views_map),
        "rows_upserted": len(final_rows),
        "upsert_error": upsert_error,
        "insights_errors": insights_errors,
        "profile_picture_url": profile_pic,
        "last_refresh_at": now_iso,
    }
