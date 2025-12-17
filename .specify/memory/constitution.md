<!-- SYNC IMPACT REPORT
Version change: N/A -> 1.0.0
Modified principles: N/A (new constitution)
Added sections: All sections (new constitution)
Removed sections: N/A
Templates requiring updates: ⚠ pending - .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
Follow-up TODOs: None
-->
# Backend for Physical AI & Humanoid Robotics Chatbot Constitution

## Core Principles

### Modularity
Separation of concerns between Scraper, Embedder, VectorStore, and Agent. This ensures each component can be developed, tested, and maintained independently while maintaining clear interfaces between components.

### Performance
Async-first approach (FastAPI + Async Qdrant/OpenAI). All operations should be designed to support asynchronous execution to maximize throughput and minimize blocking operations, ensuring optimal performance under load.

### Reliability
Robust error handling for network-heavy tasks (scraping/API calls). Network operations must include appropriate retry mechanisms, timeouts, and graceful degradation to maintain service availability despite external service fluctuations.

### Security
Secure handling of API_KEYs via environment variables (never hardcoded). All sensitive credentials must be stored securely outside the codebase and accessed through secure configuration management to prevent accidental exposure.

### Documentation and Type Safety
All endpoints must be documented with FastAPI/Pydantic schemas. The codebase must be PEP 8 compliant with comprehensive type hints using Python 3.10+ features to ensure code clarity and prevent type-related errors.

### Observability
Structured logging to track ingestion status and agent reasoning. All components must emit structured logs with appropriate metadata to enable debugging, monitoring, and performance analysis of the system.

## Key Standards

All endpoints must be documented with FastAPI/Pydantic schemas. Logging: Use structured logging to track ingestion status and agent reasoning. Coding Style: PEP 8 compliant, type-hinted Python 3.10+. Dependency Management: Requirements.txt or pyproject.toml included.

## Constraints

Framework: FastAPI. Vector DB: Qdrant. Embedding: Cohere (embed-english-v3.0 or latest). Agent Logic: OpenAI Agents SDK (Agent/Runner pattern).

## Governance

This constitution establishes the foundational principles for the Physical AI & Humanoid Robotics Chatbot backend. All implementation decisions must align with these principles. Any deviation requires explicit documentation of the rationale and approval from the project maintainers. Version changes follow semantic versioning, with major changes requiring community review and approval.

**Version**: 1.0.0 | **Ratified**: 2025-12-17 | **Last Amended**: 2025-12-17