import os
import logging
from google import genai
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")

def get_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def get_all_raw_models() -> list[str]:
    client = genai.Client(api_key=GEMINI_KEY)
    models = []
    try:
        for m in client.models.list():
            name = getattr(m, 'name', str(m))
            models.append(name)
    except Exception as e:
        logging.error(f"Failed to list models: {str(e)}")
    return models

def generate_embedding(text: str) -> list[float]:
    client = genai.Client(api_key=GEMINI_KEY)
    
    # 1. Cek ENV
    env_model = os.getenv("EMBEDDING_MODEL")
    if env_model:
        try:
            res = client.models.embed_content(model=env_model, contents=text)
            return res.embedding.values
        except Exception as e:
            logging.warning(f"ENV EMBEDDING_MODEL ({env_model}) failed: {str(e)}")

    # 2. Kandidat model embedding standar & alias
    candidates = [
        "text-embedding-004",
        "models/text-embedding-004",
        "text-embedding-001",
        "models/text-embedding-001",
        "embedding-001"
    ]
    
    # Tambahkan semua model hasil list dari API Key yang mengandung kata 'embed'
    raw_models = get_all_raw_models()
    for m in raw_models:
        clean_name = m.replace("models/", "")
        if "embed" in clean_name.lower() or "embedding" in clean_name.lower():
            if clean_name not in candidates:
                candidates.append(clean_name)
            if m not in candidates:
                candidates.append(m)

    errors = []
    for model_name in candidates:
        try:
            res = client.models.embed_content(model=model_name, contents=text)
            return res.embedding.values
        except Exception as e:
            errors.append(f"{model_name}: {str(e)}")
            continue

    raise RuntimeError(f"Gagal generate embedding. Detail error: {errors} | Raw models di API Key: {raw_models}")

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
