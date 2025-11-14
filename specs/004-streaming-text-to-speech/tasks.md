# Actionable Tasks: Streaming Text-to-Speech Output

**Branch**: `004-streaming-text-to-speech` | **Date**: 2025-11-13 | **Spec**: [link](./spec.md)

This document outlines the actionable tasks required to implement the streaming text-to-speech feature.

## Phase 1: Setup

- [x] T001 Add Coqui TTS to the backend dependencies in `backend/requirements.txt`
- [x] T002 Install Coqui TTS and download the required models.

## Phase 2: Foundational (Backend)

- [x] T003 Create a new file for the TTS service in `backend/src/services/tts_service.py`
- [x] T004 Implement the TTS service in `backend/src/services/tts_service.py` to load the Coqui TTS model and provide a function to convert text to an audio stream.
- [x] T005 Create a new file for the TTS API endpoint in `backend/src/api/tts.py`
- [x] T006 Implement the `/tts` API endpoint in `backend/src/api/tts.py` to stream the audio data, as defined in the OpenAPI contract.
- [x] T007 Include the TTS API router in the main FastAPI application in `backend/src/main.py`.
- [ ] T008 Add a unit test for the TTS service in `backend/tests/test_tts_service.py`
- [ ] T009 Add an integration test for the `/tts` API endpoint in `backend/tests/integration/test_tts_api.py`

## Phase 3: User Story 1 - Hear Real-Time Spoken Responses (Frontend)

**Goal**: Users can hear the MedGemma's text output as spoken words in real-time.
**Independent Test**: The frontend can receive a text string, send it to the backend, and play the returned audio stream smoothly.

- [x] T010 [US1] Create a new file for the frontend TTS service in `frontend/src/services/tts_service.py`
- [x] T011 [US1] Implement the frontend TTS service in `frontend/src/services/tts_service.py` to make requests to the backend `/tts` API.
- [x] T012 [US1] Create a new file for the audio player component in `frontend/src/components/audio_player.py`
- [x] T013 [US1] Implement the audio player component in `frontend/src/components/audio_player.py` with a "Play Audio" button.
- [x] T014 [US1] Integrate the audio player component into the main chat interface in `frontend/src/app.py`
- [ ] T015 [US1] Implement the logic in the audio player component to call the frontend TTS service and play the returned audio stream.
- [ ] T016 [US1] Add a unit test for the frontend TTS service in `frontend/tests/test_tts_service.py`

## Phase 4: User Story 2 - Control Audio Playback (Frontend)

**Goal**: Users can mute or unmute the audio output.
**Independent Test**: The audio player component's mute/unmute button correctly starts and stops the audio playback.

- [ ] T017 [US2] Add mute and unmute buttons to the audio player component in `frontend/src/components/audio_player.py`
- [ ] T018 [US2] Implement the mute and unmute functionality in the audio player component in `frontend/src/components/audio_player.py`
- [ ] T019 [US2] Add a unit test for the mute/unmute functionality in `frontend/tests/test_audio_player.py`

## Phase 5: Polish & Cross-Cutting Concerns

- [ ] T020 [P] Implement error handling in the frontend to display a user-friendly message if the TTS service fails.
- [ ] T021 [P] Add logging to the backend TTS service for monitoring and debugging.
- [ ] T022 [P] Ensure the audio playback stops when the user navigates away from the page or closes the session.
- [ ] T023 [P] Add an integration test for handling very long text inputs to ensure continuous streaming in `backend/tests/integration/test_tts_api.py`.
- [ ] T024 [P] Add a unit test for handling non-alphanumeric characters and unsupported languages in `backend/tests/test_tts_service.py`.
- [ ] T025 [P] Add an integration test to simulate unstable network conditions and verify buffering behavior in `frontend/tests/test_audio_player.py`.

## Dependencies

- **User Story 1** is dependent on the **Foundational (Backend)** tasks.
- **User Story 2** is dependent on **User Story 1**.

## Parallel Execution

- The **Foundational (Backend)** tasks can be worked on in parallel with the initial setup of the **Frontend** components (T009, T011).
- The **Polish & Cross-Cutting Concerns** tasks can be worked on in parallel with other tasks once the basic functionality is in place.

## Implementation Strategy

The implementation will follow an MVP-first approach. The initial focus will be on completing the **Foundational (Backend)** tasks and **User Story 1** to deliver the core functionality of the feature. Once the MVP is complete and tested, **User Story 2** and the **Polish & Cross-Cutting Concerns** will be addressed.
