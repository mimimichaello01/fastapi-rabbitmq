from uuid import UUID

from aio_pika import logger
from infra.models.order import StatusOrder
from infra.rabbitmq.workers.base import RabbitMQConsumerClient
from infra.repositories.order_repository_impl import OrderRepositoryImpl






# class OrderStatusWorker(RabbitMQConsumerClient):
async def process_order_status_message(order_repo: OrderRepositoryImpl, payload: dict):
    try:
        order_id = UUID(payload["order_id"])

        # 1. Получаем заказ
        order = await order_repo.get_order_by_id(order_id)
        if not order:
            logger.warning(f"Заказ с id {order_id} не найден")
            return

        # 2. Имитация какой-то логики
        # Например: если заказ уже обработан — пропускаем
        if order.status in [StatusOrder.COMPLETED, StatusOrder.FAILED]:
            logger.info(f"Заказ {order_id} уже обработан со статусом {order.status}")
            return

        logger.info(f"Обрабатываем заказ {order_id}...")

        # 3. Пример: мы просто ставим COMPLETED
        await order_repo.update_status(order_id, StatusOrder.COMPLETED)

        logger.info(f"Заказ {order_id} успешно завершён.")
    except Exception as e:
        logger.error(f"Ошибка обработки заказа: {e}")
        try:
            await order_repo.update_status(order_id, StatusOrder.FAILED)
        except Exception as update_error:
            logger.critical(f"Не удалось обновить статус на FAILED: {update_error}")
            raise
