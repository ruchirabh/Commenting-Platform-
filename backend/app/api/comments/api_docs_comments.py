"""
COMMENTS API DOCUMENTATION
=============================================================================================================================

BASE PATH: /comments

All endpoints require authentication unless noted.

-----------------------------------------------------------------------------------------------------------------------------
1. GET ALL TOP-LEVEL COMMENTS
-----------------------------------------------------------------------------------------------------------------------------
Endpoint: GET /
Description: Fetch all root-level comments (not replies)

Query Params:
- limit (default: 10)
- skip (default: 0)

Example Response:
[
    {
        "id": "686d0209764b5c8f453da5d6",
        "content": "Top level comment",
        "author_id": "686cd00466aa0a42e1f011b9",
        "parent_id": null,
        ...
    }
]

-----------------------------------------------------------------------------------------------------------------------------
2. CREATE COMMENT
-----------------------------------------------------------------------------------------------------------------------------
Endpoint: POST /
Headers:
    Authorization: Bearer <token>

Request Body:
{
    "content": "Comment text",
    "parent_id": "optional_parent_id"  // Omit for top-level
}

Example Response:
{
    "id": "686d0209764b5c8f453da5d6",
    "content": "Comment text",
    "author_id": "686cd00466aa0a42e1f011b9",
    ...
}

-----------------------------------------------------------------------------------------------------------------------------
3. UPDATE COMMENT
-----------------------------------------------------------------------------------------------------------------------------
Endpoint: PUT /{comment_id}
Headers:
    Authorization: Bearer <token>

Request Body:
{
    "content": "Updated text"
}

Example Response:
{
    "id": "686d0209764b5c8f453da5d6",
    "content": "Updated text",
    ...
}

-----------------------------------------------------------------------------------------------------------------------------
4. DELETE COMMENT
-----------------------------------------------------------------------------------------------------------------------------
Endpoint: DELETE /{comment_id}
Headers:
    Authorization: Bearer <token>

Response:
{
    "message": "Comment deleted successfully"
}

-----------------------------------------------------------------------------------------------------------------------------
5. LIKE/UNLIKE COMMENT
-----------------------------------------------------------------------------------------------------------------------------
Endpoint: POST /{comment_id}/like
Headers:
    Authorization: Bearer <token>

Response: Updated comment with likes array

-----------------------------------------------------------------------------------------------------------------------------
6. GET COMMENT REPLIES
-----------------------------------------------------------------------------------------------------------------------------
Endpoint: GET /{comment_id}/replies
Description: Get all replies to a comment

Query Params:
- limit (default: 10)
- skip (default: 0)

-----------------------------------------------------------------------------------------------------------------------------
7. ADMIN HARD DELETE
-----------------------------------------------------------------------------------------------------------------------------
Endpoint: DELETE /admin/{comment_id}
Headers:
    Authorization: Bearer <admin_token>

Response:
{
    "message": "Comment permanently deleted"
}
"""