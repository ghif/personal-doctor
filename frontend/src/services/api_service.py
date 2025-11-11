import requests
from src import config
from typing import Optional
import streamlit as st

def query_backend(prompt: str, image_file: Optional[st.uploaded_file_manager.UploadedFile] = None):
    if image_file:
        files = {'image': (image_file.name, image_file, image_file.type)}
        with requests.post(
            f"{config.BACKEND_URL}/query/image",
            files=files,
            stream=True,
        ) as r:
            if r.status_code == 200:
                # This is not a streaming response, so we read the whole body
                response_data = r.json()
                yield response_data.get("message", "")
            else:
                yield f"Error: {r.status_code} - {r.text}"

    else:
        payload = {
            "query_text": prompt,
            "input_modality": "TEXT"
        }
        with requests.post(
            f"{config.BACKEND_URL}/query",
            json=payload,
            stream=True,
        ) as r:
            for chunk in r.iter_content(chunk_size=None):
                if chunk:
                    yield chunk.decode('utf-8')
