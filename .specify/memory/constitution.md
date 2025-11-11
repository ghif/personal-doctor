# Personal Doctor AI Constitution

## Core Principles

### I. Privacy First (NON-NEGOTIABLE)
All data, including user queries, images, and conversation history, MUST remain on the user's local machine. No data should be sent to any external cloud service for processing or storage without explicit, opt-in consent for a specific, clearly defined purpose.

### II. Safety by Design (NON-NEGOTIABLE)
The assistant is an educational tool, not a medical professional. All health-related information provided MUST be accompanied by a clear, prominent disclaimer. Triage logic MUST err on the side of caution, recommending professional medical consultation for any non-trivial symptom. The system MUST NOT provide diagnoses or prescriptions.

### III. Local-First Execution
The core functionality of the AI assistant MUST operate entirely on the user's local machine. This includes the AI model, the application server, and the user interface. Cloud services should only be used for non-essential, optional features that do not compromise the privacy of core user interactions.

### IV. Test-Driven Development
All new features MUST be accompanied by a comprehensive suite of tests, including unit, integration, and end-to-end tests where appropriate. For safety-critical components like triage logic, a curated dataset of test cases MUST be used to validate behavior before release.

### V. High-Quality User Experience
The interface should be simple, intuitive, and accessible. Interactions should be responsive, with performance goals established and measured to ensure a smooth user experience.

## Governance
This constitution is the highest authority for this project, superseding all other design documents or team practices. Any proposed amendment to this constitution requires a formal review and approval process, including an analysis of its impact on user privacy and safety. All code reviews MUST include a check for compliance with these principles.

**Version**: 1.0.0 | **Ratified**: 2025-11-11 | **Last Amended**: N/A
