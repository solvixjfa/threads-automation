import os
import asyncio
import logging
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
    "lead": "llm",
    "question": "llm",
    "praise": "template",
    "greeting": "template",
    "other": "template",
    "spam": "skip",
}

MAX_POSTS_TO_FETCH = 30
MAX_REPLIES_PER_POST = 50


async def sync_posts_from_meta(db, client, acc_id: str, token: str) -> int:
    """
    Fetch list post dari /me/threads dan upsert ke tabel posts.
    Return: jumlah post baru yang masuk.
    """
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


async def sync_replies_for_post(db, client, acc_id: str, post_db_id: str, media_id: str, token: str, acc_username: str, is_enabled: bool, reply_mode: str, stats: dict):
    """
    Fetch replies untuk satu post dan proses.
    """
    url = (
        f"https://graph.threads.net/v1.0/{media_id}/replies"
        f"?fields=id,text,username,timestamp&limit={MAX_REPLIES_PER_POST}"
        f"&access_token={token}"
    )

    try:
        res = await client.get(url, timeout=15.0)
        if res.status_code != 200:
            return
        data = res.json().get("data", [])
    except Exception:
        return

    for reply in data:
        reply_id = reply.get("id")
        text = reply.get("text", "") or ""
        author_username = reply.get("username", "unknown")
        timestamp = reply.get("timestamp")

        exist_res = (
            db.schema("threads")
            .from_("replies")
            .select("id")
            .eq("threads_reply_id", reply_id)
            .execute()
        )
        if exist_res.data:
            continue

        stats["new"] += 1
        is_own_comment = author_username == acc_username

        classification = classify_comment(text)
        category = classification["category"]
        stats["by_category"][category] = stats["by_category"].get(category, 0) + 1

        reply_insert = (
            db.schema("threads")
            .from_("replies")
            .insert({
                "account_id": acc_id,
                "post_id": post_db_id,
                "threads_reply_id": reply_id,
                "author_username": author_username,
                "text": text,
                "is_lead": category == "lead",
                "classification": category,
                "is_own": is_own_comment,
                "replied_at": timestamp,
                "raw": reply,
                "processed_at": datetime.now(timezone.utc).isoformat(),
            })
            .execute()
        )
        reply_db_id = reply_insert.data[0]["id"]

        if is_own_comment:
            stats["skipped"] += 1
            continue

        if not is_enabled:
            stats["skipped"] += 1
            continue

        if category == "lead":
            await analyze_and_notify_lead(acc_id, author_username, text)

        action = CATEGORY_ACTION.get(category, "skip")
        if action == "skip":
            stats["skipped"] += 1
            continue

        draft_text = None
        llm_meta = {
            "category": category,
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


async def fetch_and_process_replies():
    db = get_supabase()

    accounts_res = (
        db.schema("threads")
        .from_("threads_accounts")
        .select("id, settings, username")
        .eq("connection_status", "connected")
        .execute()
    )
    accounts = accounts_res.data or []

    stats = {
        "new_posts": 0,
        "new_replies": 0,
        "template": 0,
        "llm": 0,
        "skipped": 0,
        "by_category": {},
    }

    async with httpx.AsyncClient() as client:
        for acc in accounts:
            acc_id = acc["id"]
            acc_username = acc.get("username", "")
            token = acc.get("settings", {}).get("access_token")
            if not token:
                continue

            # Step 1: Sync post dari Meta dulu
            new_posts = await sync_posts_from_meta(db, client, acc_id, token)
            stats["new_posts"] += new_posts

            # Step 2: Ambil post dari DB untuk fetch komen
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

            posts_res = (
                db.schema("threads")
                .from_("posts")
                .select("id, threads_media_id")
                .eq("account_id", acc_id)
                .order("created_at", desc=True)
                .limit(MAX_POSTS_TO_FETCH)
                .execute()
            )
            posts = posts_res.data or []

            for post in posts:
                media_id = post["threads_media_id"]
                post_db_id = post["id"]
                if not media_id:
                    continue

                await sync_replies_for_post(
                    db, client, acc_id, post_db_id, media_id,
                    token, acc_username, is_enabled, reply_mode, stats
                )

    logging.info(
        f"[Worker Replies Summary] "
        f"new_posts={stats['new_posts']} "
        f"new_replies={stats['new_replies']} "
        f"template={stats['template']} "
        f"llm={stats['llm']} "
        f"skipped={stats['skipped']} "
        f"by_category={stats['by_category']}"
    )


async def reply_worker_loop():
    while True:
        try:
            await fetch_and_process_replies()
        except Exception as e:
            logging.error(f"[Worker Replies Loop] Error: {str(e)}")
        await asyncio.sleep(600)
