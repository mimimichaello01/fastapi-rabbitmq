from uuid import UUID
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from application.dto.order import CreateOrderDTO, OrderResponseDTO, OrderStatusResponseDTO
from application.interfaces.repositories.order_repo_interfaces import AbstractOrderRepository
from infra.models.order import Order, StatusOrder


class OrderRepositoryImpl(AbstractOrderRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_order_by_id(self, order_id: UUID) -> Optional[OrderResponseDTO]:
        order = await self.session.get(Order, order_id)
        if order is None:
            return None
        return OrderResponseDTO.model_validate(order)

    async def create_order(self, create_order: CreateOrderDTO) -> OrderResponseDTO:
        order = Order(**create_order.model_dump())
        self.session.add(order)
        await self.session.commit()
        await self.session.refresh(order)
        return OrderResponseDTO.model_validate(order)

    async def update_status(self, order_id: UUID, new_status: StatusOrder) -> Optional[OrderStatusResponseDTO]:
        order = await self.session.get(Order, order_id)
        if order is None:
            return None

        order.status = new_status
        await self.session.commit()
        await self.session.refresh(order)

        return OrderStatusResponseDTO.model_validate(order)
