# Tasks: Stream Summary Text and Audio

**Input**: Design documents from `/specs/007-stream-summary-text/`
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

- [x] T001 Verify backend dependencies in backend/requirements.txt
- [x] T002 Verify frontend dependencies in frontend/requirements.txt

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 Ensure backend/src/api/summary.py is registered in backend/src/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Interactive Summary & Playback (Priority: P1) 🎯 MVP

**Goal**: Click button -> Stream Text -> Play Audio

**Independent Test**: Can be tested by generating a long response, clicking the "Play Audio Summary" button, and verifying the sequence of events (text streaming -> audio playback).

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T004 [P] [US1] Create unit test for `summarize_stream` in backend/tests/unit/test_summary_agent.py
- [x] T005 [P] [US1] Create integration test for `/summary_stream` in backend/tests/integration/test_integration_summary.py

### Implementation for User Story 1

- [x] T006 [P] [US1] Implement `summarize_stream` method in backend/src/agents/summary_agent.py
- [x] T007 [P] [US1] Add `/summary_stream` endpoint to backend/src/api/summary.py
- [x] T008 [P] [US1] Add `get_summary_stream` method to frontend/src/services/api_service.py
- [x] T009 [US1] Implement "Play Audio Summary" button and streaming logic in frontend/src/app.py
- [x] T010 [US1] Implement audio playback trigger after text stream completion in frontend/src/app.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Streaming Visual Feedback (Priority: P2)

**Goal**: Ensure summary text appears in real-time (streaming)

**Independent Test**: Can be tested by observing the network traffic and UI updates to ensure text arrives in chunks/tokens.

### Implementation for User Story 2

- [x] T011 [US2] Verify streaming chunk size and visual responsiveness in backend/src/agents/summary_agent.py (optimize if needed)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T012 Update Quickstart guide in specs/007-stream-summary-text/quickstart.md if usage changed
- [x] T013 Run full regression tests for backend and frontend

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
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable

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
Task: "Create unit test for `summarize_stream` in backend/tests/unit/test_summary_agent.py"
Task: "Create integration test for `/summary_stream` in backend/tests/integration/test_integration_summary.py"

# Launch all models for User Story 1 together:
# (No specific models tasks in this story, but parallel implementation tasks exist)
Task: "Implement `summarize_stream` method in backend/src/agents/summary_agent.py"
Task: "Add `/summary_stream` endpoint to backend/src/api/summary.py"
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