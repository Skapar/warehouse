from fastapi import APIRouter
from core.config import settings

from .users import router as users_router
from .roles import router as roles_router
from .products import router as product_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)

router.include_router(
    users_router,
    prefix=settings.api.v1.users,
)

router.include_router(
    roles_router,
    prefix=settings.api.v1.roles,
)

router.include_router(
    product_router,
    prefix=settings.api.v1.products
)