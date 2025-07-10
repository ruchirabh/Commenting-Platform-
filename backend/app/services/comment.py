from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from app.db.mongo import db
from app.models.comment import CommentInDB, CommentCreate
from app.models.user import UserInDB
from fastapi import HTTPException, status
from app.logs import messages


class CommentService:
    # ............................................................................................................................................

    @staticmethod
    async def create_comment(comment: CommentCreate, user_id: str) -> CommentInDB:
        user = await db.users.find_one({"_id": ObjectId(user_id)}, {"username": 1})
        username = user["username"] if user else "Anonymous"
        comment_dict = {
            "content": comment.content,
            "author_id": user_id,
            "username": username,
            "parent_id": ObjectId(comment.parent_id) if comment.parent_id else None,
            "reply_count": 0,
            "likes": [],
            "is_deleted": False,
            "created_at": datetime.utcnow(),
        }

        result = await db.comments.insert_one(comment_dict)

        # If this is a reply, increment parent's reply_count
        if comment.parent_id:
            await db.comments.update_one(
                {"_id": ObjectId(comment.parent_id)}, {"$inc": {"reply_count": 1}}
            )

        # Update user's comment count
        await db.users.update_one(
            {"_id": ObjectId(user_id)}, {"$inc": {"comment_count": 1}}
        )

        created_comment = await db.comments.find_one({"_id": result.inserted_id})
        created_comment["id"] = str(created_comment["_id"])
        del created_comment["_id"]
        if created_comment.get("parent_id"):
            created_comment["parent_id"] = str(created_comment["parent_id"])
        print(messages.seperator)
        print(messages.comment_created, created_comment)
        print(messages.seperator)
        return CommentInDB(**created_comment)

    # ............................................................................................................................................
    @staticmethod
    async def get_comment(comment_id: str) -> CommentInDB:
        comment = await db.comments.find_one({"_id": ObjectId(comment_id)})
        if not comment:
            raise HTTPException(status_code=404, detail=messages.comment_not_found)

        # Convert MongoDB document to CommentInDB
        comment["id"] = str(comment["_id"])
        del comment["_id"]
        if comment.get("parent_id"):
            comment["parent_id"] = str(comment["parent_id"])

        return CommentInDB(**comment)

    # ............................................................................................................................................
    @staticmethod
    async def get_comments(
    parent_id: Optional[str] = None,
    limit: int = 10,
    skip: int = 0
) -> List[CommentInDB]:
        query = {"is_deleted": False}
        if parent_id:
            query["parent_id"] = ObjectId(parent_id)
        else:
            query["parent_id"] = None

        # Sort by created_at in descending order (newest first)
        comments = (
            await db.comments.find(query)
            .sort("created_at", -1)  # -1 = descending order
            .skip(skip)
            .limit(limit)
            .to_list(None)
        )

        processed_comments = []
        for comment in comments:
            comment["id"] = str(comment["_id"])
            del comment["_id"]
            if comment.get("parent_id"):
                comment["parent_id"] = str(comment["parent_id"])
            processed_comments.append(CommentInDB(**comment))

        return processed_comments

    # ............................................................................................................................................

    @staticmethod
    async def update_comment(
        comment_id: str, content: str, user_id: str
    ) -> CommentInDB:
        comment = await db.comments.find_one({"_id": ObjectId(comment_id)})
        if not comment or comment["author_id"] != user_id:
            raise HTTPException(status_code=403, detail=messages.authority_error)

        await db.comments.update_one(
            {"_id": ObjectId(comment_id)},
            {"$set": {"content": content, "updated_at": datetime.utcnow()}},
        )
        print(messages.seperator)
        print(messages.comment_update, comment)
        print(messages.seperator)
        return await CommentService.get_comment(comment_id)

    # ............................................................................................................................................

    @staticmethod
    async def delete_comment(comment_id: str, user_id: str, is_admin: bool = False):
        comment = await db.comments.find_one({"_id": ObjectId(comment_id)})
        if not comment:
            print(messages.seperator)
            print(messages.comment_not_found)
            print(messages.seperator)
            raise HTTPException(status_code=404, detail=messages.comment_not_found)

        """ Only author or admin can delete """

        if comment["author_id"] != user_id and not is_admin:
            print(messages.seperator)
            print(messages.authority_error)
            print(messages.seperator)
            raise HTTPException(status_code=403, detail=messages.authority_error)

        if is_admin:

            """Hard delete for admin"""

            await db.comments.delete_one({"_id": ObjectId(comment_id)})

            print(messages.seperator)
            print(messages.admin_comment_delete)
            print(messages.seperator)

        else:

            """Soft delete for regular users"""

            await db.comments.update_one(
                {"_id": ObjectId(comment_id)}, {"$set": {"is_deleted": True}}
            )

        """ Decrement user's comment count if not hard deleted """

        if not is_admin:
            await db.users.update_one(
                {"_id": ObjectId(comment["author_id"])}, {"$inc": {"comment_count": -1}}
            )
            print(messages.seperator)
            print(messages.comment_delete_successful)
            print(messages.seperator)

    # ............................................................................................................................................

    @staticmethod
    async def toggle_like(comment_id: str, user_id: str) -> CommentInDB:
        comment = await db.comments.find_one(
            {"_id": ObjectId(comment_id), "likes": user_id}
        )

        if comment:
            await db.comments.update_one(
                {"_id": ObjectId(comment_id)}, {"$pull": {"likes": user_id}}
            )
            print(messages.seperator)
            print(f"User {user_id} unliked comment {comment_id}")
            print(messages.seperator)
        else:
            await db.comments.update_one(
                {"_id": ObjectId(comment_id)}, {"$addToSet": {"likes": user_id}}
            )
            print(messages.seperator)
            print(f"User {user_id} liked comment {comment_id}")
            print(messages.seperator)

        return await CommentService.get_comment(comment_id)

    # ............................................................................................................................................

    @staticmethod
    async def get_comments_by_user(
        user_id: str, limit: int = 10, skip: int = 0
    ) -> List[CommentInDB]:
        comments = (
            await db.comments.find({"author_id": user_id, "is_deleted": False})
            .skip(skip)
            .limit(limit)
            .to_list(None)
        )
        print(messages.seperator)
        print(f"Retrieved {len(comments)} comments by user {user_id}")
        print(messages.seperator)
        return [CommentInDB(**comment, id=str(comment["_id"])) for comment in comments]

    # ............................................................................................................................................

    @staticmethod
    async def get_comment_count_by_user(user_id: str) -> int:
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        count = user.get("comment_count", 0) if user else 0

        print(messages.seperator)
        if user:
            print(f"User {user_id} has {count} comments")
        else:
            print(f"User {user_id} not found while fetching comment count")
        print(messages.seperator)

        return count
