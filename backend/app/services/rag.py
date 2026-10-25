import os
import json
import logging
from google import genai
from google.genai import types
from supabase import create_client, Client
from groq import Groq

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")
GROQ_KEY = os.getenv("GROQ_API_KEY", "")

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
                raise Exception("Your Custom Gemini API Key is invalid (needed for RAG embeddings).")
            logging.warning(f"Embedding failed with {model_name}: {err_str}")
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

async def generate_rag_post(account_id: str, topic: str, tone: str = "Edukasi & Insight Kasual", custom_prompt: str = None, provider: str = "gemini") -> list[dict]:
    db = get_supabase()
    acc_res = db.schema("threads").from_("threads_accounts").select("custom_gemini_key, custom_groq_key, ai_credits").eq("id", account_id).limit(1).execute()
    
    if not acc_res.data: raise Exception("Account not found")
    acc = acc_res.data[0]
    
    custom_gemini = acc.get("custom_gemini_key")
    custom_groq = acc.get("custom_groq_key")
    credits = acc.get("ai_credits", 0)
    
    # RAG Embedding WAJIB pake Gemini. Jadi kita tentuin API Key Gemini dulu.
    gemini_key_to_use = custom_gemini if custom_gemini else GEMINI_KEY
    
    # Tentukan provider yang dipake
    use_groq = (provider == "groq")
    
    # Validasi Kredit (Kalau gak pake key sendiri sama sekali)
    if not custom_gemini and not custom_groq and credits <= 0:
        raise Exception("Insufficient AI Credits. Please add your own API Key in Settings or top up.")

    knowledge = await search_knowledge(account_id, topic, limit=3, api_key=gemini_key_to_use)
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
3. MUST return a pure JSON object with a single key "options" containing the array:
{{
  "options": [
    {{"id": "1", "title": "Day 1: [Title]", "content": "..."}},
    {{"id": "2", "title": "Day 2: [Title]", "content": "..."}},
    {{"id": "3", "title": "Day 3: [Title]", "content": "..."}}
  ]
}}
"""

    result_options = []
    last_error = ""

    # --- LOGIKA GROQ (PRIMARY / FAST) ---
    if use_groq:
        groq_key_to_use = custom_groq if custom_groq else GROQ_KEY
        if not groq_key_to_use:
            raise Exception("Groq API Key is missing. Please add it in Settings or use Gemini.")
            
        try:
            groq_client = Groq(api_key=groq_key_to_use)
            # llama-3.3-70b-versatile sangat cepat dan bagus untuk JSON
            chat_completion = groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                response_format={"type": "json_object"},
                temperature=0.7,
            )
            raw_text = chat_completion.choices[0].message.content
            parsed = json.loads(raw_text)
            result_options = parsed.get("options", [])
        except Exception as e:
            logging.warning(f"[Groq Failed] {str(e)}. Falling back to Gemini...")
            last_error = str(e)
            use_groq = False # Paksa fallback ke Gemini

    # --- LOGIKA GEMINI (FALLBACK / DEFAULT) ---
    if not use_groq:
        if not gemini_key_to_use:
            raise Exception("Gemini API Key is missing.")
            
        client = genai.Client(api_key=gemini_key_to_use)
        gen_config = types.GenerateContentConfig(response_mime_type="application/json")
        response = None

        for model_name in FALLBACK_MODELS:
            try:
                response = client.models.generate_content(model=model_name, contents=prompt, config=gen_config)
                break
            except Exception as e:
                err_str = str(e)
                if "API_KEY_INVALID" in err_str or "API key not valid" in err_str or "400" in err_str:
                    raise Exception("Your Custom Gemini API Key is invalid or expired. Please update it in Settings.")
                logging.warning(f"[Gemini Fallback] Model {model_name} failed: {err_str}")
                last_error = err_str

        if not response:
            raise Exception(f"All AI providers failed. Last error: {last_error}")

        raw_text = response.text.strip()
        if raw_text.startswith("```json"): raw_text = raw_text.replace("```json", "", 1).rstrip("`").strip()
        if raw_text.startswith("```"): raw_text = raw_text.replace("```", "", 1).rstrip("`").strip()
        
        parsed = json.loads(raw_text)
        result_options = parsed.get("options", parsed) # Handle kalau model gak bungkus di "options"

    # Potong kredit HANYA kalau user gak punya custom key (baik Groq maupun Gemini)
    if not custom_gemini and not custom_groq:
        db.schema("threads").from_("threads_accounts").update({"ai_credits": credits - 1}).eq("id", account_id).execute()

    if not result_options:
        raise Exception("AI returned empty content. Please try again.")

    return result_options
