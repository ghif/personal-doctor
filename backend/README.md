# Personal Doctor AI - Backend

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   Note: `google-adk` is required for the TTS Summary feature.

2. **Ollama Setup**:
   - Ensure Ollama is installed and running (`ollama serve`).
   - Pull the MedGemma model: `ollama pull amsaravi/medgemma-4b-it:q6` (or the model defined in `src/config.py`).

## Features

### TTS Summary Response (New)
The backend includes a `SummaryAgent` that intercepts long responses, summarizes them into a single punctuation-free paragraph using the local LLM, and then converts them to speech.
- **Endpoint**: `POST /summary-tts`
- **Configuration**: Managed in `src/agents/summary_agent.py` (points to local Ollama by default).
