from fastapi import FastAPI
from src.api.routers import chat, tts, transcription, summary

app = FastAPI(
    title="Personal Doctor AI API",
    version="1.0.0",
)

app.include_router(chat.router)
app.include_router(tts.router)
app.include_router(transcription.router)
app.include_router(summary.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Personal Doctor AI API"}
