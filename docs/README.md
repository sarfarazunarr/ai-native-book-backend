# AI-Powered Chatbot for Physical AI & Humanoid Robotics Book

## Overview

This project implements an AI-powered chatbot that allows users to ask questions about content from the Physical AI & Humanoid Robotics book. The system uses vector search to find relevant content and provides citations to original sources.

## Architecture

The system consists of:

- **Web API**: FastAPI-based REST API serving chat and ingestion endpoints
- **Vector Database**: Qdrant for similarity search of embedded content
- **Embedding Service**: Cohere for generating text embeddings
- **AI Agent**: OpenAI for generating responses based on retrieved content
- **Content Ingestion**: Automated scraping and processing of book website content

## Setup

### Prerequisites

- Python 3.10+
- Access to the following APIs:
  - Cohere API (for embeddings)
  - OpenAI API (for agent functionality)
  - Qdrant (vector database)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ai-book-chatbot
   ```

2. Set up environment:
   ```bash
   # Create a .env file with the following variables:
   COHERE_API_KEY=your_cohere_api_key
   QDRANT_URL=your_qdrant_url
   QDRANT_API_KEY=your_qdrant_api_key
   OPENAI_API_KEY=your_openai_api_key
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   uvicorn backend.src.main:app --reload
   ```

## Usage

### Content Ingestion

Before using the chat functionality, you need to ingest the book content:

1. Send a POST request to `/admin/ingest`:
   ```bash
   curl -X POST http://localhost:8000/admin/ingest
   ```

2. The system will:
   - Parse the sitemap.xml from the book website
   - Scrape and clean content from each page
   - Generate embeddings using Cohere
   - Store vectors in Qdrant with metadata

### Chat API

Once content is ingested, you can interact with the chatbot:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type" "application/json" \
  -d '{
    "query": "What are the main components of a humanoid robot?",
    "session_id": "optional-session-id"
  }'
```

### Health Check API

Check the status of various system components:

```bash
curl http://localhost:8000/health
```

## API Reference

### Ingestion API
- `POST /admin/ingest` - Trigger content ingestion from sitemap

### Chat API
- `POST /chat` - Submit query and receive response with citations

### Health Check API
- `GET /health` - Check system health status

## Configuration

The application can be configured using environment variables in the `.env` file:

- `COHERE_API_KEY`: API key for Cohere embedding service
- `QDRANT_URL`: URL for the Qdrant vector database
- `QDRANT_API_KEY`: API key for Qdrant access
- `OPENAI_API_KEY`: API key for OpenAI services
- `LOG_LEVEL`: Logging level (default: INFO)
- `QDRANT_HOST`: Qdrant host (default: localhost)
- `QDRANT_PORT`: Qdrant port (default: 6333)
- `ENVIRONMENT`: Environment setting (default: development)
- `QDRANT_ON_DISK_PAYLOAD`: Whether to store payloads on disk (default: true)
- `VECTOR_COLLECTION_NAME`: Name of the vector collection (default: book_content_embeddings)
- `VECTOR_SIMILARITY_THRESHOLD`: Minimum similarity score (default: 0.3)
- `VECTOR_SEARCH_LIMIT`: Maximum number of search results (default: 10)

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run specific test directory
pytest backend/tests/unit/
pytest backend/tests/integration/
pytest backend/tests/contract/
```

### Code Formatting

The project uses Black for code formatting and Flake8 for linting. Configure your editor to use these tools.

## Deployment

### Docker

The application can be deployed using Docker:

```bash
# Build the image
docker build -t ai-book-chatbot .

# Run the container
docker run -p 8000:8000 --env-file .env ai-book-chatbot
```

### Environment-specific Deployment

For production deployments, ensure:
- Secure API key management
- Proper Qdrant configuration for production
- SSL termination at the load balancer
- Proper logging and monitoring setup

## Security

- API keys are stored in environment variables and never hard-coded
- Admin endpoints require authentication (implementation pending in production)
- Input validation on all endpoints
- Rate limiting should be implemented at the infrastructure level

## Troubleshooting

### Common Issues

1. **Vector search returns no results**: 
   - Verify content ingestion completed successfully
   - Check that Qdrant is running and accessible
   - Confirm the vector collection exists

2. **API keys not working**:
   - Verify all required API keys are set in the .env file
   - Check that API keys have the necessary permissions

3. **Performance issues**:
   - Check system resources (CPU, memory)
   - Verify Qdrant performance settings
   - Review Cohere and OpenAI rate limits