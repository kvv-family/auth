from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AuthorizeRequest(BaseModel):
    username: str
    password: str
    client_id: str
    client_secret: str
    redirect_uri: str
    response_type: str
    scope: str


class AuthorizeResponse(BaseModel):
    code: str


class TokenRequest(BaseModel):
    username: str
    password: str
    grant_type: str
    scope: str
    client_id: str
    client_secret: str

    redirect_uri: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    scope: str
    client_id: str


class ProfileModel(BaseModel):
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    date_birth: Optional[datetime] = None


class RegisterRequest(BaseModel):
    username: str
    password: str
    profile: ProfileModel


class TokenData(BaseModel):
    username: str
    user_id: int
