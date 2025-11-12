import streamlit as st
from services.api_service import query_backend
from src import config
from src.components.voice_recorder import voice_recorder

st.title(config.APP_TITLE)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None
if "transcribed_text" not in st.session_state:
    st.session_state.transcribed_text = ""

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input section
with st.container():
    # File upload in a compact form
    uploaded_file = st.file_uploader("Upload an image (optional)", type=["png", "jpg", "jpeg"], key="file_upload")
    
    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file
        st.session_state.transcribed_text = ""  # Clear transcribed text when a new file is uploaded
        st.success("✅ Image uploaded successfully!")
        st.info("📝 Please provide a new text prompt to describe your symptoms with this image.")
    
    # Show current uploaded image status
    if st.session_state.uploaded_file is not None:
        st.info(f"📷 Image ready: {st.session_state.uploaded_file.name}")
        st.image(st.session_state.uploaded_file, caption="Uploaded Image.", use_column_width=True)

    # Voice recorder
    transcribed_text = voice_recorder()
    if transcribed_text:
        st.session_state.transcribed_text = transcribed_text

# Chat input - modify placeholder text based on uploaded file
if st.session_state.uploaded_file is not None:
    prompt = st.chat_input("Describe your symptoms with the uploaded image...", key="chat_input")
else:
    prompt = st.chat_input("What are your symptoms?", key="chat_input")

# Handle prompt priority: manual input always overrides transcribed text
if prompt:
    # Manual text input takes priority - clear any transcribed text
    final_prompt = prompt
    st.session_state.transcribed_text = ""  # Clear transcribed text when manual input is used
elif st.session_state.get("transcribed_text") and st.session_state.uploaded_file is None:
    # Use transcribed text only if no manual input AND no uploaded file
    final_prompt = st.session_state.transcribed_text
    st.session_state.transcribed_text = ""  # Clear after use
else:
    final_prompt = None

# Prevent auto-submission with just transcribed text when image is uploaded
if st.session_state.uploaded_file is not None and not prompt and st.session_state.get("transcribed_text"):
    st.warning("⚠️ Please enter a text prompt to describe your symptoms with the uploaded image.")
    final_prompt = None

if final_prompt:
    # Display user message
    st.chat_message("user").markdown(final_prompt)
    st.session_state.messages.append({"role": "user", "content": final_prompt})

    # Get response with image if available
    with st.chat_message("assistant"):
        response = st.write_stream(query_backend(final_prompt, st.session_state.uploaded_file))
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.uploaded_file = None # Clear the file uploader
    uploaded_file = None # Clear local variable