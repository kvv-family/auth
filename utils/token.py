from datetime import datetime, timedelta

from fastapi import HTTPException
from jose import JWTError, jwt
from pony.orm import db_session, commit

from db import AccessToken, Client, User, RefreshToken
from models.token import TokenData
from settings import setting


def create_authorization_code() -> str:
    """Функция создания кода авторизации

    :return: _description_
    :rtype: str
    """
    ...


def create_access_token(
    client: Client, user: User, data: TokenData, expires_delta: timedelta | None = None
) -> tuple[str, str]:
    """Функция создания токена доступа

    :param client: _description_
    :type client: Client
    :param user: _description_
    :type user: User
    :param data: _description_
    :type data: dict
    :param expires_delta: _description_, defaults to None
    :type expires_delta: timedelta | None, optional
    :return: _description_
    :rtype: str
    """
    to_encode = data.model_dump()
    to_encode_refresh = to_encode.copy()
    to_encode_refresh.update({"exp": datetime.utcnow() + timedelta(days=setting.REFRESH_EXPIRE)})
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, setting.SECRET_KEY, algorithm=setting.ALGORITHM)
    encoded_refresh = jwt.encode(to_encode_refresh, setting.SECRET_KEY, algorithm=setting.ALGORITHM)
    with db_session:
        refresh = RefreshToken(user=user.id, client=client.id, token=encoded_refresh)
        commit()
        AccessToken(user=user.id, client=client.id, token=encoded_jwt, refresh=refresh)
    return encoded_jwt, encoded_refresh


def verify_token(token: str) -> TokenData:
    """Функция верификации токена

    :param token: _description_
    :type token: str
    :raises HTTPException: _description_
    :raises HTTPException: _description_
    :return: _description_
    :rtype: TokenData
    """

    try:
        payload = jwt.decode(token, setting.SECRET_KEY, algorithms=[setting.ALGORITHM])
        username: str = payload.get("username")
        user_id = payload.get("user_id")
        if username is None or user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token_data = TokenData(username=username, user_id=user_id)
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_data
