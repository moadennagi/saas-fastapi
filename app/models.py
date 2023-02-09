from __future__ import annotations

from typing import List

from crud import CRUDMixin
from database.base import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, relationship, Session
from schemas import CreateUser, UpdateUser


class ValidationError(Exception):
    def __init__(self, message: str = "") -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message


class ObjectNotFound(Exception):
    def __init__(self, *args: object, **kwargs: object) -> None:
        self.message = kwargs.get('message')
        super().__init__(*args)

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
    def create(cls, session: Session, *, data: CreateUser) -> User:
        role = Role.get(session, pk=data.role_id)
        if not role:
            raise ValidationError('Role not found')
        obj = cls(**data.dict(exclude={'role_id', 'roles'}))
        obj.roles.append(role)
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj

    @classmethod
    def update(cls, session: Session, *, pk: int, data: UpdateUser) -> User:
        role = None
        obj = cls.get(session, pk=pk)
        if not obj:
            raise ObjectNotFound(message='Object not found')
        if data.role_id:
            role = Role.get(session, pk=data.role_id)
            if role and role not in obj.roles:
                obj.roles.append(role)
        
        data = data.dict(exclude_unset=True, exclude={'role', 'role_id'})
        for k, v in data.items():
            if getattr(obj, k) != v:
                setattr(obj, k, v)
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
