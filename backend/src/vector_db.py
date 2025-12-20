from typing import List, Optional, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams, PayloadSchemaType
from uuid import UUID
import logging
from .config import settings
import time


logger = logging.getLogger(__name__)


class VectorDB:
    """Class to handle vector database operations using Qdrant."""

    def __init__(self):
        """Initialize the Qdrant client and set up the connection."""
        print(f"--- DEBUG QDRANT CONFIG ---")
        print(f"URL: '{settings.qdrant_url}'")
        print(f"HOST: '{settings.qdrant_host}'")
        print(f"PORT: '{settings.qdrant_port}'")
        print(f"---------------------------")
        
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            prefer_grpc=False, # Force REST to match your script
            timeout=100
        )

        self.collection_name = settings.vector_collection_name
        self.vector_size = 1024  # Cohere embed-english-v3.0 returns 1024-dimensional vectors
        self.distance = Distance.COSINE
    
    def init_collection(self):
        """Initialize the collection if it doesn't exist."""
        max_retries = 3
        retry_count = 0

        while retry_count < max_retries:
            try:
                logger.info("Initializing collection...")
                # Check if the collection exists
                collections = self.client.get_collections()
                print(collections)
                collection_exists = any(col.name == self.collection_name for col in collections.collections)

                if not collection_exists:
                    # Create the collection with configuration for persistent storage
                    self.client.create_collection(
                        collection_name=self.collection_name,
                        vectors_config=VectorParams(
                            size=self.vector_size,
                            distance=self.distance
                        ),
                        # Configure for persistent storage
                        on_disk_payload=True  # Store payload on disk for persistence
                    )
                    logger.info(f"Created collection '{self.collection_name}' in Qdrant with persistent storage")

                    # Create index for efficient searching
                    self.client.create_payload_index(
                        collection_name=self.collection_name,
                        field_name="url",
                        field_schema=models.PayloadSchemaType.KEYWORD
                    )
                    logger.info(f"Created index on 'url' field in collection '{self.collection_name}'")

                    self.client.create_payload_index(
                        collection_name=self.collection_name,
                        field_name="title",
                        field_schema=models.PayloadSchemaType.TEXT
                    )
                    logger.info(f"Created index on 'title' field in collection '{self.collection_name}'")
                else:
                    logger.info(f"Collection '{self.collection_name}' already exists in Qdrant")

                break  # If successful, exit the retry loop

            except Exception as e:
                retry_count += 1
                logger.warning(f"Attempt {retry_count} to initialize collection failed: {str(e)}")
                if retry_count < max_retries:
                    time.sleep(2)  # Wait before retrying
                else:
                    logger.error(f"Failed to initialize collection after {max_retries} attempts: {str(e)}")
                    raise
    
    def upsert_vectors(self, points: List[Dict[str, Any]]):
        """
        Upsert vectors into the collection.

        Args:
            points: List of points to upsert, each with id, vector, and payload
        """
        max_retries = 3
        retry_count = 0

        while retry_count < max_retries:
            try:
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=points
                )
                logger.info(f"Upserted {len(points)} vectors into Qdrant collection '{self.collection_name}'")
                break  # If successful, exit the retry loop
            except Exception as e:
                retry_count += 1
                logger.warning(f"Attempt {retry_count} to upsert vectors failed: {str(e)}")
                if retry_count < max_retries:
                    time.sleep(2)  # Wait before retrying
                else:
                    logger.error(f"Failed to upsert vectors after {max_retries} attempts: {str(e)}")
                    raise
    
    def search_vectors(self, query_vector: List[float], limit: int = 10, 
                       query_filter: Optional[models.Filter] = None, 
                       score_threshold: Optional[float] = None) -> List[Dict[str, Any]]:
        """
        Updated search using the modern 'query_points' API.
        """
        try:
            # query_points is the newer replacement for .search()
            results = self.client.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                query_filter=query_filter,
                limit=limit,
                score_threshold=score_threshold,
                with_payload=True  # Ensures we get the book data back
            )

            formatted_results = []
            # results for query_points are accessed via .points
            for point in results.points:
                formatted_results.append({
                    "id": point.id,
                    "payload": point.payload,
                    "score": point.score
                })

            logger.info(f"Found {len(formatted_results)} results using query_points")
            return formatted_results

        except AttributeError:
            # Fallback for older versions if query_points isn't there either
            logger.warning("query_points not found, attempting fallback to search...")
            return self._fallback_search(query_vector, limit, query_filter, score_threshold)
        except Exception as e:
            logger.error(f"Search failed: {str(e)}")
            return []

    def _fallback_search(self, query_vector, limit, query_filter, score_threshold):
        """Old-style search fallback."""
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            query_filter=query_filter,
            limit=limit,
            score_threshold=score_threshold
        )
        return [{"id": r.id, "payload": r.payload, "score": r.score} for r in results]
    
    def close_connection(self):
        """Close the connection to Qdrant."""
        try:
            if hasattr(self.client, 'close'):
                self.client.close()
                logger.info("Closed connection to Qdrant")
        except Exception as e:
            logger.error(f"Error closing Qdrant connection: {str(e)}")


# Global instance
vector_db = VectorDB()