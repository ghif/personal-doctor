import requests
import config

def tts_service(text: str) -> bytes:
    """
    Convert text to speech using the backend API
    """
    if not text or text.strip() == "":
        print("No text provided for TTS")
        return b""
        
    url = f"{config.BACKEND_URL}/tts"
    
    try:
        payload = {"text": text.strip()}
        print(f"Sending TTS request to: {url}")
        print(f"Payload: {payload}")
        
        response = requests.post(url, json=payload, timeout=30)
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
        print(f"TTS request timeout: {e}")
        return b""
    except requests.exceptions.RequestException as e:
        print(f"Error generating TTS: {e}")
        print(f"Response text: {e.response.text if hasattr(e, 'response') and e.response else 'No response'}")
        return b""
    except Exception as e:
        print(f"Unexpected error during TTS: {e}")
        return b""

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
