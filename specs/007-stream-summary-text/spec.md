# Feature Specification: Stream Summary Text and Audio

**Feature Branch**: `007-stream-summary-text`
**Created**: 2025-11-26
**Status**: Draft
**Input**: User description: "when users click "Play Audio Summary" on frontend, show a short paragraph summary of the query agent's output first on the display in streaming mode. and then play the audio of the summarized output cntent"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Interactive Summary & Playback (Priority: P1)

As a user, I want to click a button to see a concise summary of the AI's response stream onto the screen and then hear it spoken, so that I can quickly grasp the key information both visually and auditorily without reading the full detailed text.

**Why this priority**: This is the core functionality requested: an interactive, multi-modal way to consume summaries.

**Independent Test**: Can be tested by generating a long response, clicking the "Play Audio Summary" button, and verifying the sequence of events (text streaming -> audio playback).

**Acceptance Scenarios**:

1. **Given** a response from the query agent is displayed, **When** I click "Play Audio Summary", **Then** a new area/modal/element appears displaying the summary text as it is being generated (streaming).
2. **Given** the summary text has finished streaming, **When** the text is complete, **Then** the audio playback of that summary starts automatically.
3. **Given** the audio is playing, **When** I listen, **Then** the content matches the displayed summary text.

---

### User Story 2 - Streaming Visual Feedback (Priority: P2)

As a user, I want to see the summary text appear in real-time (streaming) rather than waiting for the entire block to load, so that the application feels responsive.

**Why this priority**: "Streaming mode" was explicitly requested and improves perceived performance.

**Independent Test**: Can be tested by observing the network traffic and UI updates to ensure text arrives in chunks/tokens.

**Acceptance Scenarios**:

1. **Given** I have clicked "Play Audio Summary", **When** the summary is loading, **Then** characters/words appear sequentially on the screen.

### Edge Cases

- **Summary Generation Failure**: If the backend fails to generate a summary, the UI should show an error and not attempt to play audio.
- **Empty/Short Response**: If the original response is too short to summarize, the system should perhaps just stream the original text (cleaned) and play it.
- **User Interrupts**: If the user clicks "Stop" or navigates away while streaming/playing, the action should cease.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The Frontend MUST provide a "Play Audio Summary" button associated with the latest Query Agent response.
- **FR-002**: When "Play Audio Summary" is clicked, the Frontend MUST request a summary from the Backend.
- **FR-003**: The Backend MUST generate a short paragraph summary of the referenced response.
- **FR-004**: The Backend MUST stream the summary text to the Frontend as it is generated (or simulated if generation is instant).
- **FR-005**: The Frontend MUST display the summary text in a "streaming" fashion (updating incrementally) as data arrives.
- **FR-006**: The Frontend MUST automatically start audio playback of the summary text immediately after the text stream completes.
- **FR-007**: The Audio content MUST match the displayed summary text.

### Key Entities *(include if feature involves data)*

- **Summary Stream**: A stream of text tokens representing the summary.
- **Summary Audio**: The speech synthesis output corresponding to the Summary Text.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Time to First Token (TTFT) for the summary text display is under 2 seconds after button click.
- **SC-002**: Audio playback starts within 1 second of text streaming completion.
- **SC-003**: The displayed summary text and the spoken audio content are identical (ignoring minor formatting like invisible punctuation used for TTS hints).

## Assumptions

- The existing `SummaryAgent` can be adapted or wrapped to support streaming output (or produces output fast enough that chunked delivery is feasible).
- The TTS service can generate audio from the final summary text reasonably quickly (or audio generation can be pipelined, though strict "text first then audio" implies we might wait for text completion to ensure consistency, or start TTS generation in parallel but play only after text is done).
- "Query Agent's output" refers to the last assistant message in the chat history.