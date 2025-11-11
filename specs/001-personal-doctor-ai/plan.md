# Implementation Plan: Personal Doctor AI Assistant

**Branch**: `001-personal-doctor-ai` | **Date**: 2025-11-10 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-personal-doctor-ai/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This feature implements the "Personal Doctor," a local, privacy-preserving multimodal AI assistant for healthcare support. It will provide educational content, triage suggestions, and symptom discussion via a chat interface, with inputs from text, speech, and images.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.11+
**Primary Dependencies**: Streamlit, FastAPI, Google ADK, Ollama, uv
**Storage**: N/A (stateless, for now)
**Testing**: pytest
**Target Platform**: macOS (Apple M4 Pro)
**Project Type**: Web application (frontend/backend)
**Performance Goals**: 95% of queries respond in < 5 seconds.
**Constraints**: < 8 GB memory footprint.
**Scale/Scope**: Single-user, local deployment.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Privacy First**: **PASS**. The plan specifies that all core functionality, including the AI model, runs on the user's local machine, with no cloud dependency. This aligns with the non-negotiable principle of keeping all data local.
- **II. Safety by Design**: **PASS**. The feature specification, which this plan is based on, mandates clear disclaimers (FR-004), prohibits diagnoses (FR-005), and requires triage to err on the side of caution (FR-008). The plan implements these requirements.
- **III. Local-First Execution**: **PASS**. The technical context explicitly states the project is a local-only deployment using Ollama, Streamlit, and FastAPI on the user's machine.
- **IV. Test-Driven Development**: **PASS**. The plan includes a dedicated testing phase (Phase 6) with tasks for unit and integration tests (T026, T027) and references `pytest` as the testing framework.
- **V. High-Quality User Experience**: **PASS**. The plan includes performance goals (<5s response time) and a focus on a simple chat interface, aligning with the goal of a high-quality UX.

## Project Structure

### Documentation (this feature)

```text
specs/001-personal-doctor-ai/
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
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/
```

**Structure Decision**: The project will use a two-part structure with a `frontend` directory for the Streamlit UI and a `backend` directory for the FastAPI application. Each directory will have its own isolated Python environment managed by the `uv` package manager.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
