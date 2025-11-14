import requests
import config
from typing import Optional
from streamlit.runtime.uploaded_file_manager import UploadedFile

def query_backend(prompt: str, image_file: Optional[UploadedFile] = None):
    if image_file:
        files = {'image': (image_file.name, image_file, image_file.type)}
        data = {'prompt': prompt}
        with requests.post(
            f"{config.BACKEND_URL}/query/image",
            files=files,
            data=data,
            stream=True,
        ) as r:
            for chunk in r.iter_content(chunk_size=None):
                if chunk:
                    yield chunk.decode('utf-8')

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
