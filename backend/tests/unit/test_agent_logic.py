import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.agents.book_assistant import BookAssistant


def test_agent_initialization():
    """Test that the BookAssistant initializes correctly."""
    assistant = BookAssistant()
    
    # Verify that the assistant has the expected attributes
    assert hasattr(assistant, 'search_tool')
    assert assistant.search_tool is not None


@patch('src.agents.book_assistant.search_tool')
@patch('src.agents.book_assistant.OpenAI')
def test_agent_process_query(mock_openai_class, mock_search_tool):
    """
    Mock agent response test.
    
    This test verifies that the agent logic correctly uses the search tool
    and OpenAI API to generate responses with citations.
    """
    # Mock the search tool results
    mock_search_results = [
        {
            "url": "https://test.com/page1",
            "title": "Test Page 1",
            "content": "This is test content for page 1",
            "relevance_score": 0.9
        },
        {
            "url": "https://test.com/page2",
            "title": "Test Page 2",
            "content": "This is test content for page 2",
            "relevance_score": 0.8
        }
    ]
    mock_search_tool.search_knowledge_base.return_value = mock_search_results
    
    # Mock the OpenAI client and its response
    mock_openai_instance = Mock()
    mock_chat_completion = Mock()
    mock_choice = Mock()
    mock_choice.message.content = "This is a response based on the provided context."
    mock_chat_completion.choices = [mock_choice]
    mock_openai_instance.chat.completions.create.return_value = mock_chat_completion
    mock_openai_class.return_value = mock_openai_instance
    
    # Create the assistant and process a query
    assistant = BookAssistant()
    response = assistant.process_query("What are the main components of a humanoid robot?", "test-session-123")
    
    # Verify the search tool was called
    mock_search_tool.search_knowledge_base.assert_called_once_with("What are the main components of a humanoid robot?")
    
    # Verify the OpenAI API was called with the correct parameters
    mock_openai_instance.chat.completions.create.assert_called_once()
    
    # Verify the response structure
    assert "response" in response
    assert "sources" in response
    assert "session_id" in response
    assert response["session_id"] == "test-session-123"
    assert len(response["sources"]) == 2  # Should have both search results as sources


@patch('src.agents.book_assistant.search_tool')
@patch('src.agents.book_assistant.OpenAI')
def test_agent_process_query_no_results(mock_openai_class, mock_search_tool):
    """
    Test agent response when search returns no results.
    """
    # Mock empty search results
    mock_search_tool.search_knowledge_base.return_value = []
    
    # Mock the OpenAI client and its response
    mock_openai_instance = Mock()
    mock_chat_completion = Mock()
    mock_choice = Mock()
    mock_choice.message.content = "I couldn't find relevant information about humanoid robot components in the knowledge base."
    mock_chat_completion.choices = [mock_choice]
    mock_openai_instance.chat.completions.create.return_value = mock_chat_completion
    mock_openai_class.return_value = mock_openai_instance
    
    # Create the assistant and process a query
    assistant = BookAssistant()
    response = assistant.process_query("What are the main components of a humanoid robot?", "test-session-123")
    
    # Verify the response structure, with empty sources
    assert "response" in response
    assert "sources" in response
    assert "session_id" in response
    assert response["sources"] == []  # Should be empty since no search results
    assert response["session_id"] == "test-session-123"


@patch('src.agents.book_assistant.search_tool')
@patch('src.agents.book_assistant.OpenAI')
def test_agent_response_formatting(mock_openai_class, mock_search_tool):
    """
    Test that agent responses are properly formatted with citations.
    """
    # Mock search results with various fields
    mock_search_results = [
        {
            "url": "https://robotics-book.com/actuators",
            "title": "Actuators in Humanoid Robots",
            "content": "Actuators are critical components that enable movement...",
            "relevance_score": 0.95
        }
    ]
    mock_search_tool.search_knowledge_base.return_value = mock_search_results
    
    # Mock the OpenAI client and its response
    mock_openai_instance = Mock()
    mock_chat_completion = Mock()
    mock_choice = Mock()
    mock_choice.message.content = "Actuators are critical components of humanoid robots that enable movement."
    mock_chat_completion.choices = [mock_choice]
    mock_openai_instance.chat.completions.create.return_value = mock_chat_completion
    mock_openai_class.return_value = mock_openai_instance
    
    # Create the assistant and process a query
    assistant = BookAssistant()
    response = assistant.process_query("What are actuators in humanoid robots?", "test-session-123")
    
    # Verify the response contains properly formatted sources
    assert len(response["sources"]) == 1
    source = response["sources"][0]
    assert source["url"] == "https://robotics-book.com/actuators"
    assert source["title"] == "Actuators in Humanoid Robots"