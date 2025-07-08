# JWT IMPLEMENTATION
from datetime import datetime, timedelta
from typing import Optional
from bson import ObjectId
from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings
from fastapi.security import OAuth2PasswordBearer
from app.db.mongo import db
from app.logs import messages

SECRET_KEY = settings.jwt_secret
ALGORITHM = settings.jwt_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Generate JWT token with admin status"""

    user = await db.users.find_one({"_id": ObjectId(data["user_id"])})

    to_encode = data.copy()
    to_encode.update(
        {
            "is_admin": user.get("is_admin", False),
            "exp": datetime.utcnow()
            + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)),
        }
    )

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail=messages.validation_error,
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        if payload is None:
            raise credentials_exception
        return payload
    except JWTError:
        raise credentials_exception


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail=messages.validation_error,
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        if payload is None:
            raise credentials_exception

        # Add admin check
        user = await db.users.find_one({"_id": ObjectId(payload["user_id"])})
        if not user:
            raise credentials_exception

        payload["is_admin"] = user.get("is_admin", False)
        return payload
    except JWTError:
        raise credentials_exception
