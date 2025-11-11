import streamlit as st
from services.api_service import query_backend
from src import config
import base64

st.title(config.APP_TITLE)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# File uploader for images, placed in a less intrusive spot
uploaded_file = st.file_uploader("Upload an image (optional)", type=["png", "jpg", "jpeg"])
image_b64 = None
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    # Encode to base64
    image_b64 = base64.b64encode(bytes_data).decode()
    # Optionally, display the image
    st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)

# React to user input
if prompt := st.chat_input("What are your symptoms?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get assistant response, passing the image data if it exists
    with st.chat_message("assistant"):
        response = st.write_stream(query_backend(prompt, image_b64))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
