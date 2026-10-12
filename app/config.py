import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    GEMMA_MODEL_NAME: str = os.getenv("GEMMA_MODEL_NAME", "gemma2")
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    ELEVENLABS_API_KEY: str = os.getenv("ELEVENLABS_API_KEY", "")
    SERPAPI_API_KEY: str = os.getenv("SERPAPI_API_KEY", "")
    SENTRY_DSN: str = os.getenv("SENTRY_DSN", "")

settings = Settings()
