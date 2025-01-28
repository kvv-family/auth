from datetime import datetime

from pony.orm import Optional, PrimaryKey, Required, Set

from utils.password import hash_password, verify_password

from .base import db


class Profile(db.Entity):
    id = PrimaryKey(int, auto=True)
    user = Optional("User")
    first_name = Required(str)
    middle_name = Optional(str)
    last_name = Required(str)
    date_birth = Optional(datetime)


# Модель пользователя
class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    username = Required(str, unique=True)
    hashed_password = Required(str)
    codes = Set("AuthorizationCode")
    tokens = Set("AccessToken")
    profile = Required(Profile)
    created_at = Optional(datetime)

    def set_password(self, password: str):
        self.hashed_password = hash_password(password)

    def check_password(self, provided_password: str) -> bool:
        return verify_password(self.hashed_password, provided_password)
