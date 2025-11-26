# Quickstart: Stream Summary Text and Audio

**Feature**: Stream Summary Text and Audio
**Branch**: `007-stream-summary-text`

## Overview

This feature allows users to interactively summarize the AI's response. By clicking "Play Audio Summary", the system streams a concise text summary to the screen and automatically plays it as audio once the text stream is complete.

## Running the Application

1.  **Start the Backend**:
    ```bash
    cd backend
    source .venv/bin/activate
    uvicorn src.main:app --reload
    ```
    The backend API will be available at `http://localhost:8000`.

2.  **Start the Frontend**:
    ```bash
    cd frontend
    source .venv/bin/activate
    streamlit run src/app.py
    ```
    The UI will open at `http://localhost:8501`.

## Usage Guide

1.  **Ask a Question**: Type or speak a medical query (e.g., "What are the symptoms of flu?").
2.  **View Response**: Wait for the standard detailed response to appear.
3.  **Click "Play Audio Summary"**: Look for the button below the response.
4.  **Observe**:
    - A new text area will appear, streaming the summary in real-time.
    - Once the text stops streaming, the audio playback will begin automatically.

## Troubleshooting

-   **No Audio**: Ensure your system volume is up and the browser tab has permission to play audio.
-   **Streaming Stuck**: Check the backend logs for any errors related to `SummaryAgent` or `LiteLlm`.
-   **Button Not Appearing**: The button only appears after a response has been fully generated in the main chat.
