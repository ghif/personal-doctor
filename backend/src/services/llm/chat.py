from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
import logging
from src.core.config import MODEL_NAME
import os
import base64
import tempfile
import binascii
from PIL import Image, UnidentifiedImageError
import io
import os
import litellm

logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self):
        os.environ['LITELLM_LOG'] = 'DEBUG'
        self.model_name = f"ollama_chat/{MODEL_NAME}"
        try:
            # We initialize the LiteLlm model.
            # Note: For streaming and advanced multimodal features (local images), 
            # we might interact with the underlying litellm library or the model wrapper directly 
            # if the Agent abstraction doesn't expose streaming natively.
            self.model = LiteLlm(model=self.model_name)
            
            system_prompt = (
                "You are a helpful medical assistant. "
                "Answer the user's questions accurately and concisely. Always answer in English. "
                "If an image is provided, analyze it in the context of the medical question."
            )
            
            self.agent = Agent(
                model=self.model,
                name="medical_chat_service",
                description="An agent that answers medical queries, optionally with images.",
                instruction=system_prompt
            )
            logger.info("ChatService initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize ChatService: {e}")
            self.agent = None

    async def process_query(self, query_text: str, image_data: str = None):
        """
        Processes a user query, optionally with image data, and yields the response chunks.
        """
        temp_image_path = None
        try:
            messages = [
                {
                    "role": "system",
                    "content": self.agent.instruction
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": query_text}
                    ]
                }
            ]

            # Handle image data
            if image_data:
                try:
                    raw_image_bytes = None
                    if os.path.exists(image_data):
                        with open(image_data, "rb") as f:
                            raw_image_bytes = f.read()
                        temp_image_path = image_data # Retain original path if it was a file
                    else:
                        # Base64 string might have a prefix like "data:image/jpeg;base64,"
                        if "," in image_data:
                            image_data = image_data.split(',')[1]
                        
                        raw_image_bytes = base64.b64decode(image_data)

                    # Encode image bytes to base64 for embedding in the message content
                    base64_image_for_payload = base64.b64encode(raw_image_bytes).decode("utf-8")
                    
                    # For Ollama, the image is added to the content list
                    messages[1]["content"] = [
                        {"type": "text", "text": query_text},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": base64_image_for_payload
                            }
                        }
                    ]

                except (binascii.Error, UnidentifiedImageError) as e:
                    logger.error(f"Error processing image: {e}. First 30 chars: {image_data[:30] if isinstance(image_data, str) else 'N/A'}")
                    yield "Error processing image: Invalid image data"
                    return
                except Exception as e:
                    logger.error(f"Error processing image: {e}")
                    yield f"Error processing image: {e}"
                    return
            else:
                messages[1]["content"] = [{"type": "text", "text": query_text}]

            # Execute streaming call
            # We use litellm.acompletion directly because Agent.run usually doesn't expose stream iterator easily
            # But we use the model configured in the agent.
            
            # Note: self.model.model contains the model name string
            
            response = await litellm.acompletion(
                model=self.model_name,
                messages=messages,
                stream=True,
                api_base=os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
            )
            
            async for chunk in response:
                content = chunk.choices[0].delta.content
                if content:
                    yield content

        except Exception as e:
            logger.error(f"Error in ChatService: {e}")
            yield f"An error occurred while querying the model: {e}"
        finally:
            if temp_image_path and os.path.exists(temp_image_path) and "temp_images" not in temp_image_path:
                os.remove(temp_image_path)
