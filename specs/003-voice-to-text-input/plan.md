# Implementation Plan: Voice-to-Text Input

**Branch**: `003-voice-to-text-input` | **Date**: 2025-11-11 | **Spec**: [./spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-voice-to-text-input/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This feature adds voice input to the frontend application. It will use Streamlit's audio input to capture user speech, display the recording with playback, and transcribe it to text. The transcribed text will serve as input for the MedGemma model, supporting both English and Bahasa Indonesia.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Streamlit
**Storage**: N/A
**Testing**: pytest
**Target Platform**: Web browser
**Project Type**: Web application (existing frontend/backend structure)
**Performance Goals**: Transcription latency < 3 seconds; Word Error Rate (WER) < 10%.
**Constraints**: Must use Streamlit for audio capture, support English and Bahasa Indonesia, handle microphone permissions gracefully, and provide clear visual feedback for recording and transcription states.
**Scale/Scope**: Single-user interaction at a time.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Privacy First (NON-NEGOTIABLE)**: **NEEDS CLARIFICATION**. The feature requires audio transcription. Sending audio to an external service would violate this principle. Research is required to determine if a high-quality, local-only transcription model is feasible. If not, explicit user opt-in is mandatory.
- **II. Safety by Design (NON-NEGOTIABLE)**: **PASS**. The feature transcribes user input, which is then processed by the existing MedGemma model. It does not introduce new safety risks, but existing disclaimers remain critical.
- **III. Local-First Execution**: **NEEDS CLARIFICATION**. Same as the "Privacy First" check. An external transcription service would violate this. The primary goal is to find a viable local-first solution.
- **IV. Test-Driven Development**: **PASS**. New components will be developed with corresponding unit and integration tests.
- **V. High-Quality User Experience**: **PASS**. The specification includes clear requirements for visual feedback and usability, aligning with this principle.

## Project Structure

### Documentation (this feature)

```text
specs/003-voice-to-text-input/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
```text
frontend/
├── src/
│   ├── app.py
│   ├── components/
│   │   └── voice_recorder.py
│   └── services/
│       └── transcription_api_service.py
└── tests/
    └── test_voice_recorder.py
```

**Structure Decision**: The feature will be implemented within the existing `frontend` directory. A new `voice_recorder.py` component will handle the UI and audio capture. A `transcription_api_service.py` will be created or updated to handle the transcription logic. `app.py` will be modified to integrate the new component.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Potential use of external transcription service | Achieving high-accuracy, multi-language (English, Bahasa Indonesia) transcription with a purely local model may be difficult and resource-intensive. | A local-only model might have lower accuracy or require significant local compute resources (CPU, RAM, disk space), potentially degrading the user experience. This will be investigated during the research phase. |
