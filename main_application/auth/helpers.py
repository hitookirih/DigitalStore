from datetime import datetime, timezone, timedelta
from typing import TYPE_CHECKING

from fastapi import Depends


from auth import utils as auth_utils
from core.models import User
from core.config import settings
from crud.users import get_user_by_email

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_FIELD = "access"
REFRESH_TOKEN_FIELD = "refresh"


async def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes: int = settings.auth.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return auth_utils.encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


async def create_access_token(user: User = Depends(get_user_by_email)) -> str:
    payload = {
        "sub": user.email,
        "login": user.email,
        "name": user.name,
        "logged_in_at": datetime.now(timezone.utc).isoformat(),
    }
    return await create_jwt(
        token_type=ACCESS_TOKEN_FIELD,
        token_data=payload,
        expire_minutes=settings.auth.access_token_expire_minutes,
    )


async def create_refresh_token(user: User = Depends(get_user_by_email)) -> str:
    payload = {
        "sub": user.email,
    }
    return await create_jwt(
        token_type=REFRESH_TOKEN_FIELD,
        token_data=payload,
        expire_timedelta=timedelta(days=settings.auth.refresh_token_expire_days),
    )
