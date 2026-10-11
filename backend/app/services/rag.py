import os
import logging
from google import genai
from google.genai import types
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")

def get_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def extract_vector(response) -> list[float]:
    if hasattr(response, 'embeddings') and response.embeddings:
        first = response.embeddings[0]
        if hasattr(first, 'values'):
            return list(first.values)
        if isinstance(first, (list, tuple)):
            return list(first)
            
    if hasattr(response, 'embedding') and response.embedding:
        if hasattr(response.embedding, 'values'):
            return list(response.embedding.values)
        if isinstance(response.embedding, (list, tuple)):
            return list(response.embedding)
            
    if hasattr(response, 'values'):
        return list(response.values)
        
    raise ValueError("Gagal mengurai atribut embedding dari objek EmbedContentResponse")

def generate_embedding(text: str) -> list[float]:
    client = genai.Client(api_key=GEMINI_KEY)
    
    models_to_try = [
        os.getenv("EMBEDDING_MODEL", "gemini-embedding-2"),
        "gemini-embedding-2",
        "gemini-embedding-001",
        "gemini-embedding-2-preview",
        "models/gemini-embedding-2"
    ]
    
    embed_config = types.EmbedContentConfig(output_dimensionality=768)
    
    last_exception = None
    for model_name in models_to_try:
        try:
            res = client.models.embed_content(
                model=model_name,
                contents=text,
                config=embed_config
            )
            return extract_vector(res)
        except Exception as e:
            last_exception = e
            logging.warning(f"Embedding failed with {model_name}: {str(e)}")
            continue
            
    raise RuntimeError(f"Gagal generate embedding: {str(last_exception)}")

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

async def backfill_unembedded_knowledge(account_id: str):
    db = get_supabase()
    
    # Ambil baris yang embedding-nya masih NULL
    res = db.schema("threads").from_("brand_knowledge").select("id, content").eq("account_id", account_id).is_("embedding", "null").execute()
    rows = res.data or []
    
    updated_count = 0
    for row in rows:
        vec = generate_embedding(row["content"])
        db.schema("threads").from_("brand_knowledge").update({"embedding": vec}).eq("id", row["id"]).execute()
        updated_count += 1
        
    return {"total_unembedded_found": len(rows), "successfully_updated": updated_count}

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
