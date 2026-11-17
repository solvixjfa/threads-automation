import os
import logging
import httpx
import asyncio
import json
from google import genai
from app.services.rag import search_knowledge, get_supabase, GROQ_KEY, GEMINI_KEY, DEFAULT_GEMINI_MODELS, DEFAULT_GROQ_MODELS
from app.services.billing import check_and_spend, refund_credits, BillingError
from groq import Groq

async def generate_rag_reply(account_id: str, user_comment: str, post_text: str = "", author_username: str = "", provider: str = "gemini", model_name: str = None, tone_prompt: str = "", user_kb: str = "") -> str:
    db = get_supabase()
    ref_id = None
    try:
        ref_id = check_and_spend(account_id, "reply_ai")
    except BillingError as e:
        # Fallback ke template gratis jika kredit habis / expired
        return None # Signal ke worker untuk pake template
    except Exception:
        return None
    
    # 1. CEK KREDIT & API KEY USER
    acc_res = db.schema("threads").from_("threads_accounts").select("custom_gemini_key, custom_groq_key, credit_balance").eq("id", account_id).limit(1).execute()
    if not acc_res.data: raise Exception("Account not found")
    acc = acc_res.data[0]
    
    custom_gemini = acc.get("custom_gemini_key")
    custom_groq = acc.get("custom_groq_key")
    credits = acc.get("credit_balance", 0)
    
    if provider == "groq":
        api_key_to_use = custom_groq if custom_groq else GROQ_KEY
        is_using_saas = not custom_groq
        if not api_key_to_use: raise Exception("Groq API Key is missing on server.")
    else:
        api_key_to_use = custom_gemini if custom_gemini else GEMINI_KEY
        is_using_saas = not custom_gemini
        if not api_key_to_use: raise Exception("Gemini API Key is missing on server.")

    if is_using_saas and credits <= 0:
        raise Exception("Insufficient AI Credits. Please add your own API Key in Settings or top up.")

    # 2. TARIK RAG (Pakai Gemini Key karena Groq gak ada embedding)
    gemini_embed_key = custom_gemini if custom_gemini else GEMINI_KEY
    contexts = await search_knowledge(account_id, user_comment, limit=3, api_key=gemini_embed_key)
    knowledge_text = "\n".join([f"- {c.get('title')}: {c.get('content')}" for c in contexts]) if contexts else "No specific brand knowledge found."

    # 3. PROMPT (Disesuaikan dengan konteks komentar)
    final_tone = tone_prompt if tone_prompt else "Reply naturally, casually, and straight to the point like the account owner talking to a friend. No corporate greetings, no over-enthusiasm, no emojis unless natural."
    final_kb = user_kb if user_kb else knowledge_text

    prompt = f"""You are acting as the owner of this Threads account, replying directly to a user comment.

[LANGUAGE RULE - HIGHEST PRIORITY]
Detect the language of the user's comment below. You MUST reply in the EXACT SAME language.
- If the user comment is in English -> reply in English.
- If the user comment is in Indonesian -> reply in Indonesian.
- If mixed -> reply in the dominant language.
Do NOT translate. Do NOT reply in a different language than the user used.

[TONE & PERSONA INSTRUCTIONS]
{final_tone}

[ORIGINAL POST CONTEXT]
{post_text if post_text else "No post context available."}

[BRAND KNOWLEDGE & FACTS]
{final_kb}

[USER COMMENT]
@{author_username} says: "{user_comment}"

[REPLY RULES]
1. Reply in the SAME language as the user's comment (critical, see Language Rule above).
2. Max 1-2 short sentences. Straight to the point, no fluff.
3. If they ask about a project/service, use facts from Brand Knowledge. Do NOT invent facts.
4. Match the tone from Tone & Persona Instructions (casual/formal/etc), but language still follows the user.
5. Do NOT use hashtags. Emojis only if tone explicitly allows.
6. Do NOT sound like a corporate customer service bot. Avoid "Halo kak", "Wah ide bagus tuh", "Hai sobat", or any template greeting.
7. If Brand Knowledge does not contain the answer, say honestly and briefly that you'll follow up, instead of making something up.
"""

    result_text = ""
    
    # 4. EKSEKUSI AI
    if provider == "groq":
        try:
            groq_client = Groq(api_key=api_key_to_use)
            model_to_run = model_name or "llama-3.3-70b-versatile"
            chat_completion = groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=model_to_run,
                temperature=0.6,
            )
            result_text = chat_completion.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"Groq failed: {str(e)}")
    else:
        client = genai.Client(api_key=api_key_to_use)
        models_to_try = [model_name] if model_name else DEFAULT_GEMINI_MODELS
        last_error = ""
        for m_name in models_to_try:
            try:
                response = client.models.generate_content(model=m_name, contents=prompt)
                result_text = response.text.strip()
                break
            except Exception as e:
                last_error = str(e)
        
        if not result_text:
            raise Exception(f"All Gemini models failed. Last error: {last_error}")

    # Kredit sudah dipotong otomatis oleh check_and_spend() di awal fungsi.
    # Manual deduction dihapus untuk mencegah DOUBLE DEDUCT.

    return result_text

async def publish_reply_to_threads(account_id: str, threads_reply_to_id: str, text: str) -> str:
    db = get_supabase()
    res = db.schema("threads").from_("threads_accounts").select("settings").eq("id", account_id).limit(1).execute()
    
    if not res.data: raise Exception("Account not found")
    token = res.data[0].get("settings", {}).get("access_token")
    if not token: raise Exception("Access token not found.")

    async with httpx.AsyncClient(timeout=30.0) as client:
        url_create = "https://graph.threads.net/v1.0/me/threads"
        params_create = {
            "media_type": "TEXT", "text": text, "reply_to_id": threads_reply_to_id, "access_token": token
        }
        res_create = await client.post(url_create, params=params_create)
        if res_create.status_code != 200: raise Exception(f"Meta API Error: {res_create.text}")
        
        container_id = res_create.json().get("id")
        await asyncio.sleep(3) # Jeda Meta API
        
        url_publish = "https://graph.threads.net/v1.0/me/threads_publish"
        params_publish = {"creation_id": container_id, "access_token": token}
        res_publish = await client.post(url_publish, params=params_publish)
        if res_publish.status_code != 200: raise Exception(f"Failed to publish: {res_publish.text}")

        return res_publish.json().get("id")
