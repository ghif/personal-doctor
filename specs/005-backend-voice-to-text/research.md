# Research: Voice-to-Text Library Selection

## Decision

For the backend voice-to-text service, we will use the **OpenAI Whisper** model, as requested by the user.

## Rationale

- **User Preference**: The user explicitly requested to use Whisper, maintaining consistency with the previous frontend implementation.
- **High Accuracy**: Whisper is known for its high transcription accuracy across a wide range of audio conditions.
- **Offline First**: The model can be run locally, which aligns with our core constitutional principle of local-first execution and data privacy.
- **Open Source**: The model and its code are open source, allowing for local hosting and modification.

## Alternatives Considered

- **Vosk**: While a strong contender for its lightweight nature and offline capabilities, the decision was made to align with the user's preference for Whisper.