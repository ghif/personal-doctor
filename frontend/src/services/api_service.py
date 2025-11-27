import requests
import config
from typing import Optional, Generator
from streamlit.runtime.uploaded_file_manager import UploadedFile

def _stream_response(url: str, json_data: dict = None, files: dict = None, data: dict = None) -> Generator[str, None, None]:
    """Helper generator to stream text chunks from a response."""
    with requests.post(url, json=json_data, files=files, data=data, stream=True) as r:
        r.raise_for_status()
        for chunk in r.iter_content(chunk_size=None):
            if chunk:
                yield chunk.decode('utf-8')

def query_backend(prompt: str, image_file: Optional[UploadedFile] = None) -> Generator[str, None, None]:
    """Queries the backend chat endpoint, optionally with an image."""
    if image_file:
        files = {'image': (image_file.name, image_file, image_file.type)}
        data = {'prompt': prompt}
        yield from _stream_response(f"{config.BACKEND_URL}/query/image", files=files, data=data)
    else:
        payload = {
            "query_text": prompt,
            "input_modality": "TEXT"
        }
        yield from _stream_response(f"{config.BACKEND_URL}/query", json_data=payload)

def transcribe_audio(audio_file_path: str) -> str:
    """Transcribes the given audio file."""
    with open(audio_file_path, "rb") as f:
        files = {'file': ('audio.wav', f, 'audio/wav')}
        response = requests.post(f"{config.BACKEND_URL}/transcribe", files=files)
        response.raise_for_status()
        return response.json()["text"]

def get_summary_stream(text: str) -> Generator[str, None, None]:
    """Streams a text summary of the input text."""
    payload = {"text": text}
    yield from _stream_response(f"{config.BACKEND_URL}/summary_stream", json_data=payload)

def get_tts_audio(text: str) -> bytes:
    """Gets raw TTS audio for the given text."""
    payload = {"text": text}
    response = requests.post(
        f"{config.BACKEND_URL}/tts",
        json=payload,
        stream=True
    )
    response.raise_for_status()
    return response.content

def get_summary_tts(text: str) -> bytes:
    """Gets TTS audio for a backend-generated summary of the text."""
    if not text or not text.strip():
        return b""

    url = f"{config.BACKEND_URL}/summary-tts"
    payload = {"text": text.strip()}
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching summary TTS: {e}")
        return b""
