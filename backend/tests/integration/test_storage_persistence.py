import pytest
from unittest.mock import Mock, patch
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.vector_db import VectorDB


@pytest.fixture
def vector_db():
    """Create a VectorDB instance for testing."""
    # In a real test, we might use a test-specific collection
    # For now, we'll mock the client to avoid needing an actual Qdrant instance
    with patch('src.vector_db.QdrantClient') as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        # Mock the collections response
        mock_collections = Mock()
        mock_collections.collections = []
        mock_client.get_collections.return_value = mock_collections
        
        vector_db = VectorDB()
        vector_db.client = mock_client  # Use the mocked client
        
        yield vector_db


def test_vector_storage_initialization(vector_db):
    """Test that vector storage is properly initialized."""
    # Mock the collection check behavior
    mock_collections = Mock()
    mock_collections.collections = []
    vector_db.client.get_collections.return_value = mock_collections
    
    # Run initialization
    vector_db.init_collection()
    
    # Verify the collection was created
    vector_db.client.create_collection.assert_called_once()


def test_vector_storage_upsert_and_search(vector_db):
    """Test that vectors can be stored and retrieved."""
    # Mock upsert operation
    test_points = [
        {
            "id": "test-id-1",
            "vector": [0.1, 0.2, 0.3] + [0.0] * 1021,  # 1024-dimensional vector
            "payload": {
                "url": "https://test.com/page1",
                "title": "Test Page 1",
                "content": "This is test content for page 1"
            }
        }
    ]
    
    vector_db.upsert_vectors(test_points)
    
    # Verify upsert was called with the correct data
    vector_db.client.upsert.assert_called_once()
    
    # Mock search operation
    mock_search_result = [
        Mock()
    ]
    mock_search_result[0].id = "test-id-1"
    mock_search_result[0].payload = {
        "url": "https://test.com/page1",
        "title": "Test Page 1",
        "content": "This is test content for page 1"
    }
    mock_search_result[0].score = 0.9
    vector_db.client.search.return_value = mock_search_result
    
    # Perform search
    results = vector_db.search_vectors([0.1, 0.2, 0.3] + [0.0] * 1021)
    
    # Verify search was called
    vector_db.client.search.assert_called_once()
    
    # Verify results format
    assert len(results) == 1
    assert results[0]["id"] == "test-id-1"


def test_vector_storage_persistence_across_restarts():
    """
    Integration test to verify vector storage persists across application restarts.
    
    In a real test environment, this would involve:
    1. Starting the application and storing vectors
    2. Shutting down the application
    3. Starting again and verifying vectors still exist
    """
    # This test would require a real Qdrant instance running
    # For this mock test, we'll verify the interface works correctly
    with patch('src.vector_db.QdrantClient') as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        # Mock the collections response to simulate existing collection
        mock_collection = Mock()
        mock_collection.name = "book_content_embeddings"
        mock_collections_obj = Mock()
        mock_collections_obj.collections = [mock_collection]
        mock_client.get_collections.return_value = mock_collections_obj
        
        vector_db = VectorDB()
        
        # The init_collection method should detect existing collection 
        # and not try to create a new one
        vector_db.init_collection()
        
        # Verify create_collection was NOT called since collection exists
        mock_client.create_collection.assert_not_called()