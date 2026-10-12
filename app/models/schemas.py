from pydantic import BaseModel, Field
from typing import List, Optional

class QuestRequest(BaseModel):
    location_name: str = Field(..., example="Ann Arbor, MI")
    latitude: Optional[float] = Field(None, example=42.2808)
    longitude: Optional[float] = Field(None, example=-83.7430)
    vibe: str = Field("forest_trail", example="fall_foliage_walk")

class QuestResponse(BaseModel):
    quest_id: str
    title: str
    objective: str
    environmental_lore: str
    audio_file_path: Optional[str] = None
    weather_context: dict

class QuestVerification(BaseModel):
    quest_id: str
    reflection_notes: str
