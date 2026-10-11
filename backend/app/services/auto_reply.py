import os
from google import genai
from app.services.rag import search_knowledge

GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-flash-latest")

async def generate_rag_reply(account_id: str, user_comment: str, author_username: str = "") -> str:
    contexts = await search_knowledge(account_id, user_comment, limit=3)
    
    knowledge_text = "\n".join([f"- {c.get('title')}: {c.get('content')}" for c in contexts]) if contexts else "Tidak ada basis pengetahuan spesifik."
    
    prompt = f"""
    Kamu adalah AI Assistant resmi untuk akun Threads ini.
    Tugasmu adalah menjawab komentar user dengan ramah, lugas, santai, dan profesional.
    
    Pengetahuan Brand/Bisnis:
    {knowledge_text}
    
    Komentar dari @{author_username}:
    "{user_comment}"
    
    Aturan Balasan:
    1. Maksimal 2-3 kalimat. Bahasa Indonesia santai & natural.
    2. Jika pertanyaan terkait harga/layanan, gunakan info dari Pengetahuan Brand di atas.
    3. Jangan gunakan tagar berlebihan.
    """
    
    client = genai.Client(api_key=GEMINI_KEY)
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )
    
    return response.text.strip()
