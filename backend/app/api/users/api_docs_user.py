"""
AUTHENTICATION & USER PROFILE API DOCUMENTATION
==========================================================================================================================================

BASE PATH: /user

------------------------------------------------------------------------------------------------------------------------------------------
1. USER REGISTRATION
------------------------------------------------------------------------------------------------------------------------------------------
Endpoint: POST /user/signup
Description: Register a new user account

Request Body (JSON):
{
    "username": "string (required)",
    "email": "string (required, valid email)",
    "password": "string (required, min 8 chars)"
}

Example Response:
{
    "message": "User created successfully",
    "id": "507f1f77bcf86cd799439011"
}
------------------------------------------------------------------------------------------------------------------------------------------
2. USER LOGIN
------------------------------------------------------------------------------------------------------------------------------------------
Endpoint: POST /user/login
Content-Type: application/x-www-form-urlencoded

Form Data:
- username: string
- password: string

Example Response:
{
    "access_token": "eyJhbGciOi...",
    "token_type": "bearer",
    "user": {
        "username": "testuser",
        "email": "test@example.com",
        "user_id": "507f1f77bcf86cd799439011"
    }
}

------------------------------------------------------------------------------------------------------------------------------------------
3. GET CURRENT USER
------------------------------------------------------------------------------------------------------------------------------------------
Endpoint: GET /user/me
Headers: Authorization: Bearer <token>

Response: Returns complete user profile (excluding sensitive fields)

------------------------------------------------------------------------------------------------------------------------------------------
4. PASSWORD RESET
------------------------------------------------------------------------------------------------------------------------------------------
Endpoint: POST /user/reset-password
Headers: Content-Type: application/json

Request Body:
{
    "email": "user@example.com",
    "new_password": "newSecurePassword123"
}

Response:
{
    "message": "Password updated successfully"
}

------------------------------------------------------------------------------------------------------------------------------------------
5. PROFILE PICTURE ENDPOINTS
------------------------------------------------------------------------------------------------------------------------------------------

5.1 UPLOAD PROFILE PICTURE
Endpoint: POST /user/profile-pic
Content-Type: multipart/form-data

Form Data:
- file: image file (JPEG/PNG, max 5MB)

Response:
{
    "message": "Profile picture updated successfully"
}
------------------------------------------------------------------------------------------------------------------------------------------
5.2 GET PROFILE PICTURE
Endpoint: GET /user/profile-pic
Optional Query Param: ?user_id=<target_user_id> (admin only)

Response: Binary image data (image/jpeg)
------------------------------------------------------------------------------------------------------------------------------------------
5.3 DELETE PROFILE PICTURE
Endpoint: DELETE /user/profile-pic

Response:
{
    "message": "Profile picture removed successfully"
}

ERROR RESPONSES
------------------------------------------------------------------------------------------------------------------------------------------
Common error status codes:
- 400 Bad Request: Invalid input data
- 401 Unauthorized: Missing/invalid token
- 403 Forbidden: Insufficient permissions
- 404 Not Found: Resource not found
- 413 Payload Too Large: File exceeds 5MB limit
"""