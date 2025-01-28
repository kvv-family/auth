import os
import secrets
from pathlib import Path
from uuid import UUID

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.frontends.implementations import CookieParameters, SessionCookie
from pydantic_settings import BaseSettings
from web3 import EthereumTesterProvider, Web3

from models.session import BasicVerifier, SessionData


class Settings(BaseSettings):
    SECRET_KEY: str | None = None
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DOMAIN: str = "127.0.0.1:8000"
    SSL: bool = False
    RABBITMQ_EXCHANGE_NAME: str = "Authentication.Events"
    RABBITMQ_HOST: str = ""
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USERNAME: str = ""
    RABBITMQ_PASSWORD: str = ""
    SCOPES: str = "user"


setting = Settings()

# OAuth2 схема
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={
        "profile": "Информация о пользователе",
        "email": "Информацию о почте пользователя",
        "phone": "Информацию о номере телефона пользователя",
    },
)


BASE_DIR = Path(__file__).resolve().parent

if not setting.SECRET_KEY:
    path_key = BASE_DIR / "keys" / "secret_key"
    key = None
    if not os.path.exists(path_key):
        key = secrets.token_urlsafe(24)
        with open(path_key, "w") as f:
            f.write(key)
    else:
        with open(path_key, "r") as f:
            key = f.read()
    setting.SECRET_KEY = key

TEMPLATES = Jinja2Templates(directory="templates")

W3 = Web3(EthereumTesterProvider())

cookie_params = CookieParameters()

cookie = SessionCookie(
    cookie_name="cookie",
    identifier="general_verifier",
    auto_error=True,
    secret_key=setting.SECRET_KEY,
    cookie_params=cookie_params,
)

sessin_backend = InMemoryBackend[UUID, SessionData]()
session_verifier = BasicVerifier(
    identifier="general_verifier",
    auto_error=True,
    backend=sessin_backend,
    auth_http_exception=HTTPException(status_code=403, detail="invalid session"),
)
