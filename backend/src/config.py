import os
from typing import Optional
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

# Set up OpenAI client for agents
from openai import AsyncOpenAI
from agents import set_tracing_disabled, OpenAIChatCompletionsModel

set_tracing_disabled(True)

external_client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

MODEL = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client)

class Settings(BaseModel):
    """Application settings loaded from environment variables."""

    cohere_api_key: str = os.getenv("COHERE_API_KEY")
    qdrant_url: str = os.getenv("QDRANT_URL")  # Default to empty (will be checked in vector_db.py)
    qdrant_api_key: str = os.getenv("QDRANT_API_KEY")
    openai_api_key: str = os.getenv("OPENAI_API_KEY")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    qdrant_host: str = os.getenv("QDRANT_HOST")
    sitemap_url: str = os.getenv("SITEMAP_URL")
    qdrant_port: int = int(os.getenv("QDRANT_PORT"))
    environment: str = os.getenv("ENVIRONMENT", "development")

    qdrant_local: bool = os.getenv("QDRANT_LOCAL", "false").lower() == "true"

    # Vector storage persistence settings
    qdrant_on_disk_payload: bool = os.getenv("QDRANT_ON_DISK_PAYLOAD", "true").lower() == "true"
    vector_collection_name: str = os.getenv("VECTOR_COLLECTION_NAME", "book_content_embeddings")
    vector_similarity_threshold: float = float(os.getenv("VECTOR_SIMILARITY_THRESHOLD", "0.3"))
    vector_search_limit: int = int(os.getenv("VECTOR_SEARCH_LIMIT", "10"))

    # Security settings
    admin_token: str = os.getenv("ADMIN_TOKEN", "sarfaraz")


# Create a global settings instance
settings = Settings()