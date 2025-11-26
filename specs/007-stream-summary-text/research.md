# Research: Stream Summary Text and Audio

**Feature**: Stream Summary Text and Audio (Branch: `007-stream-summary-text`)
**Date**: 2025-11-26

## 1. Streaming from Summary Agent

**Context**: The `SummaryAgent` currently uses the ADK `Agent` class which abstracts the LLM call and returns a complete response. To support streaming (FR-004), we need to bypass the standard `Agent.run()` method if it doesn't support streaming iterators, or use the underlying model directly.

**Findings**:
- The `QueryAgent` (existing) already implements streaming by using `litellm.acompletion` directly.
- `Google ADK`'s `Agent` abstraction might be too rigid for fine-grained control over streaming tokens if not explicitly designed for it.

**Decision**:
- Adopt the `litellm.acompletion` pattern used in `QueryAgent` for the `SummaryAgent`.
- This ensures consistency and allows us to yield tokens as they are generated.

**Rationale**:
- Proven pattern in the codebase.
- Direct control over the stream (e.g., stopping generation, handling errors per chunk).
- Avoids fighting with the ADK abstraction if it lacks native streaming support for this specific provider.

## 2. Frontend Streaming & Audio Trigger

**Context**: We need to display text as it arrives (FR-005) and *then* play audio (FR-006). Streamlit's execution model is top-down.

**Findings**:
- `st.write_stream(iterator)` is available in Streamlit. It consumes a generator and displays text incrementally.
- Crucially, `st.write_stream` returns the final complete text string once the stream is finished.
- This allows a synchronous flow in the script:
  ```python
  stream_generator = api.get_summary_stream(...)
  final_text = st.write_stream(stream_generator)
  if final_text:
      # Now play audio using the final text
      play_audio(final_text)
  ```

**Decision**:
- Use `st.write_stream` for the visual component.
- Use the return value of `st.write_stream` to trigger the audio playback logic immediately in the following lines of code.

**Rationale**:
- Native Streamlit capability.
- Simplifies state management (no need to manually accumulate chunks in session state just to detect "end").
- Perfectly matches the "Text then Audio" requirement.

## 3. Backend API Design

**Context**: We need an endpoint that streams the summary text.

**Decision**:
- Create/Update `POST /summary_stream` (or similar) using FastAPI's `StreamingResponse`.
- Media type: `text/event-stream` (or `text/plain` with chunked transfer, but event-stream is standard for LLMs).

**Rationale**:
- Standard FastAPI pattern.
- Compatible with `httpx` streaming client used by Streamlit frontend.

## 4. TTS Integration

**Context**: The feature requires playing audio *after* the text summary is complete.

**Decision**:
- Reuse the existing `/tts` endpoint or `tts_service` in the backend.
- The frontend will first call `/summary_stream` -> get full text -> then call `/tts` (or a new frontend service method that calls `/tts`) to get the audio.

**Alternative Considered**:
- **Streaming Audio (TTS) immediately**: We could try to stream audio *while* the text is generating.
- **Reason for Rejection**: The spec explicitly says "play the audio... *after* the text stream completes" (FR-006). Also, the `SummaryAgent` removes punctuation which is best done on the full paragraph or at least sentence-level, making character-by-character audio streaming complex and potentially glitchy. Batching the audio generation after text completion is safer and meets the requirement.
