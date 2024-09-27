from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.schemas.role import RoleCreate, RoleRead
from crud import roles as roles_crud

router = APIRouter(tags=["Roles"])


@router.post("", response_model=RoleRead)
async def create_role(
    role: RoleCreate, session: AsyncSession = Depends(db_helper.session_getter)
):
    role = await roles_crud.create_role(session=session, role_create=role)
    return role
