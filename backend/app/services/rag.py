import os
import json
import logging
import httpx
from google import genai
from google.genai import types
from supabase import create_client, Client
from groq import Groq

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")
GROQ_KEY = os.getenv("GROQ_API_KEY", "")

DEFAULT_GEMINI_MODELS = ["gemini-3.8-flash", "gemini-3.6-flash", "gemini-3.5-flash-lite"]
DEFAULT_GROQ_MODELS = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]

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

async def get_available_models(account_id: str, provider: str) -> list[dict]:
    db = get_supabase()
    acc_res = db.schema("threads").from_("threads_accounts").select("custom_gemini_key, custom_groq_key").eq("id", account_id).limit(1).execute()
    acc = acc_res.data[0] if acc_res.data else {}
    
    if provider == "groq":
        api_key = acc.get("custom_groq_key") or GROQ_KEY
        if not api_key: return [{"id": m, "name": m} for m in DEFAULT_GROQ_MODELS]
        try:
            async with httpx.AsyncClient() as client:
                res = await client.get("https://api.groq.com/openai/v1/models", headers={"Authorization": f"Bearer {api_key}"})
                if res.status_code == 200:
                    data = res.json().get("data", [])
                    return [{"id": m["id"], "name": m["id"]} for m in data if m.get("active", True)]
        except Exception: pass
        return [{"id": m, "name": m} for m in DEFAULT_GROQ_MODELS]
    else:
        api_key = acc.get("custom_gemini_key") or GEMINI_KEY
        if not api_key: return [{"id": m, "name": m} for m in DEFAULT_GEMINI_MODELS]
        try:
            async with httpx.AsyncClient() as client:
                res = await client.get(f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}")
                if res.status_code == 200:
                    data = res.json().get("models", [])
                    valid = []
                    for m in data:
                        if "generateContent" in m.get("supportedGenerationMethods", []):
                            name = m["name"].replace("models/", "")
                            valid.append({"id": name, "name": name})
                    if valid: return valid
        except Exception: pass
        return [{"id": m, "name": m} for m in DEFAULT_GEMINI_MODELS]

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
                raise Exception("Your Custom Gemini API Key is invalid (needed for RAG embeddings).")
    raise RuntimeError("Failed to generate embedding.")

async def store_knowledge(account_id: str, title: str, content: str, category: str = "general"):
    db = get_supabase()
    acc_res = db.schema("threads").from_("threads_accounts").select("custom_gemini_key").eq("id", account_id).limit(1).execute()
    api_key = acc_res.data[0].get("custom_gemini_key") if acc_res.data and acc_res.data[0].get("custom_gemini_key") else GEMINI_KEY
    embedding = generate_embedding(content, api_key)
    data = {"account_id": account_id, "title": title, "content": content, "category": category, "embedding": embedding}
    res = db.schema("threads").from_("brand_knowledge").insert(data).execute()
    return res.data

async def backfill_unembedded_knowledge(account_id: str):
    db = get_supabase()
    acc_res = db.schema("threads").from_("threads_accounts").select("custom_gemini_key").eq("id", account_id).limit(1).execute()
    api_key = acc_res.data[0].get("custom_gemini_key") if acc_res.data and acc_res.data[0].get("custom_gemini_key") else GEMINI_KEY
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

async def generate_rag_post(account_id: str, topic: str, tone: str = "Edukasi & Insight Kasual", custom_prompt: str = None, provider: str = "gemini", model_name: str = None) -> list[dict]:
    db = get_supabase()
    acc_res = db.schema("threads").from_("threads_accounts").select("custom_gemini_key, custom_groq_key, ai_credits").eq("id", account_id).limit(1).execute()
    
    if not acc_res.data: raise Exception("Account not found")
    acc = acc_res.data[0]
    
    custom_gemini = acc.get("custom_gemini_key")
    custom_groq = acc.get("custom_groq_key")
    credits = acc.get("ai_credits", 0)
    
    if provider == "groq":
        api_key_to_use = custom_groq if custom_groq else GROQ_KEY
        is_using_saas = not custom_groq
        if not api_key_to_use: raise Exception("Groq API Key is missing on server. Please add your own key.")
    else:
        api_key_to_use = custom_gemini if custom_gemini else GEMINI_KEY
        is_using_saas = not custom_gemini
        if not api_key_to_use: raise Exception("Gemini API Key is missing on server. Please add your own key.")

    if is_using_saas and credits <= 0:
        raise Exception("Insufficient AI Credits. Please add your own API Key for this provider in Settings or top up.")

    gemini_embed_key = custom_gemini if custom_gemini else GEMINI_KEY
    if not gemini_embed_key: raise Exception("Gemini API Key is required for RAG embeddings. Please add it in Settings.")
        
    knowledge = await search_knowledge(account_id, topic, limit=3, api_key=gemini_embed_key)
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
2. MUST return a pure JSON object with a single key "options" containing the array:
{{
  "options": [
    {{"id": "1", "title": "Day 1: [Title]", "content": "..."}},
    {{"id": "2", "title": "Day 2: [Title]", "content": "..."}},
    {{"id": "3", "title": "Day 3: [Title]", "content": "..."}}
  ]
}}
"""

    result_options = []
    
    if provider == "groq":
        try:
            groq_client = Groq(api_key=api_key_to_use)
            model_to_run = model_name or "llama-3.3-70b-versatile"
            chat_completion = groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=model_to_run,
                response_format={"type": "json_object"},
                temperature=0.7,
            )
            parsed = json.loads(chat_completion.choices[0].message.content)
            result_options = parsed.get("options", [])
        except Exception as e:
            raise Exception(f"Groq Generation Failed: {str(e)}")
    else:
        client = genai.Client(api_key=api_key_to_use)
        gen_config = types.GenerateContentConfig(response_mime_type="application/json")
        response = None
        models_to_try = [model_name] if model_name else DEFAULT_GEMINI_MODELS

        for m_name in models_to_try:
            try:
                response = client.models.generate_content(model=m_name, contents=prompt, config=gen_config)
                break
            except Exception as e:
                last_error = str(e)
                if "API_KEY_INVALID" in last_error or "API key not valid" in last_error:
                    raise Exception("Your Custom Gemini API Key is invalid.")
        
        if not response: raise Exception(f"Gemini failed. Last error: {last_error}")
        
        raw_text = response.text.strip()
        if raw_text.startswith("```json"): raw_text = raw_text.replace("```json", "", 1).rstrip("`").strip()
        parsed = json.loads(raw_text)
        result_options = parsed.get("options", parsed)

    if is_using_saas:
        db.schema("threads").from_("threads_accounts").update({"ai_credits": credits - 1}).eq("id", account_id).execute()

    if not result_options: raise Exception("AI returned empty content.")
    return result_options

async def repurpose_content(account_id: str, source_text: str, angle: str, provider: str = "gemini", model_name: str = None) -> list[dict]:
    db = get_supabase()
    acc_res = db.schema("threads").from_("threads_accounts").select("custom_gemini_key, custom_groq_key, ai_credits").eq("id", account_id).limit(1).execute()
    
    if not acc_res.data: raise Exception("Account not found")
    acc = acc_res.data[0]
    
    custom_gemini = acc.get("custom_gemini_key")
    custom_groq = acc.get("custom_groq_key")
    credits = acc.get("ai_credits", 0)
    
    if provider == "groq":
        api_key_to_use = custom_groq if custom_groq else GROQ_KEY
        is_using_saas = not custom_groq
        if not api_key_to_use: raise Exception("Groq API Key is missing on server. Please add your own key.")
    else:
        api_key_to_use = custom_gemini if custom_gemini else GEMINI_KEY
        is_using_saas = not custom_gemini
        if not api_key_to_use: raise Exception("Gemini API Key is missing on server. Please add your own key.")

    if is_using_saas and credits <= 0:
        raise Exception("Insufficient AI Credits. Please add your own API Key for this provider in Settings or top up.")

    prompt = f"""You are a professional Threads Copywriter.
Your task is to REWRITE / REPURPOSE the original text below into 3 different variations.
Do not invent new facts, just change the format, tone, and structure to fit the requested angle.

[REQUESTED ANGLE]
{angle}

[ORIGINAL TEXT]
{source_text}

[OUTPUT INSTRUCTIONS]
1. Create 3 different variations.
2. MUST return a pure JSON object with a single key "options" containing the array:
{{
  "options": [
    {{"id": "1", "content": "Variation 1 text..."}},
    {{"id": "2", "content": "Variation 2 text..."}},
    {{"id": "3", "content": "Variation 3 text..."}}
  ]
}}
"""

    result_options = []
    
    if provider == "groq":
        try:
            groq_client = Groq(api_key=api_key_to_use)
            model_to_run = model_name or "llama-3.3-70b-versatile"
            chat_completion = groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=model_to_run,
                response_format={"type": "json_object"},
                temperature=0.7,
            )
            parsed = json.loads(chat_completion.choices[0].message.content)
            result_options = parsed.get("options", [])
        except Exception as e:
            raise Exception(f"Groq Generation Failed: {str(e)}")
    else:
        client = genai.Client(api_key=api_key_to_use)
        gen_config = types.GenerateContentConfig(response_mime_type="application/json")
        response = None
        models_to_try = [model_name] if model_name else DEFAULT_GEMINI_MODELS

        last_error = ""
        for m_name in models_to_try:
            try:
                response = client.models.generate_content(model=m_name, contents=prompt, config=gen_config)
                break
            except Exception as e:
                last_error = str(e)
        
        if not response: raise Exception(f"Gemini failed. Last error: {last_error}")
        
        raw_text = response.text.strip()
        if raw_text.startswith("```json"): raw_text = raw_text.replace("```json", "", 1).rstrip("`").strip()
        parsed = json.loads(raw_text)
        result_options = parsed.get("options", parsed)

    if is_using_saas:
        db.schema("threads").from_("threads_accounts").update({"ai_credits": credits - 1}).eq("id", account_id).execute()

    if not result_options: raise Exception("AI returned empty content.")
    return result_options

async def get_repurpose_recommendations(account_id: str) -> list[dict]:
    db = get_supabase()
    
    # 1. Ambil semua posts & metriknya (sama kayak logic get-analytics)
    posts_res = db.schema("threads").from_("posts").select(
        "id, threads_media_id, created_at, post_metrics(views, likes, replies, reposts, snapshot_label)"
    ).eq("account_id", account_id).execute()
    
    if not posts_res.data:
        return []

    # 2. Ambil teks dari scheduled_posts
    sp_res = db.schema("threads").from_("scheduled_posts").select(
        "text, published_media_id, scheduled_for"
    ).eq("account_id", account_id).eq("status", "published").execute()
    
    sp_map = {str(sp.get("published_media_id")): sp for sp in (sp_res.data or []) if sp.get("published_media_id")}

    formatted = []
    for p in posts_res.data:
        media_id = str(p.get("threads_media_id"))
        sp = sp_map.get(media_id)
        
        # Skip kalau teksnya gak ketemu atau kosong
        if not sp or not sp.get("text"):
            continue
            
        latest_metrics = next((m for m in p.get("post_metrics", []) if m.get("snapshot_label") == "latest"), None)
        if not latest_metrics and p.get("post_metrics"):
            latest_metrics = p.get("post_metrics")[0]
            
        views = latest_metrics.get("views", 0) if latest_metrics else 0
        likes = latest_metrics.get("likes", 0) if latest_metrics else 0
        
        # Hitung Engagement Rate kasar
        er = ((likes + latest_metrics.get("replies", 0) + latest_metrics.get("reposts", 0)) / views * 100) if views > 0 and latest_metrics else 0
        
        formatted.append({
            "id": p["id"],
            "text": sp["text"],
            "views": views,
            "likes": likes,
            "er": round(er, 2),
            "posted_at": sp.get("scheduled_for") or p.get("created_at")
        })

    # 3. Urutkan berdasarkan Views terbanyak, ambil 5 teratas
    formatted.sort(key=lambda x: x["views"], reverse=True)
    return formatted[:5]
