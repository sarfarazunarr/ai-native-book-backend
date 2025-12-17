# Implementation Plan: AI-Powered Chatbot for Physical AI & Humanoid Robotics Book

**Feature**: AI-Powered Chatbot for Physical AI & Humanoid Robotics Book
**Branch**: 1-ai-book-chatbot
**Created**: 2025-12-17
**Status**: Draft

## Technical Context

The backend system will be built with FastAPI as the web framework and will include multiple components for content ingestion, vector storage, and AI-powered chat functionality. The system architecture consists of:

- **main.py**: FastAPI application and routing layer
- **ingestor.py**: Module responsible for sitemap parsing and BeautifulSoup scraping logic
- **vector_service.py**: Module containing Qdrant client and Cohere embedding wrappers
- **agent_logic.py**: Module implementing OpenAI Agents SDK (Agent definition + Tools)

The system will manage several environment variables in a `.env` file:
- COHERE_API_KEY: API key for Cohere embedding service
- QDRANT_URL: URL for the Qdrant vector database
- QDRANT_API_KEY: API key for Qdrant access
- OPENAI_API_KEY: API key for OpenAI services

The implementation will include:
- A `/admin/ingest` POST endpoint for triggering content ingestion
- Async scraping capabilities using `httpx`
- Qdrant collection creation and `upsert` logic for vector storage
- A `BookAssistant` agent with a `search_knowledge_base(query: str)` tool that performs similarity search in Qdrant
- A `/chat` POST endpoint that connects the OpenAI Agent Runner to the API

Technology Stack:
- FastAPI for the web framework
- Qdrant as the vector database
- Cohere's embed-english-v3.0 for embeddings
- OpenAI Agents SDK for the conversational agent
- BeautifulSoup for HTML parsing
- httpx for asynchronous HTTP requests

## Architecture Overview

[ARCHITECTURE_OVERVIEW]

## Constitution Check

This implementation plan aligns with the project constitution principles:

### Modularity
✓ The system separates concerns with distinct modules:
- ingestor.py handles sitemap parsing and content scraping
- vector_service.py manages vector storage and embeddings
- agent_logic.py implements the conversational agent
- main.py provides routing and application orchestration

### Performance
✓ The architecture follows an async-first approach:
- FastAPI with async endpoints
- Async scraping using httpx
- Asynchronous operations with Qdrant and OpenAI APIs

### Reliability
✓ Robust error handling for network-heavy tasks:
- Will implement retry mechanisms for API calls
- Timeout configurations for scraping operations
- Graceful degradation for external service failures

### Security
✓ Secure handling of API keys:
- All API keys (Cohere, QDRANT, OpenAI) stored in environment variables
- No hardcoded credentials in codebase
- Proper credential management through .env file

### Documentation and Type Safety
✓ All endpoints will be documented with FastAPI/Pydantic schemas
✓ Codebase will follow PEP 8 compliance with comprehensive type hints using Python 3.10+

### Observability
✓ Structured logging to track:
- Ingestion status and progress
- Agent reasoning and responses
- System performance metrics

## Phase 0: Outline & Research

### Research Tasks

- Research OpenAI Agents SDK implementation patterns and best practices
- Investigate Qdrant client usage for vector storage and similarity search operations
- Find best practices for Cohere embedding integration
- Determine optimal chunking strategies for book content
- Explore httpx async scraping patterns
- Study BeautifulSoup HTML cleaning techniques for Docusaurus sites

### Knowledge Gaps

All knowledge gaps have been resolved through research documented in research.md.

## Phase 1: Design & Contracts

### Data Model

#### BookContent
- id: UUID (primary key)
- url: String (source URL of the content)
- title: String (page title)
- content: Text (the cleaned text content)
- created_at: DateTime
- updated_at: DateTime

#### VectorEmbedding
- id: UUID (primary key)
- content_id: UUID (foreign key to BookContent)
- vector: Array<Float> (1024-dimensional embedding vector)
- metadata: JSON (includes source URL, title, content snippet)

#### ChatSession
- id: UUID (primary key)
- created_at: DateTime
- updated_at: DateTime
- history: JSON (stores conversation history)

#### UserQuery
- id: UUID (primary key)
- session_id: UUID (foreign key to ChatSession)
- query_text: Text (the user's question)
- timestamp: DateTime

#### AgentResponse
- id: UUID (primary key)
- query_id: UUID (foreign key to UserQuery)
- response_text: Text (the agent's answer)
- sources: JSON (citations/references to book content)
- timestamp: DateTime

### API Contracts

#### Ingestion API
- `POST /admin/ingest` - Trigger content ingestion from sitemap
  - Request body: { "force_reindex": boolean } (optional)
  - Response: { "status": "success", "message": string, "processed_count": integer }

#### Chat API
- `POST /chat` - Submit query and receive response
  - Request body: { "query": string, "session_id": string (optional) }
  - Response: { "response": string, "sources": array<{url: string, title: string}>, "session_id": string }

#### Health Check API
- `GET /health` - Check system health
  - Response: { "status": "healthy", "checks": object }

### Deployment Strategy

The application will be deployed as a containerized service with the following components:
- FastAPI application running in a Python 3.10+ container
- Qdrant vector database (can be hosted or self-deployed)
- Environment variables for API keys and service endpoints
- Dockerfile and docker-compose.yml for containerization
- Environment-specific configuration for local, staging, and production deployments

## Phase 2: Implementation Roadmap

### Implementation Steps

1. **Environment Setup** (Days 1-2)
   - Set up project structure with required dependencies
   - Configure environment variables and .env file handling
   - Create basic FastAPI application structure

2. **Ingestion Module Development** (Days 3-5)
   - Implement sitemap parsing functionality
   - Develop async scraping logic with httpx and BeautifulSoup
   - Create content cleaning functionality to remove Docusaurus boilerplate
   - Implement content chunking logic

3. **Vector Service Implementation** (Days 6-8)
   - Set up Qdrant client connection
   - Implement Cohere embedding integration
   - Create vector upsert functionality with metadata
   - Implement similarity search functionality

4. **Agent Logic Development** (Days 9-11)
   - Set up OpenAI Agents SDK integration
   - Create BookAssistant agent with search tool
   - Implement the search_knowledge_base tool for Qdrant queries
   - Add citation functionality to responses

5. **API Endpoint Implementation** (Days 12-13)
   - Create /admin/ingest endpoint
   - Create /chat endpoint connected to OpenAI Agent Runner
   - Implement session handling for conversations

6. **Testing and Integration** (Days 14-15)
   - Write unit tests for sitemap parsing
   - Create integration tests for Qdrant search tool
   - Implement mock agent response tests
   - Perform end-to-end testing

### Testing Strategy

- **Unit Tests**: Focus on sitemap parsing, content cleaning, and chunking algorithms
- **Integration Tests**: Validate Qdrant search tool return values and embedding accuracy
- **Mock Tests**: Test agent responses using mocked OpenAI and Cohere services
- **End-to-End Tests**: Verify complete flow from ingestion to chat responses
- **Performance Tests**: Ensure response times meet <2 second requirement
- **Security Tests**: Validate proper handling of environment variables and API keys

### Risk Analysis

- **API Limitations**: External API rate limits (Cohere, OpenAI) could limit performance
  - Mitigation: Implement request queuing and retry mechanisms with exponential backoff

- **Content Availability**: Book website may change structure or become unavailable
  - Mitigation: Implement monitoring for sitemap and content availability, with alerts for failures

- **Vector Database Costs**: Storing embeddings could become expensive with larger content
  - Mitigation: Implement efficient chunking to minimize vector count while maintaining quality

- **Query Response Quality**: Agent may provide inaccurate responses or fail to cite sources
  - Mitigation: Implement response validation and human feedback loop for quality control

## Gates

### Gate 1: Architecture Review

- ✅ Modularity: Clear separation of concerns achieved with distinct modules
- ✅ Technology stack alignment with constitution: Using FastAPI, Qdrant, Cohere, and OpenAI as specified
- ✅ Async-first design pattern implemented throughout

### Gate 2: Security Review

- ✅ API keys stored securely in environment variables
- ✅ No hardcoded credentials in the codebase
- ✅ Proper authentication method for external services verified

### Gate 3: Performance Review

- ✅ Async implementations for network-heavy operations
- ✅ Efficient vector storage and retrieval from Qdrant
- ✅ Optimized embedding techniques with Cohere's latest model

---

**Plan Version**: 1.0.0
**Last Updated**: 2025-12-17