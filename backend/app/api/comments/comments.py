from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from app.services.comment import CommentService
from app.models.comment import CommentCreate, CommentInDB
from app.core.auth_utils import get_current_user
from app.logs import messages
from app.db.mongo import db

router = APIRouter(tags=["comments"])

from pydantic import BaseModel


class CommentUpdate(BaseModel):
    content: str


# ............................................................................................................................................

"""
API  FOR FETCHING ALL COMMENTS

"""


@router.get("/", response_model=List[CommentInDB])
async def get_top_level_comments(limit: int = 10, skip: int = 0):
    return await CommentService.get_comments(None, limit, skip)


# ............................................................................................................................................

"""
API FOR WRITTING A COMMENT
--------------------------
ENDPOINT = /COMMENTS/

Headers:
    Authorization: Bearer <access_token>

Example Requests:
    {  
        "content": "This is my comment"
    }

"""


@router.post("/", response_model=CommentInDB, status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment: CommentCreate, current_user: dict = Depends(get_current_user)
):
    if current_user.get("disabled"):
        raise HTTPException(status_code=403, detail=messages.account_disabled)
    return await CommentService.create_comment(comment, current_user["user_id"])


# ............................................................................................................................................

"""
API FOR UPDATING A COMMENT

EXAMPLE USAGE=
        http://127.0.0.1:8000/comments/686d0209764b5c8f453da5d6

        {
            "content": "This is my new comment 12345"

        }

RESULT =    {
                "content": "This is my new comment 12345",
                "author_id": "686cd00466aa0a42e1f011b9",
                "parent_id": null,
                "id": "686d0209764b5c8f453da5d6",
                "created_at": "2025-07-08T11:33:29.497000",
                "updated_at": "2025-07-08T11:49:28.124000",
                "likes": [],
                "is_deleted": false,
                "reply_count": 0
            }        
"""


@router.put("/{comment_id}", response_model=CommentInDB)
async def update_comment(
    comment_id: str, data: CommentUpdate, current_user: dict = Depends(get_current_user)
):
    return await CommentService.update_comment(
        comment_id, data.content, current_user["user_id"]
    )


# ............................................................................................................................................

"""
API FOR DELETING THE COMMENT 

EXAMPLE = 
            http://127.0.0.1:8000/comments/686d0e10556006fcfa026174

RESULT = 
            {
                "message": "Comment deleted successfully "
            }
"""


@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: str, current_user: dict = Depends(get_current_user)
):
    await CommentService.delete_comment(
        comment_id, current_user["user_id"], current_user.get("is_admin", False)
    )
    return {"message": messages.comment_delete_successful}


# ............................................................................................................................................

"""
API FOR LIKING A COMMENT

EXAMPLE = 
            http://127.0.0.1:8000/comments/686d0f093a30f3ea0ef293f6/like

RESULT  = {
            "content": "the comment qqqq  ",
            "author_id": "686cd00466aa0a42e1f011b9",
            "parent_id": null,
            "id": "686d0f093a30f3ea0ef293f6",
            "created_at": "2025-07-08T12:28:57.140000",
            "updated_at": null,
            "likes": [
                "686cd00466aa0a42e1f011b9"
            ],
            "is_deleted": false,
            "reply_count": 0
        }           
"""


@router.post("/{comment_id}/like", response_model=CommentInDB)
async def toggle_like(comment_id: str, current_user: dict = Depends(get_current_user)):
    if current_user.get("disabled"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=messages.account_disabled
        )
    return await CommentService.toggle_like(comment_id, current_user["user_id"])


# ............................................................................................................................................

""" Admin-only endpoint example """


@router.delete("/admin/{comment_id}")
async def admin_delete_comment(
    comment_id: str, current_user: dict = Depends(get_current_user)
):
    if not current_user.get("is_admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=messages.admin_privilege
        )
    await CommentService.hard_delete_comment(comment_id)
    return {"message": messages.admin_comment_delete}


# ............................................................................................................................................
"""
API TO GET ALL REPLIES FOR A COMMENT

"""

@router.get("/{comment_id}/replies", response_model=List[CommentInDB])
async def get_comment_replies(comment_id: str, limit: int = 10, skip: int = 0):
    return await CommentService.get_comments(comment_id, limit, skip)
