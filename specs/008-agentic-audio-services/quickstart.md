# Quickstart: Agentic Audio Services

**Feature**: Agentic Audio Services
**Branch**: `008-agentic-audio-services`

## Overview

This feature refactors the audio services into ADK Tools.

## Verification

1.  **Start the Backend**:
    ```bash
    cd backend
    source .venv/bin/activate
    uv run src/main.py
    ```

2.  **Run Tests**:
    ```bash
    pytest backend/tests/unit/test_audio_tools.py
    ```
    *(Note: You will need to create this test file as part of the implementation)*

3.  **Verify Existing Functionality**:
    - Use the frontend to Record Voice (tests Transcription).
    - Use the frontend to Play Audio (tests TTS).
