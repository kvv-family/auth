from typing import TypedDict


class AuthorizeEvent(TypedDict): ...


class RegisterEvent(TypedDict): ...


class TokenReleaseEvent(TypedDict): ...


type RabbitMQEvents = AuthorizeEvent | RegisterEvent | TokenReleaseEvent


class RabbitMQMessage(TypedDict):
    create_at: str
    event_name: str
    data: RabbitMQEvents
    uid: str
