from typing import Sequence

from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Role
from core.schemas.role import RoleCreate


async def create_role(
    session: AsyncSession,
    role_create: RoleCreate,
) -> Role:
    role = Role(**role_create.model_dump())
    session.add(role)
    await session.commit()
    await session.refresh(role)

    return role
