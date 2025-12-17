# Feature Specification: AI-Powered Chatbot for Physical AI & Humanoid Robotics Book

**Feature Branch**: `1-ai-book-chatbot`
**Created**: 2025-12-17
**Status**: Draft
**Input**: User description: "Robotics Book AI Chatbot Backend Target audience: Readers of the "Physical AI & Humanoid Robotics" book. Source URL: https://physical-ai-humanoid-robotics-omega.vercel.app/ Functional Requirements: 1. Ingestion Engine: - Load and parse `sitemap.xml` from the Vercel site. - Fetch text content from each URL (cleaning Docusaurus boilerplate like nav/footer). - Chunk content logically for embedding. 2. Embedding & Storage: - Use Cohere's `embed-english-v3.0` for 1024-dim vectors. - Upsert vectors into Qdrant with metadata (url, title, content snippet). 3. Chat API: - `/chat` endpoint accepting user queries. - Integrate OpenAI Agents SDK (openai-agents) to handle the conversation loop. - The Agent must use a "Search Tool" to query Qdrant before answering. Use context7 for documentation about anything like openai-agents or other things. Success criteria: - Successful retrieval of book-specific context for "Humanoid" or "Actuator" queries. - Persistent vector storage (doesn't re-index on every server restart). - Clean FastAPI Swagger UI documentation. Not building: - Frontend UI (this is backend only). - User authentication/login systems (V1 is public). - Multi-language support (English only). - Automated daily re-indexing (triggered manually via /ingest endpoint)."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ask Questions About Robotics Content (Priority: P1)

As a reader of the "Physical AI & Humanoid Robotics" book, I want to ask questions about specific concepts like "Humanoid" or "Actuator" so that I can get relevant answers based on the book's content.

**Why this priority**: This is the core functionality that provides value to readers - allowing them to ask questions and get accurate answers based on the book content.

**Independent Test**: Users can submit questions via the /chat endpoint and receive answers that cite specific content from the book, demonstrating the system successfully retrieves relevant information.

**Acceptance Scenarios**:

1. **Given** a user has access to the chat API, **When** they submit a query about "Humanoid locomotion", **Then** they receive a response that includes relevant information from the book with source citations.
2. **Given** a user submits a query, **When** the system processes the query and searches the embedded book content, **Then** the response contains accurate information with proper source attribution.

---

### User Story 2 - Content Ingestion from Book Website (Priority: P2)

As a system administrator, I want the system to automatically ingest content from the book website so that the chatbot has access to all relevant book material.

**Why this priority**: Without properly ingested content, the chatbot cannot provide valuable answers to user questions.

**Independent Test**: The ingestion engine can parse the sitemap.xml from the provided URL, fetch content from each page, clean Docusaurus boilerplate, and store it for embedding.

**Acceptance Scenarios**:

1. **Given** the sitemap.xml is accessible from the book website, **When** the ingestion process starts, **Then** all pages are fetched, cleaned, and prepared for embedding.
2. **Given** the ingestion process is initiated, **When** it encounters Docusaurus-generated navigation/footer elements, **Then** these elements are removed and only actual book content is retained.

---

### User Story 3 - Persistent Knowledge Storage (Priority: P3)

As a user, I want the system to retain the book's knowledge permanently so that I don't experience delays due to re-indexing on each server restart.

**Why this priority**: Ensures a smooth user experience with consistent response times regardless of server restarts.

**Independent Test**: After the initial content ingestion, the system maintains persistent vector storage that remains available between server restarts.

**Acceptance Scenarios**:

1. **Given** content has been embedded and stored, **When** the server restarts, **Then** the vector storage remains intact and accessible for queries.
2. **Given** the system has restarted, **When** a user submits a query, **Then** response times remain consistent with no need for re-indexing.

---

### Edge Cases

- What happens when the book website is temporarily unavailable during ingestion?
- How does the system handle extremely long or complex user queries?
- What occurs when a user asks a question that has no matching content in the book?
- How does the system handle malformed sitemap.xml during ingestion?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST load and parse the sitemap.xml file from the specified Vercel site (https://physical-ai-humanoid-robotics-omega.vercel.app/)
- **FR-002**: System MUST fetch text content from each URL listed in the sitemap, cleaning Docusaurus boilerplate like navigation and footer elements
- **FR-003**: System MUST chunk the content logically to prepare it for embedding while preserving context
- **FR-004**: System MUST generate 1024-dimensional vector embeddings using Cohere's embed-english-v3.0 model
- **FR-005**: System MUST upsert vectors into Qdrant with associated metadata including URL, title, and content snippet
- **FR-006**: System MUST expose a /chat API endpoint that accepts user queries about the book content
- **FR-007**: System MUST integrate OpenAI Agents SDK to handle the conversation loop with users
- **FR-008**: The Agent MUST use a Search Tool to query Qdrant for relevant content before answering user questions
- **FR-009**: System MUST provide citations or source references from the book content in its responses to user queries
- **FR-010**: System MUST maintain persistent vector storage that survives server restarts

### Key Entities

- **Book Content**: Represents the text content from the Physical AI & Humanoid Robotics book, including chunks of text with preserved context and meaning
- **Vector Embeddings**: Mathematical representations of book content chunks that enable semantic similarity matching during search operations
- **Metadata**: Associated information with each embedding such as source URL, document title, and content snippets for reference purposes
- **User Queries**: Text-based questions submitted by readers about the book content that trigger the search and response generation process
- **Chat Sessions**: Conversational exchanges between users and the AI system containing queries, responses, and contextual information

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The system successfully retrieves book-specific context when users query for "Humanoid" or "Actuator" concepts with at least 90% accuracy in providing relevant information.
- **SC-002**: Vector storage persists across server restarts, eliminating the need for re-indexing and maintaining response times under 2 seconds.
- **SC-003**: The FastAPI Swagger UI documentation is clean and comprehensible, enabling easy API exploration and testing.
- **SC-004**: 95% of user queries result in responses that include proper citations or source references from the book content.