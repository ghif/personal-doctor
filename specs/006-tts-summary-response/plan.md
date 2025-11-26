# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement a new "TTS Summary Agent" using the Agent Development Kit (ADK) to intercept the main MedGemma response, generate a concise, punctuation-free single-paragraph summary, and pipe this summary to the existing TTS service. This re-introduces the ADK framework (previously planned but missing) to orchestrate the post-processing logic as a distinct agentic workflow.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI, Ollama, Google ADK [NEEDS CLARIFICATION: Verify exact PyPI package name and version, e.g., is it `google-generativeai`?], Coqui TTS (existing)
**Storage**: N/A (Transient processing)
**Testing**: pytest
**Target Platform**: Local Execution (macOS/Linux)
**Project Type**: Backend Service
**Performance Goals**: Summary generation + TTS start < 2s added latency
**Constraints**: Must run locally (Ollama), output must be punctuation-free
**Scale/Scope**: Single new agent, one new API endpoint

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Privacy First**: [NEEDS RESEARCH] Verify that the chosen ADK library allows for strictly local execution with Ollama and does not send data to Google Cloud by default.
- **Safety by Design**: Summarization must retain the core medical advice caveats. The full text is still displayed, which mitigates safety risks of the summary.
- **Local-First Execution**: The implementation relies on the local MedGemma model via Ollama. The ADK must support this custom model provider.
- **Test-Driven Development**: Agent logic must be unit-testable.

## Project Structure

### Documentation (this feature)

```text
specs/006-tts-summary-response/
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
│   ├── agents/          # NEW: ADK Agent definitions
│   │   ├── __init__.py
│   │   └── summary_agent.py
│   ├── api/
│   │   └── summary.py   # NEW: Endpoint for summary generation
│   ├── services/
│   │   ├── query_service.py # Existing: Main LLM
│   │   └── tts_service.py   # Existing: TTS
│   └── main.py
```

**Structure Decision**: Introduce a new `agents/` directory to house ADK-specific logic, keeping it distinct from standard `services/`.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Introducing ADK | Requested by user | "Just a function" would be simpler but violates explicit constraint to use ADK |
