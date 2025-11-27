# backend/src/api/routers/transcription.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from src.services.audio.transcription import TranscriptionService
from src.schemas.chat import TranscriptionResponse
import shutil
import os
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

transcription_service = TranscriptionService()

@router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(file: UploadFile = File(...)):
    logger.info(f"Received transcription request for file: {file.filename}, content_type: {file.content_type}")
    if not file.content_type.startswith("audio/"):
        logger.error(f"Invalid file type received: {file.content_type}")
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an audio file.")

    temp_file_path = f"temp_{file.filename}"
    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        logger.info(f"Audio file saved temporarily to {temp_file_path}")

        text = transcription_service.transcribe(temp_file_path)
        logger.info(f"Transcription successful for {file.filename}. Result: {text[:50]}...")
        return TranscriptionResponse(text=text)
    except Exception as e:
        logger.exception(f"Error during transcription for {file.filename}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            logger.info(f"Temporary file {temp_file_path} removed.")