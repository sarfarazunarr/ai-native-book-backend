from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
import logging
from pydantic import BaseModel


from ..exceptions import HTTPUnauthorizedError, HTTPInternalServerError
from ..ingestors.sitemap_parser import SitemapParser
from ..ingestors.content_scraper import ContentScraper
from ..ingestors.content_cleaner import ContentCleaner
from ..ingestors.content_chunker import ContentChunker
from ..services.embedding_service import EmbeddingService
from ..services.vector_service import VectorService


# Pydantic models for request/response validation
class IngestRequest(BaseModel):
    force_reindex: bool = False


class IngestResponse(BaseModel):
    status: str
    message: str
    processed_count: int


router = APIRouter()
logger = logging.getLogger(__name__)

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Security
import os


# Use HTTP Bearer token for admin authentication
security = HTTPBearer()


def require_admin(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Verify admin authentication using a bearer token.

    The expected admin token should be set in the ADMIN_TOKEN environment variable.
    """
    admin_token = os.getenv("ADMIN_TOKEN")

    if not admin_token:
        raise HTTPUnauthorizedError(detail="Admin token not configured on the server")

    if not credentials or credentials.credentials != admin_token:
        raise HTTPUnauthorizedError(detail="Invalid or missing admin token")

    # If we reach this point, authentication was successful
    return True


@router.post("/ingest", summary="Trigger content ingestion from sitemap", response_model=IngestResponse)
async def ingest_content(request: IngestRequest, admin: bool = Depends(require_admin)) -> Dict[str, Any]:
    """
    Trigger content ingestion from sitemap.

    Args:
        request: Ingestion request containing force_reindex flag
        admin: Admin authentication dependency

    Returns:
        Dictionary with ingestion status and count
    """
    try:
        logger.info(f"Starting content ingestion with force_reindex: {request.force_reindex}")

        # Initialize all required services
        sitemap_parser = SitemapParser()
        content_scraper = ContentScraper()
        content_cleaner = ContentCleaner()
        content_chunker = ContentChunker()
        embedding_service = EmbeddingService()
        vector_service = VectorService()

        # Step 1: Parse sitemap
        sitemap_url = "https://physical-ai-humanoid-robotics-omega.vercel.app/sitemap.xml"  
        urls = sitemap_parser.parse_sitemap_from_url(sitemap_url)

        # Step 2: Scrape content from URLs
        scraped_content = await content_scraper.scrape_urls(urls)

        # Step 3: Clean the scraped content
        cleaned_content = content_cleaner.clean_content_batch(scraped_content)

        # Step 4: Chunk the content for better embedding
        chunked_content = content_chunker.chunk_content_batch(cleaned_content)

        # Step 5: Generate embeddings for the content
        content_with_embeddings = embedding_service.embed_content_batch(chunked_content)

        # Step 6: Store embeddings in vector database
        vector_service.upsert_content_with_embeddings(content_with_embeddings)

        processed_count = len(chunked_content)

        result = {
            "status": "success",
            "message": f"Ingestion completed. Processed and stored {processed_count} content chunks.",
            "processed_count": processed_count
        }

        logger.info(f"Ingestion completed. Processed and stored {processed_count} content chunks.")
        return result

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Unexpected error in ingest endpoint: {str(e)}")
        raise HTTPInternalServerError(detail=f"Error during content ingestion: {str(e)}")