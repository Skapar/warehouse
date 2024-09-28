from fastapi import APIRouter, Depends, Request, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.schemas.user import UserRead, UserCreate, UserUpdate
from crud import users as users_crud
from utils.logger import get_logger

logger = get_logger("users")

router = APIRouter(tags=["Users"])


@router.post("", response_model=UserRead)
async def create_user(
    request: Request,
    user: UserCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    logger.info(f"Received POST request to {request.url.path}")
    try:
        created_user = await users_crud.create_user(session=session, user_create=user)
        logger.info(f"User created successfully: {created_user}")
        return created_user
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    request: Request,
    user_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    logger.info(f"Received GET request to {request.url.path} for user ID {user_id}")
    user = await users_crud.get_user_by_id(session=session, user_id=user_id)
    if not user:
        logger.warning(f"User with ID {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("", response_model=list[UserRead])
async def get_all_users(
    request: Request,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    logger.info(f"Received GET request to {request.url.path}")
    users = await users_crud.get_all_users(session=session)
    return users


@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    request: Request,
    user_id: int,
    user_update: UserUpdate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    logger.info(f"Received PUT request to {request.url.path} for user ID {user_id}")
    updated_user = await users_crud.update_user(session=session, user_id=user_id, user_update=user_update)
    if not updated_user:
        logger.warning(f"User with ID {user_id} not found for update")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"User with ID {user_id} updated successfully")
    return updated_user


@router.delete("/{user_id}", response_model=dict)
async def delete_user(
    request: Request,
    user_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    logger.info(f"Received DELETE request to {request.url.path} for user ID {user_id}")
    success = await users_crud.delete_user(session=session, user_id=user_id)
    if not success:
        logger.warning(f"User with ID {user_id} not found for deletion")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"User with ID {user_id} deleted successfully")
    return {"detail": "User deleted successfully"}