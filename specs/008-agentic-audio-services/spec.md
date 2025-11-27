# Feature Specification: Agentic Audio Services

**Feature Branch**: `008-agentic-audio-services`
**Created**: 2025-11-26
**Status**: Draft
**Input**: User description: "In the "backend", refactor the codes such that the audio services (transcription.py, tts.py) are part of the agentic architecture in ADK framework. Do not change all the main functionalities."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Agentic Transcription (Priority: P1)

As a developer, I want the transcription service to be encapsulated as an ADK Tool, so that the AI agent can theoretically invoke it dynamically if needed, while maintaining the existing direct API functionality for the frontend.

**Why this priority**: This establishes the agentic pattern for input processing.

**Independent Test**: Can be tested by invoking the new `TranscribeTool` directly with an audio file path and verifying it returns text, and ensuring the existing `/transcribe` endpoint still works by delegating to this tool (or the shared service).

**Acceptance Scenarios**:

1.  **Given** an audio file, **When** the `TranscribeTool` is run, **Then** it returns the correct transcribed text.
2.  **Given** the existing frontend app, **When** I record my voice, **Then** the transcription still works exactly as before.

---

### User Story 2 - Agentic Text-to-Speech (Priority: P1)

As a developer, I want the TTS service to be encapsulated as an ADK Tool, so that the AI agent can generate speech as an action.

**Why this priority**: This establishes the agentic pattern for output generation.

**Independent Test**: Can be tested by invoking the new `TextToSpeechTool` with text and verifying it generates an audio file/stream, and ensuring the existing `/tts` endpoint still works.

**Acceptance Scenarios**:

1.  **Given** a text string, **When** the `TextToSpeechTool` is run, **Then** it produces valid audio data.
2.  **Given** the existing frontend app, **When** I click "Play Audio", **Then** the audio plays exactly as before.

## Requirements *(mandatory)*

### Functional Requirements

-   **FR-001**: The backend MUST implement a `TranscribeTool` class compatible with the Google ADK framework.
-   **FR-002**: The backend MUST implement a `TextToSpeechTool` class compatible with the Google ADK framework.
-   **FR-003**: The `TranscribeTool` MUST wrap the existing logic from `src/services/audio/transcription.py`.
-   **FR-004**: The `TextToSpeechTool` MUST wrap the existing logic from `src/services/audio/tts.py`.
-   **FR-005**: The existing `ChatService` (Agent) MUST register these tools (even if not strictly used by the LLM for simple chat yet, they should be available in the architecture).
-   **FR-006**: The existing API endpoints (`/transcribe`, `/tts`) MUST remain functional and unchanged from the frontend's perspective. They can optionally use the Tools or the underlying Services directly. (Recommendation: Use underlying services to avoid unnecessary agent overhead for direct API calls, but ensure tools use the *same* services).

### Key Entities *(include if feature involves data)*

-   **AudioTools**: A collection of ADK-compatible tools for audio processing.

## Success Criteria *(mandatory)*

### Measurable Outcomes

-   **SC-001**: No regression in functionality: Voice input and Audio output work exactly as before.
-   **SC-002**: Code structure reflects the ADK Tool pattern (presence of `tools/audio.py` or similar).
-   **SC-003**: Unit tests exist for the new Tool classes.

## Assumptions

-   Google ADK has a `Tool` base class or interface we can implement.
-   The existing services are stateless enough (or singletons) to be wrapped easily.