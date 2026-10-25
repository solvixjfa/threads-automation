import os
import json
import logging
from google import genai
from google.genai import types
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")

FALLBACK_MODELS = [
    "gemini-3.8-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-3.1-pro-preview",
    "gemini-3-flash-preview"
]

def get_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def get_all_raw_models() -> list[str]:
    client = genai.Client(api_key=GEMINI_KEY)
    models = []
    try:
        for m in client.models.list():
            models.append(getattr(m, 'name', str(m)))
    except Exception as e:
        logging.error(f"Failed to list models: {str(e)}")
    return models

def extract_vector(response) -> list[float]:
    if hasattr(response, 'embeddings') and response.embeddings:
        first = response.embeddings[0]
        if hasattr(first, 'values'): return list(first.values)
        if isinstance(first, (list, tuple)): return list(first)
    if hasattr(response, 'embedding') and response.embedding:
        if hasattr(response.embedding, 'values'): return list(response.embedding.values)
        if isinstance(response.embedding, (list, tuple)): return list(response.embedding)
    if hasattr(response, 'values'): return list(response.values)
    raise ValueError("Failed to parse embedding")

def generate_embedding(text: str, api_key: str) -> list[float]:
    client = genai.Client(api_key=api_key)
    models_to_try = ["gemini-embedding-2", "gemini-embedding-001"]
    embed_config = types.EmbedContentConfig(output_dimensionality=768)
    for model_name in models_to_try:
        try:
            res = client.models.embed_content(model=model_name, contents=text, config=embed_config)
            return extract_vector(res)
        except Exception as e:
            err_str = str(e)
            if "API_KEY_INVALID" in err_str or "API key not valid" in err_str:
                raise Exception("Your Custom Gemini API Key is invalid. Please check your key in Settings.")
            logging.warning(f"Embedding failed with {model_name}: {err_str}")
    raise RuntimeError("Failed to generate embedding.")

async def store_knowledge(account_id: str, title: str, content: str, category: str = "general"):
    db = get_supabase()
    acc_res = db.schema("threads").from_("threads_accounts").select("custom_gemini_key").eq("id", account_id).limit(1).execute()
    
    api_key = GEMINI_KEY
    if acc_res.data and acc_res.data[0].get("custom_gemini_key"):
        api_key = acc_res.data[0].get("custom_gemini_key")

    embedding = generate_embedding(content, api_key)
    data = {"account_id": account_id, "title": title, "content": content, "category": category, "embedding": embedding}
    res = db.schema("threads").from_("brand_knowledge").insert(data).execute()
    return res.data

async def backfill_unembedded_knowledge(account_id: str):
    db = get_supabase()
    acc_res = db.schema("threads").from_("threads_accounts").select("custom_gemini_key").eq("id", account_id).limit(1).execute()
    
    api_key = GEMINI_KEY
    if acc_res.data and acc_res.data[0].get("custom_gemini_key"):
        api_key = acc_res.data[0].get("custom_gemini_key")
        
    res = db.schema("threads").from_("brand_knowledge").select("id, content").eq("account_id", account_id).is_("embedding", "null").execute()
    updated_count = 0
    for row in (res.data or []):
        vec = generate_embedding(row["content"], api_key)
        db.schema("threads").from_("brand_knowledge").update({"embedding": vec}).eq("id", row["id"]).execute()
        updated_count += 1
    return {"total_unembedded_found": len(res.data or []), "successfully_updated": updated_count}

async def search_knowledge(account_id: str, query: str, limit: int = 3, api_key: str = None):
    if not api_key: api_key = GEMINI_KEY
    query_vector = generate_embedding(query, api_key)
    db = get_supabase()
    res = db.rpc("match_brand_knowledge", {
        "query_embedding": query_vector, "match_threshold": 0.3, "match_count": limit, "p_account_id": account_id
    }).execute()
    return res.data or []

async def generate_rag_post(account_id: str, topic: str, tone: str = "Edukasi & Insight Kasual", custom_prompt: str = None) -> list[dict]:
    db = get_supabase()
    # FIX SINTAKS PYTHON: Ganti .maybeSingle() jadi .limit(1).execute()
    acc_res = db.schema("threads").from_("threads_accounts").select("custom_gemini_key, ai_credits").eq("id", account_id).limit(1).execute()
    
    if not acc_res.data:
        raise Exception("Account not found")
        
    acc = acc_res.data[0]
    custom_key = acc.get("custom_gemini_key")
    credits = acc.get("ai_credits", 0)
    
    # JIKA PAKAI CUSTOM KEY, PAKSA PAKAI ITU. JANGAN PAKAI KEY SAAS KALAU ERROR.
    if custom_key:
        api_key_to_use = custom_key
    else:
        if credits <= 0:
            raise Exception("Insufficient AI Credits. Please add your own Gemini API Key in Settings or top up.")
        api_key_to_use = GEMINI_KEY
    
    knowledge = await search_knowledge(account_id, topic, limit=3, api_key=api_key_to_use)
    context_text = "\n".join([f"- [{k.get('category', 'Fakta')} - {k.get('title')}]: {k.get('content')}" for k in knowledge])

    recent_res = db.schema("threads").from_("scheduled_posts").select("text, status, scheduled_for").eq("account_id", account_id).order("scheduled_for", desc=True).limit(5).execute()
    recent_history = "\n".join([f"- [{p['status'].upper()}] {p['text'][:150]}..." for p in recent_res.data]) if recent_res.data else "No recent posts."

    tone_instruction = f"[CUSTOM INSTRUCTION]\n{custom_prompt}" if (tone == "Custom Prompt" and custom_prompt) else f"[TONE / STYLE]\n{tone}"

    prompt = f"""You are a professional Threads Content Strategist.
Create a 3-DAY CONTENT PLAN based on the TOPIC below. Avoid repeating recent posts.

[RECENT POSTS]
{recent_history}

[RAG KNOWLEDGE BASE]
{context_text if context_text else "No specific RAG document."}

[TOPIC]
{topic}

{tone_instruction}

[OUTPUT INSTRUCTIONS]
1. Create 3 different posts for Day 1, Day 2, and Day 3.
2. Ensure logical sequence (Hook, Deep Dive, CTA).
3. MUST return pure JSON array:
[
  {{"id": "1", "title": "Day 1: [Title]", "content": "..."}},
  {{"id": "2", "title": "Day 2: [Title]", "content": "..."}},
  {{"id": "3", "title": "Day 3: [Title]", "content": "..."}}
]
"""

    client = genai.Client(api_key=api_key_to_use)
    gen_config = types.GenerateContentConfig(response_mime_type="application/json")
    last_error = None
    response = None

    for model_name in FALLBACK_MODELS:
        try:
            response = client.models.generate_content(model=model_name, contents=prompt, config=gen_config)
            break
        except Exception as e:
            err_str = str(e)
            # JIKA KEY USER SALAH, LANGSUNG LEMPAR ERROR KE FRONTEND
            if "API_KEY_INVALID" in err_str or "API key not valid" in err_str or "400" in err_str:
                raise Exception("Your Custom Gemini API Key is invalid or expired. Please update it in Settings.")
            
            logging.warning(f"[AI Fallback POST] Model {model_name} failed: {err_str}")
            last_error = err_str

    if not response:
        raise Exception(f"All Gemini models failed. Last error: {last_error}")

    # Potong kredit HANYA kalau pakai key SaaS
    if not custom_key:
        db.schema("threads").from_("threads_accounts").update({"ai_credits": credits - 1}).eq("id", account_id).execute()

    raw_text = response.text.strip()
    if raw_text.startswith("```json"): raw_text = raw_text.replace("```json", "", 1).rstrip("`").strip()
    if raw_text.startswith("```"): raw_text = raw_text.replace("```", "", 1).rstrip("`").strip()

    try:
        return json.loads(raw_text)
    except Exception:
        return [{"id": "1", "title": "Draft", "content": response.text}]
