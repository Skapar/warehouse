from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.schemas.user import UserRead, UserCreate
from crud.users import get_all_users

router = APIRouter(tags=["Users"])


@router.get("", response_model=list[UserRead])
async def get_users(session: AsyncSession = Depends(db_helper.session_getter)):
    users = await get_all_users(session=session)
    return users


@router.post("", response_model=UserRead)
async def create_user(
    user: UserCreate, session: AsyncSession = Depends(db_helper.session_getter)
):
    user = await create_user(session=session, user=user)
    return user
