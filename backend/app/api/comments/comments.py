from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from app.services.comment import CommentService
from app.models.comment import CommentCreate, CommentInDB
from app.core.auth_utils import get_current_user
from app.logs import messages

router = APIRouter(tags=["comments"])
# ............................................................................................................................................


@router.get("/{comment_id}", response_model=CommentInDB)
async def get_comment(comment_id: str):
    return await CommentService.get_comment(comment_id)


# ............................................................................................................................................


@router.get("/post/{post_id}", response_model=List[CommentInDB])
async def get_post_comments(post_id: str, limit: int = 10, skip: int = 0):
    return await CommentService.get_comments_by_post(post_id, limit, skip)


# ............................................................................................................................................


@router.post("/", response_model=CommentInDB, status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment: CommentCreate, current_user: dict = Depends(get_current_user)
):
    if current_user.get("disabled"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=messages.account_disabled
        )
    return await CommentService.create_comment(comment, current_user["user_id"])


# ............................................................................................................................................


@router.put("/{comment_id}", response_model=CommentInDB)
async def update_comment(
    comment_id: str, content: str, current_user: dict = Depends(get_current_user)
):
    return await CommentService.update_comment(
        comment_id, content, current_user["user_id"]
    )


# ............................................................................................................................................


@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: str, current_user: dict = Depends(get_current_user)
):
    await CommentService.delete_comment(
        comment_id, current_user["user_id"], current_user.get("is_admin", False)
    )
    return {"message": messages.comment_delete_successful}


# ............................................................................................................................................


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
