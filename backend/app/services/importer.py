import os
import time
import httpx
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
                if resp.status_code == 429: # Rate limit Meta
                    time.sleep(5) # Pause & retry
                    continue
                
                resp.raise_for_status()
                data = resp.json()
                
                posts = data.get("data", [])
                for p in posts:
                    db.schema("threads").from_("scheduled_posts").upsert({
                        "account_id": account_id,
                        "threads_media_id": p.get("id"),
                        "text": p.get("text", ""),
                        "status": "published",
                        "posted_at": p.get("timestamp"),
                        "permalink": p.get("permalink")
                    }, on_conflict="threads_media_id").execute()
                    
                    total_imported += 1
                
                # Check pagination cursor
                url = data.get("paging", {}).get("next")
                pages_processed += 1
                
            except Exception as e:
                print(f"Error import batch page {pages_processed}: {str(e)}")
                break
                
    return {"total_imported": total_imported, "pages_processed": pages_processed}
