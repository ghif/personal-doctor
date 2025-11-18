# backend/src/services/transcription_service.py

import whisper
import logging

logger = logging.getLogger(__name__)

class TranscriptionService:
    def __init__(self):
        logger.info("Loading Whisper model...")
        self.model = whisper.load_model("small")
        logger.info("Whisper model loaded.")

    def transcribe(self, audio_file_path: str) -> str:
        logger.info(f"Starting transcription for {audio_file_path}")
        result = self.model.transcribe(audio_file_path)
        transcribed_text = result.get("text", "")
        logger.info(f"Finished transcription for {audio_file_path}. Result: {transcribed_text[:50]}...")
        return transcribed_text