# Quickstart: Personal Doctor AI

**Date**: 2025-11-10

This guide provides instructions for setting up and running the Personal Doctor AI assistant on a local machine.

## Prerequisites

-   Python 3.11+
-   Ollama installed and running
-   The `medgemma` model pulled via `ollama pull amsaravi/medgemma-4b-it:q6`

## Setup

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd personal-doctor
    ```

2.  **Set up the backend**:
    ```bash
    cd backend
    uv venv
    source .venv/bin/activate
    uv pip install -r requirements.txt
    ```

3.  **Set up the frontend**:
    ```bash
    cd ../frontend
    uv venv
    source .venv/bin/activate
    uv pip install -r requirements.txt
    ```

## Running the Application

1.  **Start the backend**:
    ```bash
    cd backend
    source .venv/bin/activate
    uvicorn src.main:app --reload
    ```
    The backend API will be available at `http://127.0.0.1:8000`.

2.  **Start the frontend**:
    ```bash
    cd frontend
    source .venv/bin/activate
    streamlit run src/app.py
    ```
    The Streamlit UI will be available at `http://localhost:8501`.

## How to Use

1.  Open your web browser and navigate to `http://localhost:8501`.
2.  Type a health-related question into the chat input box.
3.  Optionally, upload an image to accompany your question.
4.  Press Enter or click the submit button to get a response from the AI assistant.
