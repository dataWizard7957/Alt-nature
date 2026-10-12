from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

class Database:
    client: AsyncIOMotorClient = None
    db = None

db_instance = Database()

async def connect_to_mongo():
    if not settings.MONGODB_URI or "username:password" in settings.MONGODB_URI or "cluster.mongodb.net" in settings.MONGODB_URI:
        print("MongoDB URI not configured or placeholder detected; running with in-memory fallback mode.")
        db_instance.db = None
        return
    try:
        db_instance.client = AsyncIOMotorClient(settings.MONGODB_URI, serverSelectionTimeoutMS=2000)
        db_instance.db = db_instance.client.alt_nature_db
        print("Connected to MongoDB Atlas successfully.")
    except Exception as e:
        print(f"MongoDB connection warning: {e}. Running without database persistence.")
        db_instance.db = None

async def close_mongo_connection():
    if db_instance.client:
        db_instance.client.close()
        print("Closed MongoDB connection.")

def get_database():
    return db_instance.db