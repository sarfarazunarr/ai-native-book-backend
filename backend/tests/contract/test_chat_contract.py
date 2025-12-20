import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from main import app


client = TestClient(app)


def test_chat_endpoint_contract():
    """
    Contract test for the /chat endpoint.
    
    This test verifies the endpoint accepts the correct request format
    and returns the expected response structure as defined in the API contract.
    """
    # Mock the agent response to avoid actual API calls during testing
    mock_response = {
        "response": "This is a sample response from the agent",
        "sources": [
            {
                "url": "https://physical-ai-humanoid-robotics-omega.vercel.app/actuators",
                "title": "Actuators in Humanoid Robotics"
            }
        ],
        "session_id": "test-session-123"
    }
    
    with patch('src.api.chat.BookAssistant') as mock_assistant_class:
        # Mock the assistant instance
        mock_assistant_instance = Mock()
        mock_assistant_instance.process_query.return_value = mock_response
        mock_assistant_class.return_value = mock_assistant_instance
        
        # Test the endpoint with a valid request
        response = client.post(
            "/chat",
            json={
                "query": "What are the main components of a humanoid robot?",
                "session_id": "test-session-123"
            }
        )
        
        # Verify the response
        assert response.status_code == 200
        assert "response" in response.json()
        assert "sources" in response.json()
        assert "session_id" in response.json()
        assert isinstance(response.json()["sources"], list)
        
        # Verify the request was processed
        mock_assistant_instance.process_query.assert_called_once()


def test_chat_endpoint_missing_query():
    """
    Test that the /chat endpoint returns 400 when query is missing.
    """
    response = client.post(
        "/chat",
        json={
            # Missing query field
            "session_id": "test-session-123"
        }
    )
    
    # Should return 400 Bad Request
    assert response.status_code == 422  # FastAPI validation error


def test_chat_endpoint_without_session_id():
    """
    Test the /chat endpoint when no session_id is provided.
    """
    mock_response = {
        "response": "This is a sample response from the agent",
        "sources": [],
        "session_id": "new-session-456"
    }
    
    with patch('src.api.chat.BookAssistant') as mock_assistant_class:
        # Mock the assistant instance
        mock_assistant_instance = Mock()
        mock_assistant_instance.process_query.return_value = mock_response
        mock_assistant_class.return_value = mock_assistant_instance
        
        # Test the endpoint without session_id
        response = client.post(
            "/chat",
            json={
                "query": "What are the main components of a humanoid robot?"
            }
        )
        
        # Verify the response
        assert response.status_code == 200
        assert "response" in response.json()
        assert "session_id" in response.json()