# Quickstart: Image Upload Feature

This document provides a high-level overview of the implementation steps for the image upload feature.

## 1. Frontend (`frontend/src/app.py`)

1.  **Add the file uploader component**:
    -   Use `st.file_uploader` to create the file upload UI.
    -   Set the `type` parameter to `['jpg', 'png']` to restrict file selection.
    -   Set the `accept_multiple_files` parameter to `False`.

2.  **Display a preview**:
    -   When a file is uploaded, use `st.image` to display a preview of the selected image.

3.  **Submit the image**:
    -   Add a "Submit" button using `st.button`.
    -   When the button is clicked, send the image to the backend using the `requests` library.
    -   The request should be a `POST` request to `/api/query/image` with the image data sent as `multipart/form-data`.

4.  **Handle the response**:
    -   Display a success message if the request is successful.
    -   Display an error message if the request fails.

## 2. Backend (`backend/src/api/query.py`)

1.  **Create the endpoint**:
    -   Create a new endpoint `POST /api/query/image`.
    -   The endpoint should accept a file upload using `fastapi.UploadFile`.

2.  **Validate the file**:
    -   Check the `content_type` of the uploaded file to ensure it is `image/jpeg` or `image/png`.
    -   Check the size of the uploaded file to ensure it is no larger than 10 MB.

3.  **Save the file**:
    -   For now, save the uploaded image to a temporary directory on the server.
    -   In the future, this will be replaced with logic to process the image.

4.  **Return a response**:
    -   Return a JSON response with a success message if the upload is successful.
    -   Return an appropriate HTTP error with a detail message if validation fails or an unexpected error occurs.
