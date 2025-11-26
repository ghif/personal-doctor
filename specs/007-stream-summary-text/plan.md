# Implementation Plan: Stream Summary Text and Audio

**Branch**: `007-stream-summary-text` | **Date**: 2025-11-26 | **Spec**: [link](./spec.md)
**Input**: Feature specification from `/specs/007-stream-summary-text/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This feature implements an interactive "Play Audio Summary" capability. The backend `SummaryAgent` will be updated to stream text chunks using `litellm.acompletion`, exposed via a new `/summary_stream` API endpoint. The Streamlit frontend will use `st.write_stream` to display this text in real-time and, upon completion, automatically trigger the existing TTS service to play the audio of the generated summary.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI, Streamlit, LiteLlm, Google ADK
**Storage**: N/A (Transient)
**Testing**: pytest
**Target Platform**: Local Machine (macOS/Linux)
**Project Type**: web (Frontend + Backend)
**Performance Goals**: TTFT < 2s for summary.
**Constraints**: Local execution, privacy-first.
**Scale/Scope**: Single user, local deployment.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Privacy First**: PASS. All processing is local (or via local-ish API if configured). No data storage.
- **Safety by Design**: PASS. Summary does not alter medical advice fundamental meaning (checked by "concise" instruction).
- **Local-First Execution**: PASS. Uses local components.
- **High-Quality User Experience**: PASS. Streaming improves responsiveness.

## Project Structure

### Documentation (this feature)

```text
specs/007-stream-summary-text/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── agents/
│   │   └── summary_agent.py   # Update for streaming
│   ├── api/
│   │   └── summary.py         # Update/Add streaming endpoint
│   └── main.py
└── tests/
    └── unit/
        └── test_summary_agent.py

frontend/
├── src/
│   ├── app.py                 # UI Logic for button and streaming
│   └── services/
│       └── api_service.py     # Add summary_stream call
└── tests/
```

**Structure Decision**: Web application (Option 2).