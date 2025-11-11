import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.main import app

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
