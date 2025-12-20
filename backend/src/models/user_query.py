from pydantic import BaseModel
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional


class UserQuery(BaseModel):
    """Model representing a user's query."""
    
    id: UUID
    session_id: UUID  # foreign key to ChatSession
    query_text: str
    timestamp: datetime
    
    class Config:
        # Allow UUID serialization
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }


class UserQueryCreate(BaseModel):
    """Model for creating new UserQuery instances."""
    
    session_id: UUID  # foreign key to ChatSession
    query_text: str
    id: Optional[UUID] = None
    timestamp: Optional[datetime] = None
    
    def to_user_query(self) -> UserQuery:
        """Convert to a full UserQuery instance."""
        query_id = self.id or uuid4()
        when = self.timestamp or datetime.utcnow()
        
        return UserQuery(
            id=query_id,
            session_id=self.session_id,
            query_text=self.query_text,
            timestamp=when
        )