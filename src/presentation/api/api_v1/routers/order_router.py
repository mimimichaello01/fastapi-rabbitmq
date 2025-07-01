from uuid import UUID
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from application.dto.order import CreateOrderDTO
from application.exceptions.order import OrderNotFoundException
from application.schemas.order import CreateOrderSchema, OrderResponseSchema, OrderStatusResponseSchema, UpdateOrderStatusSchema
from application.service.order_service import OrderServiceImpl
from infra.models.order import StatusOrder
from presentation.api.api_v1.dependencies.order import get_order_service
from settings.config import settings


order_router = APIRouter(
    prefix=settings.api_prefix.order.prefix,
    tags=["Order"],
)


@order_router.get("/", response_model=OrderResponseSchema)
async def get_order(
    order_id: UUID,
    service: OrderServiceImpl = Depends(get_order_service),
):
    try:
        return await service.get_order(order_id)
    except OrderNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@order_router.post("/", response_model=OrderResponseSchema)
async def create_order(
    create_order: CreateOrderSchema,
    service: OrderServiceImpl = Depends(get_order_service),
):
    dto = CreateOrderDTO(**create_order.model_dump())
    return await service.create_order(dto)


@order_router.patch("/status", response_model=OrderStatusResponseSchema)
async def update_order_status(
    data: UpdateOrderStatusSchema,
    service: OrderServiceImpl = Depends(get_order_service),
):
    try:
        return await service.update_order_status(data.order_id, data.new_status)
    except OrderNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
