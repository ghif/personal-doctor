# Feature Specification: TTS Summary Response

**Feature Branch**: `006-tts-summary-response`  
**Created**: 2025-11-25  
**Status**: Draft  
**Input**: User description: "The text-to-speech module should generate the audio based on the summarized response from the main LLM (MedGemma), not the original LLM's output. The summarized output should be in a single paragraph without any punctuations so that users don't need to hear the complete original response from the LLM."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Hear Concise Audio Summary (Priority: P1)

As a user interacting with the Personal Doctor AI, I want to hear a concise summary of the medical advice instead of the full detailed text, so that I can get the key information quickly without listening to a long speech.

**Why this priority**: This is the core value proposition of the feature—reducing the time and cognitive load required to consume the AI's response via audio.

**Independent Test**: Can be tested by asking a complex medical question and verifying that the audio output is significantly shorter than the displayed text and captures the main points.

**Acceptance Scenarios**:

1. **Given** the user asks a question that generates a long, multi-paragraph response, **When** the response is ready, **Then** the audio played is a summarized version of the text.
2. **Given** the audio is playing, **When** I compare it to the displayed text, **Then** the audio content matches the core meaning but is much shorter.

---

### User Story 2 - Continuous Audio Stream (Priority: P2)

As a user, I want the audio summary to be spoken as a continuous flow without punctuation-induced pauses, so that the listening experience is rapid and fluid.

**Why this priority**: This fulfills the specific formatting constraint ("no punctuations") requested to optimize the listening experience.

**Independent Test**: Can be tested by inspecting the text sent to the TTS engine and verifying the absence of punctuation marks.

**Acceptance Scenarios**:

1. **Given** a summary is generated, **When** it is sent to the TTS engine, **Then** the text contains no punctuation marks (periods, commas, question marks, etc.).
2. **Given** the summary is generated, **When** it is inspected, **Then** it consists of a single paragraph.

### Edge Cases

- What happens when the original response is already very short? (The summary should probably just be the original text, stripping punctuation).
- What happens if the summarization fails? (Fallback to original text or error message).
- Does "no punctuation" include removing apostrophes in contractions (e.g., "don't" -> "dont")? (Assume yes for strict adherence, or "don t"). *Assumption: Remove all standard punctuation characters.*

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST generate a text summary of the main LLM (MedGemma) response specifically for audio output.
- **FR-002**: The summary generated MUST be a single paragraph.
- **FR-003**: The summary generated MUST NOT contain any punctuation characters (e.g., `.`, `,`, `?`, `!`, `;`, `:`, `"`).
- **FR-004**: The TTS service MUST receive the generated summary as input, NOT the full original response.
- **FR-005**: The system MUST continue to display the full, original response text in the UI for the user to read.
- **FR-006**: The summarization process MUST occur automatically after the main LLM response is generated.

### Key Entities *(include if feature involves data)*

- **AudioSummary**: A string entity derived from the main response, characterized by brevity, single-paragraph structure, and absence of punctuation.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The word count of the text sent to TTS is at least 30% less than the word count of the original full response for responses > 100 words.
- **SC-002**: 100% of the text strings sent to the TTS engine contain zero punctuation characters (regex match `[^\w\s]`).
- **SC-003**: The audio generation latency (time from full text available to audio start) does not increase by more than 2 seconds due to the summarization step.