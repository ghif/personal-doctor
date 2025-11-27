import os
from TTS.api import TTS
import torch
import tempfile
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TTSService:
    def __init__(self, model_name="tts_models/en/ljspeech/vits"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {self.device}")
        self.model_name = model_name
        try:
            self.tts = TTS(self.model_name).to(self.device)
            logger.info("TTS model loaded successfully.")
        except Exception as e:
            logger.error(f"Error loading TTS model: {e}")
            self.tts = None

    def text_to_speech_stream(self, text: str):
        if not self.tts:
            logger.error("TTS model is not available.")
            return

        logger.info(f"Available speakers: {self.tts.speakers}")
        logger.info(f"Available languages: {self.tts.languages}")
        try:
            logger.info(f"Generating speech for text: {text}")
            print(f"Generating speech for text: {text}")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as fp:
                self.tts.tts_to_file(text=text, file_path=fp.name)
                logger.info(f"Speech generated and saved to temporary file: {fp.name}")
                print(f"Temporary file created at: {fp.name}")
                with open(fp.name, "rb") as f:
                    yield from f
            os.remove(fp.name)
            logger.info("Temporary file removed.")
        except Exception as e:
            logger.error(f"Error during TTS generation: {e}")
            return

tts_service = TTSService()

if __name__ == "__main__":
    # This will trigger the TTS service and show all the logs
    audio_data = list(tts_service.text_to_speech_stream("Hello, this is a test"))
    print(f"Generated audio data: {len(audio_data)} chunks")