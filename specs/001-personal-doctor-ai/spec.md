# Feature Specification: Personal Doctor AI Assistant

**Feature Branch**: `001-personal-doctor-ai`
**Created**: 2025-11-10
**Status**: Draft
**Input**: User description: "Develop Personal Doctor, a local, privacy-preserving multimodal AI assistant (text + speech + image) tailored for healthcare support (educational, advisory/triage) on a user's local Apple M4 Pro machine. It uses MedGemma as the core AI foundation model served with Ollama. Key user flows are as follows: user speaks or types a question (e.g., 'I have chest pain and a mild cough'), optionally upload an image (e.g., skin lesion photo) or speak an image description, assistant responds via chat UI, optionally via voice, providing explanation, triage suggestion ('see a doctor'), and educational content, local-only inference: model and UI run on the user's MacBook, no cloud dependency for core inference. The scope of this tool is non-clinical grade (not a replacemet for a licensed physician). Must include disclaimers. The focus is on personal health education, symptom discussion, image interpretation support, and referral guidance."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Symptom Inquiry via Text (Priority: P1)
A user types a question about their symptoms (e.g., "I have a headache and nausea") into the chat interface. The assistant analyzes the text and responds with educational information about potential causes, suggestions for at-home care, and clear guidance on when to seek professional medical help.

**Why this priority**: This is the most fundamental interaction and provides the core value of the assistant.

**Independent Test**: Can be tested by inputting a text query and verifying that a relevant, safe, and educational response is returned, including a disclaimer.

**Acceptance Scenarios**:
1. **Given** the user is on the main chat screen, **When** they type "I have a persistent cough and slight fever" and submit, **Then** the system provides a response that includes potential non-serious causes (like a common cold), self-care tips, and a clear recommendation to see a doctor if symptoms persist or worsen, along with a non-clinical-grade disclaimer.
2. **Given** the user asks a non-medical question, **When** they type "What is the weather today?", **Then** the system responds that it can only answer health-related questions.

---

### User Story 2 - Symptom Inquiry with Image Upload (Priority: P2)
A user has a visual symptom, like a skin rash. They type a query such as "What could this be?" and upload a photo of the rash. The assistant analyzes both the text and the image to provide a more contextual response, offering educational information on possible skin conditions and strongly advising a consultation with a dermatologist for diagnosis.

**Why this priority**: Adds a critical modality for a wide range of common health concerns, enhancing the assistant's utility.

**Independent Test**: Can be tested by uploading a common medical image (e.g., a rash, a mole) with a text prompt and verifying the assistant provides a relevant, safe interpretation and a strong recommendation to see a specialist.

**Acceptance Scenarios**:
1. **Given** the user is on the main chat screen, **When** they upload an image of a mole and ask "Should I be worried about this?", **Then** the system provides educational information on skin health, emphasizes it cannot diagnose, and gives a strong recommendation to see a dermatologist for a professional evaluation.
2. **Given** the user uploads a non-medical image (e.g., a picture of a car), **When** they ask a health question, **Then** the system ignores the image and answers based only on the text, or informs the user the image is not relevant.

---

### User Story 3 - Voice-to-Text and Text-to-Speech Interaction (Priority: P3)
A user prefers to interact via voice. They activate the microphone, speak their question ("I've had a stomach ache for three days"), and the assistant transcribes it to text. The assistant then processes the query and, in addition to displaying the text response, reads it aloud to the user.

**Why this priority**: Improves accessibility and provides a more natural, hands-free interaction method.

**Independent Test**: Can be tested by speaking a health query, verifying the transcription is accurate, and confirming the assistant's response is both displayed as text and read aloud clearly.

**Acceptance Scenarios**:
1. **Given** the user enables the voice input, **When** they say "What are the symptoms of the flu?", **Then** the system accurately transcribes the question, displays a text-based answer detailing flu symptoms, and simultaneously reads the answer aloud.
2. **Given** the voice assistant is reading a response, **When** the user interrupts by activating the microphone again, **Then** the text-to-speech output stops immediately, and the system is ready to accept a new voice query.

### Edge Cases
- What happens when the user uploads a low-quality or ambiguous image?
- How does the system handle queries that are on the border of being an emergency (e.g., "mild chest discomfort")?
- How does the system respond to follow-up questions that build on the initial query?
- What happens if the user's speech is unclear or in a noisy environment?

## Requirements *(mandatory)*

### Functional Requirements
- **FR-001**: The system MUST run entirely on the user's local machine, with no cloud dependency for core AI model inference.
- **FR-002**: The system MUST accept user input via text, speech, and image uploads.
- **FR-003**: The system MUST provide responses in the chat UI and optionally via text-to-speech.
- **FR-004**: Every response containing health-related information MUST prominently display a disclaimer stating the assistant is not a substitute for a licensed physician.
- **FR-005**: The system's primary function is to provide educational content, symptom discussion, image interpretation support, and referral guidance; it MUST NOT provide diagnoses or prescriptions.
- **FR-006**: The system MUST use the MedGemma model via Ollama for its core AI foundation.
- **FR-007**: The system MUST be able to interpret conversational language and extract key symptoms from user queries.
- **FR-008**: The system's triage suggestions MUST err on the side of caution, recommending users "see a doctor" for any condition that cannot be confidently identified as minor.
- **FR-009**: The system MUST allow users to disable the text-to-speech functionality.
- **FR-010**: The system MUST handle basic conversational turn-taking (e.g., answering a question and being ready for a follow-up).
- **FR-011**: The system MUST use the Google ADK to manage conversational agent logic.

### Key Entities *(include if feature involves data)*
- **UserQuery**: Represents a single interaction from the user. Contains the input text, an optional attached image, and the input modality (text, speech).
- **AIResponse**: Represents the assistant's reply. Contains the response text, educational content links, and a triage suggestion (e.g., "Self-care", "See a doctor", "Urgent care").

## Success Criteria *(mandatory)*

### Measurable Outcomes
- **SC-001**: 95% of user health queries receive a relevant response in under 5 seconds on the target Apple M4 Pro machine.
- **SC-002**: For a curated test set of 100 common symptoms, the assistant's triage suggestion matches a pre-defined "safe" recommendation (e.g., correctly advising a doctor visit for chest pain) in at least 98% of cases.
- **SC-003**: Speech-to-text transcription of health queries achieves a Word Error Rate (WER) of less than 10% in a quiet environment.
- **SC-004**: In user testing, 90% of users successfully complete the primary task of asking a question and understanding the response without assistance.
- **SC-005**: The application's memory footprint MUST remain under 8 GB, ensuring it can run alongside other common applications without significant system degradation.