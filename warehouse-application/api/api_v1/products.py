from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.schemas.product import ProductCreate, ProductRead, ProductUpdate, ProductDelete
from crud import product as products_crud

router = APIRouter(tags=["Products"])


@router.post("", response_model=ProductRead)
async def create_product(
    product: ProductCreate, session: AsyncSession = Depends(db_helper.session_getter)
):
    created_product = await products_crud.create_product(session=session, role_create=product)
    return created_product

@router.get("/{product_id}", response_model=ProductRead)
async def get_product(
    product_id: int, 
    session: AsyncSession = Depends(db_helper.session_getter)
):
    product = await products_crud.get_product_by_id(session=session, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("", response_model=list[ProductRead])
async def get_all_products(
    session: AsyncSession = Depends(db_helper.session_getter)
):
    products = await products_crud.get_all_products(session=session)
    return products


@router.put("/{product_id}", response_model=ProductRead)
async def update_product(
    product_id: int, 
    product_update: ProductUpdate, 
    session: AsyncSession = Depends(db_helper.session_getter)
):
    updated_product = await products_crud.update_product(session=session, product_id=product_id, product_update=product_update)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product


@router.delete("/{product_id}", response_model=dict)
async def delete_product(
    product_id: int,
    session: AsyncSession = Depends(db_helper.session_getter)
):
    success = await products_crud.delete_product(session=session, product_id=product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": "Product deleted successfully"}