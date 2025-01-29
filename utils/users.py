from pony.orm import db_session

from db import User
from exception import AuthorizeException


def get_user(username: str, password: str) -> User:
    with db_session:
        user: User = User.get(username=username)
        if not user:
            raise AuthorizeException(
                detail={"message": "Incorrect username or password"}
            )
        if not user.check_password(password):
            raise AuthorizeException(
                detail={"message": "Incorrect username or password"}
            )
    return user
