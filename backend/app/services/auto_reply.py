import os
import logging
import httpx
from google import genai
from app.services.rag import search_knowledge
from supabase import create_client

GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

def get_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

# Urutan Fallback Model (Sesuai request lu, dari yg paling pintar sampai paling ringan)
FALLBACK_MODELS = [
    "gemini-3.8-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-3.1-pro-preview",
    "gemini-3-flash-preview"
]

async def generate_rag_reply(account_id: str, user_comment: str, author_username: str = "") -> str:
    contexts = await search_knowledge(account_id, user_comment, limit=3)
    knowledge_text = "\n".join([f"- {c.get('title')}: {c.get('content')}" for c in contexts]) if contexts else "Tidak ada basis pengetahuan spesifik."
    
    prompt = f"""
    Kamu adalah AI Assistant resmi untuk akun Threads ini.
    Tugasmu adalah menjawab komentar user dengan ramah, lugas, santai, dan profesional.
    
    Pengetahuan akun threads:
    {knowledge_text}
    
    Komentar dari @{author_username}:
    "{user_comment}"
    
    Aturan Balasan:
    1. Maksimal 2-3 kalimat. Bahasa Indonesia santai & natural.
    2. Jika pertanyaan terkait harga/layanan, gunakan info dari Pengetahuan Brand di atas.
    3. Jangan gunakan tagar berlebihan.
    """
    
    client = genai.Client(api_key=GEMINI_KEY)
    
    last_error = None
    # Looping Fallback Model
    for model_name in FALLBACK_MODELS:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            logging.warning(f"[AI Fallback] Model {model_name} gagal: {str(e)}. Mencoba model selanjutnya...")
            last_error = str(e)
            continue
            
    # Kalau semua model di daftar gagal, baru lempar error 500
    raise Exception(f"Semua model Gemini sibuk/gagal. Error terakhir: {last_error}")

async def publish_reply_to_threads(account_id: str, threads_reply_to_id: str, text: str) -> str:
    """Fungsi untuk benar-benar mengirim balasan ke Threads API"""
    db = get_supabase()
    res = db.schema("threads").from_("threads_accounts").select("settings").eq("id", account_id).limit(1).execute()
    
    if not res.data:
        raise Exception("Akun tidak ditemukan")
        
    token = res.data[0].get("settings", {}).get("access_token")
    if not token:
        raise Exception("Access token tidak ditemukan, user harus hubungkan ulang akun.")
        
    async with httpx.AsyncClient() as client:
        # Step 1: Bikin Container Balasan
        url_create = "https://graph.threads.net/v1.0/me/threads"
        params_create = {
            "media_type": "TEXT",
            "text": text,
            "reply_to_id": threads_reply_to_id, # ID komentar audiens yang mau dibalas
            "access_token": token
        }
        res_create = await client.post(url_create, params=params_create)
        
        if res_create.status_code != 200:
            raise Exception(f"Gagal membuat container Meta: {res_create.text}")
            
        container_id = res_create.json().get("id")
        
        # Step 2: Publish Container tersebut ke Publik
        url_publish = "https://graph.threads.net/v1.0/me/threads_publish"
        params_publish = {
            "creation_id": container_id,
            "access_token": token
        }
        res_publish = await client.post(url_publish, params=params_publish)
        
        if res_publish.status_code != 200:
            raise Exception(f"Gagal mem-publish ke Threads: {res_publish.text}")
            
        return res_publish.json().get("id") # Mengembalikan ID postingan balasan
