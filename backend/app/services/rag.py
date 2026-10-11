import os
import logging
from google import genai
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")

def get_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def get_available_embedding_models() -> list[str]:
    client = genai.Client(api_key=GEMINI_KEY)
    found = []
    try:
        for m in client.models.list():
            methods = getattr(m, 'supported_generation_methods', []) or []
            if 'embedContent' in methods or 'embed_content' in methods:
                name = m.name.replace("models/", "") if hasattr(m, 'name') else str(m)
                found.append(name)
    except Exception as e:
        logging.error(f"Error listing models: {str(e)}")
    return found

def generate_embedding(text: str) -> list[float]:
    client = genai.Client(api_key=GEMINI_KEY)
    
    # 1. Coba dari Environment Variable jika di-set di Railway
    env_model = os.getenv("EMBEDDING_MODEL")
    if env_model:
        try:
            res = client.models.embed_content(model=env_model, contents=text)
            return res.embedding.values
        except Exception as e:
            logging.warning(f"ENV EMBEDDING_MODEL ({env_model}) failed: {str(e)}")

    # 2. Auto-discover model embedding yang diizinkan oleh API Key
    discovered = get_available_embedding_models()
    for m_name in discovered:
        try:
            res = client.models.embed_content(model=m_name, contents=text)
            return res.embedding.values
        except Exception as e:
            logging.warning(f"Discovered embedding model {m_name} failed: {str(e)}")
            continue

    # 3. Fallback manual jika discovery kosong
    for fallback in ["text-embedding-004", "text-embedding-001"]:
        try:
            res = client.models.embed_content(model=fallback, contents=text)
            return res.embedding.values
        except Exception as e:
            logging.warning(f"Fallback {fallback} failed: {str(e)}")
            continue

    raise RuntimeError(f"Gagal generate embedding. Model embedding terdeteksi di API Key: {discovered}")

async def store_knowledge(account_id: str, title: str, content: str, category: str = "general"):
    embedding = generate_embedding(content)
    db = get_supabase()
    
    data = {
        "account_id": account_id,
        "title": title,
        "content": content,
        "category": category,
        "embedding": embedding
    }
    
    res = db.schema("threads").from_("brand_knowledge").insert(data).execute()
    return res.data

async def search_knowledge(account_id: str, query: str, limit: int = 3):
    query_vector = generate_embedding(query)
    db = get_supabase()
    
    res = db.rpc("match_brand_knowledge", {
        "query_embedding": query_vector,
        "match_threshold": 0.5,
        "match_count": limit,
        "p_account_id": account_id
    }).execute()
    
    return res.data or []
