from pony.orm import Required, Set

from .base import db
from .client import Client
from .user import User


# Модель кода авторизации
class AuthorizationCode(db.Entity):
    code = Required(str, unique=True)
    user = Required(User)
    client = Required(Client)
    active = Required(bool, default=True)


class RefreshToken(db.Entity):
    token = Required(str, unique=True)
    user = Required(User)
    client = Required(Client)
    access_tokens = Set("AccessToken")


# Модель токена доступа
class AccessToken(db.Entity):
    token = Required(str, unique=True)
    refresh = Required(RefreshToken)
    user = Required(User)
    client = Required(Client)
