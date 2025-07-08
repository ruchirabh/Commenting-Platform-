from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from bson import ObjectId

class CommentBase(BaseModel):
    content: str
    author_id: str  # Reference to user
    parent_id: Optional[str] = None  # For nested comments/replies
    post_id: str  # Or whatever you're commenting on

class CommentCreate(CommentBase):
    pass

class CommentInDB(CommentBase):
    id: str
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    likes: List[str] = []  # List of user IDs who liked
    is_deleted: bool = False  # Soft delete
    
    class Config:
        from_attributes = True