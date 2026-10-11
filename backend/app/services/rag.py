import os
from google import genai
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")

def get_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def generate_embedding(text: str) -> list[float]:
    client = genai.Client(api_key=GEMINI_KEY)
    
    candidates = [
        os.getenv("EMBEDDING_MODEL", "text-embedding-004"),
        "text-embedding-004",
        "text-embedding-001",
        "models/text-embedding-004"
    ]
    
    seen = set()
    models_to_try = [m for m in candidates if not (m in seen or seen.add(m))]
    
    last_exception = None
    for model_name in models_to_try:
        try:
            response = client.models.embed_content(
                model=model_name,
                contents=text
            )
            return response.embedding.values
        except Exception as e:
            last_exception = e
            continue
            
    if last_exception:
        raise last_exception
    raise RuntimeError("Gagal menghasilkan embedding: tidak ada model yang merespons.")

async def store_knowledge(account_id: str, title: str, content: str):
    embedding = generate_embedding(content)
    db = get_supabase()
    
    data = {
        "account_id": account_id,
        "title": title,
        "content": content,
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
