import jwt
import bcrypt
import datetime
from database import User
from fastapi import HTTPException, status


def create_token(user: User) -> str:
    payload = {'sub': user.username, 'iat': datetime.datetime.utcnow(),
               'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=90)}
    token = jwt.encode(payload, key='secret')
    return token


def authenticate_user(username: str, password: str) -> User:
    exception = HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Invalid credentials'
                )
    # find user in the database
    user = None
    if not user:
        raise exception
    if not bcrypt.checkpw(password.encode(), user.password.encode()):
        raise exception
    return user
