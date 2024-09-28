from typing import Sequence

from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from core.schemas.user import UserCreate, UserUpdate


async def create_user(session: AsyncSession, user_create: UserCreate):
    user = User(**user_create.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def get_user_by_id(session: AsyncSession, user_id: int):
    return await session.get(User, user_id)

async def get_all_users(session: AsyncSession):
    stmt = select(User).order_by(User.id)
    result = await session.execute(stmt)
    return result.scalars().all()

async def update_user(session: AsyncSession, user_id: int, user_update: UserUpdate):
    user = await session.get(User, user_id)
    if user:
        for key, value in user_update.model_dump().items():
            setattr(user, key, value)
        await session.commit()
        await session.refresh(user)
        return user
    return None

async def delete_user(session: AsyncSession, user_id: int):
    user = await session.get(User, user_id)
    if user:
        await session.delete(user)
        await session.commit()
        return True
    return False