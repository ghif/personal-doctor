# Implementation Plan: Streaming Text-to-Speech Output

**Branch**: `004-streaming-text-to-speech` | **Date**: 2025-11-13 | **Spec**: [link](./spec.md)
**Input**: Feature specification from `/specs/004-streaming-text-to-speech/spec.md`

## Summary

This plan outlines the implementation of a real-time, streaming text-to-speech (TTS) feature for the MedGemma assistant. The core requirement is to use an open-source TTS solution that can be deployed locally on a user's machine (specifically Apple M4 Pro) with acceptable latency for a real-time experience. The user will be able to initiate, mute, and unmute the audio playback.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI, Streamlit, Coqui TTS
**Storage**: N/A
**Testing**: pytest
**Target Platform**: Local machine (macOS with Apple M4 Pro)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: Audio latency < 2 seconds from text generation to playback.
**Constraints**: Must run entirely on the user's local machine.
**Scale/Scope**: Single-user application.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Check | Notes |
|---|---|---|
| I. Privacy First | PASS | The plan adheres to the Privacy First principle by specifying a local, open-source TTS solution, ensuring no data is sent to external cloud services. |
| II. Safety by Design | PASS | This feature does not directly impact the safety-critical aspects of the application, such as medical advice or triage logic. |
| III. Local-First Execution | PASS | The core requirement of the user is to have a local-first TTS solution, which is in line with this principle. |
| IV. Test-Driven Development | PASS | New components will require unit and integration tests. |
| V. High-Quality User Experience | PASS | The focus on low-latency, streaming audio output directly supports a high-quality user experience. |

## Project Structure

### Documentation (this feature)

```text
specs/004-streaming-text-to-speech/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── services/
│   │   └── tts_service.py # New service for TTS
│   └── api/
│       └── tts.py         # New API endpoint for TTS
└── tests/

frontend/
├── src/
│   ├── components/
│   │   └── audio_player.py # New component for audio playback
│   └── services/
│       └── tts_service.py  # New service to interact with the TTS API
└── tests/
```

**Structure Decision**: The existing frontend/backend structure will be extended with new services and components to handle the text-to-speech functionality.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|---|---|---|
| N/A | | |