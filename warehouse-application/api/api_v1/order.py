from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper
from core.schemas.order import OrderCreate, OrderRead
from crud import order as orders_crud
from utils.logger import get_logger
from typing import List, Literal

logger = get_logger("orders")

router = APIRouter(tags=["Orders"])

@router.post("", response_model=OrderRead)
async def create_new_order(
    request: Request,
    order_create: OrderCreate,
    db: AsyncSession = Depends(db_helper.session_getter),
):
    logger.info(f"Received POST request to {request.url.path}")
    order = await orders_crud.create_order(db, order_create)
    if order is None:
        logger.error("Error creating order")
        raise HTTPException(status_code=400, detail="Error creating order")
    logger.info(f"Order created successfully: {order.id}")
    return order

@router.get("/{order_id}", response_model=OrderRead)
async def read_order(
    request: Request,
    order_id: int,
    db: AsyncSession = Depends(db_helper.session_getter),
):
    logger.info(f"Received GET request to {request.url.path} for order ID {order_id}")
    order = await orders_crud.get_order_by_id(db, order_id)
    if order is None:
        logger.warning(f"Order with ID {order_id} not found")
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("", response_model=List[OrderRead])
async def read_orders(
    request: Request,
    db: AsyncSession = Depends(db_helper.session_getter),
):
    logger.info(f"Received GET request to {request.url.path}")
    orders = await orders_crud.get_all_orders(db)
    return orders

@router.patch("/{order_id}/status", response_model=OrderRead)
async def update_order_status(
    request: Request,
    order_id: int,
    status: Literal["IN PROCESS", "SENT", "DELIVERED"],
    db: AsyncSession = Depends(db_helper.session_getter),
):
    logger.info(f"Received PATCH request to {request.url.path} for order ID {order_id} with status {status}")
    order = await orders_crud.update_order_status(db, order_id, status)
    if order is None:
        logger.warning(f"Order with ID {order_id} not found for status update")
        raise HTTPException(status_code=404, detail="Order not found")
    logger.info(f"Order status updated successfully: {order.id} - {status}")
    return order

