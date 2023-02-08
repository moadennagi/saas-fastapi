from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from config import settings

engine = create_engine(settings.database_url)
SessionMaker = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


Base.metadata.create_all(bind=engine)
