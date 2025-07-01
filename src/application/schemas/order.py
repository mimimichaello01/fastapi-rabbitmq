from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from pydantic import EmailStr

from infra.models.order import StatusOrder


class OrderResponseSchema(BaseModel):
    """
    Схема ответа с информацией о заказе.
    """

    id: UUID
    user_email: EmailStr
    item_name: str
    status: StatusOrder
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class OrderStatusResponseSchema(BaseModel):
    """
    Схема ответа с информацией о статусе заказа.
    """

    id: UUID
    status: StatusOrder

    model_config = ConfigDict(
        from_attributes=True,
    )


class CreateOrderSchema(BaseModel):
    """
    Схема для создания нового заказа.
    """

    user_email: EmailStr
    item_name: str
    status: StatusOrder = StatusOrder.PENDING


class UpdateOrderStatusSchema(BaseModel):
    """
    Схема для обновления статуса заказа.
    """

    order_id: UUID
    new_status: StatusOrder
