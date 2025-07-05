from uuid import UUID
from application.exceptions.base import ApplicationException


class OrderNotFoundException(ApplicationException):
    """
    Исключение, которое выбрасывается, если заказ не найден.
    """
    def __init__(self, order_id: UUID):
        super().__init__(f"Заказ с id {order_id} не найден.")
        self.order_id = order_id
