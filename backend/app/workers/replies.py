import os
import asyncio
import logging
import time
import httpx
from datetime import datetime, timezone
from supabase import create_client, Client
from app.services.leads import analyze_and_notify_lead
from app.services.comment_classifier import classify_comment
from app.services.comment_templates import pick_template, has_template
from app.services.auto_reply import generate_rag_reply


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
    return {
        "new_replies": 0,
        "template": 0,
        "llm": 0,
        "skipped": 0,
        "by_category": {},
    }


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
        f"?fields=id,text,timestamp,permalink&limit={MAX_POSTS_TO_FETCH}"
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
        db.schema("threads")
        .from_("posts")
        .select("threads_media_id")
        .eq("account_id", acc_id)
        .in_("threads_media_id", media_ids)
        .execute()
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
    token: str, acc_username: str, is_enabled: bool, reply_mode: str
) -> dict:
    """
    Fetch replies dari Meta untuk satu post.
    Pakai batch check dan bulk insert untuk minimize round trip ke Supabase.
    """
    stats = empty_stats()

    url = (
        f"https://graph.threads.net/v1.0/{media_id}/replies"
        f"?fields=id,text,username,timestamp&limit={MAX_REPLIES_PER_POST}"
        f"&access_token={token}"
    )

    try:
        res = await client.get(url, timeout=15.0)
        if res.status_code != 200:
            return stats
        data = res.json().get("data", [])
    except Exception:
        return stats

    if not data:
        return stats

    meta_ids = [r.get("id") for r in data if r.get("id")]
    if not meta_ids:
        return stats

    # Batch check existing replies (1 query instead of N)
    try:
        exist_res = (
            db.schema("threads")
            .from_("replies")
            .select("threads_reply_id")
            .in_("threads_reply_id", meta_ids)
            .execute()
        )
        existing_set = {r["threads_reply_id"] for r in (exist_res.data or [])}
    except Exception as e:
        logging.error(f"[Batch Check Error] {str(e)}")
        return stats

    # Filter hanya reply baru dan siapkan payload bulk insert
    new_replies_payload = []
    new_replies_meta = []

    for reply in data:
        reply_id = reply.get("id")
        if not reply_id or reply_id in existing_set:
            continue

        text = reply.get("text", "") or ""
        author_username = reply.get("username", "unknown")
        timestamp = reply.get("timestamp")

        classification = classify_comment(text)
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
        })

    if not new_replies_payload:
        return stats

    # Bulk insert (1 query instead of N)
    try:
        insert_res = (
            db.schema("threads")
            .from_("replies")
            .insert(new_replies_payload)
            .execute()
        )
        inserted_by_meta_id = {
            row["threads_reply_id"]: row
            for row in (insert_res.data or [])
        }
    except Exception as e:
        logging.error(f"[Bulk Insert Error] {str(e)}")
        return stats

    # Proses AI draft per reply baru
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
        category = classification["category"]

        if is_own_comment:
            stats["skipped"] += 1
            continue

        if not is_enabled:
            stats["skipped"] += 1
            continue

        if is_lead:
            await analyze_and_notify_lead(acc_id, author_username, text)

        action = CATEGORY_ACTION.get(category, "skip")
        if action == "skip":
            stats["skipped"] += 1
            continue

        draft_text = None
        llm_meta = {
            "category": category,
            "is_lead": is_lead,
            "matched_signals": classification["matched_signals"],
            "confidence": classification["confidence"],
            "incoming_comment": text,
            "username": author_username,
        }

        if action == "template":
            if not has_template(category):
                stats["skipped"] += 1
                continue
            draft_text = pick_template(category)
            llm_meta["mode"] = "template"
            stats["template"] += 1

        elif action == "llm":
            try:
                draft_text = await generate_rag_reply(
                    account_id=acc_id,
                    user_comment=text,
                    author_username=author_username,
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

        try:
            db.schema("threads").from_("auto_reply_logs").insert({
                "account_id": acc_id,
                "reply_id": reply_db_id,
                "status": "pending_review" if reply_mode == "review" else "approved",
                "generated_text": draft_text,
                "final_text": draft_text,
                "llm_meta": llm_meta,
            }).execute()
        except Exception as log_err:
            logging.error(f"[Log Insert Error]: {str(log_err)}")

    return stats


async def sync_post_with_semaphore(
    sem: asyncio.Semaphore,
    db, client, acc_id: str, post_db_id: str, media_id: str,
    token: str, acc_username: str, is_enabled: bool, reply_mode: str
) -> dict:
    async with sem:
        try:
            return await sync_replies_for_post(
                db, client, acc_id, post_db_id, media_id,
                token, acc_username, is_enabled, reply_mode
            )
        except Exception as e:
            logging.error(f"[Parallel Sync] Post {media_id} error: {str(e)}")
            return empty_stats()


async def process_account(db, client, acc: dict) -> dict:
    account_stats = {
        "new_posts": 0,
        **empty_stats(),
    }

    acc_id = acc["id"]
    acc_username = acc.get("username", "")
    token = acc.get("settings", {}).get("access_token")
    if not token:
        return account_stats

    new_posts = await sync_posts_from_meta(db, client, acc_id, token)
    account_stats["new_posts"] = new_posts

    settings_res = (
        db.schema("threads")
        .from_("auto_reply_settings")
        .select("*")
        .eq("account_id", acc_id)
        .limit(1)
        .execute()
    )
    auto_settings = settings_res.data[0] if settings_res.data else {}
    is_enabled = auto_settings.get("enabled", True)
    reply_mode = auto_settings.get("mode", "review")

    from datetime import datetime, timezone, timedelta
    cutoff = (datetime.now(timezone.utc) - timedelta(days=MAX_POST_AGE_DAYS)).isoformat()

    posts_res = (
        db.schema("threads")
        .from_("posts")
        .select("id, threads_media_id")
        .eq("account_id", acc_id)
        .gte("posted_at", cutoff)
        .order("posted_at", desc=True)
        .limit(MAX_POSTS_TO_FETCH)
        .execute()
    )
    posts = posts_res.data or []

    valid_posts = [p for p in posts if p.get("threads_media_id")]
    if not valid_posts:
        return account_stats

    sem = asyncio.Semaphore(SYNC_CONCURRENCY)
    tasks = [
        sync_post_with_semaphore(
            sem, db, client, acc_id, p["id"], p["threads_media_id"],
            token, acc_username, is_enabled, reply_mode
        )
        for p in valid_posts
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    for r in results:
        if isinstance(r, dict):
            merge_stats(account_stats, r)

    return account_stats


async def fetch_and_process_replies():
    started = time.time()
    db = get_supabase()

    accounts_res = (
        db.schema("threads")
        .from_("threads_accounts")
        .select("id, settings, username")
        .eq("connection_status", "connected")
        .execute()
    )
    accounts = accounts_res.data or []

    total = {
        "new_posts": 0,
        **empty_stats(),
    }

    async with httpx.AsyncClient() as client:
        for acc in accounts:
            acc_stats = await process_account(db, client, acc)
            total["new_posts"] += acc_stats.get("new_posts", 0)
            merge_stats(total, acc_stats)

    elapsed = round(time.time() - started, 2)

    logging.info(
        f"[Worker Replies Summary] "
        f"new_posts={total['new_posts']} "
        f"new_replies={total['new_replies']} "
        f"template={total['template']} "
        f"llm={total['llm']} "
        f"skipped={total['skipped']} "
        f"by_category={total['by_category']} "
        f"elapsed={elapsed}s"
    )


async def reply_worker_loop():
    while True:
        try:
            await fetch_and_process_replies()
        except Exception as e:
            logging.error(f"[Worker Replies Loop] Error: {str(e)}")
        await asyncio.sleep(600)
