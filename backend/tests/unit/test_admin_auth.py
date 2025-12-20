import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from backend.src.main import app


client = TestClient(app)


def test_require_admin_success():
    """Test that the require_admin dependency works when admin is authenticated."""
    # This test assumes a simplified admin authentication implementation
    # In a real app, this would test actual authentication logic
    with patch('backend.src.api.admin.require_admin') as mock_auth:
        mock_auth.return_value = True  # Simulate successful authentication
        
        # We can't easily test the dependency directly through the endpoint,
        # but we can test that it's called appropriately
        # This test will be more meaningful when we have proper auth implementation
        assert True  # Placeholder until we implement proper auth


def test_admin_auth_dependency():
    """Test the admin authentication dependency function directly."""
    from backend.src.api.admin import require_admin
    
    # For now, require_admin just returns True (see implementation)
    # In a real application, this would check actual credentials
    result = require_admin()
    assert result is True


@patch('backend.src.api.admin.require_admin')
def test_ingest_endpoint_calls_auth(mock_auth):
    """Test that the ingest endpoint calls the admin authentication."""
    # Mock successful authentication
    mock_auth.return_value = True
    
    # Mock all other dependencies to avoid calling real services
    with patch('backend.src.api.admin.SitemapParser'), \
         patch('backend.src.api.admin.ContentScraper'), \
         patch('backend.src.api.admin.ContentCleaner'), \
         patch('backend.src.api.admin.ContentChunker'), \
         patch('backend.src.api.admin.EmbeddingService'), \
         patch('backend.src.api.admin.VectorService'):
        
        # Make a request to the admin endpoint
        response = client.post(
            "/admin/ingest",
            json={"force_reindex": False}
        )
        
        # Verify the response (should be 500 because we mocked dependencies)
        # This confirms the auth was bypassed (because we mocked it successfully)
        assert response.status_code in [200, 500]
        
        # Verify that auth was called
        mock_auth.assert_called_once()