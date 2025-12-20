import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.tools.search_tool import SearchTool


@pytest.fixture
def mock_vector_db():
    """Mock vector database instance."""
    mock_db = Mock()
    mock_db.search_vectors.return_value = [
        {
            "id": "test-id-1",
            "payload": {
                "url": "https://test.com/page1",
                "title": "Test Page 1",
                "content": "This is test content for page 1"
            },
            "score": 0.9
        },
        {
            "id": "test-id-2", 
            "payload": {
                "url": "https://test.com/page2",
                "title": "Test Page 2", 
                "content": "This is test content for page 2"
            },
            "score": 0.8
        }
    ]
    return mock_db


def test_search_tool_return_values(mock_vector_db):
    """
    Integration test for Qdrant 'Search' tool return values.
    
    This test verifies that the search tool correctly interacts with 
    the vector database and returns properly formatted results.
    """
    # Create the search tool with mocked vector database
    search_tool = SearchTool(vector_db=mock_vector_db)
    
    # Perform a search
    query = "humanoid robot components"
    results = search_tool.search_knowledge_base(query)
    
    # Verify the vector DB was called with correct parameters
    mock_vector_db.search_vectors.assert_called_once()
    
    # Verify the results format
    assert isinstance(results, list)
    assert len(results) == 2  # We expect 2 results from our mock
    
    # Verify each result has the required fields
    for result in results:
        assert "url" in result
        assert "title" in result
        assert "content" in result
        assert "relevance_score" in result  # The score should be mapped to relevance_score


def test_search_tool_empty_results(mock_vector_db):
    """
    Test search tool when query returns no results.
    """
    # Mock empty results
    mock_vector_db.search_vectors.return_value = []
    
    search_tool = SearchTool(vector_db=mock_vector_db)
    results = search_tool.search_knowledge_base("nonexistent query")
    
    # Should return empty list
    assert results == []


def test_search_tool_with_cohere_integration():
    """
    Integration test to verify the search tool works with Cohere embedding.
    """
    with patch('src.tools.search_tool.vector_db') as mock_vector_db:
        # Mock the embedding generation
        with patch('src.tools.search_tool.COHERE_CLIENT') as mock_cohere:
            mock_cohere.embed.return_value = MagicMock(embeddings=[[0.1, 0.2, 0.3] + [0.0] * 1021])  # 1024-dim vector
            
            # Mock vector DB search results
            mock_vector_db.search_vectors.return_value = [
                {
                    "id": "test-id-1",
                    "payload": {
                        "url": "https://test.com/page1",
                        "title": "Test Page 1",
                        "content": "This is test content for page 1"
                    },
                    "score": 0.9
                }
            ]
            
            # Import here to avoid circular imports during test setup
            from src.tools.search_tool import SearchTool
            search_tool = SearchTool(vector_db=mock_vector_db)
            
            # Perform search
            results = search_tool.search_knowledge_base("test query")
            
            # Verify Cohere was called to generate embedding
            mock_cohere.embed.assert_called_once()
            
            # Verify vector DB was called with the generated embedding
            mock_vector_db.search_vectors.assert_called_once()
            
            # Verify results
            assert len(results) == 1
            assert results[0]["url"] == "https://test.com/page1"