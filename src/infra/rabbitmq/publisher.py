import json
import aio_pika

from typing import Any

from infra.rabbitmq.base import RabbitMQPublisherClient
from logger.logger import setup_logger


logger = setup_logger(__name__)


class PublisherRabbitMQ(RabbitMQPublisherClient):
    """
    Клиент для отправки сообщений в RabbitMQ.
    """
    
    async def publisher(self, message: Any, routing_key: str):
        if not self.channel or not self.exchange:
            raise Exception("Клиент RabbitMQ не подключен.")

        try:
            if isinstance(message, str):
                body = message.encode()
            else:
                body = json.dumps(message).encode()

            await self.exchange.publish(
                aio_pika.Message(body=body),
                routing_key=routing_key,
            )
            logger.info(f"Сообщение успешно отправлено с routing_key={routing_key}")
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения в RabbitMQ: {e}")
            raise
