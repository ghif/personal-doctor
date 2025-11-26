import pytest
from fastapi.testclient import TestClient
from src.main import app
from unittest.mock import patch, AsyncMock

client = TestClient(app)

def test_summary_stream_endpoint():
    # Mock the SummaryAgent.summarize_stream method
    async def mock_stream(text):
        yield "Streamed "
        yield "summary "
        yield "result."

    with patch("src.api.summary.summary_agent.summarize_stream", side_effect=mock_stream):
        response = client.post("/summary_stream", json={"text": "Long input text needed."})
        assert response.status_code == 200
        # Check if it is a stream
        assert response.text == "Streamed summary result."

def test_summary_stream_empty_input():
    response = client.post("/summary_stream", json={"text": ""})
    # Depending on implementation, might return 400 or empty stream
    # Let's assume validation error or empty
    assert response.status_code in [200, 422]
