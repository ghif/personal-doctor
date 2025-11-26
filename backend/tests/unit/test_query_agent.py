import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from src.agents.query_agent import QueryAgent

@pytest.fixture
def mock_litellm_acompletion():
    with patch("src.agents.query_agent.litellm.acompletion", new_callable=AsyncMock) as mock:
        yield mock

@pytest.fixture
def mock_agent_class():
    with patch("src.agents.query_agent.Agent") as mock:
        yield mock

@pytest.fixture
def mock_litellm_class():
    with patch("src.agents.query_agent.LiteLlm") as mock:
        yield mock

@pytest.mark.asyncio
async def test_process_query_text_only(mock_litellm_acompletion, mock_agent_class, mock_litellm_class):
    # Setup mock response
    async def async_gen(*args, **kwargs):
        chunks = ["Hello", " world"]
        for c in chunks:
            mock_chunk = MagicMock()
            mock_chunk.choices = [MagicMock()]
            mock_chunk.choices[0].delta.content = c
            yield mock_chunk

    mock_litellm_acompletion.side_effect = async_gen
    
    agent = QueryAgent()
    
    # Execute
    response = []
    async for chunk in agent.process_query("Test query"):
        response.append(chunk)
    
    # Verify
    assert "".join(response) == "Hello world"
    mock_litellm_acompletion.assert_called_once()
    call_args = mock_litellm_acompletion.call_args[1]
    assert call_args["messages"][1]["content"][0]["text"] == "Test query"

@pytest.mark.asyncio
async def test_process_query_with_base64_image(mock_litellm_acompletion, mock_agent_class, mock_litellm_class):
    # Setup mock response
    mock_litellm_acompletion.return_value.__aiter__.return_value = []
    
    agent = QueryAgent()
    
    # Valid 1x1 pixel PNG base64
    valid_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mnk+A8AAQUBAScY42YAAAAASUVORK5CYII="
    
    # Execute
    async for _ in agent.process_query("Test with image", valid_base64):
        pass
        
    # Verify
    mock_litellm_acompletion.assert_called_once()
    call_args = mock_litellm_acompletion.call_args[1]
    content = call_args["messages"][1]["content"]
    assert len(content) == 2
    assert content[1]["type"] == "image_url"
    assert valid_base64 in content[1]["image_url"]["url"]

@pytest.mark.asyncio
async def test_process_query_invalid_image(mock_litellm_acompletion, mock_agent_class, mock_litellm_class):
    agent = QueryAgent()
    
    # Execute
    response = []
    async for chunk in agent.process_query("Test", "invalid_base64"):
        response.append(chunk)
        
    # Verify
    assert "Error processing image" in "".join(response)
    mock_litellm_acompletion.assert_not_called()
