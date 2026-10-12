from fastapi import APIRouter, HTTPException
import uuid
from app.models.schemas import QuestRequest, QuestResponse, QuestVerification
from app.services.serpapi_client import fetch_local_weather
from app.services.gemma_engine import generate_micro_quest
from app.services.elevenlabs_tts import generate_audio_briefing
from app.core.database import get_database

router = APIRouter(prefix="/api/quest", tags=["quests"])

@router.post("/generate", response_model=QuestResponse)
async def generate_quest(req: QuestRequest):
    weather = fetch_local_weather(req.location_name)
    quest_data = generate_micro_quest(req.location_name, req.vibe, weather)
    
    narration_text = f"Your Chlorophyll Quest: {quest_data['title']}. {quest_data['objective']} Ecological lore: {quest_data['environmental_lore']}"
    audio_path = generate_audio_briefing(narration_text)
    print(f"DEBUG AUDIO PATH RETURNED: '{audio_path}'")    
    quest_id = str(uuid.uuid4())
    record = {
        "quest_id": quest_id,
        "location": req.location_name,
        "title": quest_data["title"],
        "objective": quest_data["objective"],
        "environmental_lore": quest_data["environmental_lore"],
        "status": "active"
    }
    
    db = get_database()
    if db is not None:
        await db.quests.insert_one(record)
        
    return QuestResponse(
        quest_id=quest_id,
        title=quest_data["title"],
        objective=quest_data["objective"],
        environmental_lore=quest_data["environmental_lore"],
        audio_file_path=audio_path,
        weather_context=weather
    )

@router.post("/verify")
async def verify_quest(verification: QuestVerification):
    db = get_database()
    if db is not None:
        result = await db.quests.update_one(
            {"quest_id": verification.quest_id},
            {"$set": {"status": "completed", "reflection": verification.reflection_notes}}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Quest not found")
            
    return {"status": "success", "message": "Quest completed! You successfully touched grass."}
