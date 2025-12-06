from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import StreamingResponse
from src.schemas.chat import UserQuery
from src.services.llm.chat import ChatService
import shutil
import os
from typing import Optional

router = APIRouter()

# Create a directory for temporary file storage
TEMP_DIR = "temp_images"
os.makedirs(TEMP_DIR, exist_ok=True)

# Initialize the service
chat_service = ChatService()

async def process_query_stream(user_query: UserQuery):
    """
    Process the user query using the ChatService.
    """
    async for chunk in chat_service.process_query(user_query.query_text, user_query.image_data):
        yield chunk

@router.post("/query")
async def query(user_query: UserQuery):
    return StreamingResponse(process_query_stream(user_query), media_type="text/event-stream")

@router.post("/query/image")
async def query_image(image: UploadFile = File(...), prompt: Optional[str] = Form(None)):
    # Validate file type
    if image.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Invalid image type. Only JPG and PNG are accepted.")

    # Validate file size (10 MB limit)
    if image.file.seek(0, 2) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image is too large. Maximum size is 10 MB.")
    image.file.seek(0)

    # Save the file to a temporary directory
    temp_file_path = os.path.join(TEMP_DIR, image.filename)
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    user_query = UserQuery(
        query_text=prompt,
        input_modality="MULTIMODAL" if prompt else "IMAGE",
        image_data=temp_file_path
    )

    return StreamingResponse(process_query_stream(user_query), media_type="text/event-stream")
