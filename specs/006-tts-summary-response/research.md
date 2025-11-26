# Research: TTS Summary Response

## Decision Log

### 1. Framework Selection
**Decision**: Use `google-adk` (Agent Development Kit) v1.18.0+.
**Rationale**: Explicitly requested by user. The library exists, is actively maintained (v1.18.0 released Nov 2025), and supports model-agnostic backends including local LLMs via LiteLLM compatibility.
**Alternatives**:
- *Direct Function Call*: Simpler but violates user constraints.
- *LangChain/CrewAI*: More mature ecosystems, but not what was requested.

### 2. Integration with Local MedGemma (Ollama)
**Decision**: Configure `google-adk` to use the existing Ollama endpoint.
**Details**: `google-adk` abstracts the model provider. We will define a custom model config that points to the local Ollama instance (`http://localhost:11434`), likely using its compatibility layer or a custom provider definition if required.
**Fallback**: If native Ollama support is tricky, use `litellm` as a bridge, which `google-adk` supports.

### 3. Agent Architecture
**Decision**: Create a single `SummaryAgent` responsible for the transformation.
**Responsibility**:
- Input: Full text response from MedGemma.
- Process: Prompt a model (MedGemma itself) to summarize.
- Output: Clean text for TTS.
**Tools**: The agent does not need external tools, just the summarization capability. It functions more as a "chain" or single-turn agent.

### 4. Audio Pipeline
**Decision**: Sequential piping.
**Flow**: User Query -> Main Agent (MedGemma) -> Full Text -> Summary Agent (MedGemma) -> Summary Text -> TTS Service -> Audio.
**Latency Mitigation**: The Summary Agent should stream its output if possible, but given the single-paragraph constraint, buffering the short summary text before TTS is acceptable and safer for punctuation removal.

## Technical Details

### Dependencies
- `google-adk>=1.18.0`

### Agent Definition (Conceptual)
```python
from google_adk.agent import Agent
from google_adk.model import Model

# Configure to use local Ollama
model = Model.from_config(
    provider="ollama",
    model_name="medgemma:latest",
    base_url="http://localhost:11434"
)

summary_agent = Agent(
    model=model,
    system_prompt="You are a summarizer. Compress the input into one paragraph. Remove all punctuation."
)
```
