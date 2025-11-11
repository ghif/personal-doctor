# Research: Image Upload Feature

## 1. Streamlit File Uploader

- **Decision**: Use `st.file_uploader` for the frontend UI.
- **Rationale**: It is the standard and most straightforward way to handle file uploads in Streamlit. It provides a simple and intuitive user interface for selecting files from the local filesystem.
- **Alternatives considered**: None, as this is the idiomatic approach in Streamlit.

## 2. Image Handling in Python

- **Decision**: Use the Pillow library for image handling.
- **Rationale**: Pillow is a powerful and widely-used library for image processing in Python. It provides a rich set of features for opening, manipulating, and saving many different image file formats. It is also lightweight and easy to use.
- **Alternatives considered**:
    - **OpenCV**: While powerful, OpenCV is more complex and better suited for computer vision tasks rather than simple image handling. It also has a larger footprint.
    - **Scikit-image**: This is another powerful library for image processing, but it is more focused on scientific and research applications.

## 3. Backend Interaction

- **Decision**: Send the image as a file upload in a `multipart/form-data` request.
- **Rationale**: This is the standard and most efficient way to handle file uploads in web applications. It is well-supported by both `requests` on the frontend and `FastAPI` on the backend.
- **Alternatives considered**:
    - **Base64 encoding**: This involves encoding the image data as a string and sending it in a JSON payload. While this can be simpler for some use cases, it is less efficient for binary data like images, as it increases the payload size by about 33%.
