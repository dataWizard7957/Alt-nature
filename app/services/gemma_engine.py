import ollama
import json
import sentry_sdk
from app.config import settings

def generate_micro_quest(location: str, vibe: str, weather: dict) -> dict:
    with sentry_sdk.start_span(op="ai.inference", description="Gemma Quest Generation"):
        prompt = f"""
        You are Alt-nature, an open-source AI outdoor guide that designs micro-quests to get software developers off their screens and into nature.
        
        Location: {location}
        Vibe: {vibe}
        Current Weather/Environment: {weather.get('condition')}, {weather.get('temperature')}, Foliage: {weather.get('foliage_status')}
        
        Generate a creative, screen-free outdoor micro-quest with voice-guided mindfulness in mind. Output strict JSON with the following keys:
        - "title": A catchy name for the outdoor quest
        - "objective": A clear, engaging instruction of what to find or observe outside without looking at your phone (e.g., finding a specific leaf pattern or seed pod).
        - "environmental_lore": A soothing, 3-sentence voice-guided sensory script. It should weave together fascinating local ecological facts with calming mindfulness instructions (e.g., inviting them to take a deep breath, notice the scent of the air, or feel the textures around them) so it sounds peaceful when read aloud.
        """
        
        try:
            response = ollama.chat(
                model=settings.GEMMA_MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0.7}
            )
            content = response['message']['content']
            
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
                
            return json.loads(content)
        except Exception as e:
            print(f"Local Gemma inference fallback triggered due to: {e}")
            return {
                "title": "The Golden Maple Hunt",
                "objective": "Walk 50 paces down the trail, find a sugar maple leaf showing brilliant crimson transition, and observe its vein structure up close.",
                "environmental_lore": "Sugar maples draw down their chlorophyll in autumn, trapping carotenoids and anthocyanins that produce brilliant fall reds."
            }
