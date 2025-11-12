import streamlit as st
from services.transcription_service import transcribe_audio
import tempfile
import os

def voice_recorder():
    """Single-click voice recorder - no button state management needed."""
    
    # Direct audio input - single click to record
    audio_value = st.audio_input("🎤 Click to record your voice")
    
    if audio_value:
        # Display audio playback immediately
        st.audio(audio_value)
        
        # Read bytes from UploadedFile object
        audio_bytes = audio_value.read()
        
        # Save audio to temporary file for transcription
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_bytes)
            audio_path = tmp_file.name
        
        try:
            with st.spinner("Transcribing..."):
                transcribed_text = transcribe_audio(audio_path)
                if transcribed_text:
                    st.success(f"✅ Transcribed: {transcribed_text}")
                    return transcribed_text
                else:
                    st.warning("No speech detected in the recording.")
        except Exception as e:
            st.error(f"Transcription failed: {str(e)}")
            st.info("You can still use the audio recording above.")
        finally:
            # Clean up temporary file
            if os.path.exists(audio_path):
                os.unlink(audio_path)
    
    return ""