from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from application.dto.order import CreateOrderDTO, OrderResponseDTO, OrderStatusResponseDTO
from infra.models.order import StatusOrder


class AbstractOrderRepository(ABC):
    @abstractmethod
    async def get_order_by_id(self, order_id:UUID) -> Optional[OrderResponseDTO]:
        ...

    @abstractmethod
    async def create_order(self, create_order: CreateOrderDTO) -> OrderResponseDTO:
        ...

    @abstractmethod
    async def update_status(self, order_id: UUID, new_status: StatusOrder) -> OrderStatusResponseDTO:
        ...
