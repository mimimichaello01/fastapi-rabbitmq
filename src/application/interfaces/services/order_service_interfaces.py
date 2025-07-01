from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from application.dto.order import (
    CreateOrderDTO,
    OrderResponseDTO,
    OrderStatusResponseDTO,
)
from infra.models.order import StatusOrder


class AbstractOrderService(ABC):
    @abstractmethod
    async def get_order(self, order_id: UUID) -> Optional[OrderResponseDTO]: ...

    @abstractmethod
    async def create_order(self, order_data: CreateOrderDTO) -> OrderResponseDTO: ...

    @abstractmethod
    async def update_order_status(
        self, order_id: UUID, new_status: StatusOrder
    ) -> Optional[OrderStatusResponseDTO]: ...
