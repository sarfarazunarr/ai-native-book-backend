---

description: "Task list for AI-powered Chatbot for Physical AI & Humanoid Robotics Book implementation"
---

# Tasks: AI-Powered Chatbot for Physical AI & Humanoid Robotics Book

**Input**: Design documents from `/specs/1-ai-book-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Unit tests, integration tests, and mock agent response tests as specified in the plan.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/` with subdirectories for different modules
- **Tests**: `backend/tests/` at repository root
- **Configuration**: `.env` and `requirements.txt` at repository root

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan in backend/
- [ ] T002 Initialize Python 3.10+ project with FastAPI, Qdrant, Cohere, OpenAI, BeautifulSoup, httpx dependencies in requirements.txt
- [ ] T003 [P] Configure linting and formatting tools (flake8, black, mypy)
- [ ] T004 Create .env file structure with placeholders for API keys

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 Setup configuration management for environment variables in backend/src/config.py
- [ ] T006 [P] Setup logging infrastructure in backend/src/logging_config.py
- [ ] T007 [P] Setup database schema and Qdrant connection in backend/src/vector_db.py
- [ ] T008 Create base models/entities that all stories depend on based on data-model.md in backend/src/models/
- [ ] T009 Setup API routing and middleware structure in backend/src/main.py
- [ ] T010 Configure error handling infrastructure in backend/src/exceptions.py
- [ ] T011 Setup health check endpoint in backend/src/api/health.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Ask Questions About Robotics Content (Priority: P1) 🎯 MVP

**Goal**: Enable users to submit questions via the /chat endpoint and receive answers that cite specific content from the book, demonstrating the system successfully retrieves relevant information.

**Independent Test**: Users can submit questions via the /chat endpoint and receive answers that cite specific content from the book.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T012 [P] [US1] Contract test for /chat endpoint in backend/tests/contract/test_chat_contract.py
- [ ] T013 [P] [US1] Integration test for Qdrant "Search" tool return values in backend/tests/integration/test_search_tool.py
- [ ] T014 [P] [US1] Mock agent response test in backend/tests/unit/test_agent_logic.py

### Implementation for User Story 1

- [ ] T015 [P] [US1] Create ChatSession model in backend/src/models/chat_session.py (from data-model.md)
- [ ] T016 [P] [US1] Create UserQuery model in backend/src/models/user_query.py (from data-model.md)
- [ ] T017 [P] [US1] Create AgentResponse model in backend/src/models/agent_response.py (from data-model.md)
- [ ] T018 [US1] Implement chat session service in backend/src/services/chat_service.py
- [ ] T019 [US1] Implement search tool for Qdrant queries in backend/src/tools/search_tool.py
- [ ] T020 [US1] Implement BookAssistant agent logic in backend/src/agents/book_assistant.py
- [ ] T021 [US1] Implement /chat endpoint in backend/src/api/chat.py
- [ ] T022 [US1] Add citation functionality to responses in backend/src/agents/book_assistant.py
- [ ] T023 [US1] Add logging for chat operations in backend/src/api/chat.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Content Ingestion from Book Website (Priority: P2)

**Goal**: Enable the ingestion engine to parse the sitemap.xml from the provided URL, fetch content from each page, clean Docusaurus boilerplate, and store it for embedding.

**Independent Test**: The ingestion engine can parse the sitemap.xml from the book website, fetch content from each page, clean Docusaurus boilerplate, and store it for embedding.

### Tests for User Story 2 ⚠️

- [ ] T024 [P] [US2] Contract test for /admin/ingest endpoint in backend/tests/contract/test_ingest_contract.py
- [ ] T025 [P] [US2] Unit test for Sitemap parsing in backend/tests/unit/test_sitemap_parser.py

### Implementation for User Story 2

- [ ] T026 [P] [US2] Create BookContent model in backend/src/models/book_content.py (from data-model.md)
- [ ] T027 [P] [US2] Create VectorEmbedding model in backend/src/models/vector_embedding.py (from data-model.md)
- [ ] T028 [US2] Implement sitemap parser in backend/src/ingestors/sitemap_parser.py
- [ ] T029 [US2] Implement async scraping logic with httpx in backend/src/ingestors/content_scraper.py
- [ ] T030 [US2] Create content cleaning function for Docusaurus boilerplate in backend/src/ingestors/content_cleaner.py
- [ ] T031 [US2] Implement content chunking logic in backend/src/ingestors/content_chunker.py
- [ ] T032 [US2] Implement embedding service using Cohere in backend/src/services/embedding_service.py
- [ ] T033 [US2] Implement /admin/ingest endpoint in backend/src/api/admin.py
- [ ] T034 [US2] Add logging for ingestion operations in backend/src/api/admin.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Persistent Knowledge Storage (Priority: P3)

**Goal**: Maintain persistent vector storage that remains available between server restarts, ensuring response times remain consistent with no need for re-indexing.

**Independent Test**: After the initial content ingestion, the system maintains persistent vector storage that remains available between server restarts.

### Tests for User Story 3 ⚠️

- [ ] T035 [P] [US3] Integration test for vector storage persistence in backend/tests/integration/test_storage_persistence.py

### Implementation for User Story 3

- [ ] T036 [P] [US3] Update Qdrant vector storage with proper indexing in backend/src/vector_db.py
- [ ] T037 [US3] Implement vector upsert functionality with metadata in backend/src/services/vector_service.py
- [ ] T038 [US3] Implement similarity search functionality in backend/src/tools/search_tool.py
- [ ] T039 [US3] Add configuration for persistent storage settings in backend/src/config.py
- [ ] T040 [US3] Implement health checks for vector storage in backend/src/api/health.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T041 [P] Documentation updates in docs/README.md
- [ ] T042 Code cleanup and refactoring across modules
- [ ] T043 Performance optimization across all stories
- [ ] T044 [P] Additional unit tests (if requested) in backend/tests/unit/
- [ ] T045 Security hardening especially for admin endpoints
- [ ] T046 Run quickstart.md validation
- [ ] T047 Create Dockerfile and docker-compose.yml for containerization

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Contract test for /chat endpoint in backend/tests/contract/test_chat_contract.py"
Task: "Integration test for Qdrant 'Search' tool return values in backend/tests/integration/test_search_tool.py"
Task: "Mock agent response test in backend/tests/unit/test_agent_logic.py"

# Launch all models for User Story 1 together:
Task: "Create ChatSession model in backend/src/models/chat_session.py"
Task: "Create UserQuery model in backend/src/models/user_query.py"
Task: "Create AgentResponse model in backend/src/models/agent_response.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence