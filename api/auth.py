from typing import Annotated, Literal
from uuid import uuid4

from fastapi import Depends, Form, HTTPException
from fastapi.requests import Request
from fastapi.responses import RedirectResponse, Response
from fastapi.routing import APIRouter
from pony.orm import commit, db_session

from db import Profile, User
from exception import AuthorizeException, AuthorizeTemplateException
from models import ErrorMessage
from models.session import SessionData
from models.token import RegisterRequest, TokenData
from settings import TEMPLATES, cookie, sessin_backend, session_verifier
from utils import clients, token, users
from utils.password import hash_password

auth_router = APIRouter(tags=["auth"])


# Эндпоинт для регистрации пользователя
@auth_router.post("/register", responses={401: {"model": ErrorMessage}})
async def register(data: RegisterRequest):
    with db_session:
        user = User.get(username=data.username)
        if user:
            raise HTTPException(
                status_code=400, detail={"message": "Username already exists"}
            )
        hashed_password = hash_password(data.password)
        profile_dump = data.profile.model_dump()
        profile = Profile(**profile_dump)
        commit()
        User(username=data.username, hashed_password=hashed_password, profile=profile)
    return {"message": "User created successfully"}


# Форма для авторизации
@auth_router.get("/authorize", dependencies=[Depends(cookie)])
async def authorize(
    request: Request,
    client_id: str,
    redirect_uri: str,
    scope: str,
    state: str,
    session_data=Depends(session_verifier),
):
    print(session_data)
    try:
        # Блок получения клиента и проверки клиента
        client = clients.get_client(client_id=client_id, redirect_uri=redirect_uri)  # noqa: F841
    except AuthorizeException as exc:
        raise AuthorizeTemplateException(detail=exc.detail)

    return TEMPLATES.TemplateResponse(
        request=request,
        name="login.html",
        context=dict(
            client_id=client_id,
            redirect_uri=redirect_uri,
            scope=scope,
            state=state,
        ),
    )


@auth_router.post("/authorize")
async def authorize_post(
    response: Response,
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    client_id: Annotated[str, Form()],
    scope: Annotated[str, Form()],
    state: Annotated[str, Form()],
    redirect_uri: Annotated[str | None, Form()] = None,
    form: Annotated[Literal["form", "api"], Form()] = "form",
):
    try:
        # Блок получения клиента
        client = clients.get_client(client_id=client_id, redirect_uri=redirect_uri)

        # Блок получения пользователя
        user = users.get_user(username=username, password=password)
    except AuthorizeException as exc:
        if form == "form":
            raise AuthorizeTemplateException(detail=exc.detail)
        else:
            raise HTTPException(status_code=401, detail=exc.detail)
    code, refresh = token.create_access_token(
        client=client,
        user=user,
        data=TokenData(username=user.username, user_id=user.id),
    )
    url = f"{redirect_uri}{code}"
    if form == "form":
        if not redirect_uri:
            raise AuthorizeTemplateException(
                detail={"message": "Redirect url not found"}
            )
        session = uuid4()
        data = SessionData(user_id=user.id, token=code, refresh=refresh)
        await sessin_backend.create(session, data=data)
        response_redirect = RedirectResponse(url=url)
        cookie.attach_to_response(response=response_redirect, session_id=session)
        return response_redirect
    elif form == "api":
        return {
            "client_id": client_id,
            "scope": scope,
            "state": state,
            "authorization_code": code,
        }
