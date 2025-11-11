import streamlit as st
from services.api_service import query_backend
from src import config

st.title(config.APP_TITLE)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
with st.container():
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)
        if st.button("Submit Image"):
            with st.chat_message("assistant"):
                response = st.write_stream(query_backend(None, uploaded_file))
            st.session_state.messages.append({"role": "assistant", "content": response})

    if prompt := st.chat_input("What are your symptoms?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Get assistant response, passing the image data if it exists
        with st.chat_message("assistant"):
            response = st.write_stream(query_backend(prompt, uploaded_file))
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
