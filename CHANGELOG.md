# RULE TO WRITE CHANGE LOG
- feat: add a feature.
- fix: fix bugs for the system.
- refactor: fixes the code but does not fix bugs nor add features or duplicates when bugs are also fixed from the refactor work.
- docs: add/change documents.
- chores: tiny modifications unrelated to the code.
- style: these changes do not change the meaning of the code like css/ui.
- perf: improved code performance of code.
- vendor: update versions for packages, dependencies.

# Version 0.9.0 
- **feat**:
    + UI for chatbot
    + Redis for vector database
    + Data ingestion pipeline API
    + Langfuse for monitoring chatbot
    
- **fix**:

- **refractor**:

- **docs**:
    + Init documents for chatbot include README
- **chore**:

- **style**:

- **perf**:

- **vendor**:
    + Init requirements for chatbot

# Version 0.9.1
- **feat**:
    + Add datalayer to handle userfeedback (user feedback will store into langfuse with name "user_feedbacks"), help product to easy to track the effective of your AI models from user
    
- **fix**:

- **refractor**:
    + refractor HTTP message to json object, it will benefit for expand and maintain product
    + refractor load_model method to TABLE_FUNCTION, it will benefit for expand product in the future 
- **docs**:
    + Update README
    + Add changelog
- **chore**:
    + Move REDIS_HOST from configs/config.yaml to .env file to make sense with config LANGFUSE_HOST config
- **style**:

- **perf**:

- **vendor**:
