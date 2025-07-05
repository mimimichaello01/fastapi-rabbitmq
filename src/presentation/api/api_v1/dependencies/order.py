from fastapi import Depends, Request
from infra.db import db_helper
from sqlalchemy.ext.asyncio import AsyncSession
from application.service.order_service import OrderServiceImpl
from infra.rabbitmq.publisher import PublisherRabbitMQ
from infra.repositories.order_repository_impl import OrderRepositoryImpl


def get_order_repo(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> OrderRepositoryImpl:
    return OrderRepositoryImpl(session)


def get_publisher(request: Request) -> PublisherRabbitMQ:
    return request.app.state.publisher


def get_order_service(
    order_repo: OrderRepositoryImpl = Depends(get_order_repo),
    publisher: PublisherRabbitMQ = Depends(get_publisher),
) -> OrderServiceImpl:
    return OrderServiceImpl(order_repo, publisher)


