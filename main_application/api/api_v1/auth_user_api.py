from fastapi import APIRouter
from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.user_auth import get_current_active_auth_user
from core.models import User, db_helper
from core.schemas.user import UserUpdatePartial
from crud import users as users_crud

router = APIRouter(tags=["Auth_user"])


@router.get("/me/")
async def get_me(
    user: User = Depends(get_current_active_auth_user),
):
    return {
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
    }


@router.patch("/me/")
async def change_user_data(
    user_update: UserUpdatePartial,
    user: User = Depends(get_current_active_auth_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await users_crud.update_user(session, user, user_update, partial=True)


@router.delete("/me/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    user: User = Depends(get_current_active_auth_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await users_crud.delete_user(session, user)
