import streamlit as st
from services.transcription_service import transcribe_audio
import tempfile
import os

def voice_recorder():
    """Voice recorder with actual audio capture using streamlit-audio-recorder"""
    
    # Use st.audio_input to record audio
    audio_value = st.audio_input("🎤 Click to record your voice")
    
    
    if audio_value:
        # Display audio playback
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
                    
                    # Optional: Show transcription with audio in an expandable section
                    with st.expander("🎵 Audio & Transcription", expanded=True):
                        st.audio(audio_bytes, format="audio/wav")
                        st.write(f"**Transcription:** {transcribed_text}")
                    
                    return transcribed_text
        except Exception as e:
            st.error(f"Transcription failed: {str(e)}")
            # Still show audio even if transcription fails
            with st.expander("🎵 Recorded Audio", expanded=True):
                st.audio(audio_bytes, format="audio/wav")
                st.warning("Transcription failed, but you can still play back your recording.")
        finally:
            # Clean up temporary file
            if os.path.exists(audio_path):
                os.unlink(audio_path)
    
    return ""


