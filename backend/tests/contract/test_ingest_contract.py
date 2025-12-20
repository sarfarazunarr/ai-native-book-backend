import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from main import app


client = TestClient(app)


def test_ingest_endpoint_contract():
    """
    Contract test for the /admin/ingest endpoint.
    
    This test verifies the endpoint accepts the correct request format
    and returns the expected response structure as defined in the API contract.
    """
    # Mock the ingestion service to avoid actual ingestion during testing
    mock_response = {
        "status": "success",
        "message": "Ingestion started",
        "processed_count": 42
    }
    
    with patch('src.api.admin.require_admin') as mock_auth:
        mock_auth.return_value = True  # Mock successful admin authentication
        
        with patch('src.api.admin.SitemapParser') as mock_sitemap_parser:
            with patch('src.api.admin.ContentScraper') as mock_content_scraper:
                # Mock the ingestion process
                with patch('src.api.admin.ContentCleaner') as mock_content_cleaner:
                    with patch('src.api.admin.ContentChunker') as mock_content_chunker:
                        with patch('src.api.admin.EmbeddingService') as mock_embedding_service:
                            with patch('src.api.admin.VectorService') as mock_vector_service:
                                # Test the endpoint with a valid request
                                response = client.post(
                                    "/admin/ingest",
                                    json={
                                        "force_reindex": False
                                    }
                                )
                                
                                # Verify the response
                                assert response.status_code == 200
                                assert "status" in response.json()
                                assert "message" in response.json()
                                assert "processed_count" in response.json()
                                assert response.json()["status"] == "success"
                                
                                # Verify admin auth was called
                                mock_auth.assert_called_once()


def test_ingest_endpoint_with_force_reindex():
    """
    Test the /admin/ingest endpoint with force_reindex enabled.
    """
    with patch('src.api.admin.require_admin') as mock_auth:
        mock_auth.return_value = True  # Mock successful admin authentication
        
        with patch('src.api.admin.SitemapParser') as mock_sitemap_parser:
            with patch('src.api.admin.ContentScraper') as mock_content_scraper:
                with patch('src.api.admin.ContentCleaner') as mock_content_cleaner:
                    with patch('src.api.admin.ContentChunker') as mock_content_chunker:
                        with patch('src.api.admin.EmbeddingService') as mock_embedding_service:
                            with patch('src.api.admin.VectorService') as mock_vector_service:
                                # Test the endpoint with force_reindex enabled
                                response = client.post(
                                    "/admin/ingest",
                                    json={
                                        "force_reindex": True
                                    }
                                )
                                
                                # Verify the response
                                assert response.status_code == 200
                                assert "status" in response.json()
                                assert "processed_count" in response.json()


def test_ingest_endpoint_unauthorized():
    """
    Test that the /admin/ingest endpoint returns 401 when not authenticated.
    """
    # Mock failed admin authentication
    with patch('src.api.admin.require_admin') as mock_auth:
        mock_auth.side_effect = Exception("Unauthorized")  # Simulate auth failure
        
        response = client.post(
            "/admin/ingest",
            json={
                "force_reindex": False
            }
        )
        
        # Should return 401 or 403 for unauthorized access
        assert response.status_code in [401, 403]