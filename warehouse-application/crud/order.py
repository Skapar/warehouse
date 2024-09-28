import logging

from typing import Sequence, Optional

from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Order, OrderItem, Product
from core.schemas.order import OrderCreate, OrderRead, OrderItemRead

from fastapi import HTTPException

logger = logging.getLogger("app_logger")

async def create_order(session: AsyncSession, order_create: OrderCreate) -> Optional[OrderRead]:
    print("dadad")
    try:
        print("heeeloo")
        order = Order(
            user_id=order_create.user_id,
            status=order_create.status,
        )
        session.add(order)
        await session.flush()
        for item in order_create.order_items:
            product = await session.execute(
                select(Product).where(Product.id == item.product_id)
            )
            product = product.scalars().first()

            if product is None:
                logger.error(f"Product with ID {item.product_id} not found.")
                raise HTTPException(status_code=404, detail=f"Product with ID {item.product_id} not found.")

            if product.quantity_in_stock < item.quantity:
                logger.error(f"Insufficient stock for product {product.name}. Available: {product.quantity_in_stock}, Requested: {item.quantity}")
                raise HTTPException(status_code=400, detail=f"Insufficient stock for product {product.name}.")

            product.quantity_in_stock -= item.quantity
            session.add(product)
            order_item = OrderItem(
                product_id=item.product_id,
                quantity=item.quantity,
                order_id=order.id
            )
            session.add(order_item)

        await session.commit()
        
        await session.refresh(order)
        order_read = OrderRead(
            id=order.id,
            created_at=order.created_at,
            status=order.status,
            items=[OrderItemRead(id=order_item.id, product_id=order_item.product_id, quantity=order_item.quantity)
                   for order_item in order.order_items] 
        )
        print(order_read)
        logger.info(f"Order created successfully: {order.id}")
        return order_read

    except Exception as e:
        logger.error(f"Error creating order: {e}")
        await session.rollback()
        return None

async def get_order_by_id(session: AsyncSession, order_id: int) -> Optional[Order]:
    return await session.get(Order, order_id)

async def get_all_orders(session: AsyncSession) -> Sequence[Order]:
    result = await session.execute(select(Order))
    return result.scalars().all()

async def update_order_status(session: AsyncSession, order_id: int, status: str) -> Optional[Order]:
    order = await session.get(Order, order_id)
    if order:
        order.status = status
        await session.commit()
        await session.refresh(order)
        logger.info(f"Order status updated successfully: {order.id} - {status}")
        return order
    logger.warning(f"Order with ID {order_id} not found for status update")
    return None
