# Tasks: Agentic Audio Services

**Input**: Design documents from `/specs/008-agentic-audio-services/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create tools directory `backend/src/tools/` and `__init__.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T002 Verify `google-adk` dependency for Tool implementation (assumed present based on research)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Agentic Transcription (Priority: P1) 🎯 MVP

**Goal**: Encapsulate transcription service as an ADK Tool

**Independent Test**: Can be tested by invoking the new `TranscribeTool` directly with an audio file path and verifying it returns text, and ensuring the existing `/transcribe` endpoint still works by delegating to this tool (or the shared service).

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T003 [P] [US1] Create unit test for `TranscribeTool` in `backend/tests/unit/test_audio_tools.py`

### Implementation for User Story 1

- [x] T004 [US1] Implement `TranscribeTool` in `backend/src/tools/audio_tools.py` wrapping `TranscriptionService`
- [ ] T005 [US1] Register `TranscribeTool` with `ChatService` in `backend/src/services/llm/chat.py`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Agentic Text-to-Speech (Priority: P1)

**Goal**: Encapsulate TTS service as an ADK Tool

**Independent Test**: Can be tested by invoking the new `TextToSpeechTool` with text and verifying it generates an audio file/stream, and ensuring the existing `/tts` endpoint still works.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [x] T006 [P] [US2] Create unit test for `TextToSpeechTool` in `backend/tests/unit/test_audio_tools.py`

### Implementation for User Story 2

- [x] T007 [US2] Implement `TextToSpeechTool` in `backend/src/tools/audio_tools.py` wrapping `TTSService`
- [ ] T008 [US2] Register `TextToSpeechTool` with `ChatService` in `backend/src/services/llm/chat.py`

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T009 Run regression tests for existing `/transcribe` and `/tts` endpoints to ensure no breakage

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Create unit test for `TranscribeTool` in `backend/tests/unit/test_audio_tools.py`"

# Launch all models for User Story 1 together:
# (No models in this story)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
3. Stories complete and integrate independently