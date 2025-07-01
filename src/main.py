import asyncio
from contextlib import asynccontextmanager
from functools import partial
import os
from fastapi import FastAPI, APIRouter
from infra.rabbitmq.publisher import PublisherRabbitMQ
from infra.rabbitmq.workers import worker_status
from infra.rabbitmq.workers.base import RabbitMQConsumerClient
from infra.repositories.order_repository_impl import OrderRepositoryImpl
from settings.config import settings
from infra.db import db_helper

from presentation.api.api_v1.routers.order_router import order_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    publisher = PublisherRabbitMQ()
    await publisher.connect()
    app.state.publisher = publisher

    async for session in db_helper.session_getter():
        order_repo = OrderRepositoryImpl(session)
        callback = partial(worker_status.process_order_status_message, order_repo)

        consumer_client = RabbitMQConsumerClient(
            queue_name="order_status",
            routing_key=settings.rabbitmq.routing_key_status,
            callback=callback,
        )
        await consumer_client.connect()
        task = asyncio.create_task(consumer_client.start_consuming())

        try:
            yield
        finally:
            task.cancel()
            await consumer_client.close()
            await db_helper.dispose()
        break


api_router = APIRouter(prefix=settings.api_prefix.prefix)
api_router.include_router(order_router)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Order System",
        docs_url="/api/docs",
        debug=True,
        lifespan=lifespan,
    )
    app.include_router(api_router)
    return app
