# In app/db/init_db.py (create this file)
from app.db.mongo import db
from app.core.auth_utils import get_password_hash
from app.models.user import UserCreate
from app.logs import messages
from app.core.config import settings


async def create_initial_admin():
    admin_email = settings.admin_email
    if not await db.users.find_one({"email": admin_email}):
        admin_user = UserCreate(
            username=settings.admin_username, email=admin_email, password=settings.admin_password
        )
        hashed_password = get_password_hash(admin_user.password)
        await db.users.insert_one(
            {
                "username": admin_user.username,
                "email": admin_user.email,
                "hashed_password": hashed_password,
                "is_admin": True,
                "disabled": False,
            }
        )
        print(messages.admin_created)
