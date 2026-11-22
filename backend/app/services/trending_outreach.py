import asyncio
import logging
import random
from datetime import datetime, timezone, timedelta
import httpx
from app.services.rag import get_supabase
from app.services.auto_reply import generate_rag_reply, publish_reply_to_threads

CATEGORY_SEEDS = {
    "all": ["teknologi", "bisnis", "kreator", "startup"],
    "tech": ["AI", "software", "programming", "gadget"],
    "business": ["bisnis", "marketing", "jualan", "startup"],
    "finance": ["investasi", "keuangan", "saham", "crypto"],
    "lifestyle": ["produktivitas", "karir", "self improvement", "kesehatan"],
}

REGION_HINTS = {
    "ID": "Indonesia",
    "GLOBAL": "",
}

STYLE_PROMPTS = {
    "insight": "Add a sharp, practical insight or short takeaway relevant to the post. Keep it concise and conversational.",
    "question": "Ask one natural, thought-provoking follow-up question that sparks discussion without sounding generic.",
    "value": "Share a brief, helpful tip or real-world observation related to the topic without hard-selling.",
}


def _get_account_guard(db, account_id: str) -> dict:
    res = (
        db.schema("threads")
        .from_("threads_accounts")
        .select("id, username, settings, connection_status, kill_switch, ai_provider")
        .eq("id", account_id)
        .limit(1)
        .execute()
    )
    if not res.data:
        raise ValueError("Account not found")
    acc = res.data[0]
    if acc.get("connection_status") != "connected":
        raise ValueError("Threads account is not connected")
    if acc.get("kill_switch"):
        raise ValueError("Kill Switch is active for this account")
    token = (acc.get("settings") or {}).get("access_token")
    if not token:
        raise ValueError("Threads access token not found")
    acc["_token"] = token
    return acc


def _is_already_commented(db, account_id: str, media_id: str) -> bool:
    res = (
        db.schema("threads")
        .from_("outreach_logs")
        .select("id")
        .eq("account_id", account_id)
        .eq("target_media_id", media_id)
        .eq("status", "sent")
        .limit(1)
        .execute()
    )
    return bool(res.data)


def _count_sent_last_hour(db, account_id: str) -> int:
    one_hour_ago = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
    res = (
        db.schema("threads")
        .from_("outreach_logs")
        .select("id", count="exact")
        .eq("account_id", account_id)
        .eq("status", "sent")
        .gte("created_at", one_hour_ago)
        .execute()
    )
    return res.count or 0


def _enrich_and_filter_posts(db, account_id: str, own_username: str, raw_posts: list[dict]) -> list[dict]:
    own_lower = (own_username or "").lstrip("@").lower()
    external_posts = []
    own_posts = []

    for p in raw_posts:
        mid = p.get("id")
        if not mid:
            continue
        item = {**p, "already_replied": _is_already_commented(db, account_id, mid)}
        author_lower = (item.get("username") or "").lstrip("@").lower()
        if own_lower and author_lower == own_lower:
            own_posts.append(item)
        else:
            external_posts.append(item)

    return external_posts if external_posts else own_posts



DEFAULT_TRENDING_TOPICS = ["AI", "Bisnis", "Startup", "Marketing", "Produktivitas"]


async def fetch_official_trending_topics(
    account_id: str,
    force_refresh: bool = False,
    cache_only: bool = False,
) -> dict:
    db = get_supabase()
    acc = _get_account_guard(db, account_id)
    token = acc["_token"]
    cache_key = "topics:v1:official"
    now = datetime.now(timezone.utc)

    if not force_refresh:
        q = (
            db.schema("threads")
            .from_("trending_cache")
            .select("payload, fetched_at, expires_at")
            .eq("cache_key", cache_key)
            .limit(1)
        )
        if not cache_only:
            q = q.gt("expires_at", now.isoformat())
        cached = q.execute()
        if cached.data:
            topics = cached.data[0].get("payload") or DEFAULT_TRENDING_TOPICS
            return {"topics": topics, "cached": True}
        if cache_only:
            return {"topics": DEFAULT_TRENDING_TOPICS, "cached": True}

    extracted = []
    async with httpx.AsyncClient(timeout=15.0) as client:
        for params in (
            {"country_code": "US", "access_token": token},
            {"access_token": token},
        ):
            try:
                res = await client.get("https://graph.threads.net/v1.0/trending_topics", params=params)
                if res.status_code != 200:
                    logging.warning(f"[Trending Topics] Meta status {res.status_code}: {res.text[:200]}")
                    continue
                items = res.json().get("data") or []
                for item in items:
                    if isinstance(item, str):
                        label = item.strip()
                    elif isinstance(item, dict):
                        label = (item.get("topic") or item.get("name") or item.get("title") or "").strip()
                    else:
                        label = ""
                    if label and label not in extracted:
                        extracted.append(label)
                if extracted:
                    break
            except Exception as e:
                logging.error(f"[Trending Topics] Error: {e}")

    final_topics = extracted[:10] if extracted else DEFAULT_TRENDING_TOPICS
    try:
        db.schema("threads").from_("trending_cache").upsert({
            "cache_key": cache_key,
            "region": "GLOBAL",
            "category": "topics",
            "query_text": "official_trending_topics",
            "payload": final_topics,
            "fetched_at": now.isoformat(),
            "expires_at": (now + timedelta(minutes=60)).isoformat(),
        }, on_conflict="cache_key").execute()
    except Exception as e:
        logging.warning(f"[Trending Topics Cache] Save failed: {e}")

    return {"topics": final_topics, "cached": False}


async def discover_trending_posts(
    account_id: str,
    region: str = "ID",
    category: str = "all",
    query: str = "",
    limit: int = 20,
    force_refresh: bool = False,
    cache_only: bool = False,
) -> dict:
    db = get_supabase()
    acc = _get_account_guard(db, account_id)
    token = acc["_token"]
    own_username = acc.get("username") or ""

    norm_region = (region or "ID").upper()
    norm_cat = (category or "all").lower()
    clean_q = (query or "").strip()
    cache_key = f"v1:{norm_region}:{norm_cat}:{clean_q.lower()}:{limit}"
    now = datetime.now(timezone.utc)

    if cache_only:
        latest_q = (
            db.schema("threads")
            .from_("trending_cache")
            .select("payload, fetched_at")
            .order("fetched_at", desc=True)
            .limit(1)
        )
        if clean_q or norm_cat != "all" or norm_region != "ID":
            latest_q = (
                db.schema("threads")
                .from_("trending_cache")
                .select("payload, fetched_at")
                .eq("cache_key", cache_key)
                .limit(1)
            )
        cached_any = latest_q.execute()
        if cached_any.data:
            row = cached_any.data[0]
            filtered = _enrich_and_filter_posts(db, account_id, own_username, row.get("payload") or [])
            return {"posts": filtered, "cached": True, "fetched_at": row.get("fetched_at")}
        return {"posts": [], "cached": True, "fetched_at": None}

    if not force_refresh:
        cached = (
            db.schema("threads")
            .from_("trending_cache")
            .select("payload, fetched_at, expires_at")
            .eq("cache_key", cache_key)
            .gt("expires_at", now.isoformat())
            .limit(1)
            .execute()
        )
        if cached.data:
            row = cached.data[0]
            filtered = _enrich_and_filter_posts(db, account_id, own_username, row.get("payload") or [])
            return {"posts": filtered, "cached": True, "fetched_at": row.get("fetched_at")}

    search_terms = [clean_q] if clean_q else CATEGORY_SEEDS.get(norm_cat, CATEGORY_SEEDS["all"])[:2]
    region_suffix = (
        f" {REGION_HINTS[norm_region]}"
        if norm_region == "ID" and clean_q and "indonesia" not in clean_q.lower()
        else ""
    )

    seen_ids = set()
    collected = []

    async with httpx.AsyncClient(timeout=20.0) as client:
        for term in search_terms:
            q_param = f"{term}{region_suffix}".strip()
            url = "https://graph.threads.net/v1.0/keyword_search"
            params = {
                "q": q_param,
                "search_type": "TOP",
                "fields": "id,text,username,timestamp,permalink,media_type,media_url",
                "access_token": token,
            }
            try:
                res = await client.get(url, params=params)
                if res.status_code != 200:
                    logging.warning(f"[Trending Search] Meta status {res.status_code}: {res.text[:200]}")
                    continue
                items = res.json().get("data") or []
                for item in items:
                    mid = item.get("id")
                    if not mid or mid in seen_ids:
                        continue
                    seen_ids.add(mid)
                    collected.append({
                        "id": mid,
                        "text": item.get("text") or "",
                        "username": item.get("username") or "creator",
                        "timestamp": item.get("timestamp") or "",
                        "permalink": item.get("permalink") or "",
                        "media_type": item.get("media_type") or "TEXT",
                        "media_url": item.get("media_url") or "",
                        "topic_tag": term,
                        "region": norm_region,
                        "category": norm_cat,
                    })
                    if len(collected) >= limit:
                        break
            except Exception as e:
                logging.error(f"[Trending Search] Error for '{q_param}': {e}")
            if len(collected) >= limit:
                break

    expires_at = (now + timedelta(minutes=60)).isoformat()
    try:
        db.schema("threads").from_("trending_cache").upsert({
            "cache_key": cache_key,
            "region": norm_region,
            "category": norm_cat,
            "query_text": clean_q,
            "payload": collected,
            "fetched_at": now.isoformat(),
            "expires_at": expires_at,
        }, on_conflict="cache_key").execute()
    except Exception as e:
        logging.warning(f"[Trending Cache] Failed to save cache: {e}")

    filtered = _enrich_and_filter_posts(db, account_id, own_username, collected)
    return {"posts": filtered, "cached": False, "fetched_at": now.isoformat()}


async def inspect_creator_profile(account_id: str, username: str) -> dict:
    db = get_supabase()
    acc = _get_account_guard(db, account_id)
    token = acc["_token"]
    clean_user = (username or "").lstrip("@").strip()
    if not clean_user:
        raise ValueError("Username is required")

    own_user = (acc.get("username") or "").lstrip("@").strip().lower()
    threads_url = f"https://www.threads.net/@{clean_user}"

    async with httpx.AsyncClient(timeout=15.0) as client:
        if own_user and clean_user.lower() == own_user:
            res = await client.get(
                "https://graph.threads.net/v1.0/me",
                params={
                    "fields": "username,name,threads_profile_picture_url,threads_biography,followers_count",
                    "access_token": token,
                },
            )
            if res.status_code == 200:
                data = res.json()
                return {
                    "username": data.get("username") or clean_user,
                    "name": data.get("name") or clean_user,
                    "avatar_url": data.get("threads_profile_picture_url") or "",
                    "bio": data.get("threads_biography") or "",
                    "followers_count": data.get("followers_count"),
                    "threads_url": threads_url,
                    "limited": False,
                }

        res = await client.get(
            "https://graph.threads.net/v1.0/profile_discovery",
            params={
                "username": clean_user,
                "fields": "username,name,threads_profile_picture_url,threads_biography,followers_count",
                "access_token": token,
            },
        )
        if res.status_code == 200:
            data = res.json()
            return {
                "username": data.get("username") or clean_user,
                "name": data.get("name") or clean_user,
                "avatar_url": data.get("threads_profile_picture_url") or "",
                "bio": data.get("threads_biography") or "",
                "followers_count": data.get("followers_count"),
                "threads_url": threads_url,
                "limited": False,
            }

    return {
        "username": clean_user,
        "name": f"@{clean_user}",
        "avatar_url": "",
        "bio": "",
        "followers_count": None,
        "threads_url": threads_url,
        "limited": True,
    }


async def generate_outreach_reply_draft(
    account_id: str,
    target_text: str,
    target_username: str = "creator",
    reply_style: str = "insight",
    provider: str = None,
    model_name: str = None,
) -> str:
    db = get_supabase()
    acc = _get_account_guard(db, account_id)
    chosen_provider = provider or acc.get("ai_provider") or "groq"
    style_hint = STYLE_PROMPTS.get(reply_style, STYLE_PROMPTS["insight"])
    tone_prompt = (
        f"{style_hint} Match the language of the target post naturally. "
        "Keep it 1-2 short sentences, authentic, non-spammy, and do not force links or promotions unless naturally relevant."
    )
    draft = await generate_rag_reply(
        account_id=account_id,
        user_comment=target_text or "Share a thoughtful perspective on this post.",
        post_text=target_text or "",
        author_username=target_username or "creator",
        provider=chosen_provider,
        model_name=model_name,
        tone_prompt=tone_prompt,
    )
    if not draft:
        raise ValueError("Unable to generate AI reply (check AI credits or API key)")
    return draft.strip()


async def send_outreach_comment(
    account_id: str,
    target_media_id: str,
    reply_text: str,
    target_username: str = "",
    target_text: str = "",
    target_permalink: str = "",
    campaign_id: str = None,
    mode: str = "manual",
) -> dict:
    db = get_supabase()
    _get_account_guard(db, account_id)

    clean_text = (reply_text or "").strip()
    if not target_media_id or not clean_text:
        raise ValueError("target_media_id and reply_text are required")

    if _is_already_commented(db, account_id, target_media_id):
        raise ValueError("This post has already been commented on by this account")

    published_id = await publish_reply_to_threads(account_id, target_media_id, clean_text)

    row_payload = {
        "account_id": account_id,
        "campaign_id": campaign_id,
        "mode": mode,
        "target_media_id": target_media_id,
        "target_username": target_username,
        "target_text": (target_text or "")[:1000],
        "target_permalink": target_permalink,
        "reply_threads_id": published_id,
        "reply_text": clean_text,
        "status": "sent",
        "error_message": None,
    }

    try:
        res = (
            db.schema("threads")
            .from_("outreach_logs")
            .upsert(row_payload, on_conflict="account_id,target_media_id")
            .execute()
        )
        saved = res.data[0] if res.data else row_payload
    except Exception as e:
        logging.error(f"[Outreach Log] Upsert warning: {e}")
        saved = row_payload

    return {"reply_threads_id": published_id, "log": saved}


async def run_auto_comment_cycle(account_id: str) -> dict:
    db = get_supabase()
    acc = _get_account_guard(db, account_id)
    now = datetime.now(timezone.utc)

    camp_res = (
        db.schema("threads")
        .from_("outreach_campaigns")
        .select("*")
        .eq("account_id", account_id)
        .eq("is_active", True)
        .limit(5)
        .execute()
    )
    campaigns = camp_res.data or []
    if not campaigns:
        return {"processed": 0, "sent": 0, "skipped": 0, "reason": "No active campaign"}

    sent_count = 0
    skipped_count = 0

    for camp in campaigns:
        max_per_hour = max(1, min(int(camp.get("max_per_hour") or 3), 10))
        already_hour = _count_sent_last_hour(db, account_id)
        remaining_quota = max_per_hour - already_hour
        if remaining_quota <= 0:
            skipped_count += 1
            continue

        keywords = camp.get("keywords") or []
        query_seed = random.choice(keywords) if keywords else ""
        disc = await discover_trending_posts(
            account_id=account_id,
            region=camp.get("region") or "ID",
            category=camp.get("category") or "all",
            query=query_seed,
            limit=10,
            force_refresh=False,
        )

        for post in disc.get("posts") or []:
            if sent_count >= remaining_quota or _count_sent_last_hour(db, account_id) >= max_per_hour:
                break
            mid = post.get("id")
            post_body = (post.get("text") or "").strip()
            author = post.get("username") or "creator"
            if not mid or len(post_body) < 15 or author.lower() == (acc.get("username") or "").lower():
                skipped_count += 1
                continue
            if _is_already_commented(db, account_id, mid):
                skipped_count += 1
                continue

            try:
                draft = await generate_outreach_reply_draft(
                    account_id=account_id,
                    target_text=post_body,
                    target_username=author,
                    reply_style=camp.get("reply_style") or "insight",
                    provider=acc.get("ai_provider") or "groq",
                )
                await send_outreach_comment(
                    account_id=account_id,
                    target_media_id=mid,
                    reply_text=draft,
                    target_username=author,
                    target_text=post_body,
                    target_permalink=post.get("permalink") or "",
                    campaign_id=camp.get("id"),
                    mode="auto",
                )
                sent_count += 1
                await asyncio.sleep(2)
            except Exception as e:
                logging.warning(f"[Auto Outreach] Skip post {mid}: {e}")
                skipped_count += 1

        try:
            db.schema("threads").from_("outreach_campaigns").update({
                "last_run_at": now.isoformat(),
                "updated_at": now.isoformat(),
            }).eq("id", camp["id"]).execute()
        except Exception:
            pass

    return {"processed": sent_count + skipped_count, "sent": sent_count, "skipped": skipped_count}
