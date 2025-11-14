# Quickstart: Streaming Text-to-Speech Output

**Date**: 2025-11-13
**Feature**: Streaming Text-to-Speech Output

## Overview

This document provides a quick guide on how to use the new text-to-speech (TTS) feature.

## Backend

The backend exposes a new API endpoint at `/tts` that accepts a JSON object with a `text` field. It uses Coqui TTS to generate an audio stream from the provided text and returns it as an `audio/mpeg` stream.

### Running the TTS Service

1.  **Install Coqui TTS**: Follow the instructions in the Coqui TTS documentation to install the library and download the necessary models.
2.  **Run the backend server**: `cd backend && uvicorn src.main:app --reload`

## Frontend

The frontend includes a new audio player component that can interact with the `/tts` endpoint.

### Using the Audio Player

1.  **Initiate Playback**: When a new message from MedGemma is received, the user can click the "Play Audio" button to initiate the TTS process.
2.  **Streaming Audio**: The audio player will then make a request to the `/tts` endpoint and stream the audio response, playing it back in real-time.
3.  **Controls**: The user can mute and unmute the audio using the provided controls.
