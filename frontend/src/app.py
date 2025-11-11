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
        st.success("✅ Image uploaded successfully!")
    
    # Show current uploaded image status
    if st.session_state.uploaded_file is not None:
        st.info(f"📷 Image ready: {st.session_state.uploaded_file.name}")
        st.image(st.session_state.uploaded_file, caption="Uploaded Image.", use_column_width=True)

    # Voice recorder
    transcribed_text = voice_recorder()
    if transcribed_text:
        st.session_state.transcribed_text = transcribed_text

# Chat input
prompt = st.chat_input("What are your symptoms?", key="chat_input")
if st.session_state.get("transcribed_text"):
    prompt = st.session_state.transcribed_text
    st.session_state.transcribed_text = "" # Clear after use

if prompt:
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get response with image if available
    with st.chat_message("assistant"):
        response = st.write_stream(query_backend(prompt, st.session_state.uploaded_file))
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.uploaded_file = None # Clear the file uploader
    uploaded_file = None # Clear local variable