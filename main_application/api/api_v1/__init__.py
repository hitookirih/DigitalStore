from fastapi import APIRouter

from core.config import settings
from .users import router as users_router
from .products import router as products_router
from .orders import router as orders_router
from auth.user_auth import router as auth_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)

router.include_router(
    users_router,
    prefix=settings.api.v1.users,
)

router.include_router(
    products_router,
    prefix=settings.api.v1.products,
)

router.include_router(
    orders_router,
    prefix=settings.api.v1.orders,
)

router.include_router(
    auth_router,
    prefix=settings.api.v1.auth,
)
