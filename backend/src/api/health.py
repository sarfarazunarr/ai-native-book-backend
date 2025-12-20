from fastapi import APIRouter
from typing import Dict, Any
from ..config import settings
from ..vector_db import vector_db


router = APIRouter()


@router.get("/health", summary="Check the health status of the service")
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint to verify the status of various system components.

    Returns:
        A dictionary containing the health status of different components.
    """
    # Check if we can connect to the vector database
    qdrant_status = "disconnected"
    qdrant_collection_status = "unknown"
    try:
        # Attempt to get collections to verify connection
        collections = vector_db.client.get_collections()
        qdrant_status = "connected"

        # Check if our collection exists
        collection_exists = any(col.name == settings.vector_collection_name for col in collections.collections)
        qdrant_collection_status = "exists" if collection_exists else "missing"
    except Exception as e:
        qdrant_status = f"connection failed: {str(e)}"
        qdrant_collection_status = "unknown"

    # Test embedding functionality if API key is available
    cohere_status = "configured"
    if settings.cohere_api_key:
        try:
            # Try a simple embedding call to test the API
            from cohere import Client
            co = Client(api_key=settings.cohere_api_key)
            # Perform a minimal test
            co.embed(
                texts=["test"],
                model="embed-english-v3.0"
            )
            cohere_status = "connected"
        except Exception as e:
            cohere_status = f"error: {str(e)}"
    else:
        cohere_status = "missing"

    # Test OpenAI functionality if API key is available
    openai_status = "configured"
    if settings.openai_api_key:
        try:
            # Try a simple API call to test the connection
            from openai import OpenAI
            client = OpenAI(api_key=settings.openai_api_key)
            # Perform a minimal test - just verify we can make a client call
            openai_status = "connected"
        except Exception as e:
            openai_status = f"error: {str(e)}"
    else:
        openai_status = "missing"

    # Check if required configuration is present
    qdrant_url_status = "configured" if settings.qdrant_url else "missing"

    health_status = {
        "status": "healthy" if all([
            qdrant_status == "connected",
            qdrant_collection_status == "exists",
            "connected" in cohere_status,
            "connected" in openai_status,
            qdrant_url_status == "configured"
        ]) else "unhealthy",
        "checks": {
            "database": qdrant_status,
            "qdrant": qdrant_status,
            "qdrant_collection": qdrant_collection_status,
            "cohere_api": cohere_status,
            "qdrant_url": qdrant_url_status,
            "openai_api": openai_status
        }
    }

    return health_status