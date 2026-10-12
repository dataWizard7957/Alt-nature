import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.telemetry import init_sentry
from app.core.database import connect_to_mongo, close_mongo_connection
from app.routers import quests

init_sentry()

app = FastAPI(title="Alt-nature API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()
    # Ensure the static folder exists for ElevenLabs audio file generation
    os.makedirs("static", exist_ok=True)

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

app.include_router(quests.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return {"message": "Welcome to Alt-nature API. Touch grass today!"}