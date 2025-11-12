import streamlit as st
from services.transcription_service import transcribe_audio
import tempfile
import os

def voice_recorder():
    """Single-click voice recorder - no button state management needed."""

    # Check if image is uploaded to show required status
    image_uploaded = st.session_state.get("uploaded_file") is not None
    
    # Dynamic label based on whether image is uploaded
    if image_uploaded:
        label = "🎤 🚨 REQUIRED: Record description of your symptoms with the image"
    else:
        label = "🎤 Click to record your voice (optional)"
    
    # Direct audio input - single click to record
    audio_value = st.audio_input(label)

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
                    if image_uploaded:
                        st.success(f"✅ Voice description recorded: {transcribed_text}")
                        st.info("🚀 Processing your image analysis automatically...")
                    else:
                        st.success(f"✅ Transcribed: {transcribed_text}")
                        
                    st.session_state.auto_submit = True
                    return transcribed_text
                else:
                    st.warning("No speech detected in the recording.")
                    if image_uploaded:
                        st.error("🚨 Please try recording again or use the text input below to describe your image.")
        except Exception as e:
            st.error(f"Transcription failed: {str(e)}")
            if image_uploaded:
                st.error("🚨 Voice recording failed. Please use the text input below to describe your image.")
            else:
                st.info("You can still use the audio recording above.")
        finally:
            # Clean up temporary file
            if os.path.exists(audio_path):
                os.unlink(audio_path)
    
    return ""