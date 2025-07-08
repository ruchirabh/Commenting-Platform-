from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional
from bson.binary import Binary
from pydantic import EmailStr
from app.models.user import UserCreate
from pydantic import BaseModel
from app.db.mongo import db
from app.logs import messages
from bson import ObjectId
from app.core.auth_utils import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Response,
    status,
)

router = APIRouter(tags=["auth"])


class ResetPasswordRequest(BaseModel):
    email: str
    new_password: str


ALLOWED_FILE_TYPES = ["image/jpeg", "image/png"]
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
# ............................................................................................................................................

"""" API FOR REGISTRATION OF NEW USER """


@router.post("/signup")
async def signup(user: UserCreate):
    if await db.users.find_one({"email": user.email}):
        print(messages.seperator)
        print(messages.existing_email)
        print(messages.seperator)
        raise HTTPException(status_code=400, detail=messages.existing_email)

    hashed_password = get_password_hash(user.password)
    user_dict = user.dict()
    user_dict.pop("password")
    user_dict["hashed_password"] = hashed_password
    user_dict["disabled"] = False

    result = await db.users.insert_one(user_dict)
    print(messages.seperator)
    print(messages.successfull_signup, result)
    print(messages.seperator)
    return {"message": messages.successfull_signup, "id": str(result.inserted_id)}


# ............................................................................................................................................

""" API FOR LOGIN """


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await db.users.find_one({"username": form_data.username})

    if not user or not verify_password(form_data.password, user["hashed_password"]):
        print(messages.seperator)
        print(messages.wrong_credentials)
        print(messages.seperator)
        raise HTTPException(status_code=400, detail=messages.wrong_credentials)
    access_token = create_access_token(
        data={
            "sub": user["username"],
            "email": user["email"],
            "user_id": str(user["_id"]),
            "disabled": user.get("disabled", False),
        },
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    user_data = dict(user)
    user_data["_id"] = str(user_data["_id"])
    del user_data["hashed_password"]
    del user_data["profile_pic"]

    print(messages.seperator)
    print(messages.successfull_login, user_data)
    print(messages.seperator)
    return {
        "msg": messages.successfull_login,
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_data,
    }


# ............................................................................................................................................

"""API FOR IDENTIFY CURRENT USER"""


@router.get("/me")
async def read_current_user(current_user: dict = Depends(get_current_user)):
    return current_user


# ............................................................................................................................................

""" API FOR PASSWORD RESET  """


@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest):

    user = await db.users.find_one({"email": request.email})
    if not user:
        print(messages.seperator)
        print(messages.user_not_found)
        print(messages.seperator)
        raise HTTPException(status_code=404, detail=messages.user_not_found)

    hashed_password = get_password_hash(request.new_password)

    await db.users.update_one(
        {"email": request.email}, {"$set": {"hashed_password": hashed_password}}
    )
    print(messages.seperator)
    print(messages.password_reset_success)
    print(messages.seperator)
    return {"message": messages.password_reset_success}


# ............................................................................................................................................

""" API FOR UPLOADING A PROFILE PICTURE """


@router.post("/profile-pic")
async def upload_profile_pic(
    file: UploadFile = File(...), current_user: dict = Depends(get_current_user)
):
    """
    Upload a profile picture with validation for:
    - File type (jpeg, png, gif)
    - File size (max 5MB)
    """
    # Validate file type
    if file.content_type not in ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{messages.unsupported_file_type} {', '.join(ALLOWED_FILE_TYPES)}",
        )

    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"{messages.file_too_large} {MAX_FILE_SIZE//(1024*1024)}MB",
        )

    # Store in MongoDB
    encoded_image = Binary(contents)
    await db.users.update_one(
    {"_id": ObjectId(current_user["user_id"])}, 
    {"$set": {"profile_pic": encoded_image}}
)

    return {"message": messages.profile_pic_updated_success}


# ............................................................................................................................................

""" API FOR FETCHING THE PROFILE PIC """


@router.get("/profile-pic")
async def get_profile_pic(
    user_id: Optional[str] = None, current_user: dict = Depends(get_current_user)
):
    """
    Get profile picture for specified user or current user if no ID provided
    Returns 404 if user or profile picture not found
    """
    query_id = user_id if user_id else current_user["user_id"]

    user = await db.users.find_one({"_id": query_id}, {"profile_pic": 1})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=messages.user_not_found
        )

    if "profile_pic" not in user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=messages.profile_pic_not_found
        )

    return Response(content=user["profile_pic"], media_type="image/jpeg")


# ............................................................................................................................................

""" API FOR DELETING THE PROFILE PIC """


@router.delete("/profile-pic")
async def delete_profile_pic(current_user: dict = Depends(get_current_user)):
    """
    Remove the profile picture for current user
    """
    result = await db.users.update_one(
        {"_id": current_user["_id"]}, {"$unset": {"profile_pic": ""}}
    )

    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=messages.no_profile_pic_to_delete,
        )

    return {"message": messages.removed_profile_pic}
