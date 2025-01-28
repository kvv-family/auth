from datetime import datetime
from uuid import uuid4

import aio_pika
from aio_pika.abc import AbstractChannel, AbstractRobustConnection
from settings import setting

from models import events
import json


def save_event(message: events.RabbitMQMessage):
    """Сохранение логов сообщения

    :param message: Сообщение для сохранения
    :type message: events.RabbitMQMessage
    """
    ...


async def create_connection(virtualhost: str = "/") -> AbstractRobustConnection:
    connection: AbstractRobustConnection = await aio_pika.connect_robust(
        host=setting.RABBITMQ_HOST,
        port=setting.RABBITMQ_PORT,
        login=setting.RABBITMQ_USERNAME,
        password=setting.RABBITMQ_PASSWORD,
        virtualhost=virtualhost,
    )
    return connection


async def send_event(event_name: str, data: events.RabbitMQEvents, client: str = "/"):
    """Отправка событий в шину

    :param event_name: Название события
    :type event_name: str
    :param data: Тело события
    :type data: events.RabbitMQEvents
    :param client: Viertual host для отправки, defaults to "/"
    :type client: str, optional
    """    
    now = datetime.now()
    id = uuid4()
    message: events.RabbitMQMessage = {
        "event_name": event_name,
        "create_at": now.isoformat(),
        "uid": str(id),
        "data": data,
    }

    save_event(message=message)

    connection: AbstractRobustConnection = await create_connection(virtualhost=client)
    rabbit_message = aio_pika.Message(json.dumps(message))
    channel: AbstractChannel = await connection.channel()

    exchange = await channel.declare_exchange(
        setting.RABBITMQ_EXCHANGE_NAME, type=aio_pika.ExchangeType.FANOUT
    )

    await exchange.publish(
        message=rabbit_message,
        routing_key=""
    )

    await connection.close()
