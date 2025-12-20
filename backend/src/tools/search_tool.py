from typing import List, Dict, Any, Optional
from cohere import Client
from qdrant_client import models
from ..config import settings
from ..vector_db import vector_db as global_vdb
import logging


logger = logging.getLogger(__name__)

# Initialize Cohere client
COHERE_CLIENT = Client(api_key=settings.cohere_api_key)


class SearchTool:
    """Tool for searching the knowledge base using vector similarity."""
    
    def __init__(self, vector_db_instance=None):
        """
        Initialize the search tool.
        
        Args:
            vector_db: Optional vector database instance (for testing)
        """
        self.vector_db = vector_db_instance or global_vdb
    
    def search_knowledge_base(self, query: str, limit: int = 10, filters: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """
        Search the knowledge base for content relevant to the query.

        Args:
            query: The search query string
            limit: Maximum number of results to return (default 10)
            filters: Optional filters to apply to the search

        Returns:
            List of documents with fields: url, title, content, relevance_score
        """
        try:
            # Generate embedding for the query using Cohere
            response = COHERE_CLIENT.embed(
                texts=[query],
                model="embed-english-v3.0",
                input_type="search_document"
            )

            # Extract the embedding vector (should be 1024-dimensional)
            query_embedding = response.embeddings[0]

            # Prepare filters if provided
            search_filter = None
            if filters:
                search_filter = models.Filter(
                    must=[
                        models.FieldCondition(
                            key=key,
                            match=models.MatchValue(value=value)
                        ) for key, value in filters.items()
                    ]
                )

            # Search for similar vectors in the database with filters and score threshold
            results = self.vector_db.search_vectors(
                query_vector=query_embedding,
                limit=limit,
                query_filter=search_filter,
                score_threshold=settings.vector_similarity_threshold
            )

            # Format the results
            formatted_results = []
            for result in results:
                payload = result.get("payload", {})
                formatted_results.append({
                    "url": payload.get("url", ""),
                    "title": payload.get("title", ""),
                    "content": payload.get("content_full", payload.get("content", "")),  # Use full content
                    "relevance_score": result.get("score", 0.0),
                    "word_count": payload.get("word_count", 0),
                    "created_at": payload.get("created_at", "")
                })

            logger.info(f"Found {len(formatted_results)} results for query: {query[:50]}...")
            return formatted_results

        except Exception as e:
            logger.error(f"Error searching knowledge base: {str(e)}")
            # Return empty list in case of error
            return []


    def search_vectors_with_filters(self, query: str, filters: Dict[str, Any], limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search vectors with specific filters.

        Args:
            query: The search query string
            filters: Filters to apply to the search
            limit: Maximum number of results to return

        Returns:
            List of documents with fields: url, title, content, relevance_score
        """
        return self.search_knowledge_base(query, limit, filters)


# Global instance for use in other modules
search_tool = SearchTool()