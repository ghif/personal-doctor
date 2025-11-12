import streamlit as st
from services.api_service import query_backend
from src import config
from src.components.voice_recorder import voice_recorder

# Welcome header
# st.title(config.APP_TITLE)
st.set_page_config(
    page_title="Personal Doctor AI",
    page_icon="🩺",
    # layout="wide",
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



# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Input section
with st.container():
    # File upload in a compact form
    st.markdown("**📷 Upload Medical Image**")
    st.markdown("*Share photos of symptoms, test results, or medical documents*")
    uploaded_file = st.file_uploader("", type=["png", "jpg", "jpeg"], key="file_upload")
    
    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file
        st.session_state.transcribed_text = ""  # Clear transcribed text when a new file is uploaded
        st.success("✅ Image uploaded successfully!")
        st.warning("📝 **Required:** Please describe your symptoms or what you'd like me to analyze in this image using text or voice input below.")
    
    # Show current uploaded image status
    if st.session_state.uploaded_file is not None:
        st.info(f"📷 Image ready: {st.session_state.uploaded_file.name}")
        st.image(st.session_state.uploaded_file, caption="Uploaded Image.", use_column_width=True)

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
    # Manual text input takes priority - clear any transcribed text
    final_prompt = prompt
    st.session_state.transcribed_text = ""  # Clear transcribed text when manual input is used
    st.session_state.auto_submit = False  # Reset auto-submit flag
# elif st.session_state.get("transcribed_text") and st.session_state.uploaded_file is None:
elif st.session_state.get("transcribed_text"):
    # Use transcribed text only if no manual input AND no uploaded file
    final_prompt = st.session_state.transcribed_text
    st.session_state.transcribed_text = ""  # Clear after use
    st.session_state.auto_submit = False  # Reset auto-submit flag
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

    # Clear inputs after processing
    st.session_state.uploaded_file = None
    st.session_state.auto_submit = False  # Reset auto-submit flag
    uploaded_file = None # Clear local variable