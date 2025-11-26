import streamlit as st
from services.api_service import query_backend, get_summary_stream, get_tts_audio
from components.voice_recorder import voice_recorder
from components.audio_player import audio_player

# Welcome header
st.set_page_config(
    page_title="Personal Doctor AI",
    page_icon="🩺",
    initial_sidebar_state="collapsed"
)

st.markdown("""<style>
.doctor-welcome {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2rem;
    border-radius: 15px;
    text-align: center;
    margin-bottom: 2rem;
}
</style>""", unsafe_allow_html=True)

st.markdown("""
<div class="doctor-welcome">
    <h1>🩺 Your AI Personal Doctor</h1>
    <p style="font-size: 1.0rem; margin: 0;">I'm here to help with your health concerns. All the information you provide will be kept confidential in your private space.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background: linear-gradient(90deg, #e3f2fd, #f3e5f5); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
    <p style="color: #1565c0; margin: 0;">💬 Describe Your Symptoms: You can type, speak, or upload an image to help me understand your condition better.</p>
</div>
""", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None
if "transcribed_text" not in st.session_state:
    st.session_state.transcribed_text = ""
if "auto_submit" not in st.session_state:
    st.session_state.auto_submit = False
if "last_response" not in st.session_state:
    st.session_state.last_response = ""

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input section
with st.container():
    # File upload in a compact form
    st.markdown("**📷 Upload Medical Image**")
    st.markdown("*Share photos of symptoms, test results, or medical documents*")
    if st.session_state.uploaded_file is None:
        uploaded_file_new = st.file_uploader("Upload an image (optional):", type=["png", "jpg", "jpeg"], key="file_upload")
        if uploaded_file_new is not None:
            st.session_state.uploaded_file = uploaded_file_new
            st.session_state.transcribed_text = ""  # Clear transcribed text when a new file is uploaded
            st.success("✅ Image uploaded successfully!")
            st.warning("📝 **Required:** Please describe your symptoms or what you'd like me to analyze in this image using text or voice input below.")
    else:
        # Show current uploaded image status and provide a clear button
        st.info(f"📷 Image ready: {st.session_state.uploaded_file.name}")
        st.image(st.session_state.uploaded_file, caption="Uploaded Image.", use_column_width=True)
        if st.button("Clear Image", key="clear_image_button"):
            st.session_state.uploaded_file = None
            st.experimental_rerun() # Rerun to remove the image and show the uploader

    # Voice recorder
    st.markdown("**🎤 Voice Recording**")
    st.markdown("*Speak naturally about your symptoms*")
    transcribed_text = voice_recorder()
    if transcribed_text:
        st.session_state.transcribed_text = transcribed_text

# Chat input - modify placeholder text based on uploaded file
st.markdown("---")

if st.session_state.uploaded_file is not None:
    prompt = st.chat_input("🚨 REQUIRED: Describe your symptoms with the uploaded image...", key="chat_input")
else:
    prompt = st.chat_input("What are your symptoms?", key="chat_input")

# Handle prompt priority: manual input always overrides transcribed text
if prompt:
    final_prompt = prompt
    st.session_state.transcribed_text = ""
    st.session_state.auto_submit = False
elif st.session_state.get("transcribed_text"):
    final_prompt = st.session_state.transcribed_text
    st.session_state.transcribed_text = ""
    st.session_state.auto_submit = False
else:
    final_prompt = None

# Only show error if image uploaded but no description AND no voice transcription available
if st.session_state.uploaded_file is not None and not final_prompt and not st.session_state.get("transcribed_text"):
    st.error("❌ **Image uploaded but no description provided!** Please type your symptoms in the chat input below or use the voice recorder above.")

if final_prompt:
    # Display user message
    st.chat_message("user").markdown(final_prompt)
    st.session_state.messages.append({"role": "user", "content": final_prompt})

    # Get response with image if available
    with st.chat_message("assistant"):
        response = st.write_stream(query_backend(final_prompt, st.session_state.uploaded_file))
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Store response for audio player and summary
    st.session_state.last_response = response
    
    # Show audio player (existing feature)
    audio_player()

    # Clear inputs after processing
    st.session_state.uploaded_file = None
    st.session_state.auto_submit = False
    uploaded_file = None

# Audio Summary Feature
if st.session_state.last_response:
    st.markdown("---")
    st.markdown("### 🔈 Audio Summary")
    if st.button("Play Audio Summary"):
        with st.container():
            st.markdown("**Generating Summary:**")
            # Stream the summary text
            summary_text = st.write_stream(get_summary_stream(st.session_state.last_response))
            
            if summary_text:
                st.markdown("**Playing Audio...**")
                try:
                    audio_bytes = get_tts_audio(summary_text)
                    st.audio(audio_bytes, format='audio/wav', autoplay=True)
                except Exception as e:
                    st.error(f"Failed to generate audio: {e}")