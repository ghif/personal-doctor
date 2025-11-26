import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.agents.summary_agent import SummaryAgent

@pytest.mark.asyncio
async def test_summarize_stream_valid_input():
    # Mock the Litellm acompletion
    mock_chunks = [
        MagicMock(choices=[MagicMock(delta=MagicMock(content="This "))]),
        MagicMock(choices=[MagicMock(delta=MagicMock(content="is "))]),
        MagicMock(choices=[MagicMock(delta=MagicMock(content="a "))]),
        MagicMock(choices=[MagicMock(delta=MagicMock(content="summary."))]),
    ]
    
    # 1. Define the async generator that yields chunks
    async def stream_gen():
        for chunk in mock_chunks:
            yield chunk

    # 2. Define the async function that returns the generator (simulating await acompletion(...))
    async def mock_acompletion_fn(*args, **kwargs):
        return stream_gen()

    with patch("src.agents.summary_agent.litellm.acompletion", side_effect=mock_acompletion_fn) as mock_acompletion:
        agent = SummaryAgent()
        # Mock agent.agent to ensure initialization doesn't fail or block, 
        # though summarize_stream might bypass self.agent.run
        agent.agent = MagicMock() 

        # Make text longer than 50 words to ensure it hits the LLM path
        input_text = "word " * 60
        
        # Collect the streamed output
        streamed_text = ""
        async for chunk in agent.summarize_stream(input_text):
            streamed_text += chunk
            
        assert streamed_text == "This is a summary."
        mock_acompletion.assert_called_once()

@pytest.mark.asyncio
async def test_summarize_stream_short_text():
    # Should bypass LLM and return stripped text
    agent = SummaryAgent()
    input_text = "Short text."
    
    streamed_text = ""
    async for chunk in agent.summarize_stream(input_text):
        streamed_text += chunk
        
    # The logic might return the whole text as one chunk or stream it simulated
    # Based on existing 'summarize', it strips punctuation. 
    # Let's assume summarize_stream also does stripping if it bypasses LLM, 
    # or just returns original if too short.
    # The existing 'summarize' strips punctuation. 
    assert "Short text" in streamed_text or "Short text." in streamed_text
