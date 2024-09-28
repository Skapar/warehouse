from typing import Sequence, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Product
from core.schemas.product import (
    ProductCreate,
    ProductRead,
    ProductUpdate,
    ProductDelete,
)
import logging

logger = logging.getLogger("uvicorn.error")


async def create_product(
    session: AsyncSession, product_create: ProductCreate
) -> Product:
    logger.info(f"Attempting to create product: {product_create}")
    new_product = Product(
        name=product_create.name,
        description=product_create.description,
        price=product_create.price,
        quantity_in_stock=product_create.quantity_in_stock,
    )
    session.add(new_product)
    await session.commit()
    await session.refresh(new_product)
    logger.info(f"Product created successfully: {new_product}")
    return new_product


async def get_all_products(session: AsyncSession) -> Sequence[Product]:
    logger.info("Fetching all products")
    result = await session.execute(select(Product))
    products = result.scalars().all()
    logger.info(f"Fetched {len(products)} products")
    return products


async def get_product_by_id(
    session: AsyncSession, product_id: int
) -> Optional[Product]:
    logger.info(f"Fetching product by ID: {product_id}")
    result = await session.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if product:
        logger.info(f"Product found: {product}")
    else:
        logger.warning(f"Product with ID {product_id} not found")
    return product


async def update_product(
    session: AsyncSession, product_id: int, product_update: ProductUpdate
) -> Optional[Product]:
    logger.info(f"Attempting to update product with ID: {product_id}")
    result = await session.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()

    if product:
        if product_update.name is not None:
            product.name = product_update.name
        if product_update.description is not None:
            product.description = product_update.description
        if product_update.price is not None:
            product.price = product_update.price
        if product_update.quantity_in_stock is not None:
            product.quantity_in_stock = product_update.quantity_in_stock

        await session.commit()
        await session.refresh(product)
        logger.info(f"Product updated successfully: {product}")
    else:
        logger.warning(f"Product with ID {product_id} not found for update")

    return product


async def delete_product(session: AsyncSession, product_id: int) -> bool:
    logger.info(f"Attempting to delete product with ID: {product_id}")
    result = await session.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()

    if product:
        await session.delete(product)
        await session.commit()
        logger.info(f"Product with ID {product_id} deleted successfully")
        return True
    else:
        logger.warning(f"Product with ID {product_id} not found for deletion")
        return False