# backend/tests/unit/test_transcription_service.py

import pytest
from unittest.mock import MagicMock, patch
from src.services.audio.transcription import TranscriptionService

@pytest.fixture
def mock_whisper():
    with patch('whisper.load_model') as mock_load_model:
        mock_model = MagicMock()
        mock_model.transcribe.return_value = {"text": "mocked transcription"}
        mock_load_model.return_value = mock_model
        yield mock_load_model

def test_transcription_service_init(mock_whisper):
    service = TranscriptionService()
    mock_whisper.assert_called_once_with("small")
    assert service.model is not None

def test_transcribe_success(mock_whisper):
    service = TranscriptionService()
    result = service.transcribe("dummy_audio.wav")
    assert result == "mocked transcription"
    service.model.transcribe.assert_called_once_with("dummy_audio.wav")