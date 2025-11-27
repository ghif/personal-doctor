
import pytest
from src.services.audio.tts import TTSService

@pytest.fixture(scope="module")
def tts_service_instance():
    """
    Provides a singleton instance of the TTSService for the test module.
    This avoids reloading the model for every single test function.
    """
    return TTSService()

def test_tts_service_produces_valid_audio_stream(tts_service_instance):
    """
    Tests that the TTSService can generate a non-empty audio stream.
    """
    text = "this is a test."
    audio_stream = tts_service_instance.text_to_speech_stream(text)
    
    # Consume the stream
    audio_chunks = list(audio_stream)
    
    # Check that the stream is not empty
    assert len(audio_chunks) > 0
    
    # Check that the content of the stream is bytes
    for chunk in audio_chunks:
        assert isinstance(chunk, bytes)
    
    # Combine the chunks to get the full audio data
    audio_data = b"".join(audio_chunks)
    assert len(audio_data) > 100 # Check for a reasonable amount of data
