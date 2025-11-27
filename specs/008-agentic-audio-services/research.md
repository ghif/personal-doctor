# Research: Agentic Audio Services

**Feature**: Agentic Audio Services (Branch: `008-agentic-audio-services`)
**Date**: 2025-11-26

## 1. Google ADK Tool Structure

**Context**: We need to implement `TranscribeTool` and `TextToSpeechTool` compatible with Google ADK.

**Findings**:
- Google ADK (Python) typically uses a `Tool` class or function decorators to define tools.
- Tools need a `name`, `description`, and a `run` (or similar) method.
- Reference: `google.adk.tools.Tool` (based on typical ADK patterns, though specific import might vary, we will assume standard ADK/LangChain-style interfaces or simple function wrapping if ADK supports it).

**Decision**:
- Create a new directory `backend/src/tools/` to house these tools.
- Implement tools as classes inheriting from `google.adk.tools.Tool` (if available) or simple python classes that the Agent can accept.
- Each tool will instantiate or use the existing singleton services from `src/services/audio/`.

**Rationale**:
- Keeps the "Tool" logic (agent interface) separate from the "Service" logic (business logic).
- Allows the services to be used by both API endpoints (direct) and Tools (agentic).

## 2. Integration with ChatService

**Context**: The `ChatService` initializes the `Agent`. We need to pass these new tools to it.

**Decision**:
- Update `ChatService.__init__` to accept a list of tools or initialize them internally.
- Pass `tools=[TranscribeTool(), TextToSpeechTool()]` to the `Agent` constructor.

**Rationale**:
- Makes the agent aware of its capabilities.

## 3. API vs Agent Use

**Context**: Existing endpoints call services directly. Should they call Tools instead?

**Decision**:
- **No.** API endpoints should continue calling `src/services/audio/*` directly.
- Tools are wrappers *around* services for the Agent's benefit.
- Calling a Tool from an API endpoint adds unnecessary abstraction overhead (Agent Tool logic) when we just want the function result.

**Rationale**:
- Performance and simplicity. Tools are for the LLM to use; Services are for the application to use. They share the same underlying logic.
