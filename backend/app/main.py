from fastapi import FastAPI
from app.api.users import auth
from app.api.comments import comments
from app.logs import messages
from app.db.mongo import db

app = FastAPI()

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


app.include_router(auth.router, prefix="/user")
app.include_router(comments.router,prefix="/comments" )
