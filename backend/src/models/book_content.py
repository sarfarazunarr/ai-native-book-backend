from pydantic import BaseModel
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional


class BookContent(BaseModel):
    """Model representing content from the book."""
    
    id: UUID
    url: str
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        # Allow UUID serialization
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }


class BookContentCreate(BaseModel):
    """Model for creating new BookContent instances."""
    
    url: str
    title: str
    content: str
    id: Optional[UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def to_book_content(self) -> BookContent:
        """Convert to a full BookContent instance."""
        content_id = self.id or uuid4()
        now = self.created_at or datetime.utcnow()
        
        return BookContent(
            id=content_id,
            url=self.url,
            title=self.title,
            content=self.content,
            created_at=now,
            updated_at=now
        )