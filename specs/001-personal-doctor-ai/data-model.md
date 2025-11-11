# Data Models: Personal Doctor AI

**Date**: 2025-11-10

This document defines the core data entities for the Personal Doctor AI assistant, based on the feature specification.

## 1. UserQuery

Represents a single input from the user to the assistant.

| Field | Type | Description | Constraints |
|---|---|---|---|
| `query_text` | String | The text of the user's query. | Required. |
| `image_data` | String (Base64) | Optional. The user-uploaded image, encoded as a Base64 string. | - |
| `input_modality` | Enum | The method of input. | Required. Must be one of: `TEXT`, `SPEECH`, `IMAGE`. |
| `timestamp` | DateTime | The time the query was received. | Required. |

## 2. AIResponse

Represents a single response from the assistant to the user.

| Field | Type | Description | Constraints |
|---|---|---|---|
| `response_text` | String | The main text of the assistant's response. | Required. |
| `educational_content` | Array[String] | A list of URLs or snippets of educational material. | Optional. |
| `triage_suggestion` | Enum | The assistant's high-level suggestion. | Required. Must be one of: `SELF_CARE`, `SEE_DOCTOR`, `URGENT_CARE`, `INFO_ONLY`. |
| `disclaimer` | String | The standard non-clinical-grade disclaimer text. | Required. |
| `timestamp` | DateTime | The time the response was generated. | Required. |

## 3. Conversation

Represents a single, continuous interaction session between the user and the assistant.

| Field | Type | Description | Constraints |
|---|---|---|---|
| `conversation_id` | UUID | A unique identifier for the session. | Required. |
| `history` | Array[UserQuery \| AIResponse] | A chronological list of all queries and responses in the session. | Required. |
| `start_time` | DateTime | The time the conversation was initiated. | Required. |
| `end_time` | DateTime | The time the conversation was concluded. | Optional. |

## Relationships

- A `Conversation` contains a `history` array composed of one or more `UserQuery` and `AIResponse` objects.
- Each `UserQuery` is typically followed by one `AIResponse`.
