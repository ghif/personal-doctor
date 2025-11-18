# Implementation Tasks: Backend Voice-to-Text Service (Whisper)

This document outlines the development tasks required to implement the backend voice-to-text service using OpenAI's Whisper model.

## Phase 1: Setup

- [x] T001 Add `openai-whisper` to `backend/requirements.txt`.
- [x] T002 Add `ffmpeg` to the backend `Dockerfile` as it is a system dependency for Whisper.

## Phase 2: Foundational Tasks

- [x] T003 Create a new file for the transcription service at `backend/src/services/transcription_service.py`.
- [x] T004 Create a new file for the transcription API endpoint at `backend/src/api/transcription.py`.

## Phase 3: User Story 1 - Backend Audio Transcription

**Goal**: Move the voice-to-text transcription to be processed on the backend using Whisper.
**Independent Test**: The frontend can successfully send a WAV audio recording to the `/transcribe` backend endpoint and receive the transcribed text, displaying it to the user.

### Implementation Tasks

- [x] T005 [US1] In `backend/src/models/models.py`, define the `TranscriptionResponse` Pydantic model.
- [x] T006 [US1] In `backend/src/services/transcription_service.py`, implement a `TranscriptionService` class that loads the Whisper model and provides a method to transcribe an audio file.
- [x] T007 [US1] In `backend/src/api/transcription.py`, create a FastAPI router and define the `POST /transcribe` endpoint. This endpoint will use the `TranscriptionService` to handle the transcription.
- [x] T008 [US1] In `backend/src/main.py`, include the new transcription API router.
- [x] T009 [US1] In `frontend/src/services/api_service.py`, add a new method to call the backend's `/transcribe` endpoint.
- [x] T010 [US1] In `frontend/src/services/transcription_service.py`, update the `transcribe_audio` function to use the new `api_service` method instead of the local Whisper model.

### Test Tasks

- [x] T011 [P] [US1] Create unit tests for the `TranscriptionService` in `backend/tests/unit/test_transcription_service.py`.
- [x] T012 [P] [US1] Create an integration test for the `/transcribe` endpoint in `backend/tests/integration/test_transcription_api.py`.

## Phase 4: Polish & Cross-Cutting Concerns

- [x] T013 Add structured logging to the transcription service and API endpoint.
- [x] T014 Review and update the project's `README.md` to reflect the use of Whisper in the backend.

## Dependencies

- **User Story 1** is the only user story and has no dependencies on other stories.

## Parallel Execution

Within User Story 1, the following tasks can be parallelized:
- Backend and frontend development (`T005`-`T008` and `T009`-`T010`) can be done in parallel once the API contract is firm.
- Backend unit and integration tests (`T011`, `T012`) can be developed in parallel with the backend implementation.

## Implementation Strategy

The implementation will follow an MVP-first approach, focusing on completing all tasks for User Story 1 to deliver the core functionality. The frontend and backend tasks will be developed in parallel to ensure a smooth integration.