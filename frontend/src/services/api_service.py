import requests
from src import config
from typing import Optional

def query_backend(prompt: str, image_data: Optional[str] = None):
    payload = {
        "query_text": prompt,
        "input_modality": "TEXT"
    }
    if image_data:
        payload["image_data"] = image_data
        payload["input_modality"] = "IMAGE"

    with requests.post(
        f"{config.BACKEND_URL}/query",
        json=payload,
        stream=True,
    ) as r:
        for chunk in r.iter_content(chunk_size=None):
            if chunk:
                yield chunk.decode('utf-8')
