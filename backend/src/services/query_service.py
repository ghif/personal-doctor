from src.models.models import UserQuery
from ollama import AsyncClient
from src import config
import base64
import uuid
import os
import tempfile
import binascii
from PIL import Image, UnidentifiedImageError
import io

async def process_query(user_query: UserQuery):
    temp_image_path = None
    try:
        messages = [{
            'role': 'user',
            'content': user_query.query_text,
        }]
        
        # Handle image data if it exists
        if user_query.image_data:
            try:
                # Check if image_data is a path or base64 string
                if os.path.exists(user_query.image_data):
                    temp_image_path = user_query.image_data
                else:
                    # The image_data is a base64 string, decode it
                    image_bytes = base64.b64decode(user_query.image_data)
                    
                    # Try to open the image to verify it's a valid image
                    Image.open(io.BytesIO(image_bytes))

                    # Create a temporary file to store the image
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                        temp_file.write(image_bytes)
                        temp_image_path = temp_file.name
                
                # Add the image path to the message for Ollama
                messages[0]['images'] = [temp_image_path]
            except (binascii.Error, UnidentifiedImageError):
                # If image processing fails, yield an error and stop
                yield f"Error processing image: Invalid image data"
                return
            except Exception as e:
                # If image processing fails, yield an error and stop
                yield f"Error processing image: {e}"
                return

        stream = await AsyncClient().chat(
            model=config.MODEL_NAME,
            messages=messages,
            stream=True,
        )
        async for chunk in stream:
            yield chunk['message']['content']
    except Exception as e:
        yield f"An error occurred while querying the model: {e}"
    finally:
        # Clean up the temporary file if it was created and it's not the one from the temp_images folder
        if temp_image_path and os.path.exists(temp_image_path) and "temp_images" not in temp_image_path:
            os.remove(temp_image_path)

