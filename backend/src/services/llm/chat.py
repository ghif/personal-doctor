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
import litellm

logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self):
        self.model_name = f"ollama_chat/{MODEL_NAME}"
        try:
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
                    if os.path.exists(image_data):
                        temp_image_path = image_data
                    else:
                        # Base64 string
                        image_bytes = base64.b64decode(image_data)
                        Image.open(io.BytesIO(image_bytes)) # Verify image
                        
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                            temp_file.write(image_bytes)
                            temp_image_path = temp_file.name
                    
                    with open(temp_image_path, "rb") as image_file:
                         base64_image = base64.b64encode(image_file.read()).decode('utf-8')
                    
                    messages[1]["content"].append({
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    })

                except (binascii.Error, UnidentifiedImageError):
                    yield "Error processing image: Invalid image data"
                    return
                except Exception as e:
                    yield f"Error processing image: {e}"
                    return

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
