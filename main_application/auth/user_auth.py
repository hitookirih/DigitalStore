from datetime import datetime, timezone

from jwt.exceptions import InvalidTokenError
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    OAuth2PasswordBearer,
)
from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, User
from core.schemas.token import TokenInfo
from auth import utils as auth_utils
from crud.users import get_user_by_email

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login/",
)
router = APIRouter(tags=["Auth"])


async def validate_auth_user(
    # the user should enter their email here
    username: str = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    email = username
    unauth_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid email or password",
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


async def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> User:
    try:
        payload = auth_utils.decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token error {e}",
        )
    return payload


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> User:
    email: str | None = payload.get("sub")
    user = await get_user_by_email(session, email)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalid",
    )


async def get_current_active_auth_user(
    user: User = Depends(get_current_auth_user),
):
    if user.is_active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Inactive user",
    )


@router.post("/login/", response_model=TokenInfo)
async def auth_user_issue(
    user: User = Depends(validate_auth_user),
):
    payload = {
        "sub": user.email,
        "login": user.email,
        "name": user.name,
        "logged_in_at": datetime.now(timezone.utc).isoformat(),
    }
    access_token = auth_utils.encode_jwt(payload)
    return TokenInfo(
        access_token=access_token,
        token_type="Bearer",
    )
