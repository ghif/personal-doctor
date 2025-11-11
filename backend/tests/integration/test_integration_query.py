import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from src.main import app
import os

client = TestClient(app)

@pytest.fixture
def mock_ollama_chat():
    """
    Mocks the ollama.AsyncClient.chat function to return a streaming response.
    """
    mock_chat_stream = AsyncMock()
    
    async def async_gen():
        response_chunks = [
            {'message': {'content': "This "}},
            {'message': {'content': "is "}},
            {'message': {'content': "a "}},
            {'message': {'content': "mocked "}},
            {'message': {'content': "Ollama "}},
            {'message': {'content': "response."}},
        ]
        for chunk in response_chunks:
            yield chunk
            
    mock_chat_stream.return_value = async_gen()

    with patch("src.services.query_service.AsyncClient.chat", new=mock_chat_stream) as mock:
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
    with patch("src.services.query_service.AsyncClient.chat", new=mock_chat_stream):
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

@patch("src.services.query_service.os.remove")
@patch("src.services.query_service.tempfile.NamedTemporaryFile")
def test_query_endpoint_image_file_cleanup(mock_tempfile, mock_os_remove, mock_ollama_chat):
    """
    Tests that the temporary image file is cleaned up after the query.
    """
    mock_file = mock_tempfile.return_value.__enter__.return_value
    mock_file.name = "/tmp/fake_image.png"

    image_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
    
    # We need to patch os.path.exists to return True so that os.remove is called.
    with patch("src.services.query_service.os.path.exists", return_value=True):
        response = client.post(
            "/query",
            json={
                "query_text": "test query with image for cleanup",
                "input_modality": "MULTIMODAL",
                "image_data": image_data,
            },
        )
        assert response.status_code == 200
    
    mock_os_remove.assert_called_once_with("/tmp/fake_image.png")
