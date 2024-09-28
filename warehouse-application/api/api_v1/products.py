from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper
from core.schemas.product import ProductCreate, ProductRead, ProductUpdate
from crud import product as products_crud
from utils.logger import get_logger

logger = get_logger("products")

router = APIRouter(tags=["Products"])


@router.post("", response_model=ProductRead)
async def create_product(
    request: Request,
    product: ProductCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    logger.info(f"Received POST request to {request.url.path}")
    try:
        created_product = await products_crud.create_product(session=session, product_create=product)
        logger.info(f"Product created successfully: {created_product}")
        return created_product
    except Exception as e:
        logger.error(f"Error creating product: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.get("/{product_id}", response_model=ProductRead)
async def get_product(
    request: Request,
    product_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    logger.info(f"Received GET request to {request.url.path} for product ID {product_id}")
    product = await products_crud.get_product_by_id(session=session, product_id=product_id)
    if not product:
        logger.warning(f"Product with ID {product_id} not found")
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("", response_model=list[ProductRead])
async def get_all_products(
    request: Request,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    logger.info(f"Received GET request to {request.url.path}")
    products = await products_crud.get_all_products(session=session)
    return products


@router.put("/{product_id}", response_model=ProductRead)
async def update_product(
    request: Request,
    product_id: int,
    product_update: ProductUpdate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    logger.info(f"Received PUT request to {request.url.path} for product ID {product_id}")
    updated_product = await products_crud.update_product(session=session, product_id=product_id, product_update=product_update)
    if not updated_product:
        logger.warning(f"Product with ID {product_id} not found for update")
        raise HTTPException(status_code=404, detail="Product not found")
    logger.info(f"Product with ID {product_id} updated successfully")
    return updated_product


@router.delete("/{product_id}", response_model=dict)
async def delete_product(
    request: Request,
    product_id: int,
    session: AsyncSession = Depends(db_helper.session_getter), 
):
    logger.info(f"Received DELETE request to {request.url.path} for product ID {product_id}")
    success = await products_crud.delete_product(session=session, product_id=product_id)
    if not success:
        logger.warning(f"Product with ID {product_id} not found for deletion")
        raise HTTPException(status_code=404, detail="Product not found")
    logger.info(f"Product with ID {product_id} deleted successfully")
    return {"detail": "Product deleted successfully"}