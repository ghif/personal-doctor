import os

# OLLAMA_API_BASE = os.environ.get("OLLAMA_API_BASE", "http://127.0.0.1:11434")
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
MODEL_NAME = "amsaravi/medgemma-4b-it:q6"
DISCLAIMER = "This is an AI assistant and not a substitute for professional medical advice. Please consult a doctor for any health concerns."

TRIAGE_SUGGESTION_INFO_ONLY = "INFO_ONLY"
TRIAGE_SUGGESTION_SEE_DOCTOR = "SEE_DOCTOR"
TRIAGE_SUGGESTION_URGENT_CARE = "URGENT_CARE"
TRIAGE_SUGGESTION_ERROR = "ERROR"
