from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import logging
from src.services.llm.summary import SummaryService
from src.services.audio.tts import tts_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize SummaryService
summary_service = SummaryService()

class TTSRequest(BaseModel):
    text: str

@router.post("/summary-tts")
async def summary_tts_endpoint(request: TTSRequest):
    logger.info(f"Received Summary TTS request for text length: {len(request.text)}")
    try:
        # 1. Summarize
        summary_text = await summary_service.summarize(request.text)
        logger.info(f"Summarized text to: {summary_text}")
        
        # 2. TTS Stream
        return StreamingResponse(tts_service.text_to_speech_stream(summary_text), media_type="audio/wav")
    except Exception as e:
        logger.error(f"Error in Summary TTS endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/summary_stream")
async def summary_stream_endpoint(request: TTSRequest):
    logger.info(f"Received Summary Stream request for text length: {len(request.text)}")
    try:
        return StreamingResponse(summary_service.summarize_stream(request.text), media_type="text/event-stream")
    except Exception as e:
        logger.error(f"Error in Summary Stream endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
