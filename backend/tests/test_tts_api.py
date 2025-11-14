
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.main import app

client = TestClient(app)

@pytest.fixture
def mock_tts_service():
    # Create a mock for the tts_service object
    mock_service = MagicMock()

    # Define the behavior of the mock's text_to_speech_stream method
    def mock_text_to_speech_stream(text: str):
        # Simulate an audio stream
        audio_content = f"fake audio data for {text}".encode("utf-8")
        # The service returns a generator/stream, so we yield the content
        yield audio_content

    # Assign the mock method to the mock service instance
    mock_service.text_to_speech_stream.side_effect = mock_text_to_speech_stream

    # Patch the tts_service object in the api module where it is used
    with patch("src.api.tts.tts_service", new=mock_service) as _mock:
        yield _mock

def test_tts_endpoint_success(mock_tts_service):
    """
    Tests the /tts endpoint with a valid request.
    """
    response = client.post("/tts", json={"text": "hello world"})
    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/wav"
    # The TestClient will consume the stream and provide the full content
    assert response.content == b"fake audio data for hello world"

def test_tts_endpoint_empty_text(mock_tts_service):
    """
    Tests the /tts endpoint with an empty text string.
    """
    response = client.post("/tts", json={"text": ""})
    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/wav"
    assert response.content == b"fake audio data for "

def test_tts_endpoint_internal_error(mock_tts_service):
    """
    Tests the /tts endpoint when the service raises an exception.
    """
    # Configure the mock to raise an exception
    mock_tts_service.text_to_speech_stream.side_effect = Exception("TTS service failed")

    response = client.post("/tts", json={"text": "this will fail"})
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal Server Error"}
