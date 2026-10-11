import os
import json
import logging
from google import genai
from google.genai import types
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
        "match_threshold": 0.3,
        "match_count": limit,
        "p_account_id": account_id
    }).execute()
    
    return res.data or []

async def generate_rag_post(account_id: str, topic: str, tone: str = "Edukasi & Insight Kasual", custom_prompt: str = None) -> list[dict]:
    knowledge = await search_knowledge(account_id, topic, limit=3)
    
    context_text = ""
    if knowledge:
        context_text = "\n".join([f"- [{k.get('category', 'Fakta')} - {k.get('title')}]: {k.get('content')}" for k in knowledge])
    
    # Switch instruksi tone jika memilih Custom Prompt
    if tone == "Custom Prompt" and custom_prompt:
        tone_instruction = f"[INSTRUKSI KHUSUS DARI USER]\n{custom_prompt}"
    else:
        tone_instruction = f"[GAYA BAHASA / TONE]\n{tone}"
        
    prompt = f"""Kamu adalah Content Strategist & Copywriter Threads profesional.
Buat 3 variasi draf postingan Threads berbeda berdasarkan TOPIK dan KONTEKS BRAND di bawah ini.

[TOPIK / IDE POSTINGAN]
{topic}

{tone_instruction}

[KONTEKS KHUSUS BRAND / RAG KNOWLEDGE BASE]
{context_text if context_text else "Tidak ada dokumen RAG khusus. Gunakan fakta umum bisnis."}

[PETUNJUK PENULISAN]
1. Tulis dalam bahasa Indonesia yang natural, menarik (hook kuat), dan berbobot khas Threads.
2. Sisipkan fakta, angka, atau detail spesifik dari KONTEKS KHUSUS BRAND jika ada.
3. Hasilkan tepat 3 variasi draf yang siap pakai.

WAJIB kembalikan respon DALAM FORMAT JSON ARRAY murni tanpa teks pembuka/penutup markdown:
[
  {{"id": "1", "title": "Draf 1: Storytelling", "content": "isi teks draf 1..."}},
  {{"id": "2", "title": "Draf 2: Insight / Edukasi", "content": "isi teks draf 2..."}},
  {{"id": "3", "title": "Draf 3: Hook & Diskusi", "content": "isi teks draf 3..."}}
]
"""

    client = genai.Client(api_key=GEMINI_KEY)
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )
    
    raw_text = response.text.strip()
    if raw_text.startswith("```json"):
        raw_text = raw_text.replace("```json", "", 1).rstrip("`").strip()
    if raw_text.startswith("```"):
        raw_text = raw_text.replace("```", "", 1).rstrip("`").strip()
        
    try:
        return json.loads(raw_text)
    except Exception:
        return [
            {"id": "1", "title": "Draf Utama", "content": response.text}
        ]
