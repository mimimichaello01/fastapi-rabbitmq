from typing import Optional
from uuid import UUID

from application.dto.order import (
    CreateOrderDTO,
    OrderResponseDTO,
    OrderStatusResponseDTO,
)
from application.exceptions.order import OrderNotFoundException
from application.interfaces.services.order_service_interfaces import (
    AbstractOrderService,
)
from infra.models.order import StatusOrder
from infra.rabbitmq.publisher import PublisherRabbitMQ
from infra.repositories.order_repository_impl import OrderRepositoryImpl
from logger.logger import setup_logger


logger = setup_logger(__name__)


class OrderServiceImpl(AbstractOrderService):
    """
    Реализация сервиса для работы с заказами.
    """

    def __init__(self, order_repo: OrderRepositoryImpl, publisher: PublisherRabbitMQ):
        self.order_repo = order_repo
        self.publisher = publisher

    async def get_order(self, order_id: UUID) -> Optional[OrderResponseDTO]:
        """
        Получение заказа по его id.
        """
        logger.info(f"Получение заказа с id {order_id}")

        order = await self.order_repo.get_order_by_id(order_id)


        if not order:
            logger.warning(f"Заказ с id {order_id} не найден.")
            raise OrderNotFoundException(order_id)


        logger.info(f"Заказ с id {order_id} возвращен.")
        return order

    async def create_order(self, create_order: CreateOrderDTO) -> OrderResponseDTO:
        """
        Создание нового заказа.
        """
        logger.info("Создание нового заказа.")
        logger.info("Данные заказа: %s", create_order.model_dump())
        order_response = await self.order_repo.create_order(create_order)

        message = {
            "order_id": str(order_response.id),
            "status": order_response.status.value ,
        }

        await self.publisher.publisher(message, self.publisher.config.routing_key_status)

        logger.info(f"Заказ с id {order_response.id} создан.")

        return order_response


    async def update_order_status(
        self, order_id: UUID, new_status: StatusOrder
    ) -> OrderStatusResponseDTO:
        """
        Обновление статуса заказа.
        """
        logger.info("Обновление статуса заказа.")
        logger.info(f"ID заказа: {order_id}, новый статус заказа: {new_status}")

        updated_status_dto = await self.order_repo.update_status(order_id, new_status)
        if not updated_status_dto:
            logger.warning(f"Заказ с id {order_id} не найден.")
            raise OrderNotFoundException(order_id)

        logger.info(f"Статус заказа с id {order_id} обновлен.")
        return updated_status_dto
