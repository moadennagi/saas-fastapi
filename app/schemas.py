from typing import List, Optional
from pydantic import BaseModel


class PydanticPermission(BaseModel):
    id: int
    resource: str
    action: str

    class Config:
        orm_mode = True


class PydanticRole(BaseModel):
    id: int
    name: str
    permissions: List[PydanticPermission]

    class Config:
        orm_mode = True


class PydanticUser(BaseModel):
    id: int
    username: str
    password: str
    role_id: int
    roles: Optional[List[PydanticRole]]

    class Config:
        orm_mode = True


class PydanticCreateUser(PydanticUser):
    id: Optional[str]


class LoginData(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    type: str
