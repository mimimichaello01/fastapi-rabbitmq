from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from pydantic import EmailStr

from infra.models.order import StatusOrder


class OrderResponseDTO(BaseModel):
    id: UUID
    user_email: EmailStr
    item_name: str
    status: StatusOrder
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class OrderStatusResponseDTO(BaseModel):
    id: UUID
    status: StatusOrder

    model_config = ConfigDict(
        from_attributes=True,
    )


class CreateOrderDTO(BaseModel):
    user_email: EmailStr
    item_name: str
    status: StatusOrder = StatusOrder.PENDING
