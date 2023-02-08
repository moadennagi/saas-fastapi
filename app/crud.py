from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import TypeVar, Optional
from database import Base


Model = TypeVar('Model', bound=Base)
CreateSchema = TypeVar('CreateSchema', bound=BaseModel)
UpdateSchema = TypeVar('UpdateSchema', bound=BaseModel)


class CRUDMixin:

    @classmethod
    def get(cls, session: Session, *, pk: int) -> Optional[Model]:
        res = session.query(cls).filter(cls.id == pk).first()
        return res

    @classmethod
    def create(cls, session: Session, *, data: CreateSchema) -> Model:
        obj = cls(**data.dict())
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj

    @classmethod
    def update(
        cls,
        session: Session,
        *,
        pk: int,
        data: UpdateSchema
    ) -> Model:
        ...

    @classmethod
    def delete(cls, session: Session, *, pk: int) -> Optional[Model]:
        ...
