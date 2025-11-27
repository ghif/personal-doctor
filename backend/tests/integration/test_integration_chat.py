import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock
from src.main import app
import os
from io import BytesIO

client = TestClient(app)

@pytest.fixture
def mock_ollama_chat():
    """
    Mocks the litellm.acompletion function to return a streaming response.
    """
    mock_chat_stream = AsyncMock()
    
    async def async_gen(*args, **kwargs):
        response_chunks = ["This ", "is ", "a ", "mocked ", "Ollama ", "response."]
        for content in response_chunks:
            mock_chunk = MagicMock()
            mock_chunk.choices = [MagicMock()]
            mock_chunk.choices[0].delta.content = content
            yield mock_chunk
            
    mock_chat_stream.side_effect = async_gen

    with patch("src.services.llm.chat.litellm.acompletion", new=mock_chat_stream) as mock:
        yield mock

def test_query_endpoint_integration_streaming(mock_ollama_chat):
    """
    Tests the /query endpoint with a mocked Ollama service.
    This is an integration test that checks the API and the service layer.
    """
    response = client.post("/query", json={"query_text": "test query", "input_modality": "TEXT"})
    assert response.status_code == 200
    
    expected_response = "This is a mocked Ollama response."
    assert response.text == expected_response

def test_query_endpoint_with_image_integration(mock_ollama_chat):
    """
    Tests the /query endpoint with image data.
    """
    image_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
    
    response = client.post(
        "/query",
        json={
            "query_text": "test query with image",
            "input_modality": "MULTIMODAL",
            "image_data": image_data,
        },
    )
    assert response.status_code == 200
    
    expected_response = "This is a mocked Ollama response."
    assert response.text == expected_response

def test_query_endpoint_ollama_error():
    """
    Tests that the endpoint handles errors from the ollama service gracefully.
    """
    mock_chat_stream = AsyncMock(side_effect=Exception("Ollama connection failed"))
    with patch("src.services.llm.chat.litellm.acompletion", new=mock_chat_stream):
        response = client.post("/query", json={"query_text": "test query", "input_modality": "TEXT"})
        assert response.status_code == 200
        assert "An error occurred while querying the model: Ollama connection failed" in response.text

def test_query_endpoint_invalid_image_data():
    """
    Tests the endpoint's response to invalid base64 image data.
    """
    response = client.post(
        "/query",
        json={
            "query_text": "test with invalid image",
            "input_modality": "MULTIMODAL",
            "image_data": "this is not valid base64",
        },
    )
    assert response.status_code == 200
    assert "Error processing image: Invalid image data" in response.text

def test_query_image_integration(mock_ollama_chat):
    """
    Tests the /query/image endpoint with a file upload.
    """
    image_content = b"fake image data"
    response = client.post(
        "/query/image",
        files={"image": ("test.jpg", BytesIO(image_content), "image/jpeg")}
    )
    assert response.status_code == 200
    expected_response = "This is a mocked Ollama response."
    assert response.text == expected_response
    # Check if the file was saved
    assert os.path.exists("temp_images/test.jpg")
    # Clean up the created file
    os.remove("temp_images/test.jpg")

def test_multimodal_query_integration(mock_ollama_chat):
    """
    Tests the /query/image endpoint with a file upload and a text prompt.
    """
    image_content = b"fake image data"
    prompt_text = "This is a test prompt."
    response = client.post(
        "/query/image",
        files={"image": ("test.jpg", BytesIO(image_content), "image/jpeg")},
        data={"prompt": prompt_text}
    )
    assert response.status_code == 200
    expected_response = "This is a mocked Ollama response."
    assert response.text == expected_response
    # Check if the file was saved
    assert os.path.exists("temp_images/test.jpg")
    # Clean up the created file
    os.remove("temp_images/test.jpg")
