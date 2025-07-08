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

"""GET ALL TOP-LEVEL COMMENTS"""


@router.get("/", response_model=List[CommentInDB])
async def get_top_level_comments(limit: int = 10, skip: int = 0):
    return await CommentService.get_comments(None, limit, skip)


# ............................................................................................................................................

"""CREATE COMMENT"""


@router.post("/", response_model=CommentInDB, status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment: CommentCreate, current_user: dict = Depends(get_current_user)
):
    if current_user.get("disabled"):
        raise HTTPException(status_code=403, detail=messages.account_disabled)
    return await CommentService.create_comment(comment, current_user["user_id"])


# ............................................................................................................................................

"""UPDATE COMMENT"""


@router.put("/{comment_id}", response_model=CommentInDB)
async def update_comment(
    comment_id: str, data: CommentUpdate, current_user: dict = Depends(get_current_user)
):
    return await CommentService.update_comment(
        comment_id, data.content, current_user["user_id"]
    )


# ............................................................................................................................................

"""DELETE COMMENT"""


@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: str, current_user: dict = Depends(get_current_user)
):
    await CommentService.delete_comment(
        comment_id, current_user["user_id"], current_user.get("is_admin", False)
    )
    return {"message": messages.comment_delete_successful}


# ............................................................................................................................................

"""LIKE/UNLIKE COMMENT"""


@router.post("/{comment_id}/like", response_model=CommentInDB)
async def toggle_like(comment_id: str, current_user: dict = Depends(get_current_user)):
    if current_user.get("disabled"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=messages.account_disabled
        )
    return await CommentService.toggle_like(comment_id, current_user["user_id"])


# ............................................................................................................................................

""" ADMIN HARD DELETE"""


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

"""GET COMMENT REPLIES"""


@router.get("/{comment_id}/replies", response_model=List[CommentInDB])
async def get_comment_replies(comment_id: str, limit: int = 10, skip: int = 0):
    return await CommentService.get_comments(comment_id, limit, skip)


# ............................................................................................................................................
