from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
import logging
import re
from src.config import MODEL_NAME

logger = logging.getLogger(__name__)

class SummaryAgent:
    def __init__(self):
        # Configuration for the ADK Model
        # Assuming ADK supports generic providers or has an 'ollama' provider extension
        # If native ollama is not supported, we might need 'openai' provider with base_url
        
        self.agent = None
        self.initialize_agent()

    def initialize_agent(self):
        try:
            logger.info("Initializing SummaryAgent")
            
            system_prompt = (
                "You are an expert medical summarizer. "
                "Your goal is to summarize the provided medical advice into a concise, single paragraph. "
                "Do not lose critical safety information, but remove verbose explanations. "
                "The output must contain spaces, numbers, dots, and commas as punctuation marks. "
                "Remove question marks, exclamation marks, colons, and semicolons. "
                "The output must be a continuous stream of words and numbers with appropriate spacing and allowed punctuation."
            )
            
            self.agent = Agent(
                model=LiteLlm(model=f"ollama_chat/{MODEL_NAME}"),
                name="medical_summary_agent",
                description="An agent that summarizes medical advice into concise paragraphs.",
                instruction=system_prompt
            )
            logger.info("SummaryAgent initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize SummaryAgent: {e}")
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
            logger.warning("SummaryAgent not initialized, returning clean original text")
            return self._strip_punctuation(text)
            
        try:
            prompt = f"Summarize the following text into a single paragraph without specific punctuation, retaining spaces, numbers, dots, and commas:\n\n{text}"
            response = await self.agent.run(prompt)
            # ADK response structure might vary, assuming .text or str(response) works
            summary = response.text if hasattr(response, 'text') else str(response)
            
            return self._strip_punctuation(summary)
        except Exception as e:
            logger.error(f"Error during summarization: {e}")
            # Fallback: Return original text but stripped of punctuation to meet audio constraints
            return self._strip_punctuation(text)

    def _strip_punctuation(self, text: str) -> str:
        # Remove characters that are not alphanumeric, spaces, periods, or commas
        clean_text = re.sub(r'[^a-zA-Z0-9_., ]', '', text)
        # Normalize whitespace (collapse multiple spaces, strip leading/trailing)
        return re.sub(r'\s+', ' ', clean_text).strip()

