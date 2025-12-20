from typing import List, Dict, Any
from cohere import Client
from ..config import settings
import logging


logger = logging.getLogger(__name__)

# Initialize Cohere client
COHERE_CLIENT = Client(api_key=settings.cohere_api_key)


class EmbeddingService:
    """Service class to handle text embedding operations using Cohere."""
    
    def __init__(self, model_name: str = "embed-english-v3.0"):
        """
        Initialize the embedding service.
        
        Args:
            model_name: Name of the Cohere embedding model to use
        """
        self.model_name = model_name
    
    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector as a list of floats
        """
        try:
            response = COHERE_CLIENT.embed(
                texts=[text],
                model=self.model_name,
                input_type="search_document"
            )
            
            # Extract the embedding (first item since we sent only one text)
            embedding = response.embeddings[0]
            
            logger.debug(f"Generated embedding for text of length {len(text)}")
            return embedding
            
        except Exception as e:
            logger.error(f"Error generating embedding for text: {str(e)}")
            raise
    
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        if not texts:
            return []
        
        try:
            response = COHERE_CLIENT.embed(
                texts=texts,
                model=self.model_name,
                input_type="search_document"
            )
            
            # Extract all embeddings
            embeddings = response.embeddings
            
            logger.info(f"Generated embeddings for {len(texts)} texts")
            return embeddings
            
        except Exception as e:
            logger.error(f"Error generating embeddings for {len(texts)} texts: {str(e)}")
            raise
    
    def embed_content_batch(self, content_list: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """
        Generate embeddings for a batch of content.
        
        Args:
            content_list: List of content items with 'url', 'title', and 'content' keys
            
        Returns:
            List of items with embeddings and metadata
        """
        try:
            # Extract just the content text for embedding
            texts = [item['content'] for item in content_list]
            
            # Generate embeddings for all texts at once
            embeddings = self.embed_texts(texts)
            
            # Create result with embeddings and metadata
            result = []
            for i, content_item in enumerate(content_list):
                result.append({
                    'content_id': content_item.get('id'),  # Might be None for new content
                    'url': content_item['url'],
                    'title': content_item['title'],
                    'content': content_item['content'],
                    'embedding': embeddings[i]
                })
            
            logger.info(f"Generated embeddings for {len(content_list)} content items")
            return result
            
        except Exception as e:
            logger.error(f"Error generating embeddings for content batch: {str(e)}")
            raise