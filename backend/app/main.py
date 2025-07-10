from fastapi import FastAPI
from app.api.users import auth
from app.api.comments import comments
from app.logs import messages
from app.db.mongo import db
from app.db.init_db import create_initial_admin
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace "*" with your Vercel frontend URL
    allow_methods=["*"],
    allow_headers=["*"],
)

print(messages.seperator)
print(messages.server_start)
print(messages.seperator)

# mongo connection check
@app.on_event("startup")
async def startup_db():
    try:
        await db.command("ping")
        print(messages.seperator)
        print(messages.mongo_connection)
        print(messages.seperator)
    except Exception as e:
        print(messages.mongo_connection_fail, e)

# admin creation
@app.on_event("startup")
async def startup_db():
    await create_initial_admin()
    print(messages.seperator)
    print(messages.admin_created)
    print(messages.seperator)

app.include_router(auth.router, prefix="/user")
app.include_router(comments.router, prefix="/comments")
