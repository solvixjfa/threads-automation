import os
import asyncio
import logging
import time
import httpx
from datetime import datetime, timezone, timedelta
from supabase import create_client, Client
from app.services.leads import analyze_and_notify_lead
from app.services.comment_classifier import classify_comment
from app.services.comment_templates import (
    pick_template, has_template, is_category_enabled, get_custom_templates,
)
from app.services.auto_reply import generate_rag_reply, publish_reply_to_threads

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

def get_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

CATEGORY_ACTION = {
    "question": "llm",
    "praise": "template",
    "neutral": "template",
    "spam": "skip",
    "toxic": "skip",
    "unclassified": "skip",
}

MAX_POSTS_TO_FETCH = 15
MAX_POST_AGE_DAYS = 7
MAX_REPLIES_PER_POST = 50
SYNC_CONCURRENCY = 8

def empty_stats() -> dict:
    return {"new_replies": 0, "template": 0, "llm": 0, "skipped": 0, "by_category": {}}

def merge_stats(target: dict, source: dict):
    target["new_replies"] += source.get("new_replies", 0)
    target["template"] += source.get("template", 0)
    target["llm"] += source.get("llm", 0)
    target["skipped"] += source.get("skipped", 0)
    for cat, n in (source.get("by_category") or {}).items():
        target["by_category"][cat] = target["by_category"].get(cat, 0) + n


async def sync_posts_from_meta(db, client, acc_id: str, token: str) -> int:
    url = (
        "https://graph.threads.net/v1.0/me/threads"
        f"?fields=id,text,timestamp,permalink,media_type,media_url&limit={MAX_POSTS_TO_FETCH}"
        f"&access_token={token}"
    )
    try:
        res = await client.get(url, timeout=15.0)
        if res.status_code != 200:
            logging.warning(f"[Sync Posts] Meta API status {res.status_code}: {res.text[:200]}")
            return 0
        data = res.json().get("data", [])
    except Exception as e:
        logging.error(f"[Sync Posts] Error fetching posts: {str(e)}")
        return 0

    if not data:
        return 0

    media_ids = [p.get("id") for p in data if p.get("id")]
    if not media_ids:
        return 0

    exist_res = (
        db.schema("threads").from_("posts").select("threads_media_id")
        .eq("account_id", acc_id).in_("threads_media_id", media_ids).execute()
    )
    existing_ids = {row["threads_media_id"] for row in (exist_res.data or [])}

    new_count = 0
    for p in data:
        media_id = p.get("id")
        if not media_id or media_id in existing_ids:
            continue
        ts = p.get("timestamp")
        if not ts:
            continue
        try:
            db.schema("threads").from_("posts").insert({
                "account_id": acc_id,
                "threads_media_id": media_id,
                "text": p.get("text", "") or "",
                "permalink": p.get("permalink"),
                "posted_at": ts,
                "source": "meta_sync",
            }).execute()
            new_count += 1
        except Exception as e:
            logging.error(f"[Sync Posts] Insert error for {media_id}: {str(e)}")

    return new_count


async def sync_replies_for_post(
    db, client, acc_id: str, post_db_id: str, media_id: str,
    token: str, acc_username: str, is_enabled: bool, reply_mode: str,
    category_rules: dict = None, ai_provider: str = "groq", auto_settings: dict = None
) -> dict:
    stats = empty_stats()

    url = (
        f"https://graph.threads.net/v1.0/{media_id}/replies"
        f"?fields=id,text,username,timestamp,permalink,media_type,media_url&limit={MAX_REPLIES_PER_POST}"
        f"&access_token={token}"
    )
    try:
        res = await client.get(url, timeout=15.0)
        if res.status_code != 200:
            return stats
        data = res.json().get("data", [])
    except Exception as e:
        logging.error(f"[Sync Replies] Error fetching for {media_id}: {str(e)}")
        return stats

    if not data:
        return stats

    meta_ids = [r.get("id") for r in data if r.get("id")]
    if not meta_ids:
        return stats

    try:
        exist_res = (
            db.schema("threads").from_("replies").select("threads_reply_id")
            .in_("threads_reply_id", meta_ids).execute()
        )
        existing_set = {r["threads_reply_id"] for r in (exist_res.data or [])}
    except Exception as e:
        logging.error(f"[Batch Check Error] {str(e)}")
        return stats

    new_replies_payload = []
    new_replies_meta = []

    for reply in data:
        reply_id = reply.get("id")
        if not reply_id or reply_id in existing_set:
            continue

        text = reply.get("text", "") or ""
        author_username = reply.get("username", "unknown")
        timestamp = reply.get("timestamp")
        media_url = reply.get("media_url")
        media_type = reply.get("media_type")
        has_media = bool(media_url) or (media_type in ["IMAGE", "VIDEO", "CAROUSEL_ALBUM"])

        classification = classify_comment(text, has_media=has_media)
        category = classification["category"]
        is_lead = classification.get("is_lead", False)
        is_own_comment = author_username == acc_username

        stats["new_replies"] += 1
        stats["by_category"][category] = stats["by_category"].get(category, 0) + 1

        new_replies_payload.append({
            "account_id": acc_id,
            "post_id": post_db_id,
            "threads_reply_id": reply_id,
            "author_username": author_username,
            "text": text,
            "is_lead": is_lead,
            "classification": category,
            "is_own": is_own_comment,
            "replied_at": timestamp,
            "media_url": media_url,
            "raw": reply,
            "processed_at": datetime.now(timezone.utc).isoformat(),
        })
        new_replies_meta.append({
            "reply_id": reply_id,
            "classification": classification,
            "text": text,
            "author_username": author_username,
            "is_own": is_own_comment,
            "is_lead": is_lead,
            "has_media": has_media,
        })

    if not new_replies_payload:
        return stats

    try:
        insert_res = db.schema("threads").from_("replies").insert(new_replies_payload).execute()
        inserted_by_meta_id = {row["threads_reply_id"]: row for row in (insert_res.data or [])}
    except Exception as e:
        logging.error(f"[Bulk Insert Error] {str(e)}")
        return stats

    for meta_item in new_replies_meta:
        reply_db = inserted_by_meta_id.get(meta_item["reply_id"])
        if not reply_db:
            continue

        reply_db_id = reply_db["id"]
        classification = meta_item["classification"]
        text = meta_item["text"]
        author_username = meta_item["author_username"]
        is_own_comment = meta_item["is_own"]
        is_lead = meta_item["is_lead"]
        has_media = meta_item["has_media"]
        category = classification["category"]

        if is_own_comment or not is_enabled:
            stats["skipped"] += 1
            continue

        if category_rules and not is_category_enabled(category_rules, category):
            stats["skipped"] += 1
            continue

        if is_lead:
            try:
                await analyze_and_notify_lead(acc_id, author_username, text)
            except Exception as e:
                logging.error(f"[Lead Error] {str(e)}")

        # BACA DARI SETTINGAN USER (UI)
        rule = category_rules.get(category, {}) if category_rules else {}
        action = rule.get("action", CATEGORY_ACTION.get(category, "skip"))
        if not rule.get("enabled", True):
            action = "skip"

        if action == "skip":
            stats["skipped"] += 1
            continue

        # Rate Limit per hour
        max_per_hour = auto_settings.get("max_per_hour", 10) if auto_settings else 10
        if max_per_hour > 0:
            one_hour_ago = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
            try:
                limit_check = db.schema("threads").from_("auto_reply_logs").select("id", count="exact").eq("account_id", acc_id).eq("status", "sent").gte("created_at", one_hour_ago).execute()
                if limit_check.count >= max_per_hour:
                    logging.warning(f"[Rate Limit] Max replies/hour reached.")
                    stats["skipped"] += 1
                    continue
            except Exception as e:
                logging.error(f"[Rate Limit Check Error] {str(e)}")

        draft_text = None
        llm_meta = {
            "category": category, "is_lead": is_lead,
            "matched_signals": classification["matched_signals"],
            "confidence": classification["confidence"], "incoming_comment": text,
            "username": author_username, "has_media": has_media,
        }

        if action == "template":
            custom_tpls = get_custom_templates(category_rules or {}, category)
            if not has_template(category, custom_tpls):
                stats["skipped"] += 1
                continue
            draft_text = pick_template(category, custom_tpls)
            llm_meta["mode"] = "template"
            stats["template"] += 1

        elif action == "llm":
            ai_input = text.strip() if text.strip() else "[User sent an image without any text...]"
            try:
                draft_text = await generate_rag_reply(
                    account_id=acc_id, user_comment=ai_input,
                    author_username=author_username, provider=ai_provider,
                )
                llm_meta["mode"] = "llm"
                stats["llm"] += 1
            except Exception as ai_err:
                logging.error(f"[AI Draft Error]: {str(ai_err)}")
                stats["skipped"] += 1
                continue

        if not draft_text:
            stats["skipped"] += 1
            continue

        log_status = "pending_review"
        if reply_mode == "auto":
            try:
                await asyncio.sleep(2)
                await publish_reply_to_threads(acc_id, meta_item["reply_id"], draft_text)
                log_status = "sent"
            except Exception as pub_err:
                logging.error(f"[Auto-Publish Failed]: {str(pub_err)}")
                log_status = "pending_review"
                llm_meta["auto_publish_error"] = str(pub_err)

        try:
            db.schema("threads").from_("auto_reply_logs").insert({
                "account_id": acc_id, "reply_id": reply_db_id, "status": log_status,
                "generated_text": draft_text, "final_text": draft_text, "llm_meta": llm_meta,
            }).execute()
        except Exception as log_err:
            logging.error(f"[Log Insert Error]: {str(log_err)}")

    return stats


async def sync_post_with_semaphore(
    sem: asyncio.Semaphore, db, client, acc_id: str, post_db_id: str,
    media_id: str, token: str, acc_username: str, is_enabled: bool,
    reply_mode: str, category_rules: dict = None, ai_provider: str = "groq", auto_settings: dict = None
) -> dict:
    async with sem:
        try:
            return await sync_replies_for_post(
                db, client, acc_id, post_db_id, media_id,
                token, acc_username, is_enabled, reply_mode, category_rules, ai_provider, auto_settings
            )
        except Exception as e:
            logging.error(f"[Parallel Sync] Post {media_id} error: {str(e)}")
            return empty_stats()


async def process_account(db, client, acc: dict) -> dict:
    account_stats = {"new_posts": 0, **empty_stats()}

    acc_id = acc["id"]
    acc_username = acc.get("username", "")
    token = acc.get("settings", {}).get("access_token")
    if not token:
        return account_stats

    ai_provider = acc.get("ai_provider") or "groq"

    new_posts = await sync_posts_from_meta(db, client, acc_id, token)
    account_stats["new_posts"] = new_posts

    settings_res = (
        db.schema("threads").from_("auto_reply_settings").select("*")
        .eq("account_id", acc_id).limit(1).execute()
    )
    auto_settings = settings_res.data[0] if settings_res.data else {}
    is_enabled = auto_settings.get("enabled", True)
    reply_mode = auto_settings.get("mode", "review")
    category_rules = auto_settings.get("rules") or {}

    cutoff = (datetime.now(timezone.utc) - timedelta(days=MAX_POST_AGE_DAYS)).isoformat()
    posts_res = (
        db.schema("threads").from_("posts")
        .select("id, threads_media_id")
        .eq("account_id", acc_id)
        .gte("posted_at", cutoff)
        .order("posted_at", desc=True)
        .limit(MAX_POSTS_TO_FETCH)
        .execute()
    )
    posts = posts_res.data or []
    valid_posts = [p for p in posts if p.get("threads_media_id") and p.get("id")]
    if not valid_posts:
        return account_stats

    sem = asyncio.Semaphore(SYNC_CONCURRENCY)
    tasks = [
        sync_post_with_semaphore(
            sem, db, client, acc_id, p["id"], p["threads_media_id"],
            token, acc_username, is_enabled, reply_mode, category_rules, ai_provider, auto_settings
        ) for p in valid_posts
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)
    for r in results:
        if isinstance(r, dict):
            merge_stats(account_stats, r)
        elif isinstance(r, Exception):
            logging.error(f"[Gather Exception] {str(r)}")

    return account_stats


async def fetch_and_process_replies():
    started = time.time()
    db = get_supabase()

    accounts_res = (
        db.schema("threads").from_("threads_accounts")
        .select("id, settings, username, ai_provider, custom_gemini_key, custom_groq_key, ai_credits")
        .eq("connection_status", "connected")
        .execute()
    )
    accounts = accounts_res.data or []

    total = {"new_posts": 0, **empty_stats()}

    async with httpx.AsyncClient() as client:
        for acc in accounts:
            try:
                acc_stats = await process_account(db, client, acc)
                total["new_posts"] += acc_stats.get("new_posts", 0)
                merge_stats(total, acc_stats)
            except Exception as e:
                logging.error(f"[Process Account Error] {acc.get('id')}: {str(e)}")

    elapsed = round(time.time() - started, 2)
    logging.info(
        f"[Worker Replies Summary] new_posts={total['new_posts']} new_replies={total['new_replies']} "
        f"template={total['template']} llm={total['llm']} skipped={total['skipped']} "
        f"by_category={total['by_category']} elapsed={elapsed}s"
    )


async def reply_worker_loop():
    while True:
        try:
            await fetch_and_process_replies()
        except Exception as e:
            logging.error(f"[Worker Replies Loop] Error: {str(e)}")
        await asyncio.sleep(600)
