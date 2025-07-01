import json
import aio_pika
from aio_pika.abc import AbstractIncomingMessage
from logger.logger import setup_logger
from settings.config import RabbitMQConfig
from settings.config import settings


logger = setup_logger(__name__)


class RabbitMQConsumerClient:
    def __init__(
        self,
        queue_name: str,
        routing_key: str,
        callback,
        config: RabbitMQConfig = settings.rabbitmq,
    ):
        self.config = config
        self.queue_name = queue_name
        self.routing_key = routing_key
        self.callback = callback

        self.connection = None
        self.channel = None
        self.exchange = None
        self.queue = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(
            host=self.config.host,
            port=self.config.port,
            login=self.config.user,
            password=self.config.password,
        )

        self.channel = await self.connection.channel()

        self.exchange = await self.channel.declare_exchange(
            name=self.config.exchange, type=aio_pika.ExchangeType.DIRECT, durable=True
        )

        self.queue = await self.channel.declare_queue(
            name=self.queue_name,
            auto_delete=False,
            durable=True,
        )

        await self.queue.bind(exchange=self.exchange, routing_key=self.routing_key)

    async def start_consuming(self):
        await self.connect()

        if not self.queue:
            raise Exception("Клиент RabbitMQ не подключен.")

        await self.queue.consume(self._on_message, no_ack=True)

    async def _on_message(self, message: AbstractIncomingMessage):
        async with message.process():
            try:
                payload = json.loads(message.body.decode())
                await self.callback(payload)
            except Exception as e:
                logger.error(f"Ошибка при обработке сообщения: {e}")
                raise

    async def close(self):
        if self.channel and not self.channel.is_closed:
            await self.channel.close()
        if self.connection and not self.connection.is_closed:
            await self.connection.close()
