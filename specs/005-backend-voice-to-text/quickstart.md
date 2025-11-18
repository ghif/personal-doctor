# Quickstart: Backend Voice-to-Text Service

This guide provides a quick overview of how to use the new backend transcription service.

## Prerequisites

- The backend server is running.
- You have a WAV audio file to transcribe.

## Transcribing Audio

To transcribe an audio file, send a POST request to the `/transcribe` endpoint with the audio file as a multipart/form-data attachment.

### Example using cURL

```bash
curl -X POST -F "file=@/path/to/your/audio.wav" http://localhost:8000/transcribe
```

### Example Response

A successful request will return a JSON object with the transcribed text:

```json
{
  "text": "This is the transcribed text from the audio file."
}
```

## Error Handling

- If the audio file is invalid or in an unsupported format, the API will return a `400 Bad Request` error.
- If the transcription process fails on the server, the API will return a `500 Internal Server Error`.