from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.schemas.role import RoleCreate, RoleRead
from crud.roles import create_role

router = APIRouter(tags=["Roles"])


@router.post("", response_model=RoleRead)
async def create_role(
    role: RoleCreate, session: AsyncSession = Depends(db_helper.session_getter)
):
    role = await create_role(session=session, role=role)
    return role
