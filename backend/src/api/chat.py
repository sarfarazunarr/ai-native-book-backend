from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging
from pydantic import BaseModel

from ..agents.book_assistant import BookAssistant
from ..exceptions import HTTPBadRequestError, HTTPInternalServerError


# Pydantic models for request/response validation
class ChatRequest(BaseModel):
    query: str
    session_id: str = None


class ChatResponse(BaseModel):
    response: str
    sources: list
    session_id: str


router = APIRouter()
logger = logging.getLogger(__name__)

# Global instance of the BookAssistant
book_assistant = BookAssistant()


@router.post("/chat", summary="Submit a query to the chatbot", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest) -> Dict[str, Any]:
    """
    Submit a query to the chatbot and receive a response with citations.
    
    Args:
        request: Chat request containing the query and optional session_id
        
    Returns:
        Dictionary with the response, sources, and session_id
    """
    try:
        logger.info(f"Received chat request for session: {request.session_id}")
        
        # Validate the query is not empty
        if not request.query or not request.query.strip():
            raise HTTPBadRequestError(detail="Query cannot be empty")
        
        # Process the query using the BookAssistant
        result = await book_assistant.process_query(request.query, request.session_id)
        
        logger.info(f"Successfully processed chat request for session: {result['session_id']}")
        return result
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {str(e)}")
        raise HTTPInternalServerError(detail=f"Error processing chat query: {str(e)}")


# Additional endpoint for creating new chat sessions if needed
@router.post("/chat/new-session", summary="Create a new chat session", response_model=dict)
async def create_new_session() -> Dict[str, str]:
    """
    Create a new chat session and return the session ID.
    
    Returns:
        Dictionary with the new session ID
    """
    try:
        import uuid
        new_session_id = f"sess-{uuid.uuid4()}"
        logger.info(f"Created new chat session: {new_session_id}")
        return {"session_id": new_session_id}
        
    except Exception as e:
        logger.error(f"Error creating new session: {str(e)}")
        raise HTTPInternalServerError(detail=f"Error creating new session: {str(e)}")