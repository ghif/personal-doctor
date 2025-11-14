import whisper
import streamlit as st

@st.cache_resource
def load_model():
    # model = whisper.load_model("base")
    model = whisper.load_model("small")
    return model

def transcribe_audio(audio_file_path):
    model = load_model()
    result = model.transcribe(audio_file_path)
    return result["text"]