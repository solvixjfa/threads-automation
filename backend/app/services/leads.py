import os
import httpx
from google import genai

GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-flash-latest")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")

async def analyze_and_notify_lead(account_id: str, username: str, comment: str):
    client = genai.Client(api_key=GEMINI_KEY)
    
    prompt = f"""
    Analisis komentar Threads berikut:
    User: @{username}
    Komentar: "{comment}"
    
    Klasifikasikan apakah ini 'HOT_LEAD' (tertarik beli/tanya harga/minta kontak), 'INQUIRY' (tanya biasa), atau 'OTHER'.
    Jawab HANYA dengan salah satu kata tersebut.
    """
    
    res = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )
    
    intent = res.text.strip().upper()
    
    if "HOT_LEAD" in intent and DISCORD_WEBHOOK_URL:
        payload = {
            "embeds": [{
                "title": "🚨 New Hot Lead Detected on Threads!",
                "color": 5814783,
                "fields": [
                    {"name": "Username", "value": f"@{username}", "inline": True},
                    {"name": "Komentar", "value": comment, "inline": False}
                ]
            }]
        }
        async with httpx.AsyncClient() as http:
            await http.post(DISCORD_WEBHOOK_URL, json=payload)
            
    return {"username": username, "intent": intent}
