from .api_service import transcribe_audio as transcribe_audio_backend

def transcribe_audio(audio_file_path):
    return transcribe_audio_backend(audio_file_path)