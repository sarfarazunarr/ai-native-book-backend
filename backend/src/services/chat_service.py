from typing import Dict, Optional
from datetime import datetime
import logging
from uuid import UUID

from ..models.chat_session import ChatSession, ChatSessionCreate
from ..models.user_query import UserQuery, UserQueryCreate
from ..models.agent_response import AgentResponse, AgentResponseCreate


logger = logging.getLogger(__name__)


class ChatService:
    """Service class to handle chat session operations and history."""
    
    def __init__(self):
        """Initialize the chat service."""
        # In a real implementation, this would connect to a database
        # For now, we'll use in-memory storage for demonstration
        self.sessions: Dict[UUID, ChatSession] = {}
        self.queries: Dict[UUID, UserQuery] = {}
        self.responses: Dict[UUID, AgentResponse] = {}
    
    def get_or_create_session(self, session_id: Optional[str] = None) -> ChatSession:
        """
        Get an existing session or create a new one.
        
        Args:
            session_id: Optional session ID
            
        Returns:
            ChatSession instance
        """
        if session_id:
            # Try to get existing session
            try:
                session_uuid = UUID(session_id)
                if session_uuid in self.sessions:
                    return self.sessions[session_uuid]
                else:
                    # Session ID provided but not found, create new with that ID
                    session_create = ChatSessionCreate(
                        id=session_uuid,
                        history=[]
                    )
                    new_session = session_create.to_chat_session()
                    self.sessions[new_session.id] = new_session
                    return new_session
            except ValueError:
                # Invalid UUID format, create new session
                logger.warning(f"Invalid session ID format: {session_id}, creating new session")
        
        # Create new session
        session_create = ChatSessionCreate(history=[])
        new_session = session_create.to_chat_session()
        self.sessions[new_session.id] = new_session
        logger.info(f"Created new chat session: {new_session.id}")
        return new_session
    
    def add_query_to_session(self, session_id: UUID, query_text: str) -> UserQuery:
        """
        Add a user query to a session.
        
        Args:
            session_id: ID of the session
            query_text: The user's query text
            
        Returns:
            UserQuery instance
        """
        query_create = UserQueryCreate(
            session_id=session_id,
            query_text=query_text
        )
        user_query = query_create.to_user_query()
        
        # Store the query
        self.queries[user_query.id] = user_query
        
        # Update session history
        if session_id in self.sessions:
            session = self.sessions[session_id]
            session.history.append({
                "type": "user_query",
                "id": str(user_query.id),
                "text": query_text,
                "timestamp": user_query.timestamp.isoformat()
            })
            session.updated_at = datetime.utcnow()
        
        logger.info(f"Added query {user_query.id} to session {session_id}")
        return user_query
    
    def add_response_to_session(self, query_id: UUID, response_text: str, sources: list) -> AgentResponse:
        """
        Add an agent response to a session.
        
        Args:
            query_id: ID of the corresponding query
            response_text: The agent's response text
            sources: List of sources cited in the response
            
        Returns:
            AgentResponse instance
        """
        if query_id not in self.queries:
            raise ValueError(f"Query with ID {query_id} not found")
        
        query = self.queries[query_id]
        
        response_create = AgentResponseCreate(
            query_id=query_id,
            response_text=response_text,
            sources=sources
        )
        agent_response = response_create.to_agent_response()
        
        # Store the response
        self.responses[agent_response.id] = agent_response
        
        # Update session history
        session_id = query.session_id
        if session_id in self.sessions:
            session = self.sessions[session_id]
            session.history.append({
                "type": "agent_response",
                "id": str(agent_response.id),
                "text": response_text,
                "sources": sources,
                "timestamp": agent_response.timestamp.isoformat()
            })
            session.updated_at = datetime.utcnow()
        
        logger.info(f"Added response {agent_response.id} to session {session_id}")
        return agent_response
    
    def get_session_history(self, session_id: UUID) -> list:
        """
        Get the history of a chat session.
        
        Args:
            session_id: ID of the session
            
        Returns:
            List of session history items
        """
        if session_id in self.sessions:
            return self.sessions[session_id].history
        else:
            return []


# Global instance of the chat service
chat_service = ChatService()