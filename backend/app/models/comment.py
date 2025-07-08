# In models/comment.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from bson import ObjectId

class CommentBase(BaseModel):
    content: str
    author_id: str  
    parent_id: Optional[str] = None  

class CommentCreate(BaseModel):
    content: str
    parent_id: Optional[str] = None  

class CommentInDB(CommentBase):
    id: str
    created_at: datetime = datetime.utcnow()
    updated_at: Optional[datetime] = None
    likes: List[str] = [] 
    is_deleted: bool = False
    reply_count: int = 0  
    
    class Config:
        from_attributes = True