from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
import logging
import re
import litellm
from src.core.config import MODEL_NAME

logger = logging.getLogger(__name__)

class SummaryService:
    def __init__(self):
        # Configuration for the ADK Model
        # Assuming ADK supports generic providers or has an 'ollama' provider extension
        # If native ollama is not supported, we might need 'openai' provider with base_url
        
        self.agent = None
        self.initialize_agent()

    def initialize_agent(self):
        try:
            logger.info("Initializing SummaryService")
            
            system_prompt = (
                "You are an expert medical summarizer. "
                "Your goal is to summarize the provided medical advice into a concise, single paragraph. "
                "Ensure the summary flows naturally when read aloud. "
                "YOU MUST USE periods (.) and commas (,) to create natural pauses. "
                "DO NOT use other punctuation marks like question marks (?), exclamation marks (!), colons (:), or semicolons (;). "
                "Keep the summary focused on the key medical advice and safety instructions."
            )
            
            self.agent = Agent(
                model=LiteLlm(model=f"ollama_chat/{MODEL_NAME}"),
                name="medical_summary_service",
                description="An agent that summarizes medical advice into concise paragraphs.",
                instruction=system_prompt
            )
            logger.info("SummaryService initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize SummaryService: {e}")
            # We don't raise here to allow the app to start, but summarize will fail
            self.agent = None

    async def summarize(self, text: str) -> str:
        if not text:
            return ""

        # Pre-processing: Check if text is short (e.g. < 50 words)
        # If so, skip LLM summarization but still strip punctuation
        word_count = len(text.split())
        if word_count < 50:
            logger.info(f"Text is short ({word_count} words), skipping LLM summarization")
            return self._strip_punctuation(text)

        if not self.agent:
            logger.warning("SummaryService not initialized, returning clean original text")
            return self._strip_punctuation(text)
            
        try:
            prompt = f"Summarize the following text into a single paragraph. Use periods and commas for pauses. Do not use other punctuation:\n\n{text}"
            response = await self.agent.run(prompt)
            # ADK response structure might vary, assuming .text or str(response) works
            summary = response.text if hasattr(response, 'text') else str(response)
            
            return self._strip_punctuation(summary)
        except Exception as e:
            logger.error(f"Error during summarization: {e}")
            # Fallback: Return original text but stripped of punctuation to meet audio constraints
            return self._strip_punctuation(text)

    async def summarize_stream(self, text: str):
        """
        Summarizes the provided text into a concise paragraph, streaming the output chunks.
        """
        if not text:
            yield ""
            return

        word_count = len(text.split())
        if word_count < 50:
            logger.info(f"Text is short ({word_count} words), returning stripped text directly")
            yield self._strip_punctuation(text)
            return

        try:
            logger.info("Starting streaming summarization")
            
            system_instruction = (
                "You are an expert medical summarizer. "
                "Your goal is to summarize the provided medical advice into a concise, single paragraph. "
                "Ensure the summary flows naturally when read aloud. "
                "YOU MUST USE periods (.) and commas (,) to create natural pauses. "
                "DO NOT use other punctuation marks like question marks (?), exclamation marks (!), colons (:), or semicolons (;). "
                "Keep the summary focused on the key medical advice and safety instructions."
            )
            
            prompt = f"Summarize the following text into a single paragraph. Use periods and commas for pauses. Do not use other punctuation:\n\n{text}"

            messages = [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt}
            ]

            # Use litellm.acompletion directly for streaming
            response = await litellm.acompletion(
                model=f"ollama/{MODEL_NAME}",
                messages=messages,
                stream=True
            )

            async for chunk in response:
                content = chunk.choices[0].delta.content
                if content:
                    # Ideally we would strip punctuation on the fly, 
                    # but simple regex per chunk might be risky if a token splits a special char.
                    # Given the prompt instructs the model to remove punctuation, we rely on that mostly,
                    # or apply a safe filter.
                    # For safety, we can apply a simple filter or just yield as is and trust prompt + post-processing if needed.
                    # The requirement says "The Backend MUST stream the summary text... as it is generated".
                    yield self._strip_punctuation_stream(content)
                    
        except Exception as e:
            logger.error(f"Error during streaming summarization: {e}")
            # Fallback
            yield self._strip_punctuation(text)

    def _strip_punctuation_stream(self, text: str) -> str:
        # Lighter version for chunks, avoiding strip() which kills spaces between chunks
        clean_text = re.sub(r'[^a-zA-Z0-9_., ]', '', text)
        return clean_text

    def _strip_punctuation(self, text: str) -> str:
        # Remove characters that are not alphanumeric, spaces, periods, or commas
        clean_text = re.sub(r'[^a-zA-Z0-9_., ]', '', text)
        # Normalize whitespace (collapse multiple spaces, strip leading/trailing)
        return re.sub(r'\s+', ' ', clean_text).strip()

