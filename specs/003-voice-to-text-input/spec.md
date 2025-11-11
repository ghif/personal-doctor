# Feature Specification: Voice-to-Text Input

**Feature Branch**: `003-voice-to-text-input`
**Created**: 2025-11-11
**Status**: Draft
**Input**: User description: "users should be able to speak with the personal AI assistant through the device microphone and then extract the text information (English or Bahasa Indonesia) to be the input to MedGemma model"

## Clarifications

### Session 2025-11-11

- Q: How should the system behave if the local transcription service is unavailable or fails to respond? → A: Display a non-blocking toast message: "Voice service unavailable".
- Q: What visual feedback should the user receive to indicate that recording is active? → A: A pulsating microphone icon or a waveform animation.
- Q: What is the maximum duration for a single voice recording? → A: No explicit limit; allow continuous recording until stopped by the user.
- Q: What visual feedback should the user receive while the audio is being transcribed? → A: A small, non-blocking spinner or "Transcribing..." text near the input field.
- Q: How should the system handle transcription errors where the transcribed text is clearly incorrect or nonsensical? → A: Allow the user to manually edit the transcribed text in the input field.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Transcribe voice input for AI assistant (Priority: P1)

As a user, I want to tap a button to record my voice, speak a question in English or Bahasa Indonesia, and see the transcribed text in the input field, so that I can easily interact with the AI assistant without typing.

**Why this priority**: This is the core functionality of the feature, enabling a hands-free and more accessible way to interact with the assistant.

**Independent Test**: This can be tested by verifying that pressing the record button, speaking a phrase, and stopping the recording results in the correct text appearing in the input field. This delivers the primary value of the feature.

**Acceptance Scenarios**:

1.  **Given** the user is on the main assistant screen, **When** they tap the "Record" button and speak "What are the symptoms of the flu?" in English, **Then** the text "What are the aymptoms of the flu?" appears in the input field.
2.  **Given** the user is on the main assistant screen, **When** they tap the "Record" button and speak "Apa saja gejala flu?" in Bahasa Indonesia, **Then** the text "Apa saja gejala flu?" appears in the input field.
3.  **Given** the recording is in progress, **When** the user taps the "Stop" button, **Then** the recording ceases and the transcription process begins.

### Edge Cases

-   **Empty Audio:** If the user starts and stops recording without speaking, the system should not input any text and perhaps show a subtle notification like "No audio detected."
-   **Background Noise:** If the recording contains significant background noise that prevents accurate transcription, the system should ideally notify the user that the transcription may be inaccurate (e.g., "Could not understand audio clearly").
-   **Microphone Permissions Denied:** If the user has not granted microphone permissions, tapping the record button should prompt them to grant permission, or show a message explaining that microphone access is required.
-   **Transcription Service Failure:** If the local transcription service is unavailable or fails, the system MUST display a non-blocking toast message to the user (e.g., "Voice service unavailable").
-   **Transcription Error:** If the transcribed text is clearly incorrect or nonsensical, the system MUST allow the user to manually edit the text in the input field.

## Requirements *(mandatory)*

### Functional Requirements

-   **FR-001**: The system MUST provide a user interface element (e.g., a microphone button) to initiate and terminate audio recording.
-   **FR-002**: The system MUST capture audio input from the device's microphone upon user activation.
-   **FR-003**: The system MUST convert the captured audio into text.
-   **FR-004**: The transcription service MUST support both "English" and "Bahasa Indonesia" languages.
-   **FR-005**: The transcribed text MUST be populated into the text input field for the MedGemma model.
-   **FR-006**: The system MUST handle cases where no speech is detected in the audio.
-   **FR-007**: The system MUST gracefully handle microphone permission denial.
-   **FR-008**: The system MUST provide clear visual feedback (e.g., a pulsating microphone icon or waveform animation) to indicate active audio recording.
-   **FR-009**: The system MUST allow continuous audio recording until explicitly stopped by the user, with no predefined maximum duration.
-   **FR-010**: The system MUST provide visual feedback (e.g., a small, non-blocking spinner or "Transcribing..." text) near the input field while audio is being transcribed.
-   **FR-011**: The system MUST allow users to manually edit the transcribed text in the input field.

## Success Criteria *(mandatory)*

### Measurable Outcomes

-   **SC-001**: For clear speech in a quiet environment, the transcription accuracy (Word Error Rate) MUST be below 10% for both supported languages.
-   **SC-002**: The end-to-end latency from the moment the user stops recording to the text appearing in the input field MUST be less than 3 seconds for an average query length (5-15 seconds of speech).
-   **SC-003**: The voice input feature MUST have a successful transaction rate of over 95% (i.e., text is successfully transcribed and populated without errors).
-   **SC-004**: User task completion rate using voice input should be comparable to text input, indicating ease of use.