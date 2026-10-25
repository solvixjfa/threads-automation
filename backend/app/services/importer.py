import os
import asyncio
import httpx
from datetime import datetime, timezone
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

def get_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

async def import_threads_history(account_id: str, access_token: str, max_pages: int = 5):
    db = get_supabase()
    url = f"https://graph.threads.net/v1.0/me/threads?fields=id,media_product_type,text,timestamp,permalink,like_count,views&access_token={access_token}"

    total_imported = 0
    pages_processed = 0

    async with httpx.AsyncClient() as client:
        while url and pages_processed < max_pages:
            try:
                resp = await client.get(url, timeout=30.0)
                if resp.status_code == 429:
                    await asyncio.sleep(5)
                    continue

                resp.raise_for_status()
                data = resp.json()

                posts = data.get("data", [])
                for p in posts:
                    media_id = p.get("id")
                    timestamp = p.get("timestamp")
                    text = p.get("text", "Post Without Text")

                    # 1. Simpan ke tabel posts
                    post_res = db.schema("threads").from_("posts").upsert({
                        "account_id": account_id,
                        "threads_media_id": media_id,
                        "created_at": timestamp
                    }, on_conflict="threads_media_id").execute()

                    # 2. Simpan ke scheduled_posts (FIX: Pakai If/Else biar gak kena error on_conflict)
                    existing_sp = db.schema("threads").from_("scheduled_posts").select("id").eq("published_media_id", media_id).execute()
                    
                    if not existing_sp.data:
                        db.schema("threads").from_("scheduled_posts").insert({
                            "account_id": account_id,
                            "published_media_id": media_id,
                            "text": text,
                            "status": "published",
                            "scheduled_for": timestamp,
                            "sequence_number": 0
                        }).execute()
                    else:
                        db.schema("threads").from_("scheduled_posts").update({
                            "text": text
                        }).eq("published_media_id", media_id).execute()

                    # 3. Tarik Metrik
                    try:
                        insight_url = f"https://graph.threads.net/v1.0/{media_id}/insights?metric=views,likes,replies,reposts,quotes&access_token={access_token}"
                        ins_resp = await client.get(insight_url, timeout=15.0)
                        if ins_resp.status_code == 200:
                            ins_data = ins_resp.json()
                            if "data" in ins_data:
                                metrics = {item["name"]: item["values"][0]["value"] for item in ins_data["data"] if "values" in item}
                                
                                if post_res.data:
                                    post_id = post_res.data[0]["id"]
                                    db.schema("threads").from_("post_metrics").delete().eq("post_id", post_id).eq("snapshot_label", "latest").execute()
                                    db.schema("threads").from_("post_metrics").insert({
                                        "post_id": post_id,
                                        "snapshot_label": "latest",
                                        "views": metrics.get("views", 0),
                                        "likes": metrics.get("likes", 0),
                                        "replies": metrics.get("replies", 0),
                                        "reposts": metrics.get("reposts", 0),
                                        "quotes": metrics.get("quotes", 0),
                                        "captured_at": datetime.now(timezone.utc).isoformat()
                                    }).execute()
                    except Exception as e:
                        print(f"[Importer] Gagal narik metrik {media_id}: {e}")

                    total_imported += 1

                url = data.get("paging", {}).get("next")
                pages_processed += 1

            except Exception as e:
                print(f"Error import batch page {pages_processed}: {str(e)}")
                break

    return {"total_imported": total_imported, "pages_processed": pages_processed}
