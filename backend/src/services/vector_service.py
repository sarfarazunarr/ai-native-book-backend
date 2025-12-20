from typing import List, Dict, Any
from uuid import uuid4
from ..vector_db import vector_db
from ..config import settings
import logging


logger = logging.getLogger(__name__)


class VectorService:
    """Service class to handle vector storage and retrieval operations."""
    
    def __init__(self):
        """Initialize the vector service."""
        self.collection_name = "book_content_embeddings"
    
    def upsert_embeddings(self, embeddings_data: List[Dict[str, Any]]):
        """
        Upsert embedding vectors into the vector database.
        
        Args:
            embeddings_data: List of items with 'embedding', 'url', 'title', 'content' keys
        """
        try:
            # Prepare points for upsert operation
            points = []
            for item in embeddings_data:
                # Create a unique ID for this vector entry if not provided
                vector_id = str(uuid4())
                
                # Create the point with metadata
                point = {
                    "id": vector_id,
                    "vector": item["embedding"],
                    "payload": {
                        "url": item["url"],
                        "title": item["title"],
                        "content": item["content"][:500] + "..." if len(item["content"]) > 500 else item["content"],  # Truncate content for payload
                        "content_full": item["content"]  # Store full content as well
                    }
                }
                
                points.append(point)
            
            # Upsert the vectors into the database
            vector_db.upsert_vectors(points)
            
            logger.info(f"Upserted {len(points)} embedding vectors to collection '{self.collection_name}'")
            
        except Exception as e:
            logger.error(f"Error upserting embeddings: {str(e)}")
            raise
    
    def upsert_content_with_embeddings(self, content_with_embeddings: List[Dict[str, Any]]):
        """
        Upsert content along with its embeddings to the vector database.

        Args:
            content_with_embeddings: List of content items with embeddings
        """
        try:
            # Prepare points for upsert operation
            points = []
            for item in content_with_embeddings:
                # Create a unique ID for this vector entry if not provided
                vector_id = str(uuid4())

                # Create the point with comprehensive metadata for better persistence and search
                point = {
                    "id": vector_id,
                    "vector": item["embedding"],
                    "payload": {
                        "url": item["url"],
                        "title": item["title"],
                        "content": item["content"][:500] + "..." if len(item["content"]) > 500 else item["content"],  # Truncate content for payload
                        "content_full": item["content"],  # Store full content as well
                        "created_at": str(item.get("created_at", "")),  # For tracking when content was added
                        "source_type": "web_page",  # For filtering content by source
                        "hash": item.get("hash", ""),  # For potential duplicate detection
                        "word_count": len(item["content"].split())  # For content statistics
                    }
                }

                points.append(point)

            # Upsert the vectors into the database
            vector_db.upsert_vectors(points)

            logger.info(f"Upserted {len(points)} content items with embeddings to collection '{self.collection_name}' with comprehensive metadata")

        except Exception as e:
            logger.error(f"Error upserting content with embeddings: {str(e)}")
            raise
    
    def search_similar_content(self, query_embedding: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for content similar to the query embedding.
        
        Args:
            query_embedding: The embedding vector to search for
            limit: Maximum number of results to return
            
        Returns:
            List of similar content items with URL, title, content, and relevance score
        """
        try:
            # Search in the vector database
            results = vector_db.search_vectors(query_vector=query_embedding, limit=limit)
            
            # Format the results
            formatted_results = []
            for result in results:
                payload = result.get("payload", {})
                formatted_results.append({
                    "id": result.get("id"),
                    "url": payload.get("url", ""),
                    "title": payload.get("title", ""),
                    "content": payload.get("content_full", payload.get("content", "")),
                    "relevance_score": result.get("score", 0.0)
                })
            
            logger.info(f"Found {len(formatted_results)} similar content items")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error searching for similar content: {str(e)}")
            raise