# Data Model: Transcription Service

This document outlines the data structures used in the backend voice-to-text transcription service.

## Entities

### TranscriptionRequest

Represents the incoming request to the transcription service.

**Fields**:
- `audio_file`: The audio data to be transcribed. The supported format is WAV.

### TranscriptionResponse

Represents the response from the transcription service.

**Fields**:
- `text`: (string) The transcribed text from the audio file.

## Validation Rules

- The `audio_file` must be a valid WAV file.
- The request size should be limited to a reasonable size to prevent abuse (e.g., 10MB).

## State Transitions

N/A - The service is stateless. It receives a request, processes it, and returns a response without maintaining any state.