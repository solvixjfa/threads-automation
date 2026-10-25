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

def generate_embedding(text: str) -> list[float]:
    client = genai.Client(api_key=GEMINI_KEY)
    models_to_try = ["gemini-embedding-2", "gemini-embedding-001", "gemini-embedding-2-preview", "models/gemini-embedding-2"]
    embed_config = types.EmbedContentConfig(output_dimensionality=768)
    for model_name in models_to_try:
        try:
            res = client.models.embed_content(model=model_name, contents=text, config=embed_config)
            return extract_vector(res)
        except Exception as e:
            logging.warning(f"Embedding failed with {model_name}: {str(e)}")
    raise RuntimeError("Gagal generate embedding")

async def store_knowledge(account_id: str, title: str, content: str, category: str = "general"):
    embedding = generate_embedding(content)
    db = get_supabase()
    data = {"account_id": account_id, "title": title, "content": content, "category": category, "embedding": embedding}
    res = db.schema("threads").from_("brand_knowledge").insert(data).execute()
    return res.data

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
    # 1. Ambil RAG
    knowledge = await search_knowledge(account_id, topic, limit=3)
    context_text = "\n".join([f"- [{k.get('category', 'Fakta')} - {k.get('title')}]: {k.get('content')}" for k in knowledge])

    # 2. AMBIL RIWAYAT POSTINGAN (CONTEXT PLANNING)
    db = get_supabase()
    recent_res = db.schema("threads").from_("scheduled_posts").select("text, status, scheduled_for").eq("account_id", account_id).order("scheduled_for", desc=True).limit(5).execute()
    recent_history = "\n".join([f"- [{p['status'].upper()}] {p['text'][:150]}..." for p in recent_res.data]) if recent_res.data else "No recent posts."

    if tone == "Custom Prompt" and custom_prompt:
        tone_instruction = f"[CUSTOM INSTRUCTION]\n{custom_prompt}"
    else:
        tone_instruction = f"[TONE / STYLE]\n{tone}"

    prompt = f"""You are a professional Threads Content Strategist.
Your task is to create a 3-DAY CONTENT PLAN based on the TOPIC below. Avoid repeating what the user has already posted recently.

[RECENT & UPCOMING POSTS (DO NOT DUPLICATE THESE)]
{recent_history}

[RAG KNOWLEDGE BASE]
{context_text if context_text else "No specific RAG document. Use general facts."}

[TOPIC]
{topic}

{tone_instruction}

[OUTPUT INSTRUCTIONS]
1. Create 3 different posts for Day 1, Day 2, and Day 3.
2. Ensure they form a logical sequence (e.g., Day 1: Hook/Teaser, Day 2: Deep Dive/Insight, Day 3: Q&A/Call to Action).
3. Use natural English or Indonesian (match the tone).
4. MUST return a pure JSON array, NO markdown formatting:
[
  {{"id": "1", "title": "Day 1: [Title]", "content": "..."}},
  {{"id": "2", "title": "Day 2: [Title]", "content": "..."}},
  {{"id": "3", "title": "Day 3: [Title]", "content": "..."}}
]
"""

    client = genai.Client(api_key=GEMINI_KEY)
    gen_config = types.GenerateContentConfig(response_mime_type="application/json")
    last_error = None
    response = None

    for model_name in FALLBACK_MODELS:
        try:
            response = client.models.generate_content(model=model_name, contents=prompt, config=gen_config)
            break
        except Exception as e:
            logging.warning(f"[AI Fallback POST] Model {model_name} failed: {str(e)}")
            last_error = str(e)

    if not response:
        raise Exception(f"All Gemini models busy/failed. Last error: {last_error}")

    raw_text = response.text.strip()
    if raw_text.startswith("```json"): raw_text = raw_text.replace("```json", "", 1).rstrip("`").strip()
    if raw_text.startswith("```"): raw_text = raw_text.replace("```", "", 1).rstrip("`").strip()

    try:
        return json.loads(raw_text)
    except Exception:
        return [{"id": "1", "title": "Draft", "content": response.text}]
