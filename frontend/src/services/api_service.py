import requests
import config
from typing import Optional
from streamlit.runtime.uploaded_file_manager import UploadedFile

def query_backend(prompt: str, image_file: Optional[UploadedFile] = None):
    if image_file:
        files = {'image': (image_file.name, image_file, image_file.type)}
        data = {'prompt': prompt}
        with requests.post(
            f"{config.BACKEND_URL}/query/image",
            files=files,
            data=data,
            stream=True,
        ) as r:
            for chunk in r.iter_content(chunk_size=None):
                if chunk:
                    yield chunk.decode('utf-8')

    else:
        payload = {
            "query_text": prompt,
            "input_modality": "TEXT"
        }
        with requests.post(
            f"{config.BACKEND_URL}/query",
            json=payload,
            stream=True,
        ) as r:
            for chunk in r.iter_content(chunk_size=None):
                if chunk:
                    yield chunk.decode('utf-8')

def transcribe_audio(audio_file_path: str):
    with open(audio_file_path, "rb") as f:
        files = {'file': ('audio.wav', f, 'audio/wav')}
        response = requests.post(f"{config.BACKEND_URL}/transcribe", files=files)
        response.raise_for_status()
        return response.json()["text"]

def get_summary_stream(text: str):
    payload = {"text": text}
    with requests.post(
        f"{config.BACKEND_URL}/summary_stream",
        json=payload,
        stream=True,
    ) as r:
        r.raise_for_status()
        for chunk in r.iter_content(chunk_size=None):
            if chunk:
                yield chunk.decode('utf-8')

def get_tts_audio(text: str):
    # This endpoint is expected to exist from previous feature (004/006)
    # Reusing /tts or /summary-tts but we need raw text-to-speech for the summarized text.
    # The spec 004 mentions /tts. Let's assume /tts exists for raw text.
    payload = {"text": text}
    response = requests.post(
        f"{config.BACKEND_URL}/tts",
        json=payload,
        stream=True
    )
    response.raise_for_status()
    return response.content

def get_summary_tts(text: str) -> bytes:
    """
    Generate a summary of the text and convert it to speech using the backend API
    """
    if not text or text.strip() == "":
        print("No text provided for Summary TTS")
        return b""

    url = f"{config.BACKEND_URL}/summary-tts"

    try:
        payload = {"text": text.strip()}
        print(f"Sending Summary TTS request to: {url}")
        print(f"Payload: {payload}")

        response = requests.post(url, json=payload, timeout=60) # Increased timeout for summarization
        print(f"Response status: {response.status_code}")
        response.raise_for_status()

        audio_content = response.content
        print(f"Received audio content: {len(audio_content)} bytes")

        if len(audio_content) == 0:
            print("Warning: Received empty audio content")

        return audio_content

    except requests.exceptions.ConnectionError as e:
        print(f"Connection error - TTS backend may not be running: {e}")
        return b""
    except requests.exceptions.Timeout as e:
        print(f"Summary TTS request timeout: {e}")
        return b""
    except requests.exceptions.RequestException as e:
        print(f"Error generating Summary TTS: {e}")
        print(f"Response text: {e.response.text if hasattr(e, 'response') and e.response else 'No response'}")
        return b""
    except Exception as e:
        print(f"Unexpected error during Summary TTS: {e}")
        return b""
