from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.logs import messages

client = AsyncIOMotorClient(settings.mongo_uri)
db = client[settings.mongo_db_name]


