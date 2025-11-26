# Quickstart: TTS Summary Response

## Prerequisites

- **Python**: 3.11+
- **Ollama**: Running locally with `medgemma` model.
- **Dependencies**: `pip install google-adk`

## Installation

1.  **Install new dependencies**:
    ```bash
    pip install -r backend/requirements.txt
    # (Ensure google-adk is added to requirements.txt)
    ```

2.  **Verify Ollama**:
    Ensure Ollama is running: `ollama serve`

## Running the Feature

1.  Start the backend:
    ```bash
    cd backend
    uvicorn src.main:app --reload
    ```

2.  Start the frontend:
    ```bash
    cd frontend
    streamlit run src/app.py
    ```

3.  **Test**:
    - Ask a medical question in the UI.
    - Wait for the text response.
    - Click "Play Audio" (or auto-play if configured).
    - Verify the audio is a short, punctuation-free summary of the text displayed.

## Troubleshooting

- **ADK Error**: If `google-adk` fails to connect to Ollama, check the `base_url` configuration in `src/agents/summary_agent.py`.
- **Empty Audio**: If audio is silent, check if the summary agent returned empty text.
