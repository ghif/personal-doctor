# Research: Open-Source, Local, Streaming Text-to-Speech (TTS)

**Date**: 2025-11-13
**Feature**: Streaming Text-to-Speech Output

## Decision

We will use **Coqui TTS** as the primary text-to-speech engine for this feature.

## Rationale

The selection of Coqui TTS is based on the following criteria:

- **Open-Source**: Coqui TTS is an open-source library, which aligns with the project's goal of using open-source technologies.
- **Local-First**: It can be run entirely on a local machine, which is a core requirement of the project's constitution (Privacy First, Local-First Execution).
- **Streaming Support**: Coqui TTS supports streaming output, which is essential for providing a real-time, low-latency user experience. The XTTSv2 model, in particular, is capable of streaming with less than 200ms latency.
- **Apple M4 Pro Compatibility**: Coqui TTS can leverage GPU acceleration, which makes it well-suited for running on modern hardware like the Apple M4 Pro, ensuring efficient local synthesis.
- **High-Quality Voice**: As a deep learning-based TTS library, Coqui TTS offers more natural-sounding voices compared to older, more robotic-sounding TTS engines.
- **Python Integration**: It has a Python API, which will allow for seamless integration with the existing Python-based backend.

## Alternatives Considered

- **Resemble AI Chatterbox**: This is a strong contender and also offers low-latency, real-time streaming. However, Resemble AI is a commercial entity, and while Chatterbox has an open-source model, it is tied to a commercial service. This conflicts with the project's constitution, which prioritizes fully open-source and local-first solutions. Coqui TTS, being fully open-source, is a better fit for the project's principles.
- **Kyutai's Open-source TTS Model**: While promising and specifically optimized for Apple Silicon, Coqui TTS is more mature and has a larger community, which means better documentation and support.
- **RealtimeTTS**: This is a wrapper library that can use Coqui TTS as a backend. While it could be useful, it adds an extra layer of abstraction. For now, we will directly integrate with Coqui TTS to have more control over the implementation.
- **Mimic TTS (Mycroft AI)**: Another good open-source option, but Coqui TTS is generally considered to have higher-quality voices.
- **pyttsx3**: This library uses the native macOS TTS engine. While it's easy to use, the voice quality is not as high as modern deep learning models.
