from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from src.services.audio.tts import tts_service
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class TTSRequest(BaseModel):
    text: str

@router.post("/tts")
async def tts_endpoint(request: TTSRequest):
    logger.info(f"Received TTS request for text: {request.text}")
    try:
        return StreamingResponse(tts_service.text_to_speech_stream(request.text), media_type="audio/wav")
    except Exception as e:
        logger.error(f"Error in TTS endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")