# Quickstart Guide: AI-Powered Chatbot for Physical AI & Humanoid Robotics Book

## Prerequisites

- Python 3.10+
- Access to the following APIs:
  - Cohere API (for embeddings)
  - OpenAI API (for agent functionality)
  - Qdrant (vector database)
- Git for version control

## Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ai-book-chatbot
```

### 2. Set up Environment

Create a `.env` file in the root directory with the following variables:

```env
COHERE_API_KEY=your_cohere_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
OPENAI_API_KEY=your_openai_api_key
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
uvicorn main:app --reload
```

The application will be available at `http://localhost:8000`.

## Initial Setup: Content Ingestion

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

## Using the Chat API

Once content is ingested, you can interact with the chatbot:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the main components of a humanoid robot?",
    "session_id": "optional-session-id"
  }'
```

## API Reference

### Ingestion API
- `POST /admin/ingest` - Trigger content ingestion from sitemap

### Chat API
- `POST /chat` - Submit query and receive response with citations

### Health Check API
- `GET /health` - Check system health status

## Running Tests

```bash
pytest
```

## Docker Deployment

Alternatively, you can run the application using Docker:

```bash
docker build -t ai-book-chatbot .
docker run -p 8000:8000 --env-file .env ai-book-chatbot
```