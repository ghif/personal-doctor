# Tasks: Personal Doctor AI

**Input**: Design documents from `/specs/001-personal-doctor-ai/`
**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/openapi.json`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure.

- [X] T001 Create the `backend` and `frontend` directories at the root of the project.
- [X] T002 [P] In the `backend` directory, initialize a `uv` environment. See `quickstart.md`.
- [X] T003 [P] In the `frontend` directory, initialize a `uv` environment. See `quickstart.md`.
- [X] T004 [P] Create the initial directory structure within `backend/src` and `frontend/src` as outlined in `plan.md`.

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented.

- [X] T005 Implement the Pydantic models for `UserQuery` and `AIResponse` in `backend/src/models/` based on `data-model.md`.
- [X] T006 Set up the FastAPI application in `backend/src/main.py`.
- [X] T007 Implement the `/query` endpoint in `backend/src/api/` as defined in `contracts/openapi.json`.
- [X] T008 Create a placeholder service in `backend/src/services/` that the `/query` endpoint can call.

## Phase 3: User Story 1 - Symptom Inquiry via Text (Priority: P1) 🎯 MVP

**Goal**: A user can type a health question and receive a text-based response from the AI assistant.
**Independent Test**: Can be tested by inputting a text query to the backend API and verifying that a relevant, safe, and educational response is returned, including a disclaimer.

### Implementation for User Story 1

- [X] T009 [US1] Implement the core logic in the `backend/src/services/` to process a text query.
- [X] T010 [US1] In the service, use the `ollama` Python library to interact with the `amsaravi/medgemma-4b-it:q6` model. Refer to `research.md`.
- [X] T011 [US1] Integrate the Google ADK for basic conversational agent logic within the service. Refer to `research.md`.
- [X] T012 [US1] Set up the main Streamlit application file in `frontend/src/app.py`.
- [X] T013 [US1] [P] Create a chat input component in `frontend/src/components/`.
- [X] T014 [US1] [P] Create a message display component in `frontend/src/components/`.
- [X] T015 [US1] Implement the service in `frontend/src/services/` to call the backend `/query` API.
- [X] T016 [US1] Connect the UI components to the frontend service to create the end-to-end chat functionality.

## Phase 4: User Story 2 - Symptom Inquiry with Image Upload (Priority: P2)

**Goal**: A user can upload an image along with their text query to get a more contextual response.
**Independent Test**: Can be tested by sending a text query and a base64-encoded image to the backend API and verifying the response is contextual to both inputs.

### Implementation for User Story 2

- [X] T017 [US2] Update the `UserQuery` model in `backend/src/models/` to handle the `image_data` field.
- [X] T018 [US2] Update the `/query` endpoint and backend service to process the `image_data`.
- [X] T019 [US2] Update the Ollama interaction logic in the backend service to pass the image data to the model. Refer to `research.md` for multimodal input handling.
- [X] T020 [US2] [P] Add a file uploader component to the Streamlit UI in `frontend/src/components/`.
- [X] T021 [US2] Update the frontend service to send the image data to the backend.

## Phase 5: User Story 3 - Voice-to-Text and Text-to-Speech Interaction (Priority: P3)

**Goal**: A user can interact with the assistant using their voice.
**Independent Test**: Can be tested by speaking into the UI, verifying the transcribed text is sent to the backend, and hearing the assistant's response read aloud.

### Implementation for User Story 3

- [ ] T022 [US3] Research and choose a library for browser-based speech-to-text (e.g., Web Speech API).
- [ ] T023 [US3] Implement the voice input functionality in the frontend, adding a microphone button to the UI.
- [ ] T024 [US3] Research and choose a library for browser-based text-to-speech (e.g., Web Speech API).
- [ ] T025 [US3] Implement the text-to-speech functionality in the frontend to read out the assistant's response.

## Phase 6: Polish & Cross-Cutting Concerns

- [X] T026 [P] Implement unit tests for the backend in the `backend/tests/` directory.
- [X] T027 [P] Implement integration tests in the `backend/tests/integration/` directory.
- [X] T028 [P] Update the `README.md` with final setup and usage instructions.
- [X] T029 Review and refine the code based on the principles in `constitution.md`.

## Dependencies & Execution Order

- **Phase 1 & 2**: Must be completed before any user story work can begin.
- **User Stories**: Can be worked on in priority order (US1 → US2 → US3). US2 and US3 depend on US1 being complete.
- **Phase 6**: Can be worked on in parallel with other phases, but should be finalized after all user stories are complete.

## Parallel Execution Examples

- **During Setup**: T002, T003, and T004 can be run in parallel.
- **During User Story 1**: T013 and T014 can be worked on in parallel.
- **During Polish**: T026, T027, and T028 can all be worked on in parallel.

## Implementation Strategy

1.  **MVP First (User Story 1)**: Complete Phases 1, 2, and 3 to deliver the core text-based chat functionality.
2.  **Incremental Delivery**: Add image support (Phase 4) and then voice support (Phase 5) as subsequent releases.
3.  **Continuous Polish**: Work on tasks from Phase 6 throughout the development process.