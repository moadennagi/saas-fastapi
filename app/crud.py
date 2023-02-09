from typing import List, Optional, TypeVar, Union

from database import Base
from pydantic import BaseModel
from schemas import UpdateUser
from sqlalchemy.orm import Session

Model = TypeVar('Model', bound=Base)
CreateSchema = TypeVar('CreateSchema', bound=BaseModel)
UpdateSchema = TypeVar('UpdateSchema', bound=Union[UpdateUser, BaseModel])


class CRUDMixin:

    @classmethod
    def get(cls, session: Session, *, pk: int) -> Optional[Model]:
        res = session.query(cls).filter(cls.id == pk).first()
        return res

    @classmethod
    def get_multiple(
        cls, session: Session, *, ids: list[int]
    ) -> List[Optional[Model]]:
        objs = session.query(cls).filter(cls.id)._in(ids)

    @classmethod
    def create(cls, session: Session, *, data: CreateSchema) -> Model:
        obj = cls(**data.dict())
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj

    @classmethod
    def update(
        cls, session: Session, *, pk: int, data: UpdateSchema
    ) -> Model:
        """Updates the record with given data
           Will not handle foreignkeys"""
        obj = cls.get(session, pk=pk)
        if not obj:
            return
        for k, v in data.dict(exclude_unset=True):
            setattr(obj, k, v)
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj

    @classmethod
    def delete(cls, session: Session, *, pk: int) -> Optional[Model]:
        ...
