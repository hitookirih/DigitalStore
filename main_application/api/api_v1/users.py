from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from .user_dependencies import user_by_id
from core.schemas.user import UserUpdatePartial
from core.models import User
from core.schemas.user import UserRead, UserCreate
from crud import users as users_crud

router = APIRouter(tags=["Users"])


@router.get("/", response_model=List[UserRead])
async def get_users(session: AsyncSession = Depends(db_helper.session_getter)):
    users = await users_crud.get_all_users(session=session)
    return users


@router.post("/", response_model=UserRead)
async def create_user(
    user_create: UserCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    user = await users_crud.create_user(
        user_create=user_create,
        session=session,
    )
    return user


@router.patch("/{user_id}/", response_model=UserRead)
async def update_user_partial(
    user_update: UserUpdatePartial,
    user: User = Depends(user_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await users_crud.update_user(session, user, user_update, partial=True)


@router.delete("/{user_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user: User = Depends(user_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await users_crud.delete_user(session, user)
