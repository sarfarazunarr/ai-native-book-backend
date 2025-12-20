from pydantic import BaseModel
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, List, Dict, Any


class AgentResponse(BaseModel):
    """Model representing the agent's response to a user query."""
    
    id: UUID
    query_id: UUID  # foreign key to UserQuery
    response_text: str
    sources: List[Dict[str, str]]  # citations/references to book content
    timestamp: datetime
    
    class Config:
        # Allow UUID serialization
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }


class AgentResponseCreate(BaseModel):
    """Model for creating new AgentResponse instances."""
    
    query_id: UUID  # foreign key to UserQuery
    response_text: str
    sources: List[Dict[str, str]]  # citations/references to book content
    id: Optional[UUID] = None
    timestamp: Optional[datetime] = None
    
    def to_agent_response(self) -> AgentResponse:
        """Convert to a full AgentResponse instance."""
        response_id = self.id or uuid4()
        when = self.timestamp or datetime.utcnow()
        
        return AgentResponse(
            id=response_id,
            query_id=self.query_id,
            response_text=self.response_text,
            sources=self.sources,
            timestamp=when
        )