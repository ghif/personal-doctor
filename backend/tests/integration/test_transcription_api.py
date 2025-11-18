# backend/tests/integration/test_transcription_api.py

import pytest
from fastapi.testclient import TestClient
from src.main import app
import wave
import os
from unittest.mock import patch

client = TestClient(app)

@pytest.fixture
def dummy_audio_file():
    file_path = "dummy_audio_for_integration.wav"
    with wave.open(file_path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(16000)
        wf.writeframes(b'\x00\x00' * 16000) # 1 second of silence
    yield file_path
    os.remove(file_path)

@patch('src.services.transcription_service.TranscriptionService.transcribe')
def test_transcribe_audio_success(mock_transcribe, dummy_audio_file):
    mock_transcribe.return_value = "mocked transcription"
    with open(dummy_audio_file, "rb") as f:
        response = client.post(
            "/transcribe",
            files={'file': ("audio.wav", f, "audio/wav")}
        )

    assert response.status_code == 200
    assert response.json() == {"text": "mocked transcription"}

def test_transcribe_audio_invalid_file_type():
    response = client.post(
        "/transcribe",
        files={'file': ("image.jpg", b"dummy_image_data", "image/jpeg")}
    )
    assert response.status_code == 400
    assert "detail" in response.json()
    assert "Invalid file type" in response.json()["detail"]

def test_transcribe_audio_no_file():
    response = client.post(
        "/transcribe",
        files={}
    )
    assert response.status_code == 422 # Unprocessable Entity for missing file