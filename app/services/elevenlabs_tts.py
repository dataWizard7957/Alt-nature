import os
import requests
import uuid
from app.config import settings

def generate_audio_briefing(text: str) -> str:
    if not settings.ELEVENLABS_API_KEY:
        print("ElevenLabs API key missing; skipping TTS audio file creation.")
        return ""
    
    voice_id = "21m00Tcm4TlvDq8ikWAM"
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": settings.ELEVENLABS_API_KEY
    }
    
    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.75,
            "similarity_boost": 0.75
        }
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            os.makedirs("static", exist_ok=True)
            filename = f"static/quest_{uuid.uuid4().hex[:8]}.mp3"
            with open(filename, "wb") as f:
                f.write(response.content)
            return filename
    except Exception as e:
        print(f"ElevenLabs TTS generation error: {e}")
        
    return ""
