from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from bson import ObjectId


class UserBase(BaseModel):
    username: str
    email: EmailStr
    disabled: bool = False


class UserCreate(UserBase):
    password: str


class UserInDB(UserBase):
    id: str
    hashed_password: str
    profile_pic: Optional[bytes] = None
    is_admin: bool = False
    comment_count: int = 0
    created_at: datetime = datetime.utcnow()

    class Config:
        from_attributes = True
