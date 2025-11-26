import pytest
from unittest.mock import MagicMock, patch

from src.agents.summary_agent import SummaryAgent

@pytest.fixture
def mock_agent_class():
    with patch("src.agents.summary_agent.Agent") as mock:
        yield mock

@pytest.mark.asyncio
async def test_summarize_success(mock_agent_class):
    # Setup
    mock_agent_instance = mock_agent_class.return_value
    mock_agent_instance.run = MagicMock()
    
    # Mock async run response
    async def async_response(prompt):
        response_mock = MagicMock()
        response_mock.text = "This is a summary."
        return response_mock
    
    mock_agent_instance.run.side_effect = async_response

    agent = SummaryAgent()
    
    # Execute
    original_text = "This is a very long text that needs summarization." * 10
    summary = await agent.summarize(original_text)
    
    # Verify
    assert summary == "This is a summary."
    mock_agent_instance.run.assert_called_once()
    args, _ = mock_agent_instance.run.call_args
    assert "Summarize the following text" in args[0]
    assert original_text in args[0]

@pytest.mark.asyncio
async def test_summarize_failure_fallback(mock_agent_class):
    # Setup
    mock_agent_instance = mock_agent_class.return_value
    mock_agent_instance.run.side_effect = Exception("ADK Error")
    
    agent = SummaryAgent()
    
    # Execute
    original_text = "Original text."
    summary = await agent.summarize(original_text)
    
    # Verify fallback
    assert summary == "Original text."

@pytest.mark.asyncio
async def test_summarize_punctuation_removal(mock_agent_class):
    # Setup
    mock_agent_instance = mock_agent_class.return_value
    mock_agent_instance.run = MagicMock()
    
    # Mock async run response with punctuation
    async def async_response(prompt):
        response_mock = MagicMock()
        response_mock.text = "This is a summary, with commas! And periods."
        return response_mock
    
    mock_agent_instance.run.side_effect = async_response

    agent = SummaryAgent()
    
    # Execute
    summary = await agent.summarize("Input text")
    
    # Verify regex cleaning (keep only words and spaces)
    assert summary == "Input text"
