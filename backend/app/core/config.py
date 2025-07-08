from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # MongoDB
    mongo_uri: str
    mongo_db_name: str

    # jwt
    jwt_secret: str
    jwt_algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
