from datetime import datetime

from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.user_dependencies import user_by_id
from core.config import settings
from core.models import db_helper, User
from core.schemas.token import TokenInfo
from core.schemas.user import UserAuth, UserBase
from auth import utils as auth_utils
from crud.users import get_user_by_email

router = APIRouter(tags=["Auth"])


async def validate_auth_user(
    email: str = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    unauth_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )

    user = await get_user_by_email(user_email=email, session=session)

    if not user:
        raise unauth_exc

    if not auth_utils.validate_password(
        password=password,
        hashed_password=user.password,
    ):
        raise unauth_exc

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    return user


@router.post("/login/", response_model=TokenInfo)
async def auth_user_issue(
    user: UserAuth = Depends(validate_auth_user),
):
    payload = {
        "sub": user.email,
        "login": user.email,
        "name": user.name,
        "logged_in_at": datetime.now().isoformat(),
    }
    access_token = auth_utils.encode_jwt(payload)
    return TokenInfo(
        access_token=access_token,
        token_type="Bearer",
    )
