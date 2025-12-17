# Data Model for AI-Powered Chatbot

## Entities

### BookContent
- id: UUID (primary key)
- url: String (source URL of the content)
- title: String (page title)
- content: Text (the cleaned text content)
- created_at: DateTime
- updated_at: DateTime

### VectorEmbedding
- id: UUID (primary key)
- content_id: UUID (foreign key to BookContent)
- vector: Array<Float> (1024-dimensional embedding vector)
- metadata: JSON (includes source URL, title, content snippet)

### ChatSession
- id: UUID (primary key)
- created_at: DateTime
- updated_at: DateTime
- history: JSON (stores conversation history)

### UserQuery
- id: UUID (primary key)
- session_id: UUID (foreign key to ChatSession)
- query_text: Text (the user's question)
- timestamp: DateTime

### AgentResponse
- id: UUID (primary key)
- query_id: UUID (foreign key to UserQuery)
- response_text: Text (the agent's answer)
- sources: JSON (citations/references to book content)
- timestamp: DateTime