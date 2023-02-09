from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str = 'sqlite+pysqlite:///dev.sqlite3'
    test_database_url: str = 'sqlite+pysqlite:///:memory:'


settings = Settings()
