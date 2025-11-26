# Tasks: TTS Summary Response

**Feature**: TTS Summary Response  
**Spec**: [specs/006-tts-summary-response/spec.md](spec.md)  
**Status**: Pending

## Phase 1: Setup
**Goal**: Initialize environment and dependencies for ADK integration.

- [x] T001 Install `google-adk` dependency by adding it to `backend/requirements.txt`
- [x] T002 Verify Ollama connection and MedGemma model availability by running a curl check (document in `backend/README.md` if needed)
- [x] T003 Create directory structure for agents: `backend/src/agents/`

## Phase 2: Foundation
**Goal**: Establish base agent structure and API scaffolding.

- [x] T004 Create `backend/src/agents/__init__.py` to export agent modules
- [x] T005 Create `backend/src/agents/summary_agent.py` with basic class structure for `SummaryAgent` using ADK
- [x] T006 Create `backend/src/api/summary.py` with placeholder `POST /api/summary-tts` endpoint
- [x] T007 Register new router in `backend/src/main.py` to include `/api/summary-tts`

## Phase 3: User Story 1 - Hear Concise Audio Summary (P1)
**Goal**: Generate a text summary from full text and play it via TTS.
**Independent Test**: Verify `/api/summary-tts` accepts long text and returns audio of a shorter version.

- [x] T008 [US1] Implement ADK model configuration in `backend/src/agents/summary_agent.py` to connect to local Ollama
- [x] T009 [US1] Implement `summarize` method in `SummaryAgent` with a prompt to compress text into a single paragraph
- [x] T010 [US1] Create unit test `backend/tests/unit/test_summary_agent.py` to verify summarization output length
- [x] T011 [US1] Update `backend/src/api/summary.py` to call `SummaryAgent.summarize` then `tts_service.text_to_speech_stream`
- [x] T012 [US1] Update `frontend/src/services/tts_service.py` to point to the new `/api/summary-tts` endpoint (or create toggle)
- [x] T013 [US1] Update `frontend/src/components/audio_player.py` or relevant UI component to use the new summary service

## Phase 4: User Story 2 - Continuous Audio Stream (P2)
**Goal**: Ensure summary is punctuation-free for fluid listening.
**Independent Test**: Send text with punctuation, verify audio/text sent to TTS has none.

- [x] T014 [US2] Update system prompt in `backend/src/agents/summary_agent.py` to explicitly forbid punctuation
- [x] T015 [US2] Add regex post-processing in `backend/src/agents/summary_agent.py` to strictly remove any remaining punctuation (`,` `.` `?` `!`)
- [x] T016 [US2] Add test case to `backend/tests/unit/test_summary_agent.py` verifying input with punctuation yields clean output

## Phase 5: Polish
**Goal**: Finalize integration and handle edge cases.

- [x] T017 Handle empty/short text inputs in `SummaryAgent` (bypass summarization if text < 50 words but still strip punctuation)
- [x] T018 Add error handling in `backend/src/api/summary.py` for agent timeouts or failures (fallback to original text or error)
- [x] T019 Update `backend/README.md` with instructions on configuring ADK/Ollama for this feature

## Implementation Strategy
- **MVP**: Complete Phase 1-3. This delivers the core summarization agent.
- **Incremental**: Phase 4 improves the quality (punctuation removal) which is a key requirement.
- **Parallelism**: Frontend updates (T012, T013) can happen alongside Backend agent work (T008, T009).

## Dependencies
- Phase 1 -> Phase 2 -> Phase 3 -> Phase 4 -> Phase 5
- T005 (Agent scaffolding) blocks T008 (Agent impl)
- T006 (API scaffolding) blocks T011 (API impl)