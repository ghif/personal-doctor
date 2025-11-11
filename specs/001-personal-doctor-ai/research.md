# Research: Technical Stack for Personal Doctor AI

**Date**: 2025-11-10

## Decisions

Based on the feature requirements and user-provided technology stack, the following decisions have been made:

1.  **Backend Framework**: FastAPI will be used to build the backend REST API.
2.  **Frontend Framework**: Streamlit will be used for the user interface.
3.  **LLM Integration**: The `ollama` Python library will be used within the FastAPI backend to communicate with the locally running MedGemma model served by Ollama.
4.  **Agent Logic**: The Google Agent Development Kit (ADK) will be used to structure the conversational logic, tool use, and state management of the AI assistant within the FastAPI application.

## Rationale

This architecture provides a robust and scalable solution:

-   **Separation of Concerns**: A dedicated FastAPI backend separates the core application logic from the Streamlit-based presentation layer. This makes the application easier to develop, test, and maintain.
-   **Performance**: FastAPI is a high-performance web framework, suitable for handling requests from the frontend efficiently.
-   **Structured Agent Development**: The Google ADK provides a clear and structured framework for building the agent. It is model-agnostic and allows for the definition of tools, which in this case will be the functions that interact with the Ollama-served LLM. The ADK's API Server, which is a pre-packaged FastAPI server, can be leveraged to expose the agent's functionality.
-   **Local-First**: This entire stack can be run locally, fulfilling the core privacy and local-inference requirements of the project.

## Alternatives Considered

-   **Streamlit-Only Architecture**: A simpler approach would be to build the entire application, including the backend logic, within Streamlit. This was rejected because it would lead to a monolithic application that is harder to scale and maintain as complexity grows.
-   **Direct Ollama Integration without ADK**: The FastAPI backend could directly call the `ollama` library without using the ADK. This was rejected because the ADK provides a valuable, structured approach to building agents, which will be beneficial as more complex conversational flows and tools are added.

## Implementation Notes

-   The FastAPI backend will expose a `/query` endpoint that the Streamlit frontend will call.
-   This endpoint will take a user's query (text, and later, image data).
-   The ADK-structured agent within FastAPI will process the query, call the Ollama service to get a response from the MedGemma model, and return the formatted response.

## Dependency Versions

Based on research into the latest stable releases, the following versions will be targeted for this project:

-   **Google ADK**: `1.18.0`
-   **Ollama Application**: `v0.12.10`
-   **Ollama Python Library**: `0.6.0`
-   **FastAPI**: `0.121.1`
-   **Streamlit**: `1.51.0`

This ensures we are building on the most recent and stable foundations for these rapidly evolving tools.

## ADK and FastAPI Integration

-   **State Management**: Leverage ADK's built-in session management for conversational history. For more complex state, consider an external store like Redis, managed via FastAPI's dependency injection.
-   **Asynchronous Operations**: Define all I/O-bound operations (API calls, etc.) within ADK tools as `async` functions to leverage FastAPI's concurrency. Use `BackgroundTasks` for long-running, non-blocking processes.
-   **Tool Structure**: Define tools as modular, single-purpose functions with clear type hinting. For more complex tools, consider a microservice approach using the Model Context Protocol (MCP).
-   **Authentication**: Secure FastAPI endpoints using standard methods like OAuth2 or API keys.

## Ollama Multimodal Input Handling

-   **Model**: Use the `amsaravi/medgemma-4b-it:q6` model for multimodal tasks.
-   **Function**: The `ollama.chat()` function is the primary method for sending both text and images.
-   **Image Handling**: Pass local file paths of images directly to the `images` parameter in `ollama.chat()`. The library handles the encoding.
-   **Limitations**: MedGemma has been primarily evaluated on single-image tasks. Performance with multiple images is not guaranteed.
-   **Prompting**: As a specialized model, MedGemma may be sensitive to prompt structure. Experimentation is key.
