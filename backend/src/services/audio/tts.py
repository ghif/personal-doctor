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
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as fp:
                # Use the helper method to generate the file
                # We close the temp file handle here so text_to_file can write to it by path if needed, 
                # or pass the path. text_to_file takes a path.
                pass 
            
            # The file exists at fp.name but is empty and closed.
            self.text_to_file(text, fp.name)
            
            print(f"Temporary file created at: {fp.name}")
            with open(fp.name, "rb") as f:
                yield from f
            
            os.remove(fp.name)
            logger.info("Temporary file removed.")
        except Exception as e:
            logger.error(f"Error during TTS stream generation: {e}")
            if 'fp' in locals() and os.path.exists(fp.name):
                 os.remove(fp.name)
            return

    def text_to_file(self, text: str, file_path: str):
        if not self.tts:
            logger.error("TTS model is not available for file generation.")
            raise RuntimeError("TTS model not loaded.")
        try:
            logger.info(f"Generating speech to file for text: {text}")
            self.tts.tts_to_file(text=text, file_path=file_path)
            logger.info(f"Speech generated and saved to {file_path}")
        except Exception as e:
            logger.error(f"Error during TTS file generation: {e}")
            raise

tts_service = TTSService()

if __name__ == "__main__":
    # This will trigger the TTS service and show all the logs
    audio_data = list(tts_service.text_to_speech_stream("Hello, this is a test"))
    print(f"Generated audio data: {len(audio_data)} chunks")