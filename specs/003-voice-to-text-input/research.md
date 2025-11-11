# Research: Voice-to-Text Model Selection

**Date**: 2025-11-11

## Decision

We will use a **fine-tuned Whisper model** for the speech-to-text functionality. Specifically, we will start with a community-provided model fine-tuned for Bahasa Indonesia, which also retains excellent English transcription capabilities.

## Rationale

1.  **High Accuracy for Required Languages**: Research and community benchmarks show that while the base OpenAI Whisper models are strong, models specifically fine-tuned on datasets like the Indonesian Common Voice achieve a significantly lower Word Error Rate (WER). This is crucial for meeting our success criteria (`SC-001`).
2.  **Local-First and Private**: Whisper models can be run entirely on-device. This aligns perfectly with our core constitution principles of "Privacy First" and "Local-First Execution," as no user audio data needs to be sent to an external cloud service.
3.  **Open Source and Active Community**: Whisper is an open-source project with a large and active community. This provides access to a wide range of pre-trained models, fine-tuning scripts, and support.
4.  **Performance**: The various model sizes (tiny, base, small, medium, large) allow for a trade-off between accuracy and performance, which can be optimized for the target user's hardware. We can start with a smaller model to ensure a responsive user experience, aligning with `SC-002`.

## Alternatives Considered

-   **Base OpenAI Whisper**: Good general performance, but less accurate for Bahasa Indonesia compared to fine-tuned versions.
-   **Kaldi/Wav2vec 2.0**: These are powerful frameworks but typically require more effort to train and deploy a custom model. Using a pre-tuned Whisper model is more efficient for our current needs.
-   **Voxtral by Mistral AI**: A promising successor to Whisper, but its performance on Bahasa Indonesia is not as well-documented as fine-tuned Whisper models. It remains a candidate for future evaluation.
