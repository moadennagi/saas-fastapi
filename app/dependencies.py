import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from schemas import PydanticUser
from database import User

oauth_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
)


def get_current_user(
    token: str = Depends(oauth_scheme)
) -> User:
    decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
    username = decoded['sub']
    # get user from database
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid credentials'
    )


class PermissionDependency:

    def __init__(self, required_permissions: list[str]) -> None:
        self.required_permissions = required_permissions

    def __call__(self, user: User = Depends(get_current_user)) -> bool:
        for r_perm in self.required_permissions:
            if r_perm not in user.permissions:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Permissions'
                )
        return True
