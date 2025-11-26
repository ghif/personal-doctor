# Data Model: Stream Summary Text and Audio

**Feature**: Stream Summary Text and Audio
**Branch**: `007-stream-summary-text`

## Conceptual Entities

### SummaryRequest
Represents the input required to generate a summary.

- **text** (string, required): The original text content (e.g., the full medical response) that needs to be summarized.

### SummaryStream
Represents the transient flow of text data from the backend to the frontend.

- **chunk** (string): A fragment of the generated summary text (e.g., a word or a few tokens).

### AudioRequest
Represents the input for the TTS service (existing entity, re-confirmed).

- **text** (string, required): The summarized text to be converted to speech.

## Persistence

- **None**: This feature deals strictly with transient data (streaming text and audio). No new database tables or persistent storage are required. The summary is generated on-the-fly and discarded after presentation (unless the user saves the chat, which is a separate concern).
