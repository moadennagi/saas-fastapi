from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel


class PermissionSchema(BaseModel):
    id: int
    resource: str
    action: str
    role_id: int
    role: RoleSchema

    class Config:
        orm_mode = True


class CreatePermission(PermissionSchema):
    id: Optional[int]
    role: Optional[RoleSchema]


class UpdateSchema(PermissionSchema):
    id: Optional[int]
    role: Optional[RoleSchema]
    resource: Optional[str]
    action: Optional[str]


class RoleSchema(BaseModel):
    id: int
    name: str
    permissions: List[PermissionSchema]

    class Config:
        orm_mode = True


class UserSchema(BaseModel):
    id: int
    username: str
    password: str
    role_id: int
    roles: Optional[List[RoleSchema]]

    class Config:
        orm_mode = True


class CreateUser(UserSchema):
    id: Optional[str]


class UpdateUser(UserSchema):
    id: Optional[int]
    username: Optional[str]
    password: Optional[str]
    role_id: Optional[int]


class LoginData(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    type: str
