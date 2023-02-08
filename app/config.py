from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str
    test_database_url: str


settings = Settings()
