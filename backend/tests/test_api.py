import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.main import app
from io import BytesIO

client = TestClient(app)

@pytest.fixture
def mock_process_query():
    async def mock_query_stream(user_query):
        response_chunks = ["This ", "is ", "a ", "mocked ", "streaming ", "response."]
        for chunk in response_chunks:
            yield chunk

    with patch("src.services.query_service.process_query", new=mock_query_stream) as _mock:
        yield _mock

def test_query_endpoint_streaming(mock_process_query):
    response = client.post("/query", json={"query_text": "test query", "input_modality": "TEXT"})
    assert response.status_code == 200
    
    # Since it's a streaming response, we can check if the content is what we expect
    # by concatenating the chunks.
    expected_response = "This is a mocked streaming response."
    # The actual response content will be a concatenation of the chunks.
    # The TestClient will read the streaming response and provide the full body.
    assert response.text == expected_response

def test_query_image_endpoint_valid_image():
    image_content = b"fake image data"
    response = client.post(
        "/query/image",
        files={"image": ("test.jpg", BytesIO(image_content), "image/jpeg")}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Image 'test.jpg' uploaded successfully"}

def test_query_image_endpoint_invalid_image_type():
    image_content = b"fake image data"
    response = client.post(
        "/query/image",
        files={"image": ("test.txt", BytesIO(image_content), "text/plain")}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid image type. Only JPG and PNG are accepted."}

def test_query_image_endpoint_image_too_large():
    # Create a file that is larger than 10 MB
    large_file_content = b"a" * (11 * 1024 * 1024)
    response = client.post(
        "/query/image",
        files={"image": ("large_image.jpg", BytesIO(large_file_content), "image/jpeg")}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Image is too large. Maximum size is 10 MB."}
