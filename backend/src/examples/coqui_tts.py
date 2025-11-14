import torch
from TTS.api import TTS

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# List available 🐸TTS models
print(TTS().list_models())

# Init TTS
# tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
tts = TTS("tts_models/en/ljspeech/vits").to(device)

# Run TTS
text = "Hi, I'm your personal doctor assistant. How can I help you today?"
# text = "Halo. Apakah kamu bisa Bahasa Indonesia?"
tts.tts_to_file(
    text=text, 
    file_path="output_en.wav"
)