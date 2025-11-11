# Implementation Plan: 002-image-upload-button

**Feature Spec**: [spec.md](./spec.md)  
**Branch**: `002-image-upload-button`  
**Created**: 2025-11-11

## Technical Context

The user wants to implement an image upload feature in the `frontend` application.

- **Technology Stack**: The `frontend` is built with Python and Streamlit.
- **User Interface**: The user wants a single button to trigger the upload, positioned similarly to the existing input textbox.
- **Backend Interaction**: The uploaded image will likely need to be processed or stored. The interaction with the backend needs to be defined. [NEEDS CLARIFICATION: How should the frontend send the image to the backend? (e.g., as a file upload in a multipart/form-data request, or as a base64 encoded string in a JSON payload?)]
- **Dependencies**:
    - `streamlit`: For the frontend UI.
    - `requests`: For making HTTP requests to the backend.
- **State Management**: The state of the upload (e.g., idle, uploading, success, error) needs to be managed in the Streamlit application.

## Constitution Check

A check against the project's constitution.

- **I. Privacy First**: **PASS**. The image upload will be handled locally and sent to the local backend. No external services are involved.
- **II. Safety by Design**: **PASS**. The feature itself does not provide medical advice.
- **III. Local-First Execution**: **PASS**. The entire process will be handled on the user's local machine.
- **IV. Test-Driven Development**: **PASS**. New tests will be added to cover the image upload functionality.
- **V. High-Quality User Experience**: **PASS**. The feature aims to provide a simple and intuitive way for users to upload images.

## Phase 0: Outline & Research

### Research Tasks

1.  **Research Streamlit File Uploader**: Investigate the `st.file_uploader` component in Streamlit to understand its capabilities, limitations, and best practices for implementation.
2.  **Research Image Handling in Python**: Explore best practices for handling image data in Python, including validation, resizing, and encoding/decoding.
3.  **Backend Interaction**: Decide on the best way for the frontend to send the image to the backend.

### Research Findings (`research.md`)

- **Decision**: Use `st.file_uploader` for the frontend UI.
- **Rationale**: It is the standard and most straightforward way to handle file uploads in Streamlit.
- **Alternatives considered**: None, as this is the idiomatic approach in Streamlit.

- **Decision**: Use the Pillow library for image handling.
- **Rationale**: Pillow is a powerful and widely-used library for image processing in Python.
- **Alternatives considered**: OpenCV, but it is more complex and better suited for computer vision tasks.

- **Decision**: Send the image as a file upload in a `multipart/form-data` request.
- **Rationale**: This is the standard way to handle file uploads in web applications and is well-supported by FastAPI.
- **Alternatives considered**: Base64 encoding, but it is less efficient for binary data.

## Phase 1: Design & Contracts

### Data Model (`data-model.md`)

- **Image**:
    - `file_name`: string
    - `file_type`: string
    - `file_size`: integer
    - `content`: bytes

### API Contracts (`contracts/openapi.json`)

- **Endpoint**: `POST /api/query/image`
- **Request**: `multipart/form-data` with a file part named `image`.
- **Response**:
    - `200 OK`: `{ "message": "Image uploaded successfully" }`
    - `400 Bad Request`: `{ "detail": "Invalid file type or size" }`
    - `500 Internal Server Error`: `{ "detail": "An unexpected error occurred" }`

### Quickstart (`quickstart.md`)

1.  **Frontend**:
    - Add a `st.file_uploader` component to the main page.
    - When a file is uploaded, display a preview and a "Submit" button.
    - When the "Submit" button is clicked, send the image to the backend using the `requests` library.
2.  **Backend**:
    - Create a new endpoint `POST /api/query/image` in `src/api/query.py`.
    - The endpoint should accept a file upload.
    - Validate the file type and size.
    - For now, the backend will just save the image to a temporary directory.

## Phase 2: Implementation Plan

### Task Breakdown

1.  **Frontend**:
    - `T1.1`: Implement the `st.file_uploader` component in `frontend/src/app.py`.
    - `T1.2`: Add logic to display a preview of the uploaded image.
    - `T1.3`: Implement the "Submit" button and the call to the backend API.
    - `T1.4`: Add error handling for API calls.
2.  **Backend**:
    - `T2.1`: Create the new endpoint `POST /api/query/image` in `backend/src/api/query.py`.
    - `T2.2`: Add validation for file type and size.
    - `T2.3`: Implement the logic to save the uploaded image.
3.  **Testing**:
    - `T3.1`: Add unit tests for the new backend endpoint.
    - `T3.2`: Add integration tests for the frontend and backend.

### Agent Context Update

- **Technologies**: No new technologies are being introduced. The plan uses the existing stack of Python, Streamlit, and FastAPI.