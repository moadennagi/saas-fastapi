from __future__ import annotations

from typing import List

from crud import CRUDMixin
from database.base import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, relationship, Session
from schemas import PydanticCreateUser


class ValidationError(Exception):
    def __init__(self, message: str = "") -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message


users_roles = Table(
    'users_roles',
    Base.metadata,
    Column('role_id', ForeignKey('roles.id')),
    Column('user_id', ForeignKey('users.id'))
)


class User(Base, CRUDMixin):
    __tablename__ = 'users'

    id: Mapped[int] = Column(Integer, primary_key=True)
    username: Mapped[str] = Column(String(255), unique=True)
    password: Mapped[str] = Column(String(255), nullable=False)

    roles: Mapped[List[Role]] = relationship(secondary=users_roles)

    @property
    def permissions(self) -> list[tuple]:
        permissions = []
        for role in self.roles:
            for permission in role.permissions:
                permissions.append((permission.resource, permission.action))
        return permissions

    def has_permissions(self, permissions: list[tuple]) -> bool:
        for permission in permissions:
            if permission not in self.permissions:
                raise PermissionError('Not enough permissions')
        return True

    @classmethod
    def create(cls, session: Session, *, data: PydanticCreateUser) -> User:
        role = Role.get(session, pk=data.role_id)
        if not role:
            raise ValidationError('Role not found')
        obj = cls(**data.dict(exclude={'role_id', 'roles'}))
        obj.roles.append(role)
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj


class Role(Base, CRUDMixin):
    __tablename__ = 'roles'

    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String(255), unique=True)

    permissions: Mapped[List[Permission]] = relationship('Permission',
                                                         back_populates='role')


class Permission(Base, CRUDMixin):
    __tablename__ = 'permissions'

    id: Mapped[int] = Column(Integer, primary_key=True)
    resource: Mapped[str] = Column(String(255), nullable=False)
    action: Mapped[str] = Column(String(255), nullable=False)
    role_id: Mapped[int] = Column(Integer, ForeignKey('roles.id'))

    role: Mapped[Role] = relationship('Role', back_populates='permissions')
