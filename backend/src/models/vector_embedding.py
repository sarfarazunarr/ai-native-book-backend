from pydantic import BaseModel
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, List, Dict, Any


class VectorEmbedding(BaseModel):
    """Model representing a vector embedding of book content."""
    
    id: UUID
    content_id: UUID
    vector: List[float]  # 1024-dimensional embedding vector
    metadata: Dict[str, Any]  # includes source URL, title, content snippet
    created_at: datetime
    
    class Config:
        # Allow UUID serialization
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }


class VectorEmbeddingCreate(BaseModel):
    """Model for creating new VectorEmbedding instances."""
    
    content_id: UUID
    vector: List[float]  # 1024-dimensional embedding vector
    metadata: Dict[str, Any]  # includes source URL, title, content snippet
    id: Optional[UUID] = None
    created_at: Optional[datetime] = None
    
    def to_vector_embedding(self) -> VectorEmbedding:
        """Convert to a full VectorEmbedding instance."""
        embedding_id = self.id or uuid4()
        now = self.created_at or datetime.utcnow()
        
        return VectorEmbedding(
            id=embedding_id,
            content_id=self.content_id,
            vector=self.vector,
            metadata=self.metadata,
            created_at=now
        )