# Implementation Plan: Agentic Audio Services

**Branch**: `008-agentic-audio-services` | **Date**: 2025-11-26 | **Spec**: [link](./spec.md)
**Input**: Feature specification from `/specs/008-agentic-audio-services/spec.md`

## Summary

Refactor the backend to wrap existing `TranscriptionService` and `TTSService` into Google ADK-compatible Tools (`TranscribeTool`, `TextToSpeechTool`). These tools will be registered with the `ChatService` agent, enabling agentic capabilities while preserving existing direct API functionality.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI, Google ADK, LiteLlm
**Storage**: N/A
**Testing**: pytest
**Target Platform**: Local Machine
**Project Type**: web (backend)

## Constitution Check

- **Privacy First**: PASS. Local processing.
- **Safety by Design**: PASS. No change to safety logic.
- **Local-First Execution**: PASS.
- **High-Quality User Experience**: PASS.

## Project Structure

### Documentation (this feature)

```text
specs/008-agentic-audio-services/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
└── tasks.md
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── tools/                 # NEW DIRECTORY
│   │   ├── __init__.py
│   │   ├── audio_tools.py     # NEW FILE: Tool wrappers
│   ├── services/
│   │   ├── llm/
│   │   │   └── chat.py        # UPDATE: Register tools
└── tests/
    └── unit/
        └── test_audio_tools.py # NEW FILE
```

**Structure Decision**: Web application (Option 2).