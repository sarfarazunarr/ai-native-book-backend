from pydantic import BaseModel
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, List, Dict, Any


class ChatSession(BaseModel):
    """Model representing a chat session."""
    
    id: UUID
    created_at: datetime
    updated_at: datetime
    history: List[Dict[str, Any]]  # stores conversation history
    
    class Config:
        # Allow UUID serialization
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }


class ChatSessionCreate(BaseModel):
    """Model for creating new ChatSession instances."""
    
    id: Optional[UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    history: Optional[List[Dict[str, Any]]] = None
    
    def to_chat_session(self) -> ChatSession:
        """Convert to a full ChatSession instance."""
        session_id = self.id or uuid4()
        now = self.created_at or datetime.utcnow()
        
        return ChatSession(
            id=session_id,
            created_at=now,
            updated_at=now,
            history=self.history or []
        )