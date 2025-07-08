from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # MongoDB
    mongo_uri: str
    mongo_db_name: str

    # jwt
    jwt_secret: str
    jwt_algorithm: str
    access_token_expire_minutes: int

    # admin

    admin_username: str
    admin_email: str
    admin_password : str

    class Config:
        env_file = ".env"


settings = Settings()
