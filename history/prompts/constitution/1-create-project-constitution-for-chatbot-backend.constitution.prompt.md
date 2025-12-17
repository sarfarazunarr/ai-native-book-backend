---
id: 1
title: Create-project-constitution-for-chatbot-backend
stage: constitution
date: 2025-12-17
surface: agent
model: gpt-4
feature: none
branch: main
user: default
command: /sp.constitution
labels: [constitution,backend,ai,robotics]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```
/sp.constitution Project: Backend for Physical AI & Humanoid Robotics Chatbot

Core principles:

- Modularity: Separation of concerns between Scraper, Embedder, VectorStore, and Agent.

- Performance: Async-first approach (FastAPI + Async Qdrant/OpenAI).

- Reliability: Robust error handling for network-heavy tasks (scraping/API calls).

- Security: Secure handling of API_KEYs via environment variables (never hardcoded).

Key standards:

- All endpoints must be documented with FastAPI/Pydantic schemas.

- Logging: Use structured logging to track ingestion status and agent reasoning.

- Coding Style: PEP 8 compliant, type-hinted Python 3.10+.

- Dependency Management: Requirements.txt or pyproject.toml included.

Constraints:

- Framework: FastAPI

- Vector DB: Qdrant

- Embedding: Cohere (embed-english-v3.0 or latest)

- Agent Logic: OpenAI Agents SDK (Agent/Runner pattern)

Success criteria:

- 100% of sitemap URLs ingested and embedded correctly.

- Agent provides citations or "source" references from the book content.

- Response time for chat under 2 seconds (excluding initial embedding).
```

## Response snapshot

Created a new project constitution for the Physical AI & Humanoid Robotics Chatbot backend based on the specified principles. The constitution includes six core principles: Modularity, Performance, Reliability, Security, Documentation and Type Safety, and Observability. It also defines key standards, constraints, and governance procedures, with version 1.0.0 ratified on 2025-12-17.

## Outcome

- ✅ Impact: Created new project constitution file with all specified principles and constraints
- 🧪 Tests: No tests required for this constitution creation
- 📁 Files: Updated .specify/memory/constitution.md with new content
- 🔁 Next prompts: Ready for implementation based on these principles
- 🧠 Reflection: Successfully translated high-level specifications into a structured constitution

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Implementation of first feature based on these principles